from __future__ import annotations

from rq_core.quotation_kernel.adapter_base import QuotationDataAdapter, QuoteRequest, QuoteSnapshot


class QuotationDataGateway:
    """统一行情数据网关。

    行情查询与交易动作分离，避免未来行情重连、订阅恢复等逻辑影响交易链路。
    """

    def __init__(self, adapter: QuotationDataAdapter) -> None:
        self._adapter = adapter

    def get_realtime_quote(self, request: QuoteRequest) -> QuoteSnapshot:
        return self._adapter.get_realtime_quote(request)
