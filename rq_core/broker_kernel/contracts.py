from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum
from abc import ABC, abstractmethod
from typing import Any


class BrokerMode(StrEnum):
    DISABLED = "disabled"
    READ_ONLY = "read_only"
    SIMULATED = "simulated"
    LIVE_GUARDED = "live_guarded"


class BrokerName(StrEnum):
    YINGLI = "yingli"
    MINIQMT = "miniqmt"
    PTRADE = "ptrade"


class OrderSide(StrEnum):
    BUY = "buy"
    SELL = "sell"


class OrderType(StrEnum):
    LIMIT = "limit"
    MARKET = "market"


class PriceType(StrEnum):
    LIMIT = "limit"
    MARKET = "market"


class OrderStatus(StrEnum):
    BLOCKED = "blocked"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    PARTIAL_FILLED = "partial_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    BROKER_REJECTED = "broker_rejected"
    FAILED = "failed"
    UNKNOWN = "unknown"


class BrokerAction(StrEnum):
    CONNECT = "connect"
    PLACE_ORDER = "place_order"
    MODIFY_ORDER = "modify_order"
    CANCEL_ORDER = "cancel_order"


@dataclass(frozen=True)
class CapabilityConfig:
    quote_http: bool = True
    quote_ws: bool = True
    account_query: bool = True
    position_query: bool = True
    order_query: bool = True
    trade_query: bool = True
    place_order: bool = False
    modify_order: bool = False
    cancel_order: bool = False
    odd_lot_order: bool = False
    ipo: bool = False


@dataclass(frozen=True)
class BrokerGatewayConfig:
    broker: BrokerName
    mode: BrokerMode = BrokerMode.READ_ONLY
    trading_enabled: bool = False
    capabilities: CapabilityConfig = field(default_factory=CapabilityConfig)
    require_oms_caller: bool = True


@dataclass(frozen=True)
class AccountRef:
    value: str


@dataclass(frozen=True)
class BrokerHealth:
    broker: BrokerName
    ok: bool
    mode: BrokerMode
    message: str = ""


@dataclass(frozen=True)
class BrokerSession:
    broker: BrokerName
    connected: bool
    account_ref: AccountRef | None = None
    session_id_masked: str | None = None
    expires_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BrokerOrderRequest:
    order_id: str
    intent_id: str
    account_ref: AccountRef
    broker: BrokerName
    market: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    price_type: PriceType
    quantity: Decimal
    limit_price: Decimal | None
    currency: str
    request_id: str
    risk_check_id: str
    trace_id: str
    manual_confirm_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class BrokerModifyRequest:
    order_id: str
    account_ref: AccountRef
    broker: BrokerName
    broker_order_id: str
    request_id: str
    trace_id: str
    risk_check_id: str
    new_quantity: Decimal | None = None
    new_limit_price: Decimal | None = None
    manual_confirm_id: str | None = None


@dataclass(frozen=True)
class BrokerCancelRequest:
    order_id: str
    account_ref: AccountRef
    broker: BrokerName
    broker_order_id: str
    request_id: str
    trace_id: str
    risk_check_id: str
    manual_confirm_id: str | None = None


@dataclass(frozen=True)
class BrokerOrderAck:
    order_id: str
    request_id: str
    status: OrderStatus
    broker: BrokerName
    broker_order_id: str | None = None
    broker_status_raw: str | None = None
    broker_response_code: str | None = None
    broker_message: str | None = None
    unknown_reason: str | None = None


@dataclass(frozen=True)
class BrokerModifyAck:
    order_id: str
    request_id: str
    status: OrderStatus
    broker: BrokerName
    broker_order_id: str | None = None
    broker_response_code: str | None = None
    broker_message: str | None = None
    unknown_reason: str | None = None


@dataclass(frozen=True)
class BrokerCancelAck:
    order_id: str
    request_id: str
    status: OrderStatus
    broker: BrokerName
    broker_order_id: str | None = None
    broker_response_code: str | None = None
    broker_message: str | None = None
    unknown_reason: str | None = None


class BrokerTradingAdapter(ABC):
    """统一券商交易适配器基类。

    具体券商只负责把统一 DTO 转成自己的 API / SDK 调用。
    是否允许真实交易，由 TradingGateway 统一判断。
    """

    broker: BrokerName

    @abstractmethod
    def health_check(self) -> BrokerHealth: ...

    @abstractmethod
    def connect(self, account_ref: AccountRef | None = None) -> BrokerSession: ...

    @abstractmethod
    def place_order(self, request: BrokerOrderRequest) -> BrokerOrderAck: ...

    @abstractmethod
    def modify_order(self, request: BrokerModifyRequest) -> BrokerModifyAck: ...

    @abstractmethod
    def cancel_order(self, request: BrokerCancelRequest) -> BrokerCancelAck: ...
