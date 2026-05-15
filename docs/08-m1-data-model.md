# M1 数据模型设计

版本：v0.1  
状态：草案  
最后更新：2026-05-15

## 1. 文档定位

本文档定义 RobustQuant M1 的 PostgreSQL 数据模型。目标是让后续 SQLAlchemy 模型和 Alembic 迁移有明确依据。

M1 只覆盖 A 股研究回测闭环，不覆盖真实下单。订单、成交、持仓、资金和实盘对账模型后续单独设计。

相关文档：

- 总体架构：[01-architecture.md](./01-architecture.md)。
- 总体路线：[05-technical-roadmap.md](./05-technical-roadmap.md)。
- 数据源路线：[06-data-source-roadmap.md](./06-data-source-roadmap.md)。
- M1 工程设计：[07-m1-engineering-design.md](./07-m1-engineering-design.md)。
- M1 Kernel 接口类设计：[09-m1-kernel-interfaces.md](./09-m1-kernel-interfaces.md)。

## 2. 建模原则

- 领域核心表归属于明确 kernel，避免所有模块随意读写同一张表。
- 行情、股票池、研究任务、回测结果必须可复现、可追踪。
- 用户可见标的使用“代码 + 名称”，例如 `688981.SH 中芯国际`；内部关联使用标准代码 `symbol`。
- 日期字段分清交易日期和系统时间：`trade_date` 使用交易所日历日期，`created_at`、`updated_at`、`ingested_at` 使用带时区时间。
- 价格、金额、成交量使用 `numeric`，不使用浮点数保存入库事实数据。
- 结构化字段优先拆列；外部源额外字段可放 `raw_payload` 或 `metadata` JSONB。
- 不在数据库保存券商 API Key、Secret、token、密码、真实账户隐私数据。
- 中间产物和大文件默认保存在 `outputs/`，数据库只保存路径、摘要和关键指标。

## 3. Kernel 表归属

| Kernel | 表 | 说明 |
| --- | --- | --- |
| `data_kernel` | `market_symbols` | 标的信息 |
| `data_kernel` | `trade_calendars` | 交易日历 |
| `data_kernel` | `daily_bars` | 日线行情 |
| `data_kernel` | `data_ingestion_runs` | 数据导入批次 |
| `data_kernel` | `data_quality_runs` | 数据质量检查批次 |
| `data_kernel` | `data_quality_issues` | 数据质量问题 |
| `universe_kernel` | `research_universes` | 研究股票池 |
| `universe_kernel` | `research_universe_members` | 股票池正式成员 |
| `universe_kernel` | `universe_candidate_runs` | 候选股票池生成批次 |
| `universe_kernel` | `universe_candidates` | 候选股票 |
| `research_kernel` | `research_tasks` | 研究任务 |
| `research_kernel` | `dataset_splits` | 数据切分记录 |
| `research_kernel` | `research_task_events` | 研究任务状态事件 |
| `backtest_kernel` | `backtest_runs` | 回测运行记录 |
| `backtest_kernel` | `backtest_metrics` | 回测指标 |
| `backtest_kernel` | `backtest_equity_curve` | 回测权益曲线 |
| `backtest_kernel` | `backtest_orders` | 回测虚拟订单 |
| `backtest_kernel` | `backtest_trades` | 回测虚拟成交 |
| `backtest_kernel` | `backtest_attribution_items` | 回测归因结果 |
| `backtest_kernel` | `backtest_drawdown_segments` | 回撤片段归因 |
| `report_kernel` | `report_artifacts` | 报告产物 |

## 4. 通用字段规范

建议所有业务主表包含：

- `created_at timestamptz not null`
- `updated_at timestamptz not null`

可选审计字段：

- `created_by text`
- `updated_by text`

命名约定：

- ID 字段使用 `uuid`，例如 `run_id`、`task_id`、`backtest_id`。
- 标的代码统一字段名为 `symbol`。
- 数据来源统一字段名为 `source` 或 `provider`。
- 状态字段统一使用 `status text`，M1 先用应用层枚举 + 数据库 check 约束。

金额和价格建议：

- 价格：`numeric(18, 6)`。
- 成交量：`numeric(24, 4)`。
- 成交额：`numeric(24, 4)`。
- 比例和收益：`numeric(18, 8)`。

## 5. data_kernel

### 5.1 `market_symbols`

用途：保存内部统一标的信息。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `symbol` | text PK | 内部统一代码，例如 `600000.SH` |
| `raw_symbol` | text | 数据源原始代码 |
| `market` | text | 市场，例如 `CN_A` |
| `exchange` | text | 交易所，例如 `SSE`、`SZSE`、`BSE` |
| `name` | text | 证券名称 |
| `asset_type` | text | `stock`、`index`、`etf` |
| `list_date` | date | 上市日期 |
| `delist_date` | date nullable | 退市日期 |
| `is_active` | boolean | 是否仍在交易 |
| `source` | text | 来源 |
| `metadata` | jsonb | 扩展信息 |
| `ingested_at` | timestamptz | 入库时间 |

约束和索引：

- 主键：`symbol`。
- 索引：`(market, exchange)`、`(name)`、`(is_active)`。

### 5.2 `trade_calendars`

用途：保存交易日历。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `market` | text | 市场 |
| `trade_date` | date | 日期 |
| `is_open` | boolean | 是否交易日 |
| `source` | text | 来源 |
| `ingested_at` | timestamptz | 入库时间 |

约束和索引：

- 主键：`(market, trade_date)`。
- 索引：`(market, is_open, trade_date)`。

### 5.3 `daily_bars`

用途：保存日线行情。M1 同时保存不复权 `none` 和前复权 `qfq`。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `bar_id` | uuid PK | 行情记录 ID |
| `symbol` | text FK | 标的代码 |
| `trade_date` | date | 交易日期 |
| `adjust` | text | `none`、`qfq`、`hfq` |
| `open` | numeric(18,6) | 开盘价 |
| `high` | numeric(18,6) | 最高价 |
| `low` | numeric(18,6) | 最低价 |
| `close` | numeric(18,6) | 收盘价 |
| `volume` | numeric(24,4) | 成交量 |
| `amount` | numeric(24,4) | 成交额 |
| `turnover_rate` | numeric(18,8) nullable | 换手率 |
| `source` | text | 数据来源 |
| `provider_version` | text | Provider 或依赖包版本 |
| `ingestion_run_id` | uuid FK | 导入批次 |
| `raw_payload_hash` | text | 原始数据哈希 |
| `ingested_at` | timestamptz | 入库时间 |

约束和索引：

- 唯一约束：`(symbol, trade_date, adjust, source)`。
- 外键：`symbol -> market_symbols.symbol`。
- 索引：`(symbol, trade_date)`、`(trade_date)`、`(source, adjust)`。

数据规则：

- `high >= low`。
- `high >= open`、`high >= close`。
- `low <= open`、`low <= close`。
- `volume >= 0`。
- `amount >= 0`。

### 5.4 `data_ingestion_runs`

用途：记录每次数据导入。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `run_id` | uuid PK | 导入批次 ID |
| `provider` | text | `akshare`、`baostock`、`miniqmt` |
| `dataset` | text | `symbols`、`daily_bars`、`trade_calendar` |
| `market` | text | 市场 |
| `universe_id` | uuid nullable | 股票池 |
| `start_date` | date nullable | 数据开始日期 |
| `end_date` | date nullable | 数据结束日期 |
| `adjust` | text nullable | 复权类型 |
| `status` | text | 状态 |
| `row_count` | integer | 写入行数 |
| `failed_count` | integer | 失败行数或标的数 |
| `config_hash` | text | 导入配置哈希 |
| `error_message` | text nullable | 错误信息 |
| `started_at` | timestamptz | 开始时间 |
| `finished_at` | timestamptz nullable | 结束时间 |

状态枚举：

- `pending`
- `running`
- `succeeded`
- `partial_failed`
- `failed`
- `cancelled`

索引：

- `(provider, dataset, started_at)`。
- `(status, started_at)`。

### 5.5 `data_quality_runs`

用途：记录数据质量检查批次。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `quality_run_id` | uuid PK | 检查批次 ID |
| `ingestion_run_id` | uuid nullable FK | 对应导入批次 |
| `dataset` | text | 检查数据集 |
| `universe_id` | uuid nullable | 股票池 |
| `start_date` | date nullable | 检查开始日期 |
| `end_date` | date nullable | 检查结束日期 |
| `status` | text | 状态 |
| `issue_count` | integer | 问题数量 |
| `started_at` | timestamptz | 开始时间 |
| `finished_at` | timestamptz nullable | 结束时间 |

状态枚举：

- `running`
- `passed`
- `warning`
- `failed`

### 5.6 `data_quality_issues`

用途：记录具体数据质量问题。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `issue_id` | uuid PK | 问题 ID |
| `quality_run_id` | uuid FK | 检查批次 |
| `severity` | text | `info`、`warning`、`error` |
| `issue_type` | text | `missing_value`、`duplicate_bar`、`price_invalid` 等 |
| `symbol` | text nullable | 标的代码 |
| `trade_date` | date nullable | 交易日期 |
| `field_name` | text nullable | 字段 |
| `message` | text | 问题说明 |
| `metadata` | jsonb | 额外上下文 |
| `created_at` | timestamptz | 创建时间 |

索引：

- `(quality_run_id)`。
- `(symbol, trade_date)`。
- `(severity, issue_type)`。

## 6. universe_kernel

### 6.1 `research_universes`

用途：保存正式研究股票池。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `universe_id` | uuid PK | 股票池 ID |
| `name` | text | 名称，例如 `m1_theme_universe` |
| `description` | text | 说明 |
| `status` | text | 状态 |
| `created_by` | text | 创建来源 |
| `created_at` | timestamptz | 创建时间 |
| `updated_at` | timestamptz | 更新时间 |

状态枚举：

- `draft`
- `active`
- `archived`

唯一约束：

- `name` 唯一。

### 6.2 `research_universe_members`

用途：保存正式股票池成员。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `member_id` | uuid PK | 成员 ID |
| `universe_id` | uuid FK | 股票池 |
| `symbol` | text FK | 标的代码 |
| `name` | text | 标的名称，冗余保存便于审计 |
| `theme` | text | 主题 |
| `source` | text | `manual`、`akshare_concept`、`ai_candidate` |
| `reason` | text | 纳入理由 |
| `confidence` | numeric(18,8) nullable | 候选置信度 |
| `is_active` | boolean | 是否启用 |
| `added_at` | timestamptz | 加入时间 |
| `removed_at` | timestamptz nullable | 移除时间 |

唯一约束：

- `(universe_id, symbol, theme)`。

索引：

- `(universe_id, is_active)`。
- `(symbol)`。
- `(theme)`。

### 6.3 `universe_candidate_runs`

用途：记录每次候选股票池生成。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `candidate_run_id` | uuid PK | 候选生成批次 |
| `name` | text | 名称 |
| `themes` | text[] | 主题列表 |
| `method` | text | `akshare_concept`、`ai_assisted`、`manual_seed` |
| `status` | text | 状态 |
| `config_hash` | text | 配置哈希 |
| `prompt_hash` | text nullable | AI 提示词哈希，不保存敏感信息 |
| `started_at` | timestamptz | 开始时间 |
| `finished_at` | timestamptz nullable | 结束时间 |

状态枚举：

- `running`
- `succeeded`
- `failed`
- `cancelled`

### 6.4 `universe_candidates`

用途：保存候选股票。候选不等于正式股票池成员。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `candidate_id` | uuid PK | 候选 ID |
| `candidate_run_id` | uuid FK | 候选批次 |
| `symbol` | text FK | 标的代码 |
| `name` | text | 标的名称 |
| `theme` | text | 主题 |
| `source` | text | 来源 |
| `reason` | text | 候选理由 |
| `confidence` | numeric(18,8) nullable | 置信度 |
| `decision_status` | text | 人工确认状态 |
| `decision_reason` | text nullable | 人工确认说明 |
| `decided_by` | text nullable | 确认人 |
| `decided_at` | timestamptz nullable | 确认时间 |

状态枚举：

- `pending`
- `approved`
- `rejected`
- `ignored`

唯一约束：

- `(candidate_run_id, symbol, theme)`。

规则：

- 只有 `approved` 的候选才能写入 `research_universe_members`。
- 候选理由不能只写关键词命中，必须说明真实关联依据。

## 7. research_kernel

### 7.1 `research_tasks`

用途：保存研究任务。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `task_id` | uuid PK | 研究任务 ID |
| `name` | text | 任务名称 |
| `universe_id` | uuid FK | 股票池 |
| `goal` | text | 研究目标 |
| `config_path` | text | YAML 配置路径 |
| `config_hash` | text | 配置哈希 |
| `status` | text | 状态 |
| `data_start_date` | date | 数据开始 |
| `data_end_date` | date | 数据结束 |
| `simulation_start_date` | date | 模拟数据开始 |
| `simulation_end_date` | date | 模拟数据结束 |
| `created_at` | timestamptz | 创建时间 |
| `updated_at` | timestamptz | 更新时间 |

状态枚举：

- `created`
- `data_ready`
- `running`
- `backtested`
- `reported`
- `failed`
- `cancelled`

### 7.2 `dataset_splits`

用途：记录建模、回测、模拟数据切分。M1 默认最近 1 年模拟，之前数据按时间 8:2 切分。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `split_id` | uuid PK | 切分 ID |
| `task_id` | uuid FK | 研究任务 |
| `split_name` | text | `modeling`、`backtest`、`simulation` |
| `start_date` | date | 开始日期 |
| `end_date` | date | 结束日期 |
| `method` | text | `time_order_8_2_plus_1y_holdout` |
| `ratio` | numeric(18,8) nullable | 比例 |
| `created_at` | timestamptz | 创建时间 |

唯一约束：

- `(task_id, split_name)`。

### 7.3 `research_task_events`

用途：记录研究任务状态变化和重要事件。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `event_id` | uuid PK | 事件 ID |
| `task_id` | uuid FK | 研究任务 |
| `event_type` | text | 事件类型 |
| `from_status` | text nullable | 原状态 |
| `to_status` | text nullable | 新状态 |
| `message` | text | 说明 |
| `metadata` | jsonb | 上下文 |
| `created_at` | timestamptz | 创建时间 |

索引：

- `(task_id, created_at)`。

## 8. backtest_kernel

### 8.1 `backtest_runs`

用途：记录回测运行。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `backtest_id` | uuid PK | 回测 ID |
| `task_id` | uuid FK | 研究任务 |
| `engine` | text | `qlib`、`vectorbt` |
| `strategy_name` | text | 策略名称 |
| `config_hash` | text | 回测配置哈希 |
| `status` | text | 状态 |
| `started_at` | timestamptz | 开始时间 |
| `finished_at` | timestamptz nullable | 结束时间 |
| `error_message` | text nullable | 错误信息 |

状态枚举：

- `pending`
- `running`
- `succeeded`
- `failed`
- `cancelled`

### 8.2 `backtest_metrics`

用途：保存回测指标。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `metric_id` | uuid PK | 指标 ID |
| `backtest_id` | uuid FK | 回测 ID |
| `metric_name` | text | 指标名 |
| `metric_value` | numeric(24,8) | 指标值 |
| `metric_unit` | text nullable | 单位 |

唯一约束：

- `(backtest_id, metric_name)`。

建议首批指标：

- `total_return`
- `annual_return`
- `max_drawdown`
- `volatility`
- `sharpe_ratio`
- `win_rate`
- `turnover`

### 8.3 `backtest_equity_curve`

用途：保存权益曲线。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `backtest_id` | uuid FK | 回测 ID |
| `trade_date` | date | 日期 |
| `equity` | numeric(24,8) | 权益 |
| `cash` | numeric(24,8) nullable | 现金 |
| `position_value` | numeric(24,8) nullable | 持仓市值 |
| `daily_return` | numeric(18,8) nullable | 日收益 |
| `drawdown` | numeric(18,8) nullable | 回撤 |

主键：

- `(backtest_id, trade_date)`。

### 8.4 `backtest_orders`

用途：保存回测虚拟订单，便于排查策略行为。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `order_id` | uuid PK | 虚拟订单 ID |
| `backtest_id` | uuid FK | 回测 ID |
| `trade_date` | date | 交易日期 |
| `symbol` | text | 标的代码 |
| `name` | text | 标的名称 |
| `side` | text | `buy`、`sell` |
| `order_type` | text | M1 默认 `limit_simulated` 或 `close_price_simulated` |
| `quantity` | numeric(24,4) | 数量 |
| `price` | numeric(18,6) | 价格 |
| `status` | text | `created`、`filled`、`rejected` |
| `reason` | text | 下单原因 |

### 8.5 `backtest_trades`

用途：保存回测虚拟成交。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `trade_id` | uuid PK | 虚拟成交 ID |
| `order_id` | uuid FK | 虚拟订单 |
| `backtest_id` | uuid FK | 回测 ID |
| `trade_date` | date | 成交日期 |
| `symbol` | text | 标的代码 |
| `side` | text | `buy`、`sell` |
| `quantity` | numeric(24,4) | 成交数量 |
| `price` | numeric(18,6) | 成交价格 |
| `fee` | numeric(18,6) | 费用 |
| `slippage` | numeric(18,6) | 滑点 |

注意：这里是回测虚拟成交，不是真实券商成交。真实订单和真实成交后续由 OMS 模型单独设计。

### 8.6 `backtest_attribution_items`

用途：保存回测归因分析结果，用来回答收益和亏损主要来自哪里。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `item_id` | uuid PK | 归因项 ID |
| `backtest_id` | uuid FK | 回测 ID |
| `attribution_type` | text | `pnl`、`return`、`drawdown`、`cost` |
| `dimension_type` | text | `symbol`、`theme`、`factor`、`time_window`、`event_window`、`cost` |
| `dimension_key` | text | 维度键，例如 `688981.SH`、`semiconductor`、`2025-01` |
| `dimension_name` | text | 用户可读名称 |
| `pnl` | numeric(24,8) nullable | 盈亏金额或模拟权益贡献 |
| `return_contribution` | numeric(18,8) nullable | 收益贡献 |
| `trade_count` | integer nullable | 相关交易次数 |
| `win_rate` | numeric(18,8) nullable | 胜率 |
| `avg_holding_days` | numeric(18,4) nullable | 平均持有天数 |
| `max_drawdown_contribution` | numeric(18,8) nullable | 对最大回撤的贡献 |
| `evidence` | text | 归因说明 |
| `metadata` | jsonb | 额外上下文 |
| `created_at` | timestamptz | 创建时间 |

索引：

- `(backtest_id, attribution_type)`。
- `(backtest_id, dimension_type)`。
- `(dimension_type, dimension_key)`。

规则：

- 归因项必须能追溯到回测持仓、虚拟成交、权益曲线、因子值、事件窗口或成本假设。
- `evidence` 不能写成确定因果，只能写可审计的统计解释，例如“该主题在样本期贡献了主要收益”。

### 8.7 `backtest_drawdown_segments`

用途：保存主要回撤区间和回撤来源拆解。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `segment_id` | uuid PK | 回撤片段 ID |
| `backtest_id` | uuid FK | 回测 ID |
| `peak_date` | date | 回撤前高点日期 |
| `trough_date` | date | 回撤低点日期 |
| `recovery_date` | date nullable | 恢复到前高日期 |
| `drawdown` | numeric(18,8) | 回撤幅度 |
| `duration_days` | integer | 持续天数 |
| `main_loss_dimensions` | jsonb | 主要亏损维度，例如标的、主题、因子、事件 |
| `explanation` | text | 面向人的解释 |
| `created_at` | timestamptz | 创建时间 |

索引：

- `(backtest_id, trough_date)`。
- `(backtest_id, drawdown)`。

规则：

- 回撤归因必须引用回测权益曲线和持仓/交易明细。
- 若无法判断主要原因，应明确写“不足以归因”，不能编造原因。

## 9. report_kernel

### 9.1 `report_artifacts`

用途：保存报告产物索引。

核心字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `artifact_id` | uuid PK | 产物 ID |
| `task_id` | uuid nullable FK | 研究任务 |
| `backtest_id` | uuid nullable FK | 回测 |
| `artifact_type` | text | `markdown_report`、`data_quality_report`、`attribution_report` |
| `path` | text | 文件路径，例如 `outputs/reports/...md` |
| `content_hash` | text | 文件哈希 |
| `status` | text | `generated`、`superseded`、`deleted` |
| `created_at` | timestamptz | 创建时间 |

规则：

- 报告文件默认不进 Git。
- 数据库只记录路径、哈希和关联任务。

## 10. 跨 kernel 访问规则

- `data_kernel` 是行情和数据质量事实源，其他 kernel 只读其标准表。
- `universe_kernel` 负责股票池和候选池，其他 kernel 只能通过 `universe_id` 使用正式成员。
- `research_kernel` 负责研究任务和数据切分，不能直接写行情表。
- `backtest_kernel` 负责回测运行和结果，不能直接调用 AKShare。
- `report_kernel` 只读取研究和回测结果生成报告，不修改研究结论。
- `cli` 和 `backend` 只能调用 kernel 服务，不能直接拼 SQL 修改核心表。
- SQLAlchemy ORM 模型只用于基础设施层落库，不能作为 kernel 间传输对象；kernel 对外传递对象按 [09-m1-kernel-interfaces.md](./09-m1-kernel-interfaces.md) 定义。

## 11. M1 最小迁移顺序

建议 Alembic 迁移拆分：

1. `market_symbols`、`trade_calendars`。
2. `data_ingestion_runs`、`daily_bars`。
3. `data_quality_runs`、`data_quality_issues`。
4. `research_universes`、`research_universe_members`。
5. `universe_candidate_runs`、`universe_candidates`。
6. `research_tasks`、`dataset_splits`、`research_task_events`。
7. `backtest_runs`、`backtest_metrics`、`backtest_equity_curve`。
8. `backtest_orders`、`backtest_trades`。
9. `backtest_attribution_items`、`backtest_drawdown_segments`。
10. `report_artifacts`。

这样拆分的好处是每一步都能独立验证，不会一口气建太多表后难以排错。

## 12. 后续不在 M1 的模型

以下模型暂不进入 M1：

- 真实账户模型。
- 真实资金模型。
- 真实持仓模型。
- 真实订单和真实成交模型。
- 券商回报和对账模型。
- 条件单模型。
- 实盘风控配置模型。

这些模型涉及真实交易链路，必须在券商 API 行为、交易时间、风控状态机和 OMS 状态机进一步确认后单独设计。
