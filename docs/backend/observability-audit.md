# 审计、日志、可观测性和隐私规范

版本：v0.1  
状态：草案，待用户确认  
最后更新：2026-05-15

## 0. 文档定位

本文档定义 RobustQuant 的日志、审计、追踪、复盘和敏感信息保护规则。

量化系统涉及资金风险，即使 M1 不接真实交易，也要从一开始形成“可复现、可追踪、可解释”的习惯。后续进入实盘时，日志和审计不是附属功能，而是安全边界的一部分。

## 1. 目标

系统出问题时，必须能回答：

- 哪个命令或接口触发了动作。
- 使用了哪个配置文件和配置哈希。
- 使用了哪个数据源、导入批次和 Provider 版本。
- 数据质量检查结果是什么。
- 哪个股票池和研究任务参与了回测。
- 回测用了哪个引擎、策略、参数和时间窗口。
- 报告来自哪个 `task_id` 和 `backtest_id`。
- 如果未来进入交易，订单来自哪个策略、意图、风控结果和 OMS 状态。

## 2. 追踪 ID

| ID | 使用场景 |
|---|---|
| `trace_id` | 一次用户操作或命令链路 |
| `run_id` | 数据导入批次 |
| `quality_run_id` | 数据质量检查批次 |
| `candidate_run_id` | 候选股票池生成批次 |
| `task_id` | 研究任务 |
| `backtest_id` | 回测运行 |
| `artifact_id` | 报告产物 |
| `intent_id` | 后续交易意图 |
| `order_id` | 后续本地订单 |
| `broker_order_id` | 后续券商订单号，日志中必须脱敏 |

规则：

- CLI 每次执行生成或接收一个 `trace_id`。
- API 每个 request 生成或接收一个 `trace_id`。
- 长任务创建自己的业务 ID，并和 `trace_id` 关联。
- 报告必须能反查 `task_id`、`backtest_id` 和数据批次。

## 3. 结构化日志

日志使用 JSON Lines，每行一个事件。

最小字段：

```json
{
  "ts": "2026-05-15T12:00:00.000Z",
  "level": "info",
  "event": "data.ingestion_completed",
  "trace_id": "00000000-0000-0000-0000-000000000000",
  "run_id": "00000000-0000-0000-0000-000000000000",
  "status": "succeeded",
  "duration_ms": 1200
}
```

建议字段：

- `command`。
- `api_path`。
- `provider`。
- `dataset`。
- `universe_id`。
- `task_id`。
- `backtest_id`。
- `error_code`。
- `message`。
- `metadata`，仅放非敏感摘要。

## 4. M1 必须记录的事件

| 事件 | 说明 |
|---|---|
| `cli.command_started` | CLI 命令开始 |
| `cli.command_completed` | CLI 命令成功 |
| `cli.command_failed` | CLI 命令失败 |
| `config.loaded` | 配置读取成功 |
| `database.migration_started` | 迁移开始 |
| `database.migration_completed` | 迁移完成 |
| `data.ingestion_started` | 数据导入开始 |
| `data.ingestion_completed` | 数据导入完成 |
| `data.ingestion_failed` | 数据导入失败 |
| `data.quality_started` | 质量检查开始 |
| `data.quality_completed` | 质量检查完成 |
| `universe.candidate_run_created` | 候选生成批次创建 |
| `universe.candidate_decided` | 候选人工决策 |
| `research.task_created` | 研究任务创建 |
| `research.dataset_split_created` | 数据切分创建 |
| `backtest.run_started` | 回测开始 |
| `backtest.run_completed` | 回测完成 |
| `backtest.run_failed` | 回测失败 |
| `report.generated` | 报告生成 |

未来实盘必须补充：

- `risk.check_completed`。
- `order.created`。
- `order.submitted`。
- `order.unknown`。
- `order.cancel_requested`。
- `broker.query_completed`。
- `reconciliation.mismatch_detected`。
- `strategy.paused`。
- `manual.action_confirmed`。

## 5. 审计事件和普通日志

普通日志用于排查运行问题。审计事件用于复盘关键业务动作。

M1 可以先用 `research_task_events`、导入批次表和报告产物表承载审计信息。后续进入 M2/M3 时，需要单独设计 `audit_events` 或事件溯源表。

审计事件特点：

- 不随日志轮转删除。
- 不能包含敏感原文。
- 能关联操作者、动作、资源和结果。
- 关键字段可查询。

## 6. 敏感信息红线

任何日志、文档、报告、错误消息和测试 fixture 都禁止包含：

- 券商 API Key。
- Secret。
- token。
- 密码。
- session cookie。
- 真实完整账号。
- 身份证、护照等真实身份证明。
- 真实资金余额、真实持仓市值等隐私数据。
- 完整外部 provider 原始认证响应。

允许记录：

- 脱敏账号，例如 `****1234`。
- 内容哈希。
- 字段数量。
- 行数。
- token 数。
- 错误码。
- 非敏感资源 ID。
- 截断后的错误摘要。

## 7. 数据血缘

每份报告都必须记录：

- 数据源。
- Provider 版本。
- 导入批次。
- 质量检查批次。
- 股票池 ID。
- 研究任务 ID。
- 回测 ID。
- 配置哈希。
- 报告生成时间。

这能避免以后出现“这份报告到底怎么来的”这种无法回答的问题。

## 8. 文件和产物

运行产物默认进入 `outputs/`：

```text
outputs/
  reports/
  backtests/
  attribution/
  data_quality/
  universe_candidates/
```

规则：

- `outputs/` 不进入 Git。
- 数据库只保存路径、哈希、类型和关联 ID。
- 报告如需长期留存，可以单独人工归档。
- 归档前必须确认不含敏感信息。

## 9. 错误处理

错误处理要求：

- 不吞异常。
- 不只打印控制台。
- CLI 返回非 0 退出码。
- 数据库状态写失败原因。
- 日志写 `trace_id` 和 `error_code`。
- 面向用户的错误信息说明下一步排查方向。

示例：

```text
error_code=data.quality_blocked
trace_id=...
message=数据质量检查发现 error 级问题，已阻止回测。请查看 quality_run_id=...
```

## 10. 可观测性分层

M1 最小：

- JSON 文件日志。
- CLI 输出关键 ID。
- 数据库保存任务状态。
- Markdown 报告保存血缘信息。

M2 可增加：

- 后台任务状态页。
- 运行中任务进度。
- 模拟盘事件日志。

M3 实盘前必须增加：

- 实时告警。
- 订单 unknown 告警。
- 对账不一致告警。
- 策略暂停告警。
- 日志集中存储。
- 关键操作人工确认记录。

## 11. 保留周期

M1 建议：

- 数据库研究记录长期保留。
- 报告产物长期保留或人工归档。
- 普通运行日志可按大小或日期轮转。
- 敏感错误上下文不得长期保留原文。

M3 实盘前必须重新定义：

- 订单、成交、对账和审计事件保留周期。
- 备份策略。
- 恢复演练。
- 日志访问权限。
