"""包冒烟测试：确保 rq_core 子包可正常导入。

M1 阶段 broker/oms/risk 等 kernel 尚未实现真实逻辑，本测试只保证当前已落地的
quotation_kernel 接口能 import，作为 CI pytest 步骤的最小桩；待 M1 各 kernel
实现到位后，由真实单元/契约测试取代，并把 pyproject.toml 的
``--cov-fail-under`` 从 0 调回 60。
"""

from __future__ import annotations

from rq_core.quotation_kernel import QuotationDataGateway


def test_quotation_kernel_importable() -> None:
    """验证 quotation_kernel 包及其统一门面类可正常 import。"""
    assert QuotationDataGateway is not None
