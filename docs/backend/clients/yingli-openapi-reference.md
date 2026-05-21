# 盈立 OpenAPI 官方文档解析说明

版本：v0.1
状态：部分确认
最后更新：2026-05-21

## 0. 文档定位

本文档只记录盈立证券 OpenAPI 官方网页文档的解析范围、已知能力和安全边界，用于后续正式券商适配器设计。

`TradingGateway` 统一券商交易网关模块设计详见 [broker-trading-gateway.md](../trading/broker-trading-gateway.md)。本文档只做官方资料事实源，不承载统一网关分层、能力模式和错误处理设计。

盈立申请材料要求“源码截图”属于当前券商接入紧急任务。登录、下单、改单、撤单的源码截图应基于离线 / dry-run 调用栈实现，具体接口设计见 [usmart-openapi-api-manual.md](usmart-openapi-api-manual.md)。申请材料代码不得触达真实登录、真实下单、改单、撤单接口，也不得泄露真实账号、密码、token 或私钥。

## 1. 官方资料

uSmart / 盈立 OpenAPI 当前以官方网页文档为真相源。本地 Markdown 转换稿位于 `API_manual/uSmart/API_manual/`：

- 交易开放 API：`https://api-doc.usmart8.com/zh-cn/trade.html`，本地 `API_manual/uSmart/API_manual/usmart-trade-openapi.zh-cn.md`
- 基础报价 API：`https://api-doc.usmart8.com/zh-cn/quote-base.html`，本地 `API_manual/uSmart/API_manual/usmart-quote-base-openapi.zh-cn.md`
- 报价推送 API：`https://api-doc.usmart8.com/zh-cn/quote-push.html`，本地 `API_manual/uSmart/API_manual/usmart-quote-push-openapi.zh-cn.md`

官方 Python demo 位于 `API_manual/uSmart/openapi-demo-py/`，只用于核对签名、加密、序列化和 WebSocket 连接流程；字段枚举和接口事实仍以官方网页文档为准。demo 配置中的账号、密码、token、私钥不得进入提交。

盈立官方资料包含三套不同 API，不能混为一套：

| API | 官方文档 | 协议 | 项目边界 |
|---|---|---|---|
| 交易开放 API | `trade.html` | HTTPS POST | 登录、账户、资金、持仓、订单、成交、下单、改单、撤单；归 `TradingGateway` |
| 基础报价 API | `quote-base.html` | HTTPS POST | 市场状态、基础信息、即时报价、分时、K 线、逐笔、盘口；归 `QuotationDataGateway` |
| 报价推送 API | `quote-push.html` | WebSocket | 行情推送订阅、取消订阅、心跳和 update；归 `QuotationDataGateway` |

当前已知能力：

- 直接管理交易：创建订单、修改或取消订单、检查订单状态。
- 查看账户信息：例如账户资金和当前持仓。
- 查询行情变化：股票或衍生品价格和其他信息。
- 接收实时变动：订单变动、持仓变动、报价变动等。

## 2. 安全边界

- 解析官方网页文档不等于启用盈立 OpenAPI 正式接入。
- M1 可在用户明确授权后实现只读联调查询；申请材料截图仍只使用 dry-run / offline request builder，不做真实登录。
- 不允许用真实下单、真实改单、真实撤单接口做连通性测试、截图演示或权限测试。
- 官方网页文档没有明确说明的 sandbox、paper trading、改单语义、订单状态和错误码，统一标记为 `unknown_by_official_doc`。
- 任何未来真实交易接入都必须重新完成 OMS、风控、交易时间检查、账户/标的白名单、人工暂停和对账设计。

## 3. 官方资料解析目标

后续解析官方网页文档时只提取设计所需事实：

- 认证方式。
- 交易、基础报价、报价推送分别对应的 base URL 和 endpoint。
- header、签名算法、请求幂等字段和加密要求。
- 登录、下单、改单、撤单参数。
- 账户资金、持仓、订单状态查询接口参数。
- 行情查询和实时推送订阅参数。
- 订单类型、价格类型、市场、盘前盘后规则。
- 错误码和订单状态码。
- 频率限制和白名单要求。

## 4. 当前已初步识别信息

当前网页文档与官方 demo 核对显示：

- 交易开放 API 提到 IP 白名单、HTTPS、`X-Sign`、`MD5withRSA`、`safeBase64`、`X-Request-Id` 幂等防重。
- 交易 API 包含登录接口 `/user-server/open-api/login`。
- 交易 API 网页文档和官方 demo 给出生产 `https://open-jy.yxzq.com`、测试 `http://open-jy-uat.yxzq.com`；真实出网仍需申请通过、IP 白名单、渠道号和密钥配置。
- 交易 API 验证码登录前置接口 `/user-server/open-api/send-phone-captcha` 的 `type=106` 表示短信登录。
- 交易 API 普通股票委托改单/撤单共用 `/stock-order-server/open-api/modify-order`，其中普通股票委托 `actionType=1` 表示改单、`actionType=0` 表示撤单；IPO 改撤单接口的 `actionType` 枚举不同，不能混用。
- 基础报价 API 使用 HTTP POST，并包含请求频率限制和统一 header。
- 报价推送 API 使用 websocket，入口示例为 `wss://open-hz.yxzq.com/wss/v1`，包含 `auth`、`sub`、`unsub`、`update` 等消息。
- 三套 API 的 base URL、签名原文、认证方式、限流和连接生命周期需要分别实现，不能共用一个 client / signer / mapper。

正式设计时必须继续以官方网页文档为准，并用官方 demo 校验实现细节。

## 5. 不进入开发范围

以下事项不作为 RobustQuant 开发任务：

- 为申请材料运行真实下单、改单、撤单。
- 在 M1 中实现真实 `uSmartOpenApiTradingAdapter` transport。
- 在 M1 中接入盈立账户、持仓、订单、成交、行情或推送。

## 6. 待解析或标记为未知

- 是否存在官方 sandbox：若官方网页文档未写明，标记为 `unknown_by_official_doc`。
- 普通股票委托的 `actionType` 已按官方网页文档核对；券商内部改单是否为原生 modify 仍未写明，本地 OMS 风险模型按 cancel + replace 处理。
- 申请材料截图格式：与开发无关，不作为本项目设计阻塞项。
