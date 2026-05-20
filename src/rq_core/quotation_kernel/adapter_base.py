from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class QuoteRequest:
    market: str
    symbol: str


@dataclass(frozen=True)
class QuoteSnapshot:
    market: str
    symbol: str
    last_price: Decimal | None = None
    source: str | None = None


class QuotationDataAdapter(ABC):
    @abstractmethod
    def get_realtime_quote(self, request: QuoteRequest) -> QuoteSnapshot: ...
