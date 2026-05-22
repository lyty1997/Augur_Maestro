from __future__ import annotations

import re
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "API_manual/uSmart/API_manual/usmart-trade-openapi.zh-cn.md"
OUTPUT = ROOT / "docs/backend/clients/api/usmart-trade-error-codes.draft.yaml"


HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$")
URL_RE = re.compile(r"`(https?://[^`]+)`")
TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
CODE_RE = re.compile(r"^-?\d+$")


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


def gateway_error_for(code: str, message: str) -> str:
    if code in {"0", "200", "201"}:
        return "broker.ok"
    if code == "401" or "TOKEN" in message.upper() or "token" in message.lower():
        return "broker.auth_expired"
    if code == "403" or "权限" in message:
        return "broker.permission_denied"
    if code == "404":
        return "broker.endpoint_not_found"
    if "冻结" in message or "锁定" in message:
        return "broker.account_restricted"
    if "密码" in message:
        return "broker.auth_failed"
    if "验证码" in message:
        return "broker.captcha_required"
    if "频率" in message or "次数过多" in message or "稍后重试" in message:
        return "broker.rate_limited"
    if "碎股" in message or "数量" in message:
        return "broker.order_rejected"
    if "非法请求" in message:
        return "broker.bad_request"
    return "broker.unclassified"


def yaml_quote(value: str | None) -> str:
    if value is None:
        return "null"
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


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

        if clean_cell(line) != "- 响应状态":
            continue

        cursor = index + 1
        while cursor < len(lines):
            cells = split_row(lines[cursor])
            if not cells:
                if rows and cursor > index + 3:
                    break
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
        "  gateway_error_layer: robustquant_stable_error_codes",
        "  default_gateway_error: broker.unclassified",
        "  notes:",
        "    - Keep broker raw code/msg for diagnostics and audit.",
        "    - Use gateway_error for OMS, risk, CLI, and API control flow.",
        "    - Response statuses are grouped by endpoint; do not treat codes as globally valid.",
        "summary:",
        f"  endpoint_count: {len(grouped)}",
        f"  response_status_row_count: {len(rows)}",
        "endpoints:",
    ]

    for (endpoint, section_id, source_section), endpoint_rows in grouped.items():
        lines.extend(
            [
                f"  - endpoint: {yaml_quote(endpoint)}",
                f"    source_section: {yaml_quote(source_section)}",
                f"    section_id: {yaml_quote(section_id)}",
                f"    response_status_count: {len(endpoint_rows)}",
                "    response_statuses:",
            ]
        )
        for row in endpoint_rows:
            lines.extend(
                [
                    f"      - code: {yaml_quote(row.code)}",
                    f"        code_type: {yaml_quote(code_type(row.code))}",
                    f"        message: {yaml_quote(row.message)}",
                    "        gateway_error: "
                    f"{yaml_quote(gateway_error_for(row.code, row.message))}",
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
    print(
        f"Wrote {len(rows)} uSmart trade response status rows "
        f"for {endpoint_count} endpoints to {OUTPUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
