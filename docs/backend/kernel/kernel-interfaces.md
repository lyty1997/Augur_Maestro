# M1 Kernel 接口类设计

版本：v0.1  
状态：草案  
最后更新：2026-05-15

## 1. 文档定位

本文档定义 Augur_Maestro M1 的 Python 层接口类。它承接 [data-model.md](../data/data-model.md) 的数据库模型，但不等同于 SQLAlchemy ORM 模型。

目标：

- 明确各 kernel 之间传递哪些对象。
- 明确哪些类是外部数据源、回测库、报告生成器的适配接口。
- 明确 CLI 和 FastAPI 只能调用服务接口，不能绕过 kernel 直接写数据库。
- 为后续代码骨架、类型检查和单元测试提供设计依据。

## 2. 总体原则

- `rq_core` 使用标准库 `dataclasses`、`enum`、`typing.Protocol` 定义核心 DTO 和接口。
- `rq_core` 不依赖 FastAPI、Typer、SQLAlchemy、Qlib、VectorBT、AKShare。
- SQLAlchemy ORM 模型只存在于基础设施层，不能作为 kernel 之间的传输对象。
- Pydantic 可以用于 API 入参、配置解析或 CLI 边界，但不作为核心领域对象的默认形态。
- 入库事实数据中的价格、金额、数量使用 `Decimal`，不使用 `float`。
- 日期使用 `date`；系统时间使用带时区的 `datetime`。
- 所有服务接口都要可测试，外部依赖通过 Protocol 注入。

推荐目录：

```text
src/
  rq_core/
    common/
      types.py
      errors.py
    data_kernel/
      records.py
      ports.py
      services.py
    universe_kernel/
      records.py
      ports.py
      services.py
    research_kernel/
      records.py
      ports.py
      services.py
    backtest_kernel/
      records.py
      ports.py
      services.py
  report_kernel/
    records.py
    ports.py
    services.py
```

## 3. common

### 3.1 基础类型

建议用轻量类型别名和枚举统一语义。

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import NewType
from uuid import UUID


SymbolCode = NewType("SymbolCode", str)
UniverseId = NewType("UniverseId", UUID)
TaskId = NewType("TaskId", UUID)
RunId = NewType("RunId", UUID)


class Market(str, Enum):
    CN_A = "CN_A"


class Exchange(str, Enum):
    SSE = "SSE"
    SZSE = "SZSE"
    BSE = "BSE"


class AssetType(str, Enum):
    STOCK = "stock"
    INDEX = "index"
    ETF = "etf"


class AdjustType(str, Enum):
    NONE = "none"
    QFQ = "qfq"
    HFQ = "hfq"
```

### 3.2 通用值对象

```python
@dataclass(frozen=True, slots=True)
class SymbolRef:
    symbol: SymbolCode
    name: str
    market: Market
    exchange: Exchange
    asset_type: AssetType

    @property
    def display_name(self) -> str:
        return f"{self.symbol} {self.name}"


@dataclass(frozen=True, slots=True)
class DateRange:
    start_date: date
    end_date: date

    def validate(self) -> None:
        if self.start_date > self.end_date:
            raise ValueError("start_date must be <= end_date")
```

### 3.3 错误类型

```python
class AugurMaestroError(Exception):
    """Base error for Augur_Maestro."""


class DomainValidationError(AugurMaestroError):
    """Raised when a domain rule is violated."""


class ExternalProviderError(AugurMaestroError):
    """Raised when an external provider fails."""


class DataQualityError(AugurMaestroError):
    """Raised when data quality blocks downstream usage."""
```

使用规则：

- 参数或业务规则错误抛 `DomainValidationError`。
- AKShare、Qlib、VectorBT 等外部依赖失败抛 `ExternalProviderError`。
- 数据质量检查阻断研究或回测时抛 `DataQualityError`。

## 4. data_kernel

### 4.1 DTO

```python
@dataclass(frozen=True, slots=True)
class SymbolRecord:
    symbol: SymbolCode
    raw_symbol: str
    market: Market
    exchange: Exchange
    name: str
    asset_type: AssetType
    list_date: date | None
    delist_date: date | None
    is_active: bool
    source: str
    ingested_at: datetime


@dataclass(frozen=True, slots=True)
class TradeCalendarRecord:
    market: Market
    trade_date: date
    is_open: bool
    source: str
    ingested_at: datetime


@dataclass(frozen=True, slots=True)
class DailyBarRecord:
    symbol: SymbolCode
    trade_date: date
    adjust: AdjustType
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    amount: Decimal
    turnover_rate: Decimal | None
    source: str
    provider_version: str
    raw_payload_hash: str
    ingested_at: datetime
```

导入和质量检查对象：

```python
@dataclass(frozen=True, slots=True)
class DailyBarImportRequest:
    universe_id: UUID
    date_range: DateRange
    adjusts: tuple[AdjustType, ...]
    provider: str


@dataclass(frozen=True, slots=True)
class IngestionRunResult:
    run_id: UUID
    provider: str
    dataset: str
    status: str
    row_count: int
    failed_count: int
    error_message: str | None


@dataclass(frozen=True, slots=True)
class DataQualityIssueRecord:
    severity: str
    issue_type: str
    message: str
    symbol: SymbolCode | None = None
    trade_date: date | None = None
    field_name: str | None = None


@dataclass(frozen=True, slots=True)
class DataQualitySummary:
    quality_run_id: UUID
    status: str
    issue_count: int
    issues: tuple[DataQualityIssueRecord, ...]
```

### 4.2 Ports

外部数据源接口：

```python
from typing import Protocol


class DataProvider(Protocol):
    provider_name: str

    def get_symbols(self, market: Market) -> list[SymbolRecord]:
        ...

    def get_trade_calendar(
        self,
        market: Market,
        date_range: DateRange,
    ) -> list[TradeCalendarRecord]:
        ...

    def get_daily_bars(
        self,
        symbol: SymbolCode,
        date_range: DateRange,
        adjust: AdjustType,
    ) -> list[DailyBarRecord]:
        ...
```

Repository 接口：

```python
class MarketDataRepository(Protocol):
    def upsert_symbols(self, records: list[SymbolRecord]) -> int:
        ...

    def upsert_trade_calendar(self, records: list[TradeCalendarRecord]) -> int:
        ...

    def upsert_daily_bars(
        self,
        records: list[DailyBarRecord],
        ingestion_run_id: UUID,
    ) -> int:
        ...

    def get_daily_bars(
        self,
        symbols: list[SymbolCode],
        date_range: DateRange,
        adjust: AdjustType,
    ) -> list[DailyBarRecord]:
        ...
```

导入和质量检查服务：

```python
class DataIngestionService(Protocol):
    def import_daily_bars(self, request: DailyBarImportRequest) -> IngestionRunResult:
        ...


class DataQualityService(Protocol):
    def validate_daily_bars(
        self,
        universe_id: UUID,
        date_range: DateRange,
        adjust: AdjustType,
    ) -> DataQualitySummary:
        ...
```

边界规则：

- `DataProvider` 只拉外部数据，不直接写数据库。
- `MarketDataRepository` 只负责读写标准表，不调用 AKShare。
- `DataIngestionService` 编排 Provider、Repository、质量检查和导入批次。

## 5. universe_kernel

### 5.1 DTO

```python
@dataclass(frozen=True, slots=True)
class ThemeSpec:
    code: str
    name: str
    description: str | None = None


@dataclass(frozen=True, slots=True)
class CandidateGenerationRequest:
    themes: tuple[ThemeSpec, ...]
    market: Market
    max_candidates_per_theme: int
    method: str


@dataclass(frozen=True, slots=True)
class UniverseCandidate:
    symbol: SymbolCode
    name: str
    theme: str
    source: str
    reason: str
    confidence: Decimal | None

    def validate_reason(self) -> None:
        if not self.reason.strip():
            raise DomainValidationError("candidate reason is required")


@dataclass(frozen=True, slots=True)
class CandidateDecision:
    candidate_id: UUID
    approved: bool
    decision_reason: str
    decided_by: str


@dataclass(frozen=True, slots=True)
class UniverseMember:
    universe_id: UUID
    symbol: SymbolCode
    name: str
    theme: str
    source: str
    reason: str
    confidence: Decimal | None
    is_active: bool
```

### 5.2 Ports

候选源接口：

```python
class UniverseCandidateSource(Protocol):
    source_name: str

    def build_candidates(
        self,
        request: CandidateGenerationRequest,
    ) -> list[UniverseCandidate]:
        ...
```

Repository 和服务：

```python
class UniverseRepository(Protocol):
    def create_candidate_run(self, request: CandidateGenerationRequest) -> UUID:
        ...

    def save_candidates(
        self,
        candidate_run_id: UUID,
        candidates: list[UniverseCandidate],
    ) -> int:
        ...

    def decide_candidate(self, decision: CandidateDecision) -> None:
        ...

    def add_approved_candidates_to_universe(
        self,
        universe_id: UUID,
        candidate_run_id: UUID,
    ) -> int:
        ...

    def list_active_members(self, universe_id: UUID) -> list[UniverseMember]:
        ...


class UniverseService(Protocol):
    def build_candidates(self, request: CandidateGenerationRequest) -> UUID:
        ...

    def approve_candidates(
        self,
        universe_id: UUID,
        decisions: list[CandidateDecision],
    ) -> int:
        ...
```

边界规则：

- AI、AKShare 概念板块、人工种子都实现 `UniverseCandidateSource`。
- 候选理由不能只写关键词命中。
- 只有用户确认 `approved` 后才能进入正式研究股票池。
- `research_kernel` 只能读取正式股票池成员，不能直接使用 pending 候选。

## 6. research_kernel

### 6.1 DTO

```python
@dataclass(frozen=True, slots=True)
class ResearchTaskConfig:
    name: str
    goal: str
    universe_id: UUID
    data_range: DateRange
    simulation_holdout_years: int
    train_ratio: Decimal
    backtest_ratio: Decimal
    adjust: AdjustType
    config_path: str
    config_hash: str


@dataclass(frozen=True, slots=True)
class DatasetSplit:
    task_id: UUID
    split_name: str
    date_range: DateRange
    method: str
    ratio: Decimal | None


@dataclass(frozen=True, slots=True)
class ResearchTask:
    task_id: UUID
    name: str
    universe_id: UUID
    goal: str
    status: str
    data_range: DateRange
    simulation_range: DateRange
```

### 6.2 Ports

```python
class DatasetSplitPolicy(Protocol):
    def build_splits(self, config: ResearchTaskConfig) -> list[DatasetSplit]:
        ...


class ResearchTaskRepository(Protocol):
    def create_task(self, config: ResearchTaskConfig) -> UUID:
        ...

    def save_splits(self, task_id: UUID, splits: list[DatasetSplit]) -> None:
        ...

    def update_status(self, task_id: UUID, status: str, message: str) -> None:
        ...

    def get_task(self, task_id: UUID) -> ResearchTask:
        ...


class ResearchTaskService(Protocol):
    def create_task(self, config: ResearchTaskConfig) -> UUID:
        ...

    def prepare_data(self, task_id: UUID) -> None:
        ...
```

边界规则：

- `ResearchTaskService` 不直接调用 AKShare。
- 数据切分策略必须按时间顺序生成，不能随机打乱。
- 研究任务只引用 `universe_id`，不复制股票池全量成员到任务配置。

## 7. backtest_kernel

### 7.1 DTO

```python
@dataclass(frozen=True, slots=True)
class BacktestConfig:
    task_id: UUID
    engine: str
    strategy_name: str
    adjust: AdjustType
    initial_cash: Decimal
    fee_rate: Decimal
    slippage_bps: Decimal
    config_hash: str


@dataclass(frozen=True, slots=True)
class BacktestInputBundle:
    task: ResearchTask
    universe: tuple[UniverseMember, ...]
    bars: tuple[DailyBarRecord, ...]
    splits: tuple[DatasetSplit, ...]
    config: BacktestConfig


@dataclass(frozen=True, slots=True)
class BacktestMetric:
    name: str
    value: Decimal
    unit: str | None = None


@dataclass(frozen=True, slots=True)
class EquityCurvePoint:
    trade_date: date
    equity: Decimal
    cash: Decimal | None
    position_value: Decimal | None
    daily_return: Decimal | None
    drawdown: Decimal | None


@dataclass(frozen=True, slots=True)
class BacktestOrderRecord:
    trade_date: date
    symbol: SymbolCode
    name: str
    side: str
    order_type: str
    quantity: Decimal
    price: Decimal
    status: str
    reason: str


@dataclass(frozen=True, slots=True)
class BacktestTradeRecord:
    trade_date: date
    symbol: SymbolCode
    side: str
    quantity: Decimal
    price: Decimal
    fee: Decimal
    slippage: Decimal


@dataclass(frozen=True, slots=True)
class BacktestResult:
    backtest_id: UUID | None
    status: str
    metrics: tuple[BacktestMetric, ...]
    equity_curve: tuple[EquityCurvePoint, ...]
    orders: tuple[BacktestOrderRecord, ...]
    trades: tuple[BacktestTradeRecord, ...]
    error_message: str | None = None


@dataclass(frozen=True, slots=True)
class AttributionItem:
    attribution_type: str
    dimension_type: str
    dimension_key: str
    dimension_name: str
    pnl: Decimal | None
    return_contribution: Decimal | None
    trade_count: int | None
    win_rate: Decimal | None
    max_drawdown_contribution: Decimal | None
    evidence: str


@dataclass(frozen=True, slots=True)
class DrawdownSegment:
    peak_date: date
    trough_date: date
    recovery_date: date | None
    drawdown: Decimal
    duration_days: int
    explanation: str


@dataclass(frozen=True, slots=True)
class AttributionReport:
    backtest_id: UUID
    items: tuple[AttributionItem, ...]
    drawdown_segments: tuple[DrawdownSegment, ...]
    summary: str
```

### 7.2 Ports

```python
class BacktestEngineAdapter(Protocol):
    engine_name: str

    def run(self, bundle: BacktestInputBundle) -> BacktestResult:
        ...


class AttributionAnalyzer(Protocol):
    analyzer_name: str

    def analyze(
        self,
        result: BacktestResult,
        bundle: BacktestInputBundle,
    ) -> AttributionReport:
        ...


class BacktestRepository(Protocol):
    def create_run(self, config: BacktestConfig) -> UUID:
        ...

    def save_result(self, backtest_id: UUID, result: BacktestResult) -> None:
        ...

    def save_attribution(
        self,
        backtest_id: UUID,
        attribution: AttributionReport,
    ) -> None:
        ...

    def get_result(self, backtest_id: UUID) -> BacktestResult:
        ...

    def get_attribution(self, backtest_id: UUID) -> AttributionReport:
        ...


class BacktestService(Protocol):
    def run_backtest(self, config: BacktestConfig) -> UUID:
        ...

    def run_attribution(self, backtest_id: UUID) -> AttributionReport:
        ...
```

边界规则：

- Qlib 和 VectorBT 只能出现在 `BacktestEngineAdapter` 的具体实现里。
- `BacktestService` 负责组装标准化数据、正式股票池成员和数据切分。
- `AttributionAnalyzer` 基于回测结果、持仓、交易、权益曲线、因子和事件窗口做解释，不能编造无法从数据追溯的原因。
- 回测订单和成交是虚拟记录，不能复用真实 OMS 表。

## 8. report_kernel

### 8.1 DTO

```python
@dataclass(frozen=True, slots=True)
class ReportRequest:
    task_id: UUID
    backtest_id: UUID
    report_type: str
    output_dir: str


@dataclass(frozen=True, slots=True)
class ReportArtifact:
    artifact_id: UUID | None
    task_id: UUID
    backtest_id: UUID
    artifact_type: str
    path: str
    content_hash: str
    status: str
```

### 8.2 Ports

```python
class ReportRenderer(Protocol):
    def render_markdown(
        self,
        request: ReportRequest,
        backtest_result: BacktestResult,
        attribution_report: AttributionReport | None,
    ) -> ReportArtifact:
        ...


class ReportRepository(Protocol):
    def save_artifact(self, artifact: ReportArtifact) -> UUID:
        ...


class ReportService(Protocol):
    def generate_backtest_report(self, request: ReportRequest) -> UUID:
        ...
```

边界规则：

- 报告文件写入 `outputs/reports/`。
- 数据库只保存路径、哈希和关联任务。
- 报告必须标注数据源、导入批次、复权方式、数据切分方式、归因分析和风险提示。

## 9. CLI 和 API 调用规则

CLI 命令调用服务层：

```text
CLI -> Service -> Repository/Provider/Adapter
```

FastAPI 调用服务层：

```text
API Router -> Service -> Repository
```

禁止：

- CLI 直接使用 SQLAlchemy session 拼 SQL 修改核心表。
- FastAPI Router 直接调用 AKShare、Qlib、VectorBT。
- 回测引擎直接读取数据库。
- 任何非 `data_kernel` 代码直接调用 `DataProvider`。

## 10. M1 最小接口实现顺序

建议实现顺序：

1. `common.types` 和 `common.errors`。
2. `data_kernel.records`、`data_kernel.ports`。
3. `universe_kernel.records`、`universe_kernel.ports`。
4. `research_kernel.records`、`research_kernel.ports`。
5. `backtest_kernel.records`、`backtest_kernel.ports`。
6. `report_kernel.records`、`report_kernel.ports`。
7. SQLAlchemy Repository 实现。
8. AKShare Provider 实现。
9. CLI 命令调用服务。

这样可以先把 kernel 边界钉住，再逐步填实现，避免一开始把数据库、AKShare、CLI 和回测库写成一团。

## 11. 后续交易链路占位接口草案

本节只作为后续交易链路的占位草案，M1 不实现真实交易、真实账户、真实订单和真实券商调用。正式进入实盘前，必须再单独补完整的风控、OMS、券商适配器、账户、持仓、资金、对账和条件单设计。

### 11.1 交易意图与风控

策略和研究模块以后也不能直接下单，只能生成交易意图。

```python
@dataclass(frozen=True, slots=True)
class TradeIntent:
    intent_id: UUID | None
    strategy_id: str
    symbol: SymbolCode
    name: str
    side: str
    target_position_pct: Decimal | None
    quantity: Decimal | None
    limit_price: Decimal | None
    reason: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class RiskCheckResult:
    intent_id: UUID
    approved: bool
    rejection_code: str | None
    rejection_reason: str | None
    checked_at: datetime


class RiskEngine(Protocol):
    def check_intent(self, intent: TradeIntent) -> RiskCheckResult:
        ...
```

规则：

- `TradeIntent` 不是订单，不能直接发送给券商。
- 风控拒绝原因必须可审计。
- 非交易时间触发的意图只能进入待审计状态，不能变成券商挂单。

### 11.2 交易时间检查

交易时间检查是后续真实下单前的硬依赖。

```python
class TradingClock(Protocol):
    def is_trading_time(self, market: Market, at: datetime) -> bool:
        ...

    def next_trading_window_start(self, market: Market, after: datetime) -> datetime:
        ...
```

规则：

- 任何真实下单或向券商提交挂单请求前，都必须先通过 `TradingClock` 检查。
- 非交易时间不能调用真实 `TradingGateway.place_order`。
- 到下一个有效交易窗口后，必须重新读取行情、重新做风控、重新检查 OMS 状态。

### 11.3 OMS 与券商适配器

```python
class BrokerCapabilityMode(str, Enum):
    READ_ONLY = "read_only"
    SIMULATED = "simulated"
    LIVE_GUARDED = "live_guarded"


@dataclass(frozen=True, slots=True)
class OrderRequest:
    order_id: UUID | None
    intent_id: UUID
    symbol: SymbolCode
    side: str
    order_type: str
    quantity: Decimal
    limit_price: Decimal | None
    created_at: datetime


@dataclass(frozen=True, slots=True)
class OrderAck:
    order_id: UUID
    broker_order_id: str | None
    status: str
    raw_message: str | None
    received_at: datetime


@dataclass(frozen=True, slots=True)
class AccountSnapshot:
    broker_name: str
    account_ref: str
    currency: str
    captured_at: datetime


@dataclass(frozen=True, slots=True)
class PositionSnapshot:
    symbol: SymbolCode
    name: str
    quantity: Decimal
    available_quantity: Decimal
    captured_at: datetime


@dataclass(frozen=True, slots=True)
class TradeSnapshot:
    broker_trade_id: str
    broker_order_id: str
    symbol: SymbolCode
    side: str
    quantity: Decimal
    price: Decimal
    traded_at: datetime


class BrokerTradingAdapter(Protocol):
    broker_name: str
    capability_mode: BrokerCapabilityMode

    def get_account(self) -> AccountSnapshot:
        ...

    def get_positions(self) -> list[PositionSnapshot]:
        ...

    def query_order(self, broker_order_id: str) -> OrderAck:
        ...

    def query_trades(self, since: datetime | None = None) -> list[TradeSnapshot]:
        ...

    def place_order(self, order: OrderRequest) -> OrderAck:
        ...

    def cancel_order(self, broker_order_id: str) -> OrderAck:
        ...


class OrderManagementService(Protocol):
    def create_order(self, intent: TradeIntent, risk_result: RiskCheckResult) -> UUID:
        ...

    def submit_order(self, order_id: UUID) -> OrderAck:
        ...

    def mark_unknown(self, order_id: UUID, reason: str) -> None:
        ...
```

规则：

- `BrokerTradingAdapter` 是券商 SDK/API 适配器边界，策略、回测、FastAPI Router 和 CLI 都不能直接调用；上层只能通过 `TradingGateway` 进入交易链路。
- miniQMT 和盈立的只读接入必须区分 API 边界：交易开放 API 只允许登录、权限检查、账户、资金、持仓、订单和成交查询；基础报价 API / 报价推送 API 只允许行情查询和订阅。两类只读测试不构成真实交易，但仍要保护账户隐私，且不得混用网关、client、signer 或 mapper。
- 任何会向券商提交委托、撤单、条件单、预埋单、止盈止损、触发单或其他可能改变券商侧订单状态的接口，都按真实交易接口处理。
- `capability_mode` 默认为 `READ_ONLY`；只有显式切到 `LIVE_GUARDED` 且 `trading_enabled=true`、人工确认、交易时间、风控、OMS 和账户/标的白名单全部通过，才允许调用 `place_order` 或 `cancel_order`。
- 不允许用真实下单、真实撤单或真实条件单接口做连通性探测、冒烟测试或权限测试。
- 非交易时间不能向 miniQMT 或盈立 OpenAPI 提交真实下单、挂单、预埋单或券商侧条件单。
- OMS 下单失败、超时、网络异常、券商返回未知状态时，绝对不能自动重试。
- 未知状态必须进入 `unknown` 或人工可审计状态，再通过订单查询、成交查询和对账确认。

### 11.4 条件单预留

条件单、止盈止损、触发单和分批下单后续需要单独设计。无论由券商原生支持还是本地 OMS 托管，触发后都不能绕过风控和 OMS；非交易时间也不能向券商提交挂单。

## 12. 后续扩展预留

M1 暂不实现，但接口设计需要避免堵死：

- `BrokerTradingAdapter` 后续用于真实券商接口，并由 `TradingGateway` 统一执行能力模式和交易安全阻断。
- `StrategyRuntime` 后续用于模拟盘和实盘策略运行。
- `RiskEngine` 后续用于真实交易前风控。
- `OrderManagementService` 后续用于真实订单生命周期。
- `EventSignalProvider` 后续用于消息面和宏观事件信号。

这些接口涉及真实交易链路，必须在后续设计文档确认后再进入代码实现。
