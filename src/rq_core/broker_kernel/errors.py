from __future__ import annotations


class BrokerGatewayError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class TradingBlockedError(BrokerGatewayError):
    pass


class BrokerContractError(BrokerGatewayError):
    pass
