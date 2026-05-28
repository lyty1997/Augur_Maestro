"""uSmart 交易错误码提取脚本的高风险映射约束测试。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def _load_extractor() -> ModuleType:
    module_path = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "scripts"
        / "docs"
        / "extract_usmart_trade_error_codes.py"
    )
    spec = importlib.util.spec_from_file_location("extract_usmart_trade_error_codes", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_usmart_gateway_error_classification_invariants_hold() -> None:
    extractor = _load_extractor()

    extractor.validate_classification_invariants()


def test_write_action_401_is_not_retryable_auth_expired() -> None:
    extractor = _load_extractor()

    assert (
        extractor.gateway_error_for(
            "401",
            "Unauthorized",
            "/stock-order-server/open-api/entrust-order",
        )
        == "broker.order_state_unknown"
    )
    assert (
        extractor.gateway_error_for(
            "401",
            "Unauthorized",
            "/stock-order-server/open-api/today-entrust",
        )
        == "broker.auth_expired"
    )


def test_verification_attempt_lock_beats_generic_rate_limit_keywords() -> None:
    extractor = _load_extractor()

    assert (
        extractor.gateway_error_for("300304", "验证次数过多，请稍后重试", None)
        == "broker.account_restricted"
    )
    assert (
        extractor.gateway_error_for("300304", "验证次数已达上限，请稍后重试", None)
        == "broker.account_restricted"
    )
    assert (
        extractor.gateway_error_for("429", "请求频率过高，请稍后重试", None)
        == "broker.rate_limited"
    )
