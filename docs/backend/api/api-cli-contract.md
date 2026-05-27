# M1 CLI / API / DTO / 日志契约

版本：v0.1  
状态：草案，待用户确认  
最后更新：2026-05-15

## 0. 文档定位

本文档定义 M1 的系统入口契约。M1 主入口是 Typer CLI，FastAPI 只保留健康检查和只读查询方向。后续如果加入 React 控制台，前端必须通过 API 读取状态，而不是直接读数据库或运行脚本。

本文档和以下文档联动：

- M1 范围：[m1-scope.md](../../project-progress/m1-scope.md)。
- M1 实施计划：[implementation-plan.md](../../project-progress/implementation-plan.md)。
- M1 Kernel 接口：[kernel-interfaces.md](../kernel/kernel-interfaces.md)。
- 审计与日志：[observability-audit.md](../observability-audit.md)。

## 1. 通用约定

### 1.1 ID

| 字段 | 范围 | 说明 |
|---|---|---|
| `trace_id` | 一次用户操作链路 | CLI 或 API 入口生成，用于串联日志、任务、报告 |
| `run_id` | 数据导入批次 | 对应 `data_ingestion_runs.run_id` |
| `quality_run_id` | 数据质量批次 | 对应 `data_quality_runs.quality_run_id` |
| `candidate_run_id` | 候选股票池生成批次 | 对应 `universe_candidate_runs.candidate_run_id` |
| `task_id` | 研究任务 | 对应 `research_tasks.task_id` |
| `backtest_id` | 回测运行 | 对应 `backtest_runs.backtest_id` |
| `artifact_id` | 报告产物 | 对应 `report_artifacts.artifact_id` |

M1 默认由应用层生成 UUID。日志、报告和错误信息应尽量输出这些 ID，方便复盘。

### 1.2 时间

- 交易日期使用 `YYYY-MM-DD`。
- 系统时间使用 ISO 8601 带时区时间。
- 数据切分、行情记录和事件记录必须区分交易日期和系统记录时间。

### 1.3 金额、价格和比例

- 入库事实数据使用 `Decimal` 和 PostgreSQL `numeric`。
- 不使用 `float` 保存价格、金额、成交量和收益率事实。
- CLI 参数可以接收字符串形式的小数，进入 kernel 前转换为 `Decimal`。

## 2. CLI 设计

### 2.1 顶层命令

```bash
augur_maestro --help
augur_maestro doctor
augur_maestro data --help
augur_maestro universe --help
augur_maestro research --help
augur_maestro backtest --help
augur_maestro report --help
```

`doctor` 用于本地环境检查，只检查 Python、依赖、配置、数据库连接和目录权限。它不得调用真实券商接口，也不得探测真实下单能力。

### 2.2 数据命令

```bash
augur_maestro data init-db
augur_maestro data import-symbols --market CN_A --provider akshare
augur_maestro data import-calendar --market CN_A --start 2016-01-01 --end 2026-05-15
augur_maestro data import-daily-bars --universe-id <uuid> --start 2016-01-01 --end 2026-05-15 --adjust none --adjust qfq
augur_maestro data validate --universe-id <uuid> --start 2016-01-01 --end 2026-05-15 --adjust qfq
```

成功输出：

```text
status=succeeded
trace_id=<uuid>
run_id=<uuid>
row_count=12345
failed_count=0
```

失败输出：

```text
status=failed
trace_id=<uuid>
error_code=data.provider_unavailable
message=AKShare provider failed; see logs for trace_id
```

规则：

- 导入任务必须先创建批次，再执行拉取和写入。
- 部分失败必须标记 `partial_failed`。
- 质量检查失败不能静默通过。
- 如果数据质量存在 `error` 级问题，下游研究任务默认拒绝使用该数据区间。

### 2.3 股票池命令

```bash
augur_maestro universe build-candidates --config configs/universe/m1_theme_universe.yaml
augur_maestro universe list-candidates --candidate-run-id <uuid>
augur_maestro universe decide --candidate-id <uuid> --decision approved --reason "人工确认属于半导体设备链"
augur_maestro universe approve-run --universe-id <uuid> --candidate-run-id <uuid>
augur_maestro universe list-members --universe-id <uuid>
```

规则：

- 候选生成只创建候选，不修改正式股票池。
- `decide` 必须记录 `decided_by`、`decision_reason` 和 `decided_at`。
- `approve-run` 只导入 `approved` 候选。
- 候选理由为空、只有关键词、只有股票名称碰瓷时，服务层应拒绝批准或标记需人工补理由。

### 2.4 研究命令

```bash
augur_maestro research create-task --config configs/research/m1_baseline.yaml
augur_maestro research prepare-data --task-id <uuid>
augur_maestro research show --task-id <uuid>
```

研究配置示例：

```yaml
name: "m1_theme_baseline"
goal: "验证主题股票池的低频动量基线"
market: "CN_A"
universe_id: "00000000-0000-0000-0000-000000000000"
data:
  start_date: "2016-01-01"
  end_date: "2026-05-15"
  adjust: "qfq"
  simulation_holdout_years: 1
split:
  method: "time_order_8_2_plus_1y_holdout"
  train_ratio: "0.8"
  backtest_ratio: "0.2"
risk_assumption:
  fee_rate: "0.0003"
  slippage_bps: "5"
```

规则：

- `create-task` 只创建任务和切分，不运行回测。
- `prepare-data` 检查股票池、数据范围和质量状态。
- 配置哈希必须入库。

### 2.5 回测命令

```bash
augur_maestro backtest run --task-id <uuid> --engine vectorbt --strategy m1_momentum_baseline
augur_maestro backtest attribution --backtest-id <uuid>
augur_maestro backtest show --backtest-id <uuid>
```

规则：

- 回测只能读取标准化数据库数据。
- 回测虚拟订单和虚拟成交必须写入回测表，不得写入真实 OMS 表。
- 回测失败写 `backtest_runs.error_message`。
- 若数据质量未通过，除非显式 `--allow-warning-data` 且只有 warning 级问题，否则拒绝运行。

### 2.6 报告命令

```bash
augur_maestro report generate --task-id <uuid> --backtest-id <uuid> --format markdown
augur_maestro report list --task-id <uuid>
```

规则：

- 报告默认写入 `outputs/reports/`。
- 报告文件哈希写入 `report_artifacts`。
- 报告必须包含风险提示。
- 报告不得包含密钥、账号隐私、真实资金隐私或完整外部 provider 凭证。

## 3. CLI 退出码

| 退出码 | 含义 |
|---:|---|
| 0 | 成功 |
| 1 | 通用失败 |
| 2 | 参数或配置错误 |
| 3 | 外部数据源失败 |
| 4 | 数据质量阻断 |
| 5 | 数据库或迁移失败 |
| 6 | 回测执行失败 |
| 7 | 安全规则阻断 |

退出码只是给 shell 和 CI 使用。面向人的具体原因必须通过 `error_code`、`trace_id` 和日志定位。

## 4. 错误码

错误码使用命名空间形式：

| 错误码 | 场景 |
|---|---|
| `config.invalid` | YAML 或 `.env` 配置不合法 |
| `database.connection_failed` | 数据库连接失败 |
| `database.migration_failed` | 迁移失败 |
| `data.provider_unavailable` | 数据源不可用 |
| `data.ingestion_partial_failed` | 部分标的导入失败 |
| `data.quality_blocked` | 数据质量问题阻断 |
| `universe.candidate_reason_required` | 候选理由缺失 |
| `universe.candidate_not_approved` | 候选未批准 |
| `research.task_not_ready` | 研究任务未满足运行条件 |
| `backtest.engine_failed` | 回测引擎失败 |
| `report.render_failed` | 报告生成失败 |
| `security.live_trading_forbidden_in_m1` | M1 禁止真实交易能力 |

后续 FastAPI 也使用同一套错误码，不在 API 响应中直接返回大段中文错误解释。

## 5. FastAPI 只读契约

M1 API 不作为主入口。若实现，基础约定如下：

- API base path：`/api/v1`。
- 健康检查：`GET /healthz`，不放在 `/api/v1` 下。
- 响应默认 JSON。
- 所有响应带 `trace_id`。

成功响应：

```json
{
  "data": {},
  "meta": {
    "trace_id": "00000000-0000-0000-0000-000000000000"
  }
}
```

错误响应：

```json
{
  "error_code": "data.quality_blocked",
  "params": {
    "quality_run_id": "00000000-0000-0000-0000-000000000000"
  },
  "trace_id": "00000000-0000-0000-0000-000000000000"
}
```

M1 可选只读接口：

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/healthz` | 健康检查 |
| `GET` | `/version` | 版本信息 |
| `GET` | `/api/v1/data/ingestion-runs` | 导入批次列表 |
| `GET` | `/api/v1/data/quality-runs/{id}` | 质量检查结果 |
| `GET` | `/api/v1/research/tasks` | 研究任务列表 |
| `GET` | `/api/v1/backtests/{id}` | 回测摘要 |
| `GET` | `/api/v1/reports` | 报告产物列表 |

M1 API 禁止：

- 触发真实交易。
- 调用券商 SDK。
- 触发下单、撤单、条件单。
- 绕过 kernel 服务直接写数据库。

## 6. DTO 落点

M1 的领域 DTO 以 [kernel-interfaces.md](../kernel/kernel-interfaces.md) 为准。

API 层如果需要 Pydantic schema，只能作为边界对象：

```text
src/
  backend/
    app/
      schemas/
        data.py
        universe.py
        research.py
        backtest.py
        report.py
```

规则：

- Pydantic schema 不替代核心 dataclass。
- SQLAlchemy ORM 模型不作为 API 返回对象。
- API handler 必须调用 service，不直接拼 SQL。
- CLI 命令也必须调用 service，不直接操作 repository。

## 7. 日志契约摘要

所有 CLI 和 API 入口必须至少记录：

- `ts`。
- `level`。
- `event`。
- `trace_id`。
- 当前命令或 API path。
- 关键资源 ID。
- `status`。
- `duration_ms`。
- `error_code`，如有。

禁止日志输出：

- 数据库密码。
- 券商 API Key、Secret、token。
- 真实账号。
- 身份证件。
- 完整 prompt。
- 完整报告正文。
- 真实资金隐私。

详细规则见 [observability-audit.md](../observability-audit.md)。
