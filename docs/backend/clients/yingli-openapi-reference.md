# 盈立 OpenAPI 官方文档解析说明

版本：v0.1
状态：部分确认
最后更新：2026-05-15

## 0. 文档定位

本文档只记录盈立证券 OpenAPI 官方 PDF 的解析范围、已知能力和安全边界，用于后续正式券商适配器设计。

`TradingGateway` 统一券商交易网关模块设计详见 [broker-trading-gateway.md](../trading/broker-trading-gateway.md)。本文档只做官方资料事实源，不承载统一网关分层、能力模式和错误处理设计。

盈立申请材料要求“源码截图”属于当前券商接入紧急任务。登录、下单、改单、撤单的源码截图应基于离线 / dry-run 调用栈实现，具体接口设计见 [usmart-openapi-api-manual.md](usmart-openapi-api-manual.md)。申请材料代码不得触达真实下单、改单、撤单接口，也不得泄露真实账号、密码、token 或私钥。

## 1. 官方资料

用户已提供繁体中文官方 PDF，位置为 `券商API/盈立/API文档/`：

- `交易開放API接口文檔V1.0-20201029(繁).pdf`
- `基礎報價開放API(繁)_20201029.pdf`
- `報價推送(繁)_20201029.pdf`

已转换为便于检索的 Markdown，位置为 `券商API/盈立/API文档/markdown/`。其中简体中文版本位于 `券商API/盈立/API文档/markdown/zh-Hans/`。Markdown 由 PDF 自动抽取文本生成，表格版式可能不如原 PDF 精确，正式设计仍以 PDF 原文为准。

盈立官方资料包含三套不同 API，不能混为一套：

| API | 官方文档 | 协议 | 项目边界 |
|---|---|---|---|
| 交易开放 API | `交易開放API接口文檔V1.0-20201029(繁).pdf` | HTTPS POST | 登录、账户、资金、持仓、订单、成交、下单、改单、撤单；归 `TradingGateway` |
| 基础报价 API | `基礎報價開放API(繁)_20201029.pdf` | HTTPS POST | 市场状态、基础信息、即时报价、分时、K 线、逐笔、盘口；归 `QuotationDataGateway` |
| 报价推送 API | `報價推送(繁)_20201029.pdf` | WebSocket | 行情推送订阅、取消订阅、心跳和 update；归 `QuotationDataGateway` |

当前已知能力：

- 直接管理交易：创建订单、修改或取消订单、检查订单状态。
- 查看账户信息：例如账户资金和当前持仓。
- 查询行情变化：股票或衍生品价格和其他信息。
- 接收实时变动：订单变动、持仓变动、报价变动等。

## 2. 安全边界

- 解析 PDF 不等于启用盈立 OpenAPI 正式接入。
- M1 不实现盈立真实下单、改单、撤单、账户查询、持仓查询或行情接入。
- 不允许用真实下单、真实改单、真实撤单接口做连通性测试、截图演示或权限测试。
- PDF 中没有明确说明的 sandbox、paper trading、改单语义、订单状态和错误码，统一标记为 `unknown_by_pdf`。
- 任何未来真实交易接入都必须重新完成 OMS、风控、交易时间检查、账户/标的白名单、人工暂停和对账设计。

## 3. PDF 解析目标

后续解析 PDF 时只提取设计所需事实：

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

初步文本解析显示：

- 交易开放 API 提到 IP 白名单、HTTPS、`X-Sign`、`MD5withRSA`、`safeBase64`、`X-Request-Id` 幂等防重。
- 交易 API 包含登录接口 `/user-server/open-api/login`。
- 交易 API 官方手册只给出相对路径，base URL 需要 OpenAPI 申请通过后由盈立提供。
- 基础报价 API 使用 HTTP POST，并包含请求频率限制和统一 header。
- 报价推送 API 使用 websocket，入口示例为 `wss://open-hz.yxzq.com/wss/v1`，包含 `auth`、`sub`、`unsub`、`update` 等消息。
- 三套 API 的 base URL、签名原文、认证方式、限流和连接生命周期需要分别实现，不能共用一个 client / signer / mapper。

以上只是初步抽取结果，正式设计时必须逐页校对 PDF。

## 5. 不进入开发范围

以下事项不作为 RobustQuant 开发任务：

- 为申请材料运行真实下单、改单、撤单。
- 在 M1 中实现真实 `uSmartOpenApiTradingAdapter` transport。
- 在 M1 中接入盈立账户、持仓、订单、成交、行情或推送。

## 6. 待解析或标记为未知

- 是否存在官方 sandbox：若 PDF 未写明，标记为 `unknown_by_pdf`。
- 改单是否为原生 modify API，还是 cancel + replace：以 PDF 为准；PDF 未写明则 `unknown_by_pdf`。
- 申请材料截图格式：与开发无关，不作为本项目设计阻塞项。
