from __future__ import annotations

import unittest
from decimal import Decimal

from rq_core.broker_kernel import (
    AccountRef,
    BrokerCancelRequest,
    BrokerGatewayConfig,
    BrokerMode,
    BrokerModifyRequest,
    BrokerName,
    BrokerOrderRequest,
    OrderSide,
    OrderType,
    PriceType,
    TradingGateway,
)
from rq_core.broker_kernel.errors import TradingBlockedError
from rq_core.broker_kernel.usmart import uSmartOpenApiClient, uSmartOpenApiTradingAdapter


class TradingGatewaySafetyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = uSmartOpenApiClient(dry_run=True)
        self.adapter = uSmartOpenApiTradingAdapter(client=self.client)
        self.gateway = TradingGateway(
            BrokerGatewayConfig(broker=BrokerName.USMART, mode=BrokerMode.READ_ONLY),
            self.adapter,
        )
        self.account = AccountRef("acct-demo")

    def test_connect_is_allowed_in_read_only_mode(self) -> None:
        session = self.gateway.connect(self.account)

        self.assertTrue(session.connected)
        self.assertEqual(len(self.client.calls), 1)
        self.assertEqual(self.client.calls[0][0], "/user-server/open-api/login")

    def test_place_order_is_blocked_before_adapter_call(self) -> None:
        with self.assertRaises(TradingBlockedError) as ctx:
            self.gateway.place_order(self._order_request())

        self.assertEqual(ctx.exception.code, "broker.trading_disabled")
        self.assertEqual(len(self.client.calls), 0)

    def test_modify_order_is_blocked_before_adapter_call(self) -> None:
        with self.assertRaises(TradingBlockedError):
            self.gateway.modify_order(self._modify_request())

        self.assertEqual(len(self.client.calls), 0)

    def test_cancel_order_is_blocked_before_adapter_call(self) -> None:
        with self.assertRaises(TradingBlockedError):
            self.gateway.cancel_order(self._cancel_request())

        self.assertEqual(len(self.client.calls), 0)

    def test_adapter_contains_complete_trade_method_shapes(self) -> None:
        body = self.adapter._build_place_order_body(self._order_request())

        self.assertEqual(body["market"], "HK")
        self.assertEqual(body["symbol"], "00700")
        self.assertEqual(body["side"], "buy")
        self.assertEqual(body["requestId"], "req-1")

    def _order_request(self) -> BrokerOrderRequest:
        return BrokerOrderRequest(
            order_id="order-1",
            intent_id="intent-1",
            account_ref=self.account,
            broker=BrokerName.USMART,
            market="HK",
            symbol="00700",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            price_type=PriceType.LIMIT,
            quantity=Decimal("100"),
            limit_price=Decimal("300"),
            currency="HKD",
            request_id="req-1",
            risk_check_id="risk-1",
            trace_id="trace-1",
        )

    def _modify_request(self) -> BrokerModifyRequest:
        return BrokerModifyRequest(
            order_id="order-1",
            account_ref=self.account,
            broker=BrokerName.USMART,
            broker_order_id="broker-order-1",
            request_id="req-2",
            trace_id="trace-1",
            risk_check_id="risk-1",
            new_limit_price=Decimal("299"),
        )

    def _cancel_request(self) -> BrokerCancelRequest:
        return BrokerCancelRequest(
            order_id="order-1",
            account_ref=self.account,
            broker=BrokerName.USMART,
            broker_order_id="broker-order-1",
            request_id="req-3",
            trace_id="trace-1",
            risk_check_id="risk-1",
        )


if __name__ == "__main__":
    unittest.main()
