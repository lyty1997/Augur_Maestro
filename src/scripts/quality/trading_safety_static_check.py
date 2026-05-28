"""交易专项安全静态检查。

扫描 rq_core 源码，强制交易安全红线：
- rq_core 是领域核心，禁止直接 import 网络库（网络访问只能在入口层和券商适配器发生）。
- 禁止绕过 TradingGateway 直接调用适配器的下单/改单/撤单方法。
- 禁止在生产代码中把 trading_enabled / place_order 等默认设为 True。

当 broker_kernel 尚未重建时（见 docs/backend/trading/broker-trading-gateway.md），
依赖具体 broker 门面结构的检查会自动跳过并打印 skip 说明；broker_kernel 按已确认
设计重建后，这些检查无需改脚本即可自动恢复。
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RQ_CORE = ROOT / "src" / "rq_core"

# rq_core 禁止直接依赖网络库；网络访问只能在入口层和券商适配器中发生。
FORBIDDEN_NETWORK_IMPORTS = {
    "aiohttp",
    "httpx",
    "requests",
    "socket",
    "urllib",
    "urllib3",
    "websocket",
}
# 交易动作方法 -> 对应 BrokerAction 枚举名。
TRADE_METHODS = {
    "cancel_order": "CANCEL_ORDER",
    "modify_order": "MODIFY_ORDER",
    "place_order": "PLACE_ORDER",
}

# broker_kernel 缺失时被跳过的门面级检查说明，由 main 统一打印。
SKIPPED: list[str] = []


class SafetyError(Exception):
    """交易安全静态检查失败。"""


def parse_python(path: Path) -> ast.Module:
    """解析 Python 源码为 AST，解析失败转成 SafetyError。"""
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        raise SafetyError(f"{path}: Python 解析失败: {exc}") from exc


def class_body(module: ast.Module, class_name: str) -> list[ast.stmt]:
    """返回指定类的语句体，找不到则报错。"""
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node.body
    raise SafetyError(f"未找到类: {class_name}")


def methods_in(body: list[ast.stmt]) -> dict[str, ast.FunctionDef]:
    """从类体语句中提取方法名到函数定义的映射。"""
    return {node.name: node for node in body if isinstance(node, ast.FunctionDef)}


def get_assignments(body: list[ast.stmt]) -> dict[str, ast.expr | None]:
    """收集类体内的字段赋值，返回字段名到右值表达式的映射。"""
    assignments: dict[str, ast.expr | None] = {}
    for stmt in body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            assignments[stmt.target.id] = stmt.value
        elif isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    assignments[target.id] = stmt.value
    return assignments


def is_bool_constant(value: ast.expr | None, expected: bool) -> bool:
    """判断表达式是否为指定布尔字面量。"""
    return isinstance(value, ast.Constant) and value.value is expected


def is_broker_mode_read_only(value: ast.expr | None) -> bool:
    """判断表达式是否为 BrokerMode.READ_ONLY。"""
    return (
        isinstance(value, ast.Attribute)
        and value.attr == "READ_ONLY"
        and isinstance(value.value, ast.Name)
        and value.value.id == "BrokerMode"
    )


def check_default_trading_safety() -> None:
    """校验券商能力与网关配置默认关闭真实交易。"""
    contracts_path = RQ_CORE / "broker_kernel" / "contracts.py"
    if not contracts_path.exists():
        SKIPPED.append("broker_kernel/contracts.py 不存在：跳过默认能力/网关安全字段检查")
        return
    module = parse_python(contracts_path)

    capability_assignments = get_assignments(class_body(module, "CapabilityConfig"))
    for field_name in ("place_order", "modify_order", "cancel_order", "odd_lot_order", "ipo"):
        if not is_bool_constant(capability_assignments.get(field_name), False):
            raise SafetyError(f"CapabilityConfig.{field_name} 必须默认 False")

    gateway_assignments = get_assignments(class_body(module, "BrokerGatewayConfig"))
    if not is_broker_mode_read_only(gateway_assignments.get("mode")):
        raise SafetyError("BrokerGatewayConfig.mode 必须默认 BrokerMode.READ_ONLY")
    if not is_bool_constant(gateway_assignments.get("trading_enabled"), False):
        raise SafetyError("BrokerGatewayConfig.trading_enabled 必须默认 False")
    if not is_bool_constant(gateway_assignments.get("require_oms_caller"), True):
        raise SafetyError("BrokerGatewayConfig.require_oms_caller 必须默认 True")


def is_guard_call(stmt: ast.stmt, action_name: str) -> bool:
    """判断语句是否为 self._guard.ensure_allowed(BrokerAction.<action>)。"""
    if not isinstance(stmt, ast.Expr) or not isinstance(stmt.value, ast.Call):
        return False
    call = stmt.value
    func = call.func
    if not (
        isinstance(func, ast.Attribute)
        and func.attr == "ensure_allowed"
        and isinstance(func.value, ast.Attribute)
        and func.value.attr == "_guard"
    ):
        return False
    if len(call.args) != 1:
        return False
    arg = call.args[0]
    return (
        isinstance(arg, ast.Attribute)
        and arg.attr == action_name
        and isinstance(arg.value, ast.Name)
        and arg.value.id == "BrokerAction"
    )


def method_calls_adapter(method: ast.FunctionDef, adapter_method: str) -> bool:
    """判断方法体内是否通过 self._adapter.<method> 调用适配器。"""
    for node in ast.walk(method):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if (
            isinstance(func, ast.Attribute)
            and func.attr == adapter_method
            and isinstance(func.value, ast.Attribute)
            and func.value.attr == "_adapter"
        ):
            return True
    return False


def check_gateway_guards() -> None:
    """校验 TradingGateway 交易方法先过能力守卫再调用统一适配器。"""
    gateway_path = RQ_CORE / "broker_kernel" / "gateway.py"
    if not gateway_path.exists():
        SKIPPED.append("broker_kernel/gateway.py 不存在：跳过 TradingGateway 门面守卫检查")
        return
    module = parse_python(gateway_path)
    trading_gateway = None
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == "TradingGateway":
            trading_gateway = node
            break
    if trading_gateway is None:
        raise SafetyError("未找到 TradingGateway")

    methods = methods_in(trading_gateway.body)
    for method_name, action_name in TRADE_METHODS.items():
        method = methods.get(method_name)
        if method is None:
            raise SafetyError(f"TradingGateway 缺少 {method_name}")
        if not method.body or not is_guard_call(method.body[0], action_name):
            raise SafetyError(
                f"TradingGateway.{method_name} 必须先调用 "
                f"_guard.ensure_allowed(BrokerAction.{action_name})"
            )
        if not method_calls_adapter(method, method_name):
            raise SafetyError(f"TradingGateway.{method_name} 必须通过统一适配器调用")


def check_usmart_real_transport_disabled() -> None:
    """校验 uSmart 客户端默认 dry_run，且真实 transport 路径被禁用。"""
    client_path = RQ_CORE / "broker_kernel" / "usmart" / "client.py"
    if not client_path.exists():
        SKIPPED.append("broker_kernel/usmart/client.py 不存在：跳过 uSmart dry_run/transport 检查")
        return
    module = parse_python(client_path)
    methods = methods_in(class_body(module, "uSmartOpenApiClient"))

    init_method = methods.get("__init__")
    if init_method is None:
        raise SafetyError("uSmartOpenApiClient 缺少 __init__")
    dry_run_arg = next(
        (arg for arg in init_method.args.kwonlyargs if arg.arg == "dry_run"),
        None,
    )
    dry_run_default: ast.expr | None = None
    if dry_run_arg is not None:
        index = init_method.args.kwonlyargs.index(dry_run_arg)
        dry_run_default = init_method.args.kw_defaults[index]
    if not is_bool_constant(dry_run_default, True):
        raise SafetyError("uSmartOpenApiClient.dry_run 必须默认 True")

    post_method = methods.get("post")
    if post_method is None:
        raise SafetyError("uSmartOpenApiClient 缺少 post")
    has_disabled_transport_raise = any(
        isinstance(node, ast.Raise)
        and isinstance(node.exc, ast.Call)
        and isinstance(node.exc.func, ast.Name)
        and node.exc.func.id == "NotImplementedError"
        for node in ast.walk(post_method)
    )
    if not has_disabled_transport_raise:
        raise SafetyError(
            "uSmartOpenApiClient.post 必须在真实 transport 路径抛 NotImplementedError"
        )


def check_no_network_imports_in_core() -> None:
    """校验 rq_core 不直接 import 网络库。"""
    for path in sorted(RQ_CORE.rglob("*.py")):
        module = parse_python(path)
        for node in ast.walk(module):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top_level_name = alias.name.split(".", maxsplit=1)[0]
                    if top_level_name in FORBIDDEN_NETWORK_IMPORTS:
                        raise SafetyError(f"{path}: rq_core 禁止直接 import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                top_level_name = node.module.split(".", maxsplit=1)[0]
                if top_level_name in FORBIDDEN_NETWORK_IMPORTS:
                    raise SafetyError(f"{path}: rq_core 禁止 from {node.module} import ...")


def check_no_direct_adapter_trade_calls() -> None:
    """校验除 TradingGateway 外，rq_core 不直接调用适配器交易方法。"""
    gateway_path = RQ_CORE / "broker_kernel" / "gateway.py"
    for path in sorted(RQ_CORE.rglob("*.py")):
        if path == gateway_path:
            continue
        module = parse_python(path)
        for node in ast.walk(module):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not isinstance(func, ast.Attribute) or func.attr not in TRADE_METHODS:
                continue
            receiver = func.value
            if isinstance(receiver, ast.Attribute) and receiver.attr in {"_adapter", "adapter"}:
                raise SafetyError(f"{path}: 禁止绕过 TradingGateway 直接调用适配器 {func.attr}")


def check_no_live_defaults() -> None:
    """校验生产代码不把真实交易开关默认设为 True。"""
    for path in sorted(RQ_CORE.rglob("*.py")):
        module = parse_python(path)
        for node in ast.walk(module):
            if isinstance(node, ast.keyword) and node.arg in {
                "trading_enabled",
                "place_order",
                "modify_order",
                "cancel_order",
            }:
                if is_bool_constant(node.value, True):
                    raise SafetyError(f"{path}: 禁止在生产代码中默认启用 {node.arg}=True")


def main() -> int:
    """运行全部交易安全静态检查，返回进程退出码。"""
    checks = [
        check_default_trading_safety,
        check_gateway_guards,
        check_usmart_real_transport_disabled,
        check_no_network_imports_in_core,
        check_no_direct_adapter_trade_calls,
        check_no_live_defaults,
    ]
    errors: list[str] = []
    for check in checks:
        try:
            check()
        except SafetyError as exc:
            errors.append(str(exc))

    for note in SKIPPED:
        sys.stdout.write(f"skip: {note}\n")

    if errors:
        sys.stderr.write("交易专项安全静态检查失败：\n")
        for error in errors:
            sys.stderr.write(f"- {error}\n")
        return 1

    sys.stdout.write("Trading safety static checks passed.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
