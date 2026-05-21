# 券商 OpenAPI 规范

## 适用范围

本规范适用于 miniQMT、盈立证券 OpenAPI 以及后续新增券商适配器。券商适配器只负责协议、认证、字段映射、错误映射和只读/交易能力边界，不承载策略逻辑。

## 文档来源

设计盈立 OpenAPI 时，优先参考：

- uSmart 官方网页文档：
  - `https://api-doc.usmart8.com/zh-cn/trade.html`
  - `https://api-doc.usmart8.com/zh-cn/quote-base.html`
  - `https://api-doc.usmart8.com/zh-cn/quote-push.html`
- 本地网页转换稿：`API_manual/uSmart/API_manual/`
- 官方 Python demo：`API_manual/uSmart/openapi-demo-py/`，只作为签名、加密、序列化和连接流程参考，不作为字段枚举真相源；不得提交或复制 demo 中的账号、密码、token、私钥或配置。
- `docs/backend/trading/broker-trading-gateway.md`
- `docs/backend/clients/usmart-openapi-call-design.md`
- `docs/architecture/open-decisions.md`

无法从券商文档确认的行为必须标记为待确认，不得写成确定事实。

## 能力分级

券商适配器必须显式区分能力等级：

- `read_only`：账户、资金、持仓、订单、成交等只读查询。
- `dry_run`：构造请求、签名、校验字段，但不发送会改变券商侧状态的请求。
- `paper`：本地模拟撮合或模拟券商。
- `live_guarded`：真实交易能力，必须经过实盘开关、风控、OMS、人工确认和审计。

默认能力必须是 `read_only` 或 `dry_run`，不得默认进入 `live_guarded`。

## 接口设计

封装层应至少覆盖：

- 登录、token 生命周期、登出或会话释放。
- 账户状态、资金、持仓。
- 订单查询、成交查询、可交易数量、改单范围。
- 下单、撤单、改单的请求建模，但真实发送默认关闭。
- 行情只读查询或订阅的认证、签名、订阅生命周期。

接口返回必须保留：

- 本地请求 ID。
- 券商流水号或 `serialNo`。
- 券商原始状态码和错误信息。
- 标准化状态。
- 脱敏后的原始响应快照，便于排查和对账。

## 字段与签名

字段映射必须有文档来源。对盈立 OpenAPI：

- 下单、改单、撤单字段应与官方网页文档中的 `serialNo`、`entrustAmount`、`entrustPrice`、`entrustProp`、`entrustType`、`exchangeType`、`stockCode`、`actionType` 等保持可追踪映射。
- 交易签名、行情签名、WebSocket 认证应分开建模，不能用一个签名函数硬套全部场景。
- `X-Request-Id`、`X-Type`、`entrustId` 语义等未确认项必须继续记录在 open decisions 中。

## 禁止事项

- 不在策略层直接引入券商 SDK 或 HTTP 客户端。
- 不用真实下单、撤单、改单接口做连通性测试。
- 不在日志、测试、文档中写入真实账号、token、密钥、身份证明或资金隐私。
- 不把券商返回的未知状态强行映射为成功。
- 不对下单失败做自动重试。
