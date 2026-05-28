from __future__ import annotations

import re
import sys
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "API_manual/uSmart/API_manual/usmart-trade-openapi.zh-cn.md"
OUTPUT = ROOT / "docs/backend/clients/api/usmart-trade-error-codes.draft.yaml"


HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$")
URL_RE = re.compile(r"`(https?://[^`]+)`")
TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
CODE_RE = re.compile(r"^-?\d+$")


# 写动作 endpoint：HTTP 401 在这些 endpoint 上意味着请求已穿过 TLS 抵达 broker、
# 订单可能已收单，必须按 broker.order_state_unknown 处理而非 auth_expired，避免
# 上层基于 retryable=true 自动重试造成重复下单/重复撤单。
WRITE_ACTION_ENDPOINTS: frozenset[str] = frozenset(
    {
        "/stock-order-server/open-api/entrust-order",
        "/stock-order-server/open-api/modify-order",
        "/stock-order-server/open-api/odd-entrust",
        "/stock-order-server/open-api/odd-modify",
        "/stock-order-server/open-api/apply-ipo",
        "/stock-order-server/open-api/modify-ipo",
        "/stock-order-server/open-api/ipo-comfirm-qyt/v1",
        "/ams-center/open-api/ma-order-submit/v1",
        "/ams-center/open-api/ma-order-cancel/v1",
        "/option-order-server/open-api/option-trade/v1",
        "/option-order-server/open-api/option-replace-order/v1",
        "/option-order-server/open-api/option-cancel-order/v1",
    }
)

# 官方手册未给出业务拒绝码的写动作 endpoint。下单后业务级失败只能通过
# broker.unclassified 兜底，需后续联调或手册补充再细化业务码到 gateway_error 映射。
ENDPOINTS_WITHOUT_BUSINESS_CODES: frozenset[str] = frozenset(
    {
        "/ams-center/open-api/ma-order-submit/v1",
        "/ams-center/open-api/ma-order-cancel/v1",
        "/option-order-server/open-api/option-trade/v1",
        "/option-order-server/open-api/option-replace-order/v1",
        "/option-order-server/open-api/option-cancel-order/v1",
    }
)


@dataclass(frozen=True)
class SectionContext:
    section_id: str
    title: str
    endpoint: str | None


@dataclass(frozen=True)
class ErrorCodeRow:
    code: str
    message: str
    schema: str | None
    section_id: str
    source_section: str
    endpoint: str | None
    source_line: int


def clean_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("<br>", " ")).strip()


def split_row(line: str) -> list[str]:
    match = TABLE_ROW_RE.match(line.strip())
    if not match:
        return []
    return [clean_cell(cell) for cell in match.group(1).split("|")]


def section_id_from_title(title: str) -> str:
    match = re.match(r"^(\d+(?:\.\d+)*)", title)
    return match.group(1) if match else ""


def code_type(code: str) -> str:
    if code == "0":
        return "success"
    if code in {"200", "201", "401", "403", "404"}:
        return "http_status"
    return "business"


# 按 message 文本特征匹配 gateway error，列表顺序即优先级。
# 「验证次数过多」必须在通用 rate_limited 分支之前匹配——它是 uSmart 账号级小时锁，
# 不是请求级 429；映射到 broker.account_restricted 才能阻止短退避重试继续累计锁定。
_MESSAGE_CLASSIFICATION_RULES: tuple[tuple[Callable[[str], bool], str], ...] = (
    (lambda m: "TOKEN" in m.upper() or "token" in m.lower(), "broker.auth_expired"),
    (lambda m: "权限" in m, "broker.permission_denied"),
    (lambda m: "冻结" in m or "锁定" in m, "broker.account_restricted"),
    (
        lambda m: "验证" in m and ("次数过多" in m or "次数已达" in m),
        "broker.account_restricted",
    ),
    (lambda m: "密码" in m, "broker.auth_failed"),
    (lambda m: "验证码" in m, "broker.captcha_required"),
    (lambda m: "频率" in m or "次数过多" in m or "稍后重试" in m, "broker.rate_limited"),
    (lambda m: "碎股" in m or "数量" in m, "broker.order_rejected"),
    (lambda m: "非法请求" in m, "broker.bad_request"),
)


def gateway_error_for(code: str, message: str, endpoint: str | None) -> str:
    """raw (endpoint, code, message) -> Augur_Maestro 稳定 gateway error 码。

    写动作 endpoint 的 HTTP 401：请求已抵达 broker、订单可能已收单，映射到
    broker.order_state_unknown（severity=critical, retryable=false），与 OMS
    unknown 状态闭环；避免被上层按 broker.auth_expired(retryable=true)
    自动重试造成重复下单/重复撤单。
    """
    if code in {"0", "200", "201"}:
        return "broker.ok"
    if code == "401":
        if endpoint is not None and endpoint in WRITE_ACTION_ENDPOINTS:
            return "broker.order_state_unknown"
        return "broker.auth_expired"
    if code == "403":
        return "broker.permission_denied"
    if code == "404":
        return "broker.endpoint_not_found"
    for predicate, error in _MESSAGE_CLASSIFICATION_RULES:
        if predicate(message):
            return error
    return "broker.unclassified"


def yaml_quote(value: str | None) -> str:
    if value is None:
        return "null"
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _parse_response_table(
    lines: list[str],
    start: int,
    rows: list[ErrorCodeRow],
    context: SectionContext,
) -> None:
    """从 start 行开始解析「响应状态」表格，命中的 ErrorCodeRow 追加到 rows。"""
    cursor = start
    while cursor < len(lines):
        cells = split_row(lines[cursor])
        if not cells:
            if rows and cursor > start + 2:
                return
            cursor += 1
            continue
        if len(cells) < 2 or set(cells[0]) <= {"-"} or cells[0] == "状态码":
            cursor += 1
            continue
        if not CODE_RE.match(cells[0]):
            cursor += 1
            continue
        rows.append(
            ErrorCodeRow(
                code=cells[0],
                message=cells[1],
                schema=cells[2] if len(cells) > 2 and cells[2] else None,
                section_id=context.section_id,
                source_section=context.title,
                endpoint=context.endpoint,
                source_line=cursor + 1,
            )
        )
        cursor += 1


def parse_rows(lines: list[str]) -> list[ErrorCodeRow]:
    rows: list[ErrorCodeRow] = []
    context = SectionContext(section_id="", title="", endpoint=None)

    for index, line in enumerate(lines):
        heading = HEADING_RE.match(line)
        if heading:
            title = clean_cell(heading.group(2))
            context = SectionContext(
                section_id=section_id_from_title(title),
                title=title,
                endpoint=context.endpoint,
            )

        url_match = URL_RE.search(line)
        if url_match:
            url = url_match.group(1)
            if "/open-api/" in url:
                context = SectionContext(
                    section_id=context.section_id,
                    title=context.title,
                    endpoint=url.split(".com", 1)[-1],
                )

        if clean_cell(line) == "- 响应状态":
            _parse_response_table(lines, index + 1, rows, context)

    return rows


def render_yaml(rows: list[ErrorCodeRow]) -> str:
    grouped: OrderedDict[tuple[str | None, str, str], list[ErrorCodeRow]] = OrderedDict()
    for row in rows:
        grouped.setdefault((row.endpoint, row.section_id, row.source_section), []).append(row)

    lines = [
        "# Generated from API_manual/uSmart/API_manual/usmart-trade-openapi.zh-cn.md.",
        "# Do not hand-edit individual entries; update the source manual or extraction script.",
        "version: 0.1.0-draft",
        "source:",
        f"  manual: {yaml_quote('API_manual/uSmart/API_manual/usmart-trade-openapi.zh-cn.md')}",
        "  api_family: trade_openapi",
        "policy:",
        "  raw_code_catalog: complete_from_official_manual_response_status_tables",
        "  gateway_error_layer: augur_maestro_stable_error_codes",
        "  default_gateway_error: broker.unclassified",
        "  notes:",
        "    - Keep broker raw code/msg for diagnostics and audit.",
        "    - Use gateway_error for OMS, risk, CLI, and API control flow.",
        "    - Response statuses are grouped by endpoint; do not treat codes as globally valid.",
        "endpoint_scoping_invariants:",
        "  # 当前实际差异化清单：endpoint scoping 已激活的映射规则；其余 raw code 在所有",
        "  # endpoint 上一致映射，scoping 作为未来按 endpoint 细化的预留能力。",
        "  http_401:",
        "    write_action_endpoints_map_to: broker.order_state_unknown",
        "    other_endpoints_map_to: broker.auth_expired",
        "    write_action_endpoints:",
        *[f"      - {ep}" for ep in sorted(WRITE_ACTION_ENDPOINTS)],
        "  other_raw_codes: globally_consistent_mapping_no_endpoint_divergence_yet",
        "summary:",
        f"  endpoint_count: {len(grouped)}",
        f"  response_status_row_count: {len(rows)}",
        "endpoints:",
    ]

    for (endpoint, section_id, source_section), endpoint_rows in grouped.items():
        endpoint_block = [
            f"  - endpoint: {yaml_quote(endpoint)}",
            f"    source_section: {yaml_quote(source_section)}",
            f"    section_id: {yaml_quote(section_id)}",
            f"    response_status_count: {len(endpoint_rows)}",
        ]
        if endpoint in ENDPOINTS_WITHOUT_BUSINESS_CODES:
            endpoint_block.append("    business_codes_unknown: true")
        endpoint_block.append("    response_statuses:")
        lines.extend(endpoint_block)
        for row in endpoint_rows:
            lines.extend(
                [
                    f"      - code: {yaml_quote(row.code)}",
                    f"        code_type: {yaml_quote(code_type(row.code))}",
                    f"        message: {yaml_quote(row.message)}",
                    "        gateway_error: "
                    f"{yaml_quote(gateway_error_for(row.code, row.message, row.endpoint))}",
                    f"        source_line: {row.source_line}",
                ]
            )
            if row.schema:
                lines.append(f"        schema: {yaml_quote(row.schema)}")
    return "\n".join(lines) + "\n"


def main() -> None:
    rows = parse_rows(SOURCE.read_text(encoding="utf-8").splitlines())
    OUTPUT.write_text(render_yaml(rows), encoding="utf-8")
    endpoint_count = len({(row.endpoint, row.section_id, row.source_section) for row in rows})
    sys.stdout.write(
        f"Wrote {len(rows)} uSmart trade response status rows "
        f"for {endpoint_count} endpoints to {OUTPUT.relative_to(ROOT)}\n"
    )


if __name__ == "__main__":
    main()
