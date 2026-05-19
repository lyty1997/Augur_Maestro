from __future__ import annotations

from typing import Any

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
    OrderStatus,
)
from rq_core.broker_kernel.errors import BrokerContractError
from rq_core.broker_kernel.usmart import endpoints
from rq_core.broker_kernel.usmart.client import uSmartOpenApiClient


class uSmartOpenApiTradingAdapter(BrokerTradingAdapter):
    broker = BrokerName.USMART

    def __init__(self, client: uSmartOpenApiClient | None = None) -> None:
        self._client = client or uSmartOpenApiClient(dry_run=True)

    def health_check(self) -> BrokerHealth:
        return BrokerHealth(
            broker=self.broker,
            ok=True,
            mode=BrokerMode.READ_ONLY,
            message="uSmart OpenAPI trading adapter loaded; real transport disabled by default",
        )

    def connect(self, account_ref: AccountRef | None = None) -> BrokerSession:
        self._client.post(
            endpoints.LOGIN,
            body={"login": "redacted"},
            trace_id="connect",
        )
        return BrokerSession(
            broker=self.broker,
            connected=True,
            account_ref=account_ref,
            session_id_masked="dry-run",
            metadata={"endpoint": endpoints.LOGIN, "dry_run": True},
        )

    def place_order(self, request: BrokerOrderRequest) -> BrokerOrderAck:
        response = self._client.post(
            endpoints.ENTRUST_ORDER,
            body=self._build_place_order_body(request),
            trace_id=request.trace_id,
        )
        return BrokerOrderAck(
            order_id=request.order_id,
            request_id=request.request_id,
            status=OrderStatus.UNKNOWN,
            broker=self.broker,
            broker_status_raw="unknown_by_pdf",
            broker_message=(
                "uSmart place order endpoint prepared; response mapping requires PDF confirmation"
            ),
            unknown_reason=f"dry_run={response.data.get('dry_run', False)}",
        )

    def modify_order(self, request: BrokerModifyRequest) -> BrokerModifyAck:
        response = self._client.post(
            endpoints.MODIFY_ORDER,
            body=self._build_modify_order_body(request),
            trace_id=request.trace_id,
        )
        return BrokerModifyAck(
            order_id=request.order_id,
            request_id=request.request_id,
            status=OrderStatus.UNKNOWN,
            broker=self.broker,
            broker_order_id=request.broker_order_id,
            broker_message=(
                "uSmart modify endpoint prepared; modify semantics require PDF confirmation"
            ),
            unknown_reason=f"dry_run={response.data.get('dry_run', False)}",
        )

    def cancel_order(self, request: BrokerCancelRequest) -> BrokerCancelAck:
        response = self._client.post(
            endpoints.MODIFY_ORDER,
            body=self._build_cancel_order_body(request),
            trace_id=request.trace_id,
        )
        return BrokerCancelAck(
            order_id=request.order_id,
            request_id=request.request_id,
            status=OrderStatus.UNKNOWN,
            broker=self.broker,
            broker_order_id=request.broker_order_id,
            broker_message=(
                "uSmart cancel uses modify endpoint; cancel parameters require PDF confirmation"
            ),
            unknown_reason=f"dry_run={response.data.get('dry_run', False)}",
        )

    @staticmethod
    def _build_place_order_body(request: BrokerOrderRequest) -> dict[str, Any]:
        return {
            "accountRef": request.account_ref.value,
            "market": request.market,
            "symbol": request.symbol,
            "side": request.side.value,
            "orderType": request.order_type.value,
            "priceType": request.price_type.value,
            "quantity": str(request.quantity),
            "limitPrice": str(request.limit_price) if request.limit_price is not None else None,
            "currency": request.currency,
            "clientOrderId": request.order_id,
            "requestId": request.request_id,
        }

    @staticmethod
    def _build_modify_order_body(request: BrokerModifyRequest) -> dict[str, Any]:
        if request.new_quantity is None and request.new_limit_price is None:
            raise BrokerContractError(
                "broker.usmart.modify_payload_empty",
                "改单请求必须至少包含新数量或新价格",
            )
        return {
            "accountRef": request.account_ref.value,
            "brokerOrderId": request.broker_order_id,
            "newQuantity": str(request.new_quantity) if request.new_quantity is not None else None,
            "newLimitPrice": (
                str(request.new_limit_price) if request.new_limit_price is not None else None
            ),
            "clientOrderId": request.order_id,
            "requestId": request.request_id,
            "semantic": "modify_unknown_by_pdf",
        }

    @staticmethod
    def _build_cancel_order_body(request: BrokerCancelRequest) -> dict[str, Any]:
        return {
            "accountRef": request.account_ref.value,
            "brokerOrderId": request.broker_order_id,
            "clientOrderId": request.order_id,
            "requestId": request.request_id,
            "semantic": "cancel_unknown_by_pdf",
        }
