from __future__ import annotations

from rq_core.broker_kernel.contracts import (
    AccountRef,
    BrokerCancelAck,
    BrokerCancelRequest,
    BrokerHealth,
    BrokerMode,
    BrokerModifyAck,
    BrokerModifyRequest,
    BrokerName,
    BrokerOrderAck,
    BrokerOrderRequest,
    BrokerSession,
    BrokerTradingAdapter,
)
from rq_core.broker_kernel.errors import BrokerContractError


class MiniQMTTradingAdapter(BrokerTradingAdapter):
    broker = BrokerName.MINIQMT

    def health_check(self) -> BrokerHealth:
        return BrokerHealth(
            broker=self.broker,
            ok=False,
            mode=BrokerMode.READ_ONLY,
            message="miniQMT adapter reserved; client binding is not configured",
        )

    def connect(self, account_ref: AccountRef | None = None) -> BrokerSession:
        raise BrokerContractError(
            "broker.miniqmt.not_configured",
            "miniQMT 客户端或桥接进程尚未配置",
        )

    def place_order(self, request: BrokerOrderRequest) -> BrokerOrderAck:
        raise BrokerContractError(
            "broker.miniqmt.not_configured",
            "miniQMT 下单适配器尚未配置",
        )

    def modify_order(self, request: BrokerModifyRequest) -> BrokerModifyAck:
        raise BrokerContractError(
            "broker.miniqmt.not_configured",
            "miniQMT 改单适配器尚未配置",
        )

    def cancel_order(self, request: BrokerCancelRequest) -> BrokerCancelAck:
        raise BrokerContractError(
            "broker.miniqmt.not_configured",
            "miniQMT 撤单适配器尚未配置",
        )
