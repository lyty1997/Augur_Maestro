# A 股历史数据源技术路线规划

版本：v0.1  
状态：部分确认  
最后更新：2026-05-14

## 1. 目标

本文档定义 RobustQuant M1 的 A 股研究回测闭环所需的历史数据源路线。核心目标是：先用足够轻量的数据源把研究、因子、回测和报告跑起来，同时保证未来可以切换到 miniQMT 或其他券商数据源，而不重写策略和回测逻辑。

M1 的数据目标不是追求全市场、全字段、全频率，而是建立一条可复现、可替换、可校验的研究数据链路。M1 具体 PostgreSQL 表、字段、约束和迁移顺序见 [08-m1-data-model.md](../20-m1/08-m1-data-model.md)。

## 2. 已确认决策

- M1 研究市场为 A 股。
- M1 默认历史行情启动源使用 AKShare。
- M1 先导入用户熟悉主题相关标的，不先导入全 A 股。
- M1 默认导入最近 10 年日线数据；最近 1 年作为模拟数据，此前数据按时间顺序 8:2 切分为建模数据和回测数据。
- AKShare 只作为研究期数据源，不作为长期生产真相源。
- 生产级目标优先使用券商接口，尤其是后续 miniQMT 可用后的 A 股行情和账户数据。
- 策略、因子、回测和研究 Agent 不能直接调用 AKShare，只能读取 RobustQuant 内部标准化数据表。
- 数据接入必须通过 `DataProvider` 抽象，后续新增 `MiniQMTDataProvider` 时不影响上层研究逻辑。
- M1 需要加入第二数据源做关键字段交叉验证，降低单一 AKShare 数据源导致的研究偏差。

## 3. 为什么先用 AKShare

AKShare 解决的是“没有券商数据接口前，如何快速拿到足够研究用的 A 股历史数据”的问题。

它适合 M1 的原因：

- 不需要先完成券商 API 权限申请。
- 能覆盖 A 股个股历史行情，支持日线、周线、月线。
- 支持前复权、后复权和不复权数据，便于先做日频技术因子和基础回测。
- Python 生态使用方便，适合快速接入 PostgreSQL 数据导入流程。

它的边界也必须明确：

- AKShare 是聚合数据接口，底层源站和字段可能变化。
- 可能遇到源站限流、字段调整、复权异常、历史数据修正等问题。
- 不提供券商级服务可用性承诺。
- 不适合作为最终实盘前唯一校验数据源。

因此 M1 可以用 AKShare 启动，但工程设计必须默认“未来会替换或并行校验数据源”。

## 4. 数据源分层路线

### 4.1 第一层：研究启动源

默认实现：

- `AkshareDataProvider`

主要用途：

- 拉取 A 股股票列表。
- 拉取或生成用户熟悉主题的候选股票池，供人工确认。
- 拉取 A 股日线行情。
- 拉取前复权和不复权行情。
- 拉取基础指数行情，用于基准收益和市场状态判断。

M1 先不依赖：

- 分钟线。
- Level-2 行情。
- 财务深度数据。
- 实时行情。
- 交易接口。

### 4.2 第二层：交叉验证源

M1 至少选择一种实现：

- `BaostockDataProvider`
- `TushareDataProvider`
- 本地 CSV/Parquet 导入 Provider。

主要用途：

- 抽样对比 AKShare 数据。
- 检查复权、停牌、涨跌停、成交量、成交额是否明显异常。
- 在 AKShare 临时不可用时保证研究流程可继续。

M1 第一版不要求全字段、全市场逐条对比。优先做主题股票池内关键字段抽样：交易日、收盘价、成交量、成交额和复权序列一致性。

### 4.3 第三层：生产目标源

后续实现：

- `MiniQMTDataProvider`

主要用途：

- 使用券商或 QMT 体系提供的行情和交易相关数据。
- 与真实账户、持仓、交易链路保持更一致的数据口径。
- 在实盘前作为主要数据源或核心校验源。

注意：miniQMT 的运行环境、权限、客户端登录、自动重连和数据接口能力仍需确认。

## 5. 数据网关设计

数据网关负责把外部数据源转成 RobustQuant 内部统一格式。上层模块只依赖数据网关和标准表，不感知 AKShare、miniQMT 或其他数据源差异。

建议接口：

```python
class DataProvider:
    provider_name: str

    def get_symbols(self, market: str) -> list[SymbolRecord]: ...

    def get_trade_calendar(
        self,
        market: str,
        start_date: str,
        end_date: str,
    ) -> list[TradeCalendarRecord]: ...

    def get_daily_bars(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        adjust: str,
    ) -> list[DailyBarRecord]: ...

    def get_index_daily_bars(
        self,
        index_code: str,
        start_date: str,
        end_date: str,
        adjust: str,
    ) -> list[DailyBarRecord]: ...
```

`adjust` 取值建议：

- `none`：不复权，接近真实历史成交价格。
- `qfq`：前复权，适合多数技术因子和收益序列研究。
- `hfq`：后复权，暂不作为 M1 默认使用。

M1 默认策略：

- 数据入库同时保存 `none` 和 `qfq`。
- 因子计算默认使用 `qfq`。
- 成交模拟、价格限制、涨跌停检查优先参考 `none`。

## 6. PostgreSQL 标准表建议

M1 先建立最小表集。

### 6.1 标的信息表

表名建议：`market_symbols`

核心字段：

- `symbol`：内部统一代码，例如 `600000.SH`。
- `raw_symbol`：数据源原始代码。
- `market`：市场，例如 `CN_A`。
- `exchange`：交易所，例如 `SSE`、`SZSE`、`BSE`。
- `name`：证券名称。
- `asset_type`：资产类型，例如 `stock`、`index`。
- `list_date`：上市日期。
- `delist_date`：退市日期，可为空。
- `is_active`：是否仍在交易。
- `source`：数据来源。
- `ingested_at`：入库时间。

### 6.2 交易日历表

表名建议：`trade_calendars`

核心字段：

- `market`：市场。
- `trade_date`：日期。
- `is_open`：是否交易日。
- `source`：数据来源。
- `ingested_at`：入库时间。

### 6.3 日线行情表

表名建议：`daily_bars`

核心字段：

- `symbol`：内部统一代码。
- `trade_date`：交易日期。
- `adjust`：复权类型，`none`、`qfq`、`hfq`。
- `open`：开盘价。
- `high`：最高价。
- `low`：最低价。
- `close`：收盘价。
- `volume`：成交量。
- `amount`：成交额。
- `turnover_rate`：换手率，可为空。
- `source`：数据来源。
- `provider_version`：Provider 或依赖包版本。
- `raw_payload_hash`：原始数据哈希，用于追踪数据是否变化。
- `ingested_at`：入库时间。

唯一约束建议：

```text
(symbol, trade_date, adjust, source)
```

### 6.4 数据导入批次表

表名建议：`data_ingestion_runs`

核心字段：

- `run_id`：导入批次 ID。
- `provider`：数据 Provider 名称。
- `market`：市场。
- `dataset`：数据集名称，例如 `daily_bars`。
- `start_date`：开始日期。
- `end_date`：结束日期。
- `status`：`running`、`succeeded`、`failed`、`partial_failed`。
- `row_count`：写入行数。
- `error_message`：错误原因。
- `started_at`：开始时间。
- `finished_at`：结束时间。

## 7. 数据导入流程

M1 推荐流程：

1. 手动或定时触发数据导入任务。
2. 记录 `data_ingestion_runs`，状态为 `running`。
3. `AkshareDataProvider` 拉取原始数据。
4. 数据网关做字段映射、代码标准化、类型转换。
5. 数据质量检查通过后写入 PostgreSQL。
6. 第二数据源对关键字段做抽样交叉验证，并记录差异报告。
7. 写入完成后更新导入批次状态。
8. 研究 Agent 和回测模块只读取 PostgreSQL 标准表。

失败处理原则：

- 数据导入失败不能静默吞掉。
- 部分股票失败时，导入批次标记为 `partial_failed`。
- 数据质量检查失败的数据不能进入“可用于回测”的状态。
- 研究报告必须记录使用的数据源、导入批次和数据时间范围。

## 8. 数据质量检查

M1 至少做以下检查。

### 8.1 字段完整性

- `open`、`high`、`low`、`close`、`volume`、`amount` 是否缺失。
- `high >= low` 是否成立。
- `high >= open/close`、`low <= open/close` 是否成立。
- 成交量和成交额是否为负数。

### 8.2 时间完整性

- 股票交易日期是否落在 A 股交易日历内。
- 非停牌股票是否存在异常缺失。
- 是否出现重复 `(symbol, trade_date, adjust, source)`。

### 8.3 价格异常

- 单日涨跌幅是否超过合理阈值。
- 前复权序列是否出现明显断裂。
- 不复权价格是否能解释涨跌停判断。

### 8.4 数据源稳定性

- 同一导入参数重复拉取后，行数是否明显变化。
- 相同日期、相同股票的关键字段是否发生变化。
- AKShare 版本升级后是否触发抽样重算。
- 第二数据源关键字段抽样对比是否出现显著差异。

## 9. 与回测的关系

回测引擎不直接访问 AKShare。回测只接收 RobustQuant 的标准化数据。

建议规则：

- 因子和收益计算默认使用前复权 `qfq` 数据。
- 交易价格、涨跌停、停牌和成交约束尽量参考不复权 `none` 数据。
- 每次回测必须记录数据快照信息，包括数据源、导入批次、复权方式和数据时间范围。
- 如果数据质量检查未通过，研究 Agent 不能输出“可进入模拟盘”结论。

这能降低一个常见风险：回测看起来很好，其实只是数据复权、停牌或未来函数处理错了。

## 10. 里程碑计划

### M1：AKShare 最小闭环

目标：

- 拉取 A 股基础股票列表。
- 通过 AKShare 概念板块、行业分类、公开资料和 AI 辅助生成候选股票池，经用户确认后建立主题股票池。
- 拉取主题股票池的日线行情。
- 同时保存不复权和前复权数据。
- 写入 PostgreSQL 标准表。
- 完成基础数据质量检查。
- 接入第二数据源，对关键字段做交叉验证。
- 让回测模块能从标准表读取数据。

验收标准：

- 能导入用户熟悉主题股票池最近 10 年日线数据；如果标的上市不足 10 年，从可获得数据首日开始。
- 能生成最近 1 年模拟数据留出，以及此前数据 8:2 建模/回测切分标记。
- 能生成导入批次记录。
- 能报告缺失、重复、价格异常等基础问题。
- 能生成第二数据源交叉验证差异摘要。
- 策略和回测代码中不出现 AKShare 直接调用。

### M1 扩展任务：全市场研究数据

目标：

- 扩展到全 A 股日线。
- 增加指数行情，例如沪深 300、中证 500、创业板指。
- 增加基础股票池过滤字段，例如上市天数、ST、停牌、成交额。
- 支持增量更新。

验收标准：

- 每个交易日可更新最新日线数据。
- 能按规则生成可研究股票池。
- 能支持第一批技术因子计算和成熟回测库输入。

### M1 必做校验任务：数据源交叉校验

目标：

- 接入 BaoStock 作为第一版校验源；Tushare Pro 或本地 CSV/Parquet 作为后续备用源。
- 对关键字段做抽样对比。
- 记录数据差异报告。

验收标准：

- 能发现并报告复权、成交额、停牌状态等明显差异。
- 能在研究报告里标记数据源风险。

### 后续数据源切换：切入券商数据源

目标：

- miniQMT 数据接口可用后，实现 `MiniQMTDataProvider`。
- 用同样的标准表和质量检查接入券商数据。
- 对比 AKShare 与 miniQMT 的历史行情差异。

验收标准：

- 上层策略、因子、回测代码无需修改即可切换数据源。
- 能输出 AKShare 与 miniQMT 的差异报告。
- 实盘候选策略必须经过券商数据源复核。

## 11. 当前待确认问题

- 主题股票池第一版具体标的清单。
- M1 默认只导入日线，分钟线延后。
- BaoStock 字段、限流或维护状态不满足 M1 需要时，是否切换本地 CSV/Parquet 作为备用校验源。
- 本地 PostgreSQL 优先 Docker Compose，若环境不便再使用本机服务。
- 后续是否需要补充商业数据源，用于财务、公告、新闻和更高质量复权数据。

## 12. 参考链接

- AKShare 股票数据文档：https://akshare.akfamily.xyz/data/stock/stock.html
- AKShare GitHub：https://github.com/akfamily/akshare
