# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目性质

Augur_Maestro 是个人低频量化研究与交易系统，**当前处于设计阶段**：`docs/` 是真相源，代码量极少（仅 `rq_core/quotation_kernel` 一个落地骨架）。

**铁律：先设计，后编码。** 任何涉及交易、风控、券商接入、账户、订单、数据模型、架构、部署的改动，必须先与用户更新 `docs/` 对应设计文档并经确认，再写代码。改动前先读 `docs/README.md` 确认当前真相源，绝不能凭代码现状推断设计意图——代码落后于文档。

## 交易安全边界（最高优先级，覆盖一切收益目标）

这是本项目的核心架构约束，不是可选项：

- **M1 只做研究、回测、dry-run、只读查询**，不接任何真实交易。
- 任何可能在券商侧形成或撤销委托的调用（下单、撤单、改单、条件单、预埋单、止盈止损、触发单），无论接口叫什么名字，都按**真实交易**处理，默认关闭（`trading_enabled=false`）。
- 不允许用真实下单/撤单接口做连通性探测、冒烟测试或权限测试。
- 策略**不得直接调用券商 API**，只能产出交易意图，经风控 → OMS → 统一券商网关。LLM 不得直接触发实盘。
- OMS 下单失败/超时/未知状态**绝不自动重试**，进入 `failed`/`unknown` 人工可审计状态，靠订单查询和对账确认。
- 不写入、不打印、不提交券商 API Key/Secret/token、真实账号、身份证明、资金/持仓隐私。

完整规则见 `docs/architecture/trading-safety.md` 与根目录 `AGENTS.md`。

## 架构

代码组织遵循「领域核心 + 入口层」分层（`docs/architecture/overview.md` 第 7 节）：

- `src/rq_core/`：领域核心，**严禁依赖** FastAPI/Typer/SQLAlchemy/AKShare/Qlib/VectorBT。按拆分 kernel 设计：
  - M1 落地：`data_kernel`、`universe_kernel`、`research_kernel`、`backtest_kernel`、`report_kernel`（多数仍是接口类）。
  - 长期预留（M1 不实现真实逻辑）：`risk_kernel`、`oms_kernel`、`broker_kernel`、`quotation_kernel`。
  - 已落地的 `quotation_kernel`：`QuotationDataGateway` + `QuotationDataAdapter` 抽象。**行情查询与交易动作分离**——行情走 `QuotationDataGateway`，交易走（未来的）`TradingGateway`，两者不混用 signer/client/连接生命周期。
- `src/backend/`：FastAPI 入口（M1 仅健康检查+只读方向），**不沉淀核心业务规则**。
- `src/cli/`：Typer CLI（M1 主入口），同样只是入口层。
- `src/scripts/quality/`：质量门禁脚本。
- 券商接入是三套独立 API：交易 API、基础报价 API、报价推送 API，不能混用。uSmart/盈立以**官方网页手册**为真相源，未确认的行为标记 `unknown_by_official_doc`，不猜为事实。

M1 主线数据流：AKShare 经 `DataProvider` 抽象 → `data_kernel` 标准化 → PostgreSQL → 研究/回测（Qlib + VectorBT 并行验证）→ Markdown 报告（写入 `outputs/`，不进 Git）。

## 常用命令

```bash
# 环境搭建
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.lock.txt
.venv/bin/python -m pre_commit install

# 质量门禁（与 CI 对齐）
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m mypy -p rq_core              # strict 模式
.venv/bin/detect-secrets-hook --baseline .secrets.baseline $(git ls-files)
.venv/bin/python -m pip_audit -r requirements-dev.lock.txt
.venv/bin/python src/scripts/quality/markdown_docs_check.py   # 校验 docs/ 内部链接
.venv/bin/python -m pytest

# 单个测试
.venv/bin/python -m pytest tests/path/test_x.py::test_name

# 依赖锁定（改了 requirements-dev.txt 后）
.venv/bin/python -m piptools compile requirements-dev.txt \
  --output-file requirements-dev.lock.txt --no-emit-index-url --no-emit-trusted-host
```

`pytest` 配置在 `pyproject.toml`：默认开启 `--cov=rq_core` 且 `--cov-fail-under=60`，所以覆盖率低于 60% 会失败。

## 工程约定

- 语言：对话与 `docs/` 用简体中文；代码注释中文为主，标准英文术语/协议名/API 名保留原文。提交信息中文，格式 `<type>(<scope>): <主题>`，不带 Co-Authored-By。
- 分支：`main` 稳定不直接提交，`dev` 开发主干，特性分支 `feature/sN-描述`。
- mypy `--strict`、ruff（含 `B/UP/RUF`，已 ignore 中文标点规则 RUF001-003）必须通过。
- `configs/*.yaml` 非敏感配置可进 Git；`.env`、`data/`、`outputs/`、`logs/` 不进 Git。
- 解决 bug 后把原因和方案追加到 `codex-rules/known-issues.md`；动手前先查阅它避免重复踩坑。

## 规则文件分层

操作规范在 `codex-rules/`（不替代 `docs/` 设计真相源）：`global-AGENTS.md` 是入口与索引，`known-issues.md` 是已知坑点，`rules/` 下按主题拆分（trading-safety / broker-openapi / python-coding / data-research / concurrency-resource-safety 等）。任务开始前按类型读取相关规则。

## 质量门禁现状

- `src/scripts/quality/trading_safety_static_check.py` 是交易安全静态门禁（AST 扫描 rq_core）。它有 6 个检查：3 个通用红线（禁网络库 import、禁绕过网关直连适配器交易方法、禁默认 `trading_enabled=True`）始终生效；3 个绑定 `broker_kernel` 的门面检查（默认能力关闭、TradingGateway 守卫、uSmart dry_run）在 `broker_kernel` 不存在时**自动 skip 并打印说明**，待该模块按已确认设计重建后自动恢复，无需改脚本。
- **pytest 当前必然失败**：`tests/` 下还没有测试用例，而 `pyproject.toml` 配了 `--cov-fail-under=60`，零测试 → 0% 覆盖率 → 失败。这是 M1 设计阶段的既有状态，不是回归。补 M1 kernel 实现时同步补 `tests/`（镜像 `src/` 结构）即可转绿。
- ruff 的 T20（禁 `print`）**未**在项目配置启用，质量脚本可以用 `print`；但不要加 `# noqa: T201`——项目启用了 RUF，未命中的 noqa 会触发 RUF100 反而失败。需要静默输出时用 `sys.stdout.write` / `sys.stderr.write`。
