## 变更摘要

- 

## 安全边界

- [ ] 不触碰真实券商接口。
- [ ] 不新增真实下单、撤单、改单、条件单、预埋单或任何会改变券商侧订单状态的调用。
- [ ] 如触及交易、风控、账户、订单、数据模型、券商适配器或部署方式，已先更新 `docs/` 并确认设计。
- [ ] 未写入、打印或提交 API Key、Secret、token、真实账户号、身份证明或真实资金隐私。

## 验证

- [ ] `python -m ruff check .`
- [ ] `python -m ruff format --check .`
- [ ] `python -m mypy rq_core`
- [ ] `detect-secrets-hook --baseline .secrets.baseline $(git ls-files)`
- [ ] `python -m pip_audit -r requirements-dev.lock.txt`
- [ ] `python scripts/quality/trading_safety_static_check.py`
- [ ] `python scripts/quality/markdown_docs_check.py`
- [ ] `python -m pytest`

## 备注

- 
