from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class YingLiOpenApiResponse:
    endpoint: str
    data: dict[str, Any]


class YingLiOpenApiClient:
    """盈立 OpenAPI HTTP 客户端外壳。

    默认 dry-run，不会触达真实券商端。后续只读联调确认后，再接入真实 HTTP
    transport、签名和 token 生命周期。
    """

    def __init__(self, *, dry_run: bool = True) -> None:
        self._dry_run = dry_run
        self.calls: list[tuple[str, dict[str, Any], str]] = []

    def post(self, endpoint: str, body: dict[str, Any], *, trace_id: str) -> YingLiOpenApiResponse:
        self.calls.append((endpoint, body, trace_id))
        if self._dry_run:
            return YingLiOpenApiResponse(
                endpoint=endpoint,
                data={
                    "dry_run": True,
                    "endpoint": endpoint,
                    "trace_id": trace_id,
                    "body_keys": sorted(body.keys()),
                },
            )
        raise NotImplementedError("Real YingLi OpenAPI HTTP transport is not enabled")
