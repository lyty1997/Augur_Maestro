from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RQ_CORE = ROOT / "src" / "rq_core"

FORBIDDEN_NETWORK_IMPORTS = {
    "aiohttp",
    "httpx",
    "requests",
    "socket",
    "urllib",
    "urllib3",
    "websocket",
}
TRADE_METHODS = {
    "cancel_order": "CANCEL_ORDER",
    "modify_order": "MODIFY_ORDER",
    "place_order": "PLACE_ORDER",
}


class SafetyError(Exception):
    pass


def parse_python(path: Path) -> ast.Module:
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        raise SafetyError(f"{path}: Python 解析失败: {exc}") from exc


def class_body(module: ast.Module, class_name: str) -> list[ast.stmt]:
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node.body
    raise SafetyError(f"未找到类: {class_name}")


def get_assignments(body: list[ast.stmt]) -> dict[str, ast.expr]:
    assignments: dict[str, ast.expr] = {}
    for stmt in body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            assignments[stmt.target.id] = stmt.value
        elif isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    assignments[target.id] = stmt.value
    return assignments


def is_bool_constant(value: ast.expr | None, expected: bool) -> bool:
    return isinstance(value, ast.Constant) and value.value is expected


def is_broker_mode_read_only(value: ast.expr | None) -> bool:
    return (
        isinstance(value, ast.Attribute)
        and value.attr == "READ_ONLY"
        and isinstance(value.value, ast.Name)
        and value.value.id == "BrokerMode"
    )


def check_default_trading_safety() -> None:
    module = parse_python(RQ_CORE / "broker_kernel" / "contracts.py")

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


def iter_methods(class_node: ast.ClassDef) -> dict[str, ast.FunctionDef]:
    return {node.name: node for node in class_node.body if isinstance(node, ast.FunctionDef)}


def call_attr_name(node: ast.stmt) -> str | None:
    if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
        return None
    func = node.value.func
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def is_guard_call(stmt: ast.stmt, action_name: str) -> bool:
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
    module = parse_python(RQ_CORE / "broker_kernel" / "gateway.py")
    trading_gateway = None
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == "TradingGateway":
            trading_gateway = node
            break
    if trading_gateway is None:
        raise SafetyError("未找到 TradingGateway")

    methods = iter_methods(trading_gateway)
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
    module = parse_python(RQ_CORE / "broker_kernel" / "usmart" / "client.py")
    body = class_body(module, "uSmartOpenApiClient")
    methods = iter_methods(
        ast.ClassDef(name="_", bases=[], keywords=[], body=body, decorator_list=[])
    )

    init_method = methods.get("__init__")
    if init_method is None:
        raise SafetyError("uSmartOpenApiClient 缺少 __init__")
    dry_run_arg = next(
        (arg for arg in init_method.args.kwonlyargs if arg.arg == "dry_run"),
        None,
    )
    dry_run_default = None
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

    if errors:
        print("交易专项安全静态检查失败：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Trading safety static checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
