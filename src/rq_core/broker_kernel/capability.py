from __future__ import annotations

from rq_core.broker_kernel.contracts import BrokerAction, BrokerGatewayConfig, BrokerMode
from rq_core.broker_kernel.errors import TradingBlockedError


class CapabilityGuard:
    def __init__(self, config: BrokerGatewayConfig) -> None:
        self._config = config

    def ensure_allowed(self, action: BrokerAction) -> None:
        if self._config.mode == BrokerMode.DISABLED:
            raise TradingBlockedError("broker.disabled", "券商交易网关已关闭")

        if action == BrokerAction.CONNECT:
            return

        if self._config.mode != BrokerMode.LIVE_GUARDED:
            raise TradingBlockedError(
                "broker.trading_disabled",
                "当前不是 live_guarded 模式，禁止调用真实交易接口",
            )

        if not self._config.trading_enabled:
            raise TradingBlockedError(
                "broker.trading_disabled",
                "trading_enabled=false，禁止调用真实交易接口",
            )

        capability = self._capability_name(action)
        if capability and not getattr(self._config.capabilities, capability):
            raise TradingBlockedError(
                "broker.capability_disabled",
                f"{capability}=false，禁止调用该交易能力",
            )

    @staticmethod
    def _capability_name(action: BrokerAction) -> str | None:
        if action == BrokerAction.PLACE_ORDER:
            return "place_order"
        if action == BrokerAction.MODIFY_ORDER:
            return "modify_order"
        if action == BrokerAction.CANCEL_ORDER:
            return "cancel_order"
        return None
