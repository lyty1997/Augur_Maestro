from __future__ import annotations

from rq_core.broker_kernel.capability import CapabilityGuard
from rq_core.broker_kernel.contracts import (
    AccountRef,
    BrokerAction,
    BrokerTradingAdapter,
    BrokerCancelAck,
    BrokerCancelRequest,
    BrokerGatewayConfig,
    BrokerHealth,
    BrokerModifyAck,
    BrokerModifyRequest,
    BrokerOrderAck,
    BrokerOrderRequest,
    BrokerSession,
)


class TradingGateway:
    """统一券商交易网关。

    上层 OMS 只依赖这个门面；盈立 OpenAPI、miniQMT 等差异由适配器处理。
    真实交易动作先经过能力锁，默认 read_only 模式下不会触达适配器。
    """

    def __init__(self, config: BrokerGatewayConfig, adapter: BrokerTradingAdapter) -> None:
        if config.broker != adapter.broker:
            raise ValueError("gateway config broker must match adapter broker")
        self._config = config
        self._adapter = adapter
        self._guard = CapabilityGuard(config)

    def health_check(self) -> BrokerHealth:
        return self._adapter.health_check()

    def connect(self, account_ref: AccountRef | None = None) -> BrokerSession:
        self._guard.ensure_allowed(BrokerAction.CONNECT)
        return self._adapter.connect(account_ref)

    def place_order(self, request: BrokerOrderRequest) -> BrokerOrderAck:
        self._guard.ensure_allowed(BrokerAction.PLACE_ORDER)
        return self._adapter.place_order(request)

    def modify_order(self, request: BrokerModifyRequest) -> BrokerModifyAck:
        self._guard.ensure_allowed(BrokerAction.MODIFY_ORDER)
        return self._adapter.modify_order(request)

    def cancel_order(self, request: BrokerCancelRequest) -> BrokerCancelAck:
        self._guard.ensure_allowed(BrokerAction.CANCEL_ORDER)
        return self._adapter.cancel_order(request)
