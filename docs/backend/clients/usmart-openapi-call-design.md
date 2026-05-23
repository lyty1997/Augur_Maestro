# uSmart / 盈立交易开放 API 调用栈全链路设计

版本：v0.1  
状态：设计草案，待用户确认  
最后更新：2026-05-21

## 0. 文档定位

本文档说明 RobustQuant 中“从本地入口到实际调用 uSmart / 盈立交易开放 API server”的全链路代码层设计。它回答券商审核最关心的几个问题：

- 从 CLI / Web / 本地服务到 uSmart / 盈立交易开放 API server，中间经过哪些层。
- 哪一层代码会发起到交易开放 API 的 HTTP 请求。
- 登录、下单、改单、撤单分别调用哪些 endpoint。
- 请求 header、签名、`X-Request-Id`、token 如何生成和传递。
- 交易动作如何先经过 `TradingGateway` 安全门控。
- 日志和错误处理如何避免泄露账号、密码、token、密钥和真实资金隐私。

本文档是 [broker-trading-gateway.md](../trading/broker-trading-gateway.md) 的下层专项设计。`TradingGateway` 是统一交易安全门面；本文档描述从本地入口、应用服务、`TradingGateway`、`uSmartOpenApiTradingAdapter`、交易开放 API client、交易开放 API signer、HTTP transport 到 uSmart / 盈立交易开放 API server 的完整调用栈。

机器可读 OpenAPI 对接草案见 [api/usmart-trade-openapi.draft.yaml](api/usmart-trade-openapi.draft.yaml)。交易响应状态 catalog 见 [api/usmart-trade-error-codes.draft.yaml](api/usmart-trade-error-codes.draft.yaml)，由 `src/scripts/docs/extract_usmart_trade_error_codes.py` 从官方网页转换稿生成，并按 `endpoint` / 手册章节分组；调用方必须按当前接口读取对应 `response_statuses`，不能把不同接口的状态码混成全局处理表。草案只用于字段对齐、契约测试和后续代码生成准备；其中 `x-pending-confirmation` 标记的字段不得视为已确认接口事实。

盈立官方资料实际拆成三套 API，本文档只覆盖第一套：

| API | 官方文档 | 协议 | RobustQuant 边界 |
|---|---|---|---|
| 交易开放 API | `https://api-doc.usmart8.com/zh-cn/trade.html` | HTTPS POST | `TradingGateway`、`BrokerTradingAdapter`、uSmart 交易适配器 |
| 基础报价 API | `https://api-doc.usmart8.com/zh-cn/quote-base.html` | HTTPS POST | `QuotationDataGateway` 后续 HTTP 行情适配器 |
| 报价推送 API | `https://api-doc.usmart8.com/zh-cn/quote-push.html` | WebSocket | `QuotationDataGateway` 后续 WS 行情适配器 |

三套 API 的 base URL、签名原文、认证 header、限流、连接生命周期和错误处理都不能混用。

uSmart / 盈立 OpenAPI 当前以官方网页文档为字段、endpoint、枚举和版本真相源。本地转换稿保存于 `API_manual/uSmart/API_manual/`。官方 Python demo 位于 `API_manual/uSmart/openapi-demo-py/`，只作为签名、加密、序列化和 WebSocket 连接流程参考，不替代网页字段表；不得提交或复制 demo 中的账号、密码、token、私钥或配置。

网页版交易开放 API base URL：

| 环境 | base URL |
|---|---|
| 生产 | `https://open-jy.yxzq.com` |
| 测试 | `http://open-jy-uat.yxzq.com` |

登录、下单、改单、撤单四条链路的接口级 API 手册、输入输出、上下调用层和当前设计缺口见 [usmart-openapi-api-manual.md](usmart-openapi-api-manual.md)。

## 1. 调用链路

RobustQuant 本地系统与 uSmart / 盈立交易开放 API 是 client-server 架构：

```mermaid
sequenceDiagram
    participant UI as CLI / Web / 任务
    participant App as RobustQuant 应用服务
    participant TG as TradingGateway
    participant AD as uSmartOpenApiTradingAdapter
    participant CL as uSmartTradeOpenApiClient
    participant SG as uSmartTradeAuthSigner
    participant HTTP as HTTP Transport
    participant API as uSmart Trading OpenAPI Server

    UI->>App: 发起登录或订单动作
    App->>TG: 调用统一交易接口
    TG->>TG: 检查 mode / trading_enabled / capability
    alt 只读安全模式下的交易动作
        TG-->>App: broker.trading_disabled
    else 允许的只读动作或未来受控实盘动作
        TG->>AD: 调用适配器方法
        AD->>CL: 构造 endpoint + body
        CL->>SG: 按端点 profile 生成 Authorization / X-Sign 等 header
        CL->>HTTP: POST JSON 请求
        HTTP->>API: HTTPS 调用交易开放 API
        API-->>HTTP: 交易开放 API 响应
        HTTP-->>CL: HTTP response
        CL-->>AD: 标准化原始响应摘要
        AD-->>TG: 映射为内部 DTO
        TG-->>App: 返回业务结果
    end
```

当前实现阶段：

- `TradingGateway` 已实现默认 `read_only` 交易阻断。
- `uSmartOpenApiTradingAdapter` 已保留登录、下单、改单、撤单方法外形；当前代码里的请求体仍是 dry-run 骨架，尚未按官方网页字段完整映射。
- 交易开放 API client 当前为 dry-run 外壳，不发真实 HTTP。
- 交易开放 API signer、真实 HTTP transport、token 生命周期管理尚未实现。
- 本文 2026-05-19 后续章节补全的是目标设计，不代表当前代码已经具备真实 OpenAPI 出网能力。

### 1.1 全链路分层总览

| 层级 | 模块 | 作用 | 是否接触 uSmart 协议字段 | 是否允许真实交易决策 |
|---|---|---|---|---|
| L0 | CLI / Web / 定时任务 | 用户或任务入口，发起登录、查询、订单动作 | 否 | 否 |
| L1 | FastAPI Router / CLI command | 参数解析、权限检查、生成 `trace_id` | 否 | 否 |
| L2 | Application Service | 编排业务用例，调用 OMS、风控或只读查询服务 | 否 | 否 |
| L3 | OMS / Risk | 订单生命周期、风控检查、交易时间和白名单检查 | 否 | 是，但只决定内部订单是否可提交 |
| L4 | `TradingGateway` | 统一交易安全门面，执行 `mode`、`trading_enabled`、capability 阻断 | 否 | 是，真实交易出网前最后一道门 |
| L5 | `BrokerTradingAdapter` | 统一券商适配器基类 | 否 | 否 |
| L6 | `uSmartOpenApiTradingAdapter` | 内部 DTO 与交易开放 API endpoint/body 字段转换 | 是 | 否 |
| L7 | 交易开放 API client | 生成 JSON、调用交易 API signer、调用 HTTP transport、解析响应 | 是 | 否 |
| L8 | 交易开放 API signer | 生成交易 API 的 `X-Sign` 和端点级认证 header | 是 | 否 |
| L9 | `uSmartHttpTransport` | 真实 HTTPS POST，处理 HTTP 状态和 timeout | 是 | 否 |
| L10 | uSmart / 盈立交易开放 API Server | 券商服务端，处理登录、查询、委托、改单、撤单 | 是 | 券商侧执行 |

关键约束：

- L0 到 L3 不允许出现 uSmart 私有字段，例如 `entrustId`、`entrustProp`、`exchangeType`。
- L6 以后才允许出现 uSmart endpoint 和字段映射。
- 真实交易动作必须在 L4 被 `TradingGateway` 允许后，才可进入 L6。
- 当前 `read_only` 模式下，`place_order`、`modify_order`、`cancel_order` 在 L4 直接阻断，不会进入 L6。

### 1.2 四条核心链路

登录链路：

```text
CLI/FastAPI
  -> ApplicationService.connect_broker
  -> TradingGateway.connect
  -> uSmartOpenApiTradingAdapter.connect
  -> uSmartTradeOpenApiClient.post('/user-server/open-api/login')
  -> uSmartTradeAuthSigner.build_headers
  -> uSmartHttpTransport.post_json
  -> uSmart / 盈立交易开放 API Server
```

只读查询链路：

```text
CLI/FastAPI
  -> QueryService
  -> TradingGateway.get_positions / query_order / query_trades
  -> uSmartOpenApiTradingAdapter
  -> uSmartTradeOpenApiClient
  -> uSmart / 盈立交易开放 API Server
```

只读安全模式下的交易阻断链路：

```text
OMS
  -> TradingGateway.place_order / modify_order / cancel_order
  -> CapabilityGuard.ensure_allowed
  -> broker.trading_disabled
  -> 审计事件 usmart.place_order_blocked / modify_order_blocked / cancel_order_blocked
```

未来受控实盘链路：

```text
OMS
  -> 风控通过 + 交易时间通过 + 研究 Agent 候选经人工发布的白名单通过 + 策略授权通过
  -> TradingGateway 允许
  -> uSmartOpenApiTradingAdapter
  -> uSmartTradeOpenApiClient
  -> uSmartTradeAuthSigner
  -> uSmartHttpTransport
  -> uSmart / 盈立交易开放 API Server
  -> 订单回报映射
  -> OMS 状态更新
  -> 对账任务复核
```

### 1.3 请求与响应追踪

全链路必须携带以下追踪字段：

| 字段 | 生成层 | 传递范围 | 说明 |
|---|---|---|---|
| `trace_id` | L1 | L1-L9 | 一次用户操作或任务链路 |
| `intent_id` | 策略/人工动作 | L2-L4 | 交易意图 ID，登录和只读查询可为空 |
| `order_id` | OMS | L3-L9 | 本地订单 ID |
| `risk_check_id` | Risk | L3-L4 | 风控结果 ID |
| `request_id` | Gateway / Client | L4-L10 | 对应 `X-Request-Id` |
| `broker_order_id` | uSmart server | L10-L3 | 券商订单号，日志中必须脱敏 |

返回路径必须从下往上逐层收敛：

```text
交易开放 API 原始响应
  -> uSmartTradeOpenApiResponse 脱敏摘要
  -> BrokerOrderAck / BrokerModifyAck / BrokerCancelAck
  -> OMS 状态
  -> ApplicationService 响应 DTO
  -> CLI/FastAPI 用户可见结果
```

禁止把 uSmart 原始响应直接返回给 CLI、Web 或报告。

### 1.4 本地 server 与券商 server 的关系

RobustQuant 后续可能有自己的 FastAPI server。它和 uSmart / 盈立交易开放 API server 是两个不同角色：

| Server | 归属 | 作用 |
|---|---|---|
| RobustQuant FastAPI server | 本地系统 | 给 Web/CLI/任务提供本地接口，调用 `TradingGateway` |
| uSmart / 盈立交易开放 API server | 券商 | 接收交易开放 API HTTPS 请求，处理登录、查询、委托、改单、撤单 |

本地 FastAPI server 不直接拼接 uSmart 请求，也不保存私钥和 token 原文。真正与交易开放 API server 通信的是 `uSmartTradeOpenApiClient` + `uSmartHttpTransport`。

## 2. 代码分层

建议目标代码结构：

```text
src/
  rq_core/
    broker_kernel/
      gateway.py                    TradingGateway：统一交易安全门面
      contracts.py                  统一 DTO、枚举、适配器基类
      capability.py                 交易能力和模式检查
      errors.py                     统一异常
      usmart/
        adapter.py                  uSmartOpenApiTradingAdapter
        client.py                   交易开放 API client
        auth.py                     交易开放 API signer
        transport.py                uSmartHttpTransport
        endpoints.py                endpoint 常量
        mapper.py                   交易开放 API 响应与内部 DTO 映射
        rate_limit.py               交易开放 API 频率限制
    quotation_kernel/
      usmart_http/                  基础报价 API HTTP 适配器，后续实现
      usmart_ws/                    报价推送 API WebSocket 适配器，后续实现
```

职责边界：

| 模块 | 职责 | 禁止事项 |
|---|---|---|
| `TradingGateway` | 检查能力模式、交易开关、调用来源，决定是否允许触达适配器 | 不拼接 uSmart 字段，不保存 token |
| `uSmartOpenApiTradingAdapter` | 将内部 DTO 转为交易开放 API endpoint 和 body | 不绕过 `TradingGateway`，不自行决定真实交易是否允许 |
| 交易开放 API client | 组织交易 API header、签名、HTTP POST、响应解析 | 不包含策略、风控、OMS 逻辑；不处理基础报价或报价推送 |
| 交易开放 API signer | 生成交易 API 的 `X-Sign` 和端点级 header profile | 不把私钥、密码、token 写入日志；不复用基础报价签名规则 |
| `uSmartHttpTransport` | 发起 HTTPS 请求、处理 timeout 和 HTTP 状态 | 不对下单/改单/撤单做自动重试 |
| `uSmartMapper` | 映射状态码、错误码、订单号和响应字段 | 不猜测官方网页未说明的状态 |

## 3. Endpoint 范围

第一版只覆盖券商申请、只读联调、对账和交易网关最小闭环需要的接口。申请材料截图只使用 dry-run / offline request builder，不做真实登录；只读联调可在用户显式授权后触达登录和查询接口，但不允许下单、改单、撤单。字段以官方网页文档为准；本文只记录当前设计映射。

### 3.1 交易 API endpoint 分组

| 能力 | 方法 | endpoint | 当前允许触达 OpenAPI |
|---|---|---|---|
| 渠道密码登录 | POST | `/user-server/open-api/login` | 申请材料只 dry-run；只读联调阶段可显式允许 |
| 获取手机验证码 | POST | `/user-server/open-api/send-phone-captcha` | 申请材料只 dry-run；短信登录验证码 `type=106`，避免自动化滥用 |
| 渠道验证码登录 | POST | `/user-server/open-api/loginCaptcha` | 申请材料只 dry-run；只读联调阶段可作为备选登录方式 |
| 获取交易解锁状态 | POST | `/user-server/open-api/get-trade-status` | 只读联调阶段可允许 |
| 普通下单 | POST | `/stock-order-server/open-api/entrust-order` | 默认禁止，需 `live_guarded` |
| 委托改单 | POST | `/stock-order-server/open-api/modify-order` | 默认禁止，需 `live_guarded` |
| 委托撤单 | POST | `/stock-order-server/open-api/modify-order` | 默认禁止，需 `live_guarded` |
| 碎股下单 | POST | `/stock-order-server/open-api/odd-entrust` | 默认禁止，需 `live_guarded` + 美股碎股能力 |
| 碎股撤单 | POST | `/stock-order-server/open-api/odd-modify` | 默认禁止，需 `live_guarded` + 美股碎股能力 |
| 改单范围查询 | POST | `/stock-order-server/open-api/modified-range` | 只读联调扩展；不进第一批只读联调 |
| 最大可买可卖数量 | POST | `/stock-order-server/open-api/trade-quantity` | 只读联调扩展；不进第一批只读联调 |
| 今日订单查询 | POST | `/stock-order-server/open-api/today-entrust` | 只读联调阶段可允许 |
| 历史订单查询 | POST | `/stock-order-server/open-api/his-entrust` | 只读联调阶段可允许 |
| 订单明细查询 | POST | `/stock-order-server/open-api/order-detail` | 只读联调阶段可允许 |
| 成交流水查询 | POST | `/stock-order-server/open-api/stock-record` | 只读联调阶段可允许 |
| 持仓查询 | POST | `/stock-order-server/open-api/stock-holding` | 只读联调阶段可允许 |
| 资产查询 | POST | `/stock-order-server/open-api/stock-asset` | 只读联调阶段可允许 |
| 客户股票资产批量查询 | POST | `/stock-order-server/open-api/stock-asset-list` | 第一版不启用；只读联调先限定单账户 |
| 聚合资产查询 | POST | `/aggregation-server/open-api/user-asset-aggregation/v1` | 第一版不启用；只读联调先限定单账户 |
| 查询汇率 | POST | `/stock-capital-server/open-api/currency-exchange-info` | 第一版可作为多币种估值辅助，不进入交易决策硬依赖 |

第一批只读联调只开放：真实登录、资产查询、持仓查询、今日订单、历史订单、订单明细、成交流水。其他只读接口后置。

不进入第一版：

- 修改、重置登录密码或交易密码。
- 交易解锁 `trade-login`。
- IPO 申购和 IPO 改单；港股新股暗盘交易若通过普通下单接口和 `sessionType=3` 处理，不属于 IPO 申购接口，但第一批只保留设计。
- 美股盘前盘后交易。
- 自动对冲、做空、融资融券、保证金交易和美股期权；后续迭代再单独设计能力、白名单、额度和高风险授权。
- 券商侧条件单、券商侧止盈止损、触发单；第一版自动止盈止损由策略模块产生普通正股买卖意图。

`trade-login` 不是下单接口，但可能改变账户交易可用状态，因此不作为只读联调接口，也不进入第一版受控实盘自动流程。遇到券商要求交易密码、交易解锁或交易锁定时，OMS 阻断交易并进入人工确认流程。

### 3.2 非本文档范围：基础报价 API 与报价推送 API

以下接口来自另外两套官方 API，不挂在 `TradingGateway` 上，也不由交易开放 API client、signer 或 mapper 承接。它们由 `QuotationDataGateway` 和后续 `uSmartQuotationHttpAdapter` / `uSmartQuotationWsAdapter` 承接。行情只读联调允许独立启用，但行情失败、延迟或权限不足时，未来实盘交易必须进入降级或暂停。

| 能力 | 方法 | endpoint / 入口 | 第一版用途 |
|---|---|---|---|
| 市场状态 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/marketstate` | 交易时间和市场状态参考 |
| 基础信息 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/basicinfo` | 标的信息补充 |
| 即时报价 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/realtime` | 只读行情快照 |
| 分时 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/timeline` | 只读行情序列 |
| K 线 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/kline` | 研究和校验辅助 |
| 逐笔 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/tick` | 第一版暂不作为交易依据 |
| 买卖盘 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/orderbook` | 只读盘口 |
| 行情推送 | WS | `wss://open-hz.yxzq.com/wss/v1` | 报价推送 API，`auth`、`sub`、`unsub`、`update`、`ping`、`pong` |

报价推送 API 第一版只允许恢复行情订阅，不允许在重连、订阅恢复或 `update` 回调中触发任何交易动作。

## 4. 交易开放 API 请求 header 设计

根据交易开放 API 网页文档和官方 Python demo 核对，交易接口 header 采用端点级 profile。公共候选字段如下：

| Header | 来源 | 说明 |
|---|---|---|
| `Authorization` | 登录后 token | 登录接口以外的交易和查询接口需要 |
| `Content-Type` | 固定 | `application/json; charset=utf-8` |
| `X-Lang` | 配置 | 语言类别，例如 `1` 表示简体 |
| `X-Channel` | uSmart 分配 | 渠道 ID |
| `X-Time` | 本地生成 | Unix epoch milliseconds 字符串；交易 demo 默认 helper 未携带，只有端点 profile 要求时外发 |
| `X-Dt` | 配置 | 设备类型数字字符串，默认 `"4"` 表示 Windows |
| `X-Type` | 配置 | APP 类别，默认 `"1"` 表示大陆版 |
| `X-Request-Id` | 本地生成 | 幂等防重 ID；官方 demo 只在部分交易端点显式携带 |
| `X-Sign` | 交易开放 API signer 生成 | 对 body 内容签名/加密后的值 |

设计规则：

- 每次券商调用都必须生成内部 `request_id` / `broker_request_id` 并写入审计记录；是否外发为 `X-Request-Id` 由端点 header profile 决定。
- 第一版交易 API header profile 跟随官方 Python demo：默认交易 helper 发送 `Content-type`、`X-Lang`、`X-Channel`、`X-Sign`、`Authorization`；`modify-order` 额外携带 `X-Request-Id`；`entrust-order` 不强制外发 header `X-Request-Id`，使用 body `serialNo` 和本地审计映射。
- `X-Sign` 只由交易开放 API signer 生成，其他模块不接触私钥。
- `Authorization` token 只保存在内存会话中，默认不落库。
- 日志只记录 header key 列表、内部 `request_id`、必要时记录外发 `X-Request-Id` 和脱敏 token 摘要，不记录完整 token 或签名。
- `X-Type` 按官方说明为 APP 类别，`"1"` 表示大陆版、`"2"` 表示港版；本项目默认大陆版。
- `Content-Type` 统一由 client 注入，调用方不允许手工传入，避免签名 body 和实际 body 不一致。
- 同一请求的 header、body_json、endpoint 和 request_id 必须作为不可变对象进入签名流程，签名后不得再修改 body。

`X-Dt` 设备类型按官方说明中的 `t1`、`t2`、`t3`、`t4`、`t5` 语义理解，但 header 示例使用数字值，因此代码中保存为数字字符串：

| `X-Dt` | 设备类型 |
|---|---|
| `"1"` | Android |
| `"2"` | iOS |
| `"3"` | 其他 |
| `"4"` | Windows |
| `"5"` | Mac |

默认值为 `"4"`，匹配本地 Windows 开发和申请材料截图环境；如盈立后续要求 `t4` 字面值，可通过配置切换。

`X-Type` APP 类别：

| `X-Type` | APP 类别 |
|---|---|
| `"1"` | 大陆版 |
| `"2"` | 港版 |

本项目默认 `"1"`，即大陆版。

### 4.1 请求 ID 策略

官方资料中存在长度描述不一致：概述中 `X-Request-Id` 描述为 19 位数字，部分接口章节又出现 30 位描述；下单 body 的 `serialNo` 明确为最长 19 位。官方 Python demo 生成的 `serialNo` 是 19 位字符串。当前实现结论：内部 `broker_request_id` 始终生成并审计；外发 `X-Request-Id` 按端点 profile 决定，长度按 30 位可配置字符串处理，不硬编码；下单 body 的 `serialNo` 按最长 19 位处理，第一版可按用户确认使用数字 JSON，若联调被拒绝再切换为字符串序列化。

| 场景 | 字段 | 设计策略 |
|---|---|---|
| HTTP header 幂等 | `X-Request-Id` | 由端点 header profile 决定是否外发；外发时由 `RequestIdGenerator` 生成，按 30 位可配置字符串校验 |
| 下单 body 流水 | `serialNo` | 与本地 `broker_request_id` 建立映射，按官方网页最长 19 位约束处理；demo 生成字符串，第一版按数字可配置 |
| 本地 OMS 订单 | `order_id` | RobustQuant 内部 ID，不直接暴露给券商 |
| 链路追踪 | `trace_id` | 可为 UUID/ULID，不参与券商幂等 |

映射关系：

```text
order_id -> broker_request_id -> X-Request-Id (only when endpoint profile sends it)
broker_request_id -> serialNo
broker_order_id <- entrustId
```

规则：

- `broker_request_id` 必须在调用券商前持久化到审计记录；如果持久化失败，不允许触达 OpenAPI。
- 只读查询也要携带 `request_id`，但查询 request_id 不得复用交易 request_id。
- 交易请求超时后，不自动复用同一个 request_id 重发，也不生成新 request_id 补发。
- 如果券商对重复 `X-Request-Id` 的返回语义不清楚，统一标记为 `unknown_by_official_doc`，不能依赖它做自动补偿。

## 5. 交易开放 API 签名与认证设计

交易开放 API 网页文档与官方 Python demo 核对信息：

- 协议：HTTPS。
- 签名 header：`X-Sign`。
- 签名算法描述：`MD5withRSA`。
- 交易开放 API 概述描述签名内容为 Body 内容。
- 官方 Python demo 的交易 HTTP helper 使用 `json.dumps(params)` 作为签名原文，`MD5withRSA` 后用标准 Base64 编码为 `X-Sign`。
- 基础报价 API 描述签名原文为 `Authorization`、`X-Channel`、`X-Lang`、`X-Request-Id`、`X-Time` 头字段与 body 内容按序拼接；这是另一套 API，不在本文档的交易 signer 中实现。
- 官方 Python demo 的基础报价 HTTP helper 使用上述 header + body 签名原文，并用 URL-safe Base64 编码；不能与交易 signer 混用。
- 编码方式：网页文档描述为 `safeBase64` / URL-safe Base64，交易 demo 使用标准 Base64；用户已确认交易 API 第一版默认跟随官方 Python demo 使用标准 Base64，保留切换到 URL-safe Base64 的配置。
- 幂等字段：外发 `X-Request-Id` 由端点 header profile 决定；本地 `broker_request_id` 始终存在。
- 用户已确认第一版跟随官方 Python demo：交易 HTTP helper 默认发送 `Content-type`、`X-Lang`、`X-Channel`、`X-Sign`、`Authorization`；`modify-order` 示例额外传入 `X-Request-Id`；`entrust-order` 使用 body `serialNo` 和本地审计映射，不强制外发 header `X-Request-Id`；`X-Time` 不作为交易 API 全局必填 header。
- 访问控制：IP 白名单。

因此第一版不能把交易开放 API、基础报价 API 和报价推送 API 硬编码成同一个 signer。本文档只定义交易开放 API signer：

| 签名器 | 适用范围 | 输入 |
|---|---|---|
| `uSmartTradeAuthSigner` | 交易开放 API | 稳定 JSON body，不拼接 header |
| `uSmartQuoteHttpAuthSigner` | 基础报价 API | 不在本文档实现；后续按基础报价网页文档独立设计 |
| `uSmartQuoteWsAuthSigner` | 报价推送 API | 不在本文档实现；后续按报价推送网页文档独立设计 |

目标接口：

```python
class uSmartTradeAuthSigner:
    def build_headers(
        self,
        *,
        endpoint: str,
        body_json: str,
        request_id: str,
        token: str | None,
        now_ms: int,
    ) -> dict[str, str]:
        ...
```

处理步骤：

1. 将 body 使用稳定 JSON 序列化，保证签名前后的 body 字节一致。
2. 生成或接收内部 `request_id` / `broker_request_id`。
3. 按交易开放 API 规则生成签名前原文：只使用稳定 JSON body，不拼接 header 字段。
4. 对交易开放 API 签名结果按配置编码，写入 `X-Sign`；默认跟随官方 Python demo 使用标准 Base64，若盈立明确要求网页手册的 URL-safe Base64，可通过配置切换。
5. 按端点 header profile 组装 `Authorization`、`X-Lang`、`X-Channel`、`X-Sign` 等 header；`X-Time`、`X-Dt`、`X-Type`、`X-Request-Id` 只有在 profile 要求或配置开启时外发。

隐私字段加密与签名分开处理：

- 官方手册同时出现“验签测试公开密钥”和“隐私资料加密测试公开密钥”，说明 `X-Sign` 渠道签名密钥材料与隐私资料加密密钥材料是两套，不得混用。
- 登录手机号、登录密码、交易密码等字段使用官方文档所说的“隐私资料加密”密钥材料，与 `X-Sign` 渠道签名私钥不是同一件事。
- 官方 Python demo 的 `common/utils.py` 已给出隐私字段加密实现：`rsa_encrypt(data)` 使用 `Crypto.Cipher.PKCS1_v1_5` 做 RSA 加密，再用 `base64.urlsafe_b64encode(...)` 输出字符串。实现按这个 transform 建模。
- demo 中 `EncryptUtil.__init__(pub_key_str, pri_key_str)` 的变量名和 PEM header 包装存在反常处：`pub_key_str` 被包成 `BEGIN PRIVATE KEY` 后用于 `rsa_encrypt`，`pri_key_str` 被包成 `BEGIN PUBLIC KEY` 后用于 `md5_with_rsa`。RobustQuant 不按变量名猜测密钥语义，配置中按 demo 参数槽位和券商最终分配的密钥材料显式绑定，并在离线测试中验证加密/签名可用。
- `uSmartTradeSensitiveFieldEncryptor` 负责加密 `phoneNumber`、`password`、交易密码等交易开放 API 字段。
- `uSmartTradeAuthSigner` 只负责交易开放 API 请求签名，不接收明文密码和手机号。
- 明文敏感字段只能从本地密钥管理层读出后在内存中短暂存在，禁止进入 DTO、日志、异常消息和测试 fixture。

待确认项：

- `X-Request-Id` 重复请求返回语义。
- 券商最终下发的密钥材料如何对应 demo 的 `public_key` / `private_key` 配置槽位。
- 项目策略已确认：UAT 测试地址不自动等同 sandbox / paper trading；是否保证交易动作不产生真实委托仍需券商确认。

## 6. 交易开放 API Client 设计

目标接口：

```python
class uSmartTradeOpenApiClient:
    def post(
        self,
        endpoint: str,
        body: dict[str, Any],
        *,
        trace_id: str,
        request_id: str,
        token_required: bool,
        operation_kind: Literal["readonly", "trade_action"],
    ) -> uSmartTradeOpenApiResponse:
        ...
```

内部流程：

1. 校验 endpoint 是否在白名单常量中，并校验交易标的命中量化研究 Agent 候选经人工发布的当前有效白名单。
2. 生成稳定 body JSON。
3. 调用 `uSmartTradeAuthSigner.build_headers(...)`。
4. 通过 `uSmartHttpTransport.post_json(...)` 发起 HTTPS 请求。
5. 解析 HTTP 状态码和 JSON 响应。
6. 生成脱敏响应摘要。
7. 返回 `uSmartTradeOpenApiResponse` 给 adapter。

重试边界：

- `operation_kind="readonly"` 可以按 `RateLimiter` 和退避策略有限重试。
- `operation_kind="trade_action"` 不允许由 client 自动重试；timeout、连接中断、未知响应统一向上抛出可审计错误，由 OMS 进入 `unknown`。
- client 只能重试传输层未出网的只读请求；是否“未出网”不能确定时，按已可能触达券商处理。

`uSmartTradeOpenApiResponse` 建议字段：

| 字段 | 说明 |
|---|---|
| `endpoint` | OpenAPI endpoint |
| `http_status` | HTTP 状态码 |
| `request_id` | `X-Request-Id` |
| `broker_code` | 券商业务返回码 |
| `broker_message` | 脱敏后的返回消息 |
| `data` | 脱敏或必要字段后的业务数据 |
| `raw_hash` | 原始响应哈希，用于审计对照 |
| `duration_ms` | 请求耗时 |

日志不得保存完整 `raw response`。

## 7. 登录 API 设计

交易开放 API 有两种登录方式。申请材料截图只展示 dry-run 请求构造和调用栈，不做真实登录；真实登录只允许在只读联调配置显式开启后发生。

1. 渠道密码登录：手机 + 登录密码 + 渠道，endpoint 为 `/user-server/open-api/login`。
2. 渠道验证码登录：先调用 `/user-server/open-api/send-phone-captcha` 获取手机验证码，短信登录验证码类型为 `type=106`；再用手机 + 验证码 + 渠道调用 `/user-server/open-api/loginCaptcha`。

统一适配器方法：

```python
class uSmartOpenApiTradingAdapter:
    def connect(self, account_ref: AccountRef | None = None) -> BrokerSession:
        ...
```

密码登录 OpenAPI：

```text
POST /user-server/open-api/login
```

密码登录请求 body 设计：

| 字段 | 来源 | 说明 |
|---|---|---|
| `areaCode` | 配置 | 区号 |
| `phoneNumber` | 本地密钥配置 | 官方网页登录接口字段，需使用隐私资料加密密钥材料处理，默认按公钥加密 |
| `login_password_secret_ref` | 本地密钥配置 | 登录密码 secret 引用 |
| `loginPasswordEncrypted` | `uSmartTradeSensitiveFieldEncryptor` | RSA 加密后的登录密码；映射到盈立官方 body 字段 `password` |

登录手机号字段名确认使用 `phoneNumber`，不使用 `mobile`、`phone` 或 `telephone`。

获取验证码请求 body 设计：

| 字段 | 来源 | 说明 |
|---|---|---|
| `areaCode` | 配置 | 区号 |
| `phoneNumber` | 本地密钥配置 | 使用隐私资料加密密钥材料处理 |
| `type` | 固定值 | `106` 表示短信登录验证码 |

验证码登录请求 body 设计：

| 字段 | 来源 | 说明 |
|---|---|---|
| `areaCode` | 配置 | 区号 |
| `phoneNumber` | 本地密钥配置 | 使用隐私资料加密密钥材料处理 |
| `captcha` | 用户输入 / 人工流程 | 手机验证码，不写日志 |

`loginCaptcha` 参数表只列出 `areaCode`、`captcha`、`phoneNumber` 三个 body 字段；请求 body 示例里出现了 `modifyUserConfigParam`。第一版不主动发送 `modifyUserConfigParam`，除非盈立确认该示例字段在当前渠道必填。

登录密码和交易密码必须在配置和代码变量名上分离：

| 语义 | 配置 / 内部变量 | 盈立官方 body 字段 |
|---|---|---|
| 登录密码 | `login_password_secret_ref`、`loginPasswordEncrypted` | 登录接口 `/login` 的 `password` |
| 交易密码 | `trade_password_secret_ref`、`tradePasswordEncrypted` | 下单、改单、撤单 body 的 `password` |

除最终 request body builder 外，代码中不得使用裸 `password` 表示某个 secret，避免把登录密码和交易密码混用。

响应处理：

- 登录响应不是 `data.token` 包装结构；手册示例为顶层对象直接包含 `token`、`expiration`、`tradePassword`、`openedAccount` 等字段。
- 成功后从顶层字段提取 `token`。
- 从顶层字段读取 token 过期时间 `expiration`，但不记录 token 原文。
- 读取 `tradePassword`、`openedAccount`、`extendStatusBit` 作为权限和账户状态摘要；仅保存脱敏布尔值或摘要，不保存完整用户资料。
- token 存入内存 `uSmartSession`。
- 第一版只维护单账户单 session；后续多账户、多设备或跨进程会话缓存必须单独设计。
- 只读查询发现 token 过期或 401 时，可以停止当前请求并触发显式重新登录后再发起新的只读查询。
- 下单、改单、撤单过程中发现 token 过期、401 或权限错误时，不允许隐式重新登录后继续提交；必须返回 `broker.auth_expired` / `broker.auth_failed`，由 OMS 重新进入可审计流程。
- 返回 `BrokerSession`，其中只包含脱敏 `session_id_masked`。
- 日志不记录手机号、密码、token 原文。

只读安全边界：

- 登录可作为只读联调的一部分。
- 登录成功不代表允许交易。
- 登录后仍不能调用下单、改单、撤单，除非 `TradingGateway` 进入受控实盘模式并满足全部风控条件。

## 8. 下单 API 设计

方法：

```python
class uSmartOpenApiTradingAdapter:
    def place_order(self, request: BrokerOrderRequest) -> BrokerOrderAck:
        ...
```

OpenAPI：

```text
POST /stock-order-server/open-api/entrust-order
```

内部字段映射：

| 内部字段 | uSmart body 字段 | 说明 |
|---|---|---|
| `request.request_id` 派生的 19 位流水 | `serialNo` | 下单 body 流水号，最长 19 位；与 `X-Request-Id` 的关系需记录审计映射 |
| `request.quantity` | `entrustAmount` | 委托数量 |
| `request.limit_price` | `entrustPrice` | 委托价格；第一版美股盘中普通单只允许限价，必须大于 0 |
| `request.price_type` + `market` | `entrustProp` | 委托属性，枚举见下表 |
| `request.side` | `entrustType` | 0 买，1 卖 |
| `request.market` | `exchangeType` | 0 港股，5 美股，6 沪港通，7 深港通；第一版真实普通单只允许 `5` |
| `request.symbol` | `stockCode` | 股票代码 |
| `request.name` | `stockName` | 可选 |
| `trade_password_secret_ref` | 内部配置 | 交易密码 secret 引用；第一版 `trade_password_required=false`，默认不读取 |
| `tradePasswordEncrypted` | `uSmartTradeSensitiveFieldEncryptor` | RSA 加密后的交易密码；仅 `trade_password_required=true` 时映射到盈立官方 body 字段 `password` |
| 是否强制委托 | `forceEntrustFlag` | 默认不启用 |
| 交易阶段 | `sessionType` | 默认不传或正常交易 |

市场映射：

| 内部市场 | `exchangeType` | 第一版策略 |
|---|---|---|
| `HK` | `0` | 可作为港股只读候选；港股新股暗盘仅保留设计，不进入第一版真实交易 |
| `US` | `5` | 主要交易市场；第一版普通真实交易只允许美股盘中限价单 |
| `SH_HK_CONNECT` | `6` | 第一版不启用真实交易 |
| `SZ_HK_CONNECT` | `7` | 第一版不启用真实交易 |
| `ALL` | `100` | 仅查询接口使用，不允许下单 |

订单方向映射：

| 内部方向 | `entrustType` |
|---|---|
| `buy` | `0` |
| `sell` | `1` |

普通下单请求里的委托属性映射：

| `entrustProp` | 官方含义 | 第一版策略 |
|---|---|---|
| `0` | 美股限价单 / 暗盘委托 limit order | 用户已确认第一版只作为美股盘中普通限价单启用；港股暗盘仅保留设计 |
| `d` | 竞价单 | 默认不启用 |
| `e` | 增强限价单 | 第一批不启用；后续港股普通交易候选 |
| `g` | 竞价限价单 | 默认不启用 |
| `w` | 市价单 | 网页版文档新增；第一批不启用 |

`h`、`j` 出现在今日订单、历史订单或订单明细等查询响应字段说明中，不在普通下单请求字段表中。`u` 出现在最大可买可卖数量接口的 `entrustProp` 参数说明中，不在碎股下单 `/stock-order-server/open-api/odd-entrust` 的请求体中。第一版 request builder 不得把 `h`、`j`、`u` 发送到普通下单接口。

交易阶段 `sessionType`：

| `sessionType` | 官方含义 | 第一版策略 |
|---|---|---|
| `0` / 不传 | 正常订单交易，默认值 | 用户已确认第一版用于美股盘中普通限价单；request builder 可按官方要求传 `0` 或省略 |
| `1` | 盘前交易 | 不进第一批实现 |
| `2` | 盘后交易 | 不进第一批实现 |
| `3` | 暗盘交易 | 港股新股暗盘仅保留设计，不进第一批实现 |
| `12` | 基金订单 | 网页版文档新增；不进第一批实现 |

`OrderType.MARKET`、`forceEntrustFlag=true`、未建模的高级订单默认拒绝。第一批普通真实下单只允许美股盘中限价单：`exchangeType=5`、`entrustProp=0`、`entrustType` 买入 `0` / 卖出 `1`、`entrustPrice>0`、`sessionType=0` 或不传。任一字段映射不确定时，真实交易必须阻断为 `broker.unsupported_order_type` 或 `unknown_by_official_doc`。第一批交易实现目标还包含美股碎股；美股碎股使用碎股专用 endpoint，不通过普通下单 `entrustProp=u` 建模。港股新股暗盘只保留设计，不实现真实请求构造。

网页版普通下单还包含 `orderType`、`validDate`、`exchange` 可选字段；第一批 request builder 不发送这些字段，后续如支持 AMO/LOO 或指定交易所再单独建模。

响应处理目标：

| uSmart 响应字段 | 内部字段 | 说明 |
|---|---|---|
| `code` | `broker_response_code` | 业务状态码 |
| `msg` | `broker_message` | 脱敏后消息 |
| `data.entrustId` | `broker_order_id` | 官方网页说明可用于查询订单、修改订单、取消订单 |
| `data.status` | `broker_status_raw` | 普通订单状态码，枚举见 12.1 |
| `data.statusName` | `broker_status_name_raw` | 状态名摘要，日志需脱敏 |

- `code=0` 且存在 `data.entrustId` 时，才能认为券商返回了可追踪订单号。
- `code=0` 但缺少 `entrustId` 时，进入 `unknown_response`，内部状态为 `unknown`。
- HTTP 2xx 不等于业务成功，必须同时检查业务 `code`。

安全规则：

- 默认 `read_only` 下，`TradingGateway.place_order` 直接返回/抛出 `broker.trading_disabled`，不会触达本方法。
- 未来即使允许调用，也必须由 OMS 发起，并携带 `order_id`、`risk_check_id`、`trace_id`。
- 下单 HTTP timeout、网络异常或未知响应时，内部订单进入 `unknown`，不得自动重试。
- 默认不启用 `forceEntrustFlag`。
- 美股为主要交易市场；第一批只做美股盘中交易和美股碎股。港股暗盘只保留设计，当前不实现真实请求构造；当前 `read_only` 阶段只构造 dry-run 请求，不真实提交。

### 8.1 美股碎股下单 API 设计

OpenAPI：

```text
POST /stock-order-server/open-api/odd-entrust
```

第一版策略：

- 用户已确认美股碎股买入和卖出都启用，`entrustType` 使用买入 `0`、卖出 `1`。
- 内部订单按委托金额建模，例如 `notional_amount`；不得让策略直接提交券商碎股股数字段。
- `entrustAmount` 是发送给券商的碎股数量，由 `notional_amount / limit_price` 换算得到，可为小数股数。
- 金额、价格和换算出的碎股数量内部使用 `Decimal`；HTTP JSON 边界按券商接受的 number 序列化，不在核心模型里使用二进制 `float`。
- `entrustPrice` 为限价，必须大于 0；市价碎股第一版不启用。
- `exchangeType` 只允许 `5`，即美股；港股碎股不做。
- 卖出碎股前必须从持仓或最大可卖查询拿到可卖碎股数量，并用换算后的 `entrustAmount` 做上限校验。
- 只读和申请材料截图阶段仍只允许 dry-run 构造，不触达真实碎股下单接口。

内部字段映射：

| 内部字段 | uSmart body 字段 | 第一版规则 |
|---|---|---|
| `request.notional_amount` / `request.limit_price` | `entrustAmount` | 小数股数，按金额除以限价换算 |
| `request.limit_price` | `entrustPrice` | 限价，必须大于 0 |
| `request.side` | `entrustType` | 买入 `0`，卖出 `1` |
| 固定值 | `exchangeType` | `5`，美股 |
| `request.symbol` | `stockCode` | 股票代码 |

## 9. 改单 API 设计

方法：

```python
class uSmartOpenApiTradingAdapter:
    def modify_order(self, request: BrokerModifyRequest) -> BrokerModifyAck:
        ...
```

OpenAPI：

```text
POST /stock-order-server/open-api/modify-order
```

官方网页交易 API 手册确认普通股票委托 `actionType=1` 表示改单。IPO 改撤单接口的 `actionType` 枚举不同，不能复用这里的映射。

内部字段映射：

| 内部字段 | uSmart body 字段 | 说明 |
|---|---|---|
| 固定值 | `actionType=1` | 改单 |
| `request.new_quantity` | `entrustAmount` | 新委托数量 |
| `request.broker_order_id` | `entrustId` | 原委托 ID |
| `request.new_limit_price` | `entrustPrice` | 新委托价格 |
| `trade_password_secret_ref` | 内部配置 | 交易密码 secret 引用；第一版 `trade_password_required=false`，默认不读取 |
| `tradePasswordEncrypted` | `uSmartTradeSensitiveFieldEncryptor` | RSA 加密后的交易密码；仅 `trade_password_required=true` 时映射到盈立官方 body 字段 `password` |
| 是否强制委托 | `forceEntrustFlag` | 默认不启用 |

响应处理目标：

| uSmart 响应字段 | 内部字段 | 说明 |
|---|---|---|
| `code` | `broker_response_code` | 业务状态码 |
| `msg` | `broker_message` | 脱敏后消息 |
| `data.entrustId` | `broker_apply_id` | 官方网页回应参数说明为“申请编号”；不得覆盖原始 `broker_order_id` |
| `data.status` | `broker_status_raw` | 普通订单状态码，`5` 表示等待改单 |
| `data.statusName` | `broker_status_name_raw` | 状态名摘要 |

改单前置校验：

- 如果接口可用，应先调用 `/stock-order-server/open-api/modified-range` 获取可改数量上下限。
- `new_quantity` 必须在可改范围内，`new_limit_price` 必须通过价格偏离和订单类型检查。
- 如果 `modified-range` 查询失败，不得继续提交真实改单。

安全规则：

- 默认 `read_only` 下，`TradingGateway.modify_order` 阻断，不触达 OpenAPI。
- 改单在 OMS 风险模型中按 cancel + replace 风险处理，即使券商接口名为 modify；改单后必须通过查询和对账确认最终订单状态。
- 改单 timeout 或未知响应进入 `unknown`，不得自动再次改单。
- 改单前必须确认本地 OMS 状态允许修改。

## 10. 撤单 API 设计

方法：

```python
class uSmartOpenApiTradingAdapter:
    def cancel_order(self, request: BrokerCancelRequest) -> BrokerCancelAck:
        ...
```

OpenAPI：

```text
POST /stock-order-server/open-api/modify-order
```

官方网页交易 API 手册确认普通股票委托 `actionType=0` 表示撤单。IPO 改撤单接口的 `actionType` 枚举不同，不能复用这里的映射。

内部字段映射：

| 内部字段 | uSmart body 字段 | 说明 |
|---|---|---|
| 固定值 | `actionType=0` | 撤单 |
| 固定值 | `entrustAmount=0` | 撤单时传 0 |
| `request.broker_order_id` | `entrustId` | 原委托 ID |
| 固定值 | `entrustPrice=0` | 撤单时传 0 |
| `trade_password_secret_ref` | 内部配置 | 交易密码 secret 引用；第一版 `trade_password_required=false`，默认不读取 |
| `tradePasswordEncrypted` | `uSmartTradeSensitiveFieldEncryptor` | RSA 加密后的交易密码；仅 `trade_password_required=true` 时映射到盈立官方 body 字段 `password` |

响应处理目标：

| uSmart 响应字段 | 内部字段 | 说明 |
|---|---|---|
| `code` | `broker_response_code` | 业务状态码 |
| `msg` | `broker_message` | 脱敏后消息 |
| `data.entrustId` | `broker_apply_id` | 官方网页回应参数说明为“申请编号”；不得覆盖原始 `broker_order_id` |
| `data.status` | `broker_status_raw` | 普通订单状态码，撤单申请后通常需查询确认最终状态 |
| `data.statusName` | `broker_status_name_raw` | 状态名摘要 |

安全规则：

- 默认 `read_only` 下，`TradingGateway.cancel_order` 阻断，不触达 OpenAPI。
- 撤单也属于真实交易行为，必须经过 OMS 状态检查。
- 撤单 timeout 或未知响应进入 `unknown`，不得自动重复撤单。
- 必须通过订单查询或对账确认最终状态。

## 11. 只读查询 API 设计

只读查询允许用于账户观察、风控辅助和对账，但仍需脱敏。

| 内部方法 | endpoint | 用途 |
|---|---|---|
| `query_today_orders` | `/stock-order-server/open-api/today-entrust` | 今日订单 |
| `query_history_orders` | `/stock-order-server/open-api/his-entrust` | 历史订单 |
| `query_order_detail` | `/stock-order-server/open-api/order-detail` | 订单明细 |
| `query_trades` | `/stock-order-server/open-api/stock-record` | 成交流水 |
| `get_positions` | `/stock-order-server/open-api/stock-holding` | 持仓 |
| `get_account` / `get_cash` | `/stock-order-server/open-api/stock-asset` | 资产和资金 |
| `query_trade_quantity` | `/stock-order-server/open-api/trade-quantity` | 最大可买可卖数量，风控辅助 |
| `query_modify_range` | `/stock-order-server/open-api/modified-range` | 改单范围，改单前校验 |

统一查询 DTO：

| DTO | 核心字段 | 说明 |
|---|---|---|
| `QueryOrderRequest` | `account_ref`、`market`、`broker_order_id`、`request_id`、`trace_id`、`page_num`、`page_size`、`start_date`、`end_date` | 查询今日、历史或单笔订单 |
| `QueryTradeRequest` | `account_ref`、`market`、`symbol`、`broker_order_id`、`start_date`、`end_date`、`page_num`、`page_size`、`request_id`、`trace_id` | 查询成交流水 |
| `PositionSnapshot` | `account_ref`、`market`、`symbol`、`quantity`、`available_quantity`、`frozen_quantity`、`odd_quantity`、`last_price`、`cost_price` | 持仓快照 |
| `CashSnapshot` | `account_ref`、`market`、`currency`、`asset`、`available_cash`、`withdrawable_cash`、`frozen_cash`、`on_way_cash` | 资金快照 |
| `BrokerOrderSnapshot` | `broker_order_id`、`market`、`symbol`、`side`、`quantity`、`filled_quantity`、`limit_price`、`avg_fill_price`、`status`、`broker_status_raw`、`final_state_flag` | 订单快照 |
| `BrokerTradeSnapshot` | `broker_trade_id`、`broker_order_id`、`market`、`symbol`、`side`、`quantity`、`price`、`amount`、`business_status`、`business_time` | 成交快照 |

官方网页字段映射：

| uSmart 字段 | 内部字段 | 来源 |
|---|---|---|
| `exchangeType` | `market` | 0 港股、5 美股、67 A 股、100 查询全部等；不同接口枚举不完全一致，必须按接口校验 |
| `stockCode` | `symbol` | 标的代码 |
| `stockName` | `name` | 标的名称，用户可见，不做主键 |
| `currentAmount` | `quantity` | 持仓数量 |
| `enableAmount` | `available_quantity` | 可卖数量 |
| `frozenAmount` | `frozen_quantity` | 冻结数量 |
| `oddAmount` | `odd_quantity` | 碎股数量 |
| `asset` | `asset` | 总资产，日志不得输出完整值 |
| `marketValue` | `market_value` | 持仓市值，日志不得输出完整值 |
| `enableBalance` | `available_cash` | 可用金额 |
| `withdrawBalance` | `withdrawable_cash` | 可取金额 |
| `frozenBalance` | `frozen_cash` | 冻结金额 |
| `onWayBalance` | `on_way_cash` | 在途资金 |
| `entrustId` | `broker_order_id` | 委托记录号 |
| `entrustType` | `side` 或成交类型 | 查询接口里可能包含买、卖、撤单、补单、改单等类型，不能简单复用下单方向枚举 |
| `orderStatus` / `status` | `broker_status_raw` | 原始状态码，必须经 mapper 转为 OMS 内部状态 |
| `finalStateFlag` | `final_state_flag` | 是否终态标识，官方字段说明为 `0` 非终态、`1` 终态，必须进入 OMS mapper |
| `businessAmount` | `filled_quantity` / `trade_quantity` | 成交数量 |
| `businessAveragePrice` / `businessPrice` | `avg_fill_price` / `trade_price` | 成交均价或成交价 |
| `businessBalance` | `trade_amount` | 成交金额 |
| `businessStatus` | `trade_status_raw` | 1 成交成功、2 成交取消 |

规则：

- 只读查询可以在 `read_only` 模式下触达 OpenAPI。
- 第一批只读联调允许真实登录、资产查询、持仓查询、今日订单、历史订单、订单明细和成交流水；不允许 `trade-login`、下单、改单、撤单、IPO 申购、IPO 改单。
- 申请材料截图不做真实登录；截图只展示 dry-run 请求构造、签名边界、脱敏和交易阻断。
- 只读联调启用前必须显式配置 `allow_real_http_readonly=true`、base URL、IP 白名单、渠道号和密钥路径；缺任一项只能 dry-run。
- 真实登录 token 只保存在进程内存；除非后续单独设计加密会话缓存，不落盘。
- 第一版只维护单账户单 session；真实登录成功会替换该账户现有内存 session，并记录脱敏 token 指纹和过期时间。
- 只读查询遇到登录态过期可以显式重新登录；重新登录后的查询必须使用新的 `request_id`，不能复用失败请求的审计 ID。
- 交易动作遇到登录态过期、401 或权限错误时立即停止，不隐式刷新 token，不自动续发下单、改单或撤单。
- 查询结果可以在控制台显示整理后的完整结果，例如自然语言账户摘要、持仓表、订单表和成交表；禁止直接输出券商原始 JSON。
- 普通日志可以保留相对完整的结构化字段：endpoint、request_id、trace_id、账户引用、查询类型、分页参数、响应 code、耗时、字段名、整理后结果摘要和 `raw_hash`；不得记录 token、密码、私钥、完整手机号或券商原始 JSON。
- 程序查询存储可以保留券商返回的原始结构化字段，用于后续 mapper、对账和问题定位；存储记录必须标记账户引用、endpoint、request_id、schema_version 和 `raw_hash`。
- 真实资金、持仓市值、订单明细和成交明细可以进入本地只读联调审计日志；审计日志可保留原始结构化字段和整理后结构化记录，但不保存原始 JSON 文本或 HTTP response 全文。
- 本地只读联调审计日志保留 30 个交易日。
- 查询失败可以按限流策略做有限重试，默认最多 2 次退避；交易动作不自动重试。
- 对账和风控只能使用结构化结果，不直接传播券商原始响应。
- 查询接口分页按官方网页手册处理：`pageNum` 当前页从 1 开始，默认值 1；`pageSize` 每页结果数默认 10，最大 20；不得无限翻页。
- 多市场 `exchangeType=100` 只允许用于查询，不允许流入下单请求。
- 只读查询结果可以用于风控辅助，但不能替代对账状态；对账异常时必须暂停相关自动交易。
- 第一版只做单账户只读联调，不启用批量资产和多账户聚合查询。

## 12. 错误处理

错误分类：

| 类型 | 示例 | 处理 |
|---|---|---|
| `transport_error` | DNS、TLS、connect timeout、read timeout | 交易动作进入 `unknown`，查询可有限重试 |
| `http_error` | 401、403、404、5xx | 映射 gateway 错误码，记录脱敏摘要 |
| `auth_error` | token 失效、签名失败、IP 白名单拒绝 | 停止交易动作，提示人工检查 |
| `trade_locked` | 需要交易密码、交易解锁或账户交易锁定 | 映射 `broker.trade_locked`，订单置为 `blocked_by_broker_trade_lock`，提示人工确认 |
| `rate_limited` | 频率限制 | 查询退避重试，交易不自动补偿 |
| `business_reject` | 资金不足、数量错误、市场规则拒绝 | 保留券商 raw code/msg，并映射 gateway 错误码 |
| `unknown_response` | 缺少订单号、状态码未知、响应结构不匹配 | 进入 `unknown_by_official_doc` 或 `unknown` |

交易动作统一原则：

- 下单、改单、撤单不做自动重试。
- HTTP timeout 不等于券商未收到请求。
- `unknown` 状态必须通过订单查询、成交查询、对账或人工确认转出。

### 12.1 状态映射初稿

普通订单 `status` 已在交易 API 手册资料字典 `5.1 訂單狀態（Status）` 中给出。今日订单、历史订单和订单详情中的 `status` / `orderStatus` 必须进入 OMS 状态 mapper；没有列出的状态码一律映射为 `unknown_by_official_doc`，并保留原始状态摘要供人工确认。

| 来源字段 | 官方值 | 官方状态名 | 内部建议状态 | 说明 |
|---|---|---|---|---|
| 普通订单 `status` | `-1` | 失败 | `broker_rejected` | 失败原因取 `msg` 或后续查询 |
| 普通订单 `status` | `0` | 全部成交 | `filled` | 订单终态候选，仍需结合成交和对账 |
| 普通订单 `status` | `1` | 等待提交 | `submitted` | 尚非终态 |
| 普通订单 `status` | `2` | 待成交 | `accepted` | 尚非终态 |
| 普通订单 `status` | `3` | 部分成交 | `partial_filled` | 尚非终态 |
| 普通订单 `status` | `4` | 等待撤单 | `cancel_pending` | 撤单申请中，尚非终态 |
| 普通订单 `status` | `5` | 等待改单 | `modify_pending` | 改单申请中，尚非终态 |
| 普通订单 `status` | `6` | 已撤单 | `cancelled` | 订单终态候选 |
| 普通订单 `status` | `7` | 部成撤单 | `partial_cancelled` | 部分成交后撤单，终态候选 |
| 普通订单 `status` | `8` | 废单 | `broker_rejected` | 订单终态候选 |
| 订单明细 `orderStatus` | `11` | 委托下单 | `submitted` 或 `accepted` 待官方枚举确认 | 示例历史节点 |
| 订单明细 `orderStatus` | `21` | 改单（最新订单） | `accepted` 或 `unknown` 待官方枚举确认 | 示例历史节点 |
| 订单明细 `orderStatus` | `0` | 全部成交（订单结束） | `filled` | 示例显示为最终成交 |
| 成交流水 `businessStatus` | `1` | 成交成功 | `filled_event` | 成交流水事件，不直接作为订单总状态 |
| 成交流水 `businessStatus` | `2` | 成交取消 | `trade_cancelled_event` | 成交流水事件，不直接作为订单总状态 |

状态映射规则：

- 下单、改单、撤单响应里的 `status` 只能表示本次申请状态，不能单独作为最终订单状态。
- 订单最终状态以订单明细、今日/历史订单、成交流水和对账综合确认。
- `finalStateFlag` 是券商返回的终态标识，官方字段说明为 `0` 非终态、`1` 终态；它必须进入 OMS mapper，但不能脱离 `status` / `orderStatus` 单独决定 OMS 终态。
- `finalStateFlag=1` 且 `status` / `orderStatus` 映射为已成交、已撤、废单、失败等终态时，OMS 可标记本地订单终态。
- `finalStateFlag=0` 时，不得把订单标记为终态。
- `finalStateFlag` 与 `status` / `orderStatus` 冲突、缺失或出现未知值时，订单进入 `unknown_by_official_doc`，需要人工或后续查询确认。
- `orderStatus` 是订单明细历史节点状态，必须进入 OMS mapper；完整枚举未覆盖前，未知值进入 `unknown_by_official_doc`。
- 任意状态名文本只能做审计辅助，不能作为唯一状态判断依据。

## 13. 配置和密钥

`.env` 或本地密钥配置示例，禁止进入 Git：

```text
USMART_API_BASE_URL=...
USMART_QUOTE_BASE_URL=https://open-hz.yxzq.com/quotes-openservice/api/v1
USMART_WS_URL=wss://open-hz.yxzq.com/wss/v1
USMART_CHANNEL_ID=...
USMART_ACCOUNT_REF=...
USMART_SIGN_PRIVATE_KEY_PATH=...
USMART_SIGN_VERIFY_PUBLIC_KEY_PATH=...
USMART_SENSITIVE_KEY_PATH=...
USMART_LOGIN_AREA_CODE=...
USMART_LOGIN_PHONE=...
USMART_LOGIN_PASSWORD_SECRET_REF=...
USMART_TRADE_PASSWORD_SECRET_REF=...
```

进入 Git 的 YAML 只允许放非敏感开关：

```yaml
broker: usmart
mode: read_only
trading_enabled: false

transport:
  connect_timeout_ms: 3000
  read_timeout_ms: 5000

headers:
  x_lang: "1"
  x_dt: "4"
  x_type: "1"
  x_time_format: epoch_ms
  x_time_type: string

sign:
  key_ref: USMART_SIGN_PRIVATE_KEY_PATH
  urlsafe_base64_strip_padding: false

sensitive_encrypt:
  key_ref: USMART_SENSITIVE_KEY_PATH
  key_role: public
  padding: unknown_by_official

capabilities:
  login: true
  trade_status_query: true
  account_query: true
  position_query: true
  order_query: true
  trade_query: true
  trade_quantity_query: true
  modify_range_query: true
  place_order: false
  modify_order: false
  cancel_order: false
  odd_lot_order: false
  grey_market_order: false
  ipo: false
  prepost_market: false
  allow_real_http_readonly: false

request_id:
  header_length: 30
  serial_no_length: 19
  generator: snowflake_or_compatible

safety:
  block_trade_login_in_read_only: true
  block_force_entrust: true
  block_unknown_session_type: true
  block_ipo_endpoints: true
  require_query_before_unknown_resolution: true
```

## 14. 日志和审计

允许记录：

- `trace_id`
- `order_id`
- `request_id`
- endpoint
- HTTP 状态码
- 券商业务错误码
- 耗时
- 脱敏账户引用
- 响应摘要哈希

错误码分两层处理：

- 券商 raw code catalog：从官方网页手册按接口提取响应状态，保留原始 `code`、`msg`、endpoint、接口族和手册来源；每个接口只处理自己 `response_statuses` 下列出的状态码。
- Gateway error code：RobustQuant 自己的稳定错误码，供 OMS、风控、CLI/API 调用方使用；不能把券商 raw code 直接泄露成内部控制流。

禁止记录：

- API Key、Secret、私钥。
- 登录密码、交易密码、验证码。
- token、session、cookie。
- 完整手机号、完整账号。
- 真实完整资金余额、真实完整持仓市值。
- 完整 OpenAPI 原始响应。

关键审计事件：

| 事件 | 说明 |
|---|---|
| `usmart.login_requested` | 发起登录 |
| `usmart.login_completed` | 登录完成 |
| `usmart.request_signed` | 请求签名完成，只记录 request_id |
| `usmart.http_request_completed` | HTTP 请求完成 |
| `usmart.place_order_blocked` | 下单被 `TradingGateway` 阻断 |
| `usmart.modify_order_blocked` | 改单被 `TradingGateway` 阻断 |
| `usmart.cancel_order_blocked` | 撤单被 `TradingGateway` 阻断 |
| `usmart.order_unknown` | 订单动作状态未知 |

## 15. 测试和验收

离线测试：

- `TradingGateway` 在 `read_only` 模式下阻断下单、改单、撤单。
- 被阻断时，`uSmartTradeOpenApiClient` 不应收到调用。
- `uSmartOpenApiTradingAdapter` 能按官方网页字段构造登录、下单、改单、撤单请求体。
- 下单请求体必须包含 `serialNo`、`entrustAmount`、`entrustPrice`、`entrustProp`、`entrustType`、`exchangeType`、`stockCode`。
- 美股碎股下单请求体必须包含 `entrustAmount`、`entrustPrice`、`entrustType`、`exchangeType=5`、`stockCode`，并验证 `entrustAmount` 来源于内部金额模型的 Decimal 换算。
- 改单请求体必须包含 `actionType=1`、`entrustAmount`、`entrustId`、`entrustPrice`。
- 撤单请求体必须包含 `actionType=0`、`entrustAmount=0`、`entrustId`、`entrustPrice=0`。
- 只读查询 DTO 能映射 `stock-asset`、`stock-holding`、`today-entrust`、`his-entrust`、`order-detail`、`stock-record` 的脱敏响应。
- `uSmartTradeAuthSigner` 使用固定测试 key 生成可重复签名。
- 日志脱敏测试确认不输出 token、密码、私钥、完整账号。
- 对官方示例状态 `1`、`5`、`11`、`21`、`0` 建立 mapper 单元测试；未识别状态必须进入 `unknown_by_official_doc`。
- 对 `X-Request-Id` 和 `serialNo` 生成、长度校验、审计映射建立单元测试。
- 对分页请求建立契约测试：默认 `pageNum=1`、默认 `pageSize=10`、最大 `pageSize=20`。
- 对券商错误码建立 catalog 生成或校验测试：官方网页手册中的响应状态必须按 endpoint 分组进入 raw code catalog，并映射到 gateway 错误码或 `broker.unclassified`。

只读联调测试：

- 只允许真实登录、资产查询、持仓查询、今日订单、历史订单、订单明细和成交流水。
- 不允许 `trade-login`；遇到需要交易密码或交易解锁时进入人工确认，不自动补交交易密码。
- 不允许触达下单、改单、撤单 endpoint。
- 不允许触达 IPO 申购、IPO 改单 endpoint。
- 申请材料截图路径必须保持 dry-run，不做真实登录。
- 控制台允许显示整理后的完整只读结果，优先用自然语言摘要和表格；不得显示原始 JSON、token、密码、私钥、完整手机号。
- 本地只读联调审计日志保留 30 个交易日，并覆盖账户、持仓、订单、成交的原始结构化字段和整理后结构化结果。

受控实盘前测试：

- 网页手册已给出 UAT 测试地址 `http://open-jy-uat.yxzq.com`。
- 项目策略已确认：不自动把 UAT 当作可交易 sandbox。
- 只有盈立明确确认 UAT 下单、改单、撤单不会产生真实委托后，才允许在 UAT 调用交易动作；确认前只允许真实登录和只读查询，交易动作继续 dry-run。
- 交易接口必须经过 OMS、风控、交易时间、白名单和策略授权；第一版只允许现金账户正股多头交易，`TradingGateway` 只承接正股买入卖出执行，止盈止损由策略模块产生普通交易意图；不启用自动对冲、做空、融资融券、保证金交易或美股期权。

## 16. 待确认问题

需要从官方网页文档或 uSmart 官方确认：

- 交易 API base URL：官方网页和 Python demo 给出生产 `https://open-jy.yxzq.com`、测试 `http://open-jy-uat.yxzq.com`；实现仍必须通过 `USMART_API_BASE_URL` 配置显式选择，默认 dry-run 不出网，真实出网需申请通过、IP 白名单、渠道号和密钥配置。
- 项目策略已确认：UAT 测试地址不自动等同 sandbox / paper trading；是否保证下单、改单、撤单不产生真实委托仍需券商确认。
- `X-Request-Id` 重复请求返回语义。
- `X-Sign` 输出编码默认跟随官方 Python demo 使用标准 Base64，并通过配置允许切换 URL-safe Base64 和 padding；签名输入已确认只使用稳定 JSON body，不拼接 header 字段。
- 隐私资料加密按官方 Python demo 的 `rsa_encrypt` transform 实现：RSA `PKCS1_v1_5` 加密后 URL-safe Base64。仍需确认券商最终下发密钥材料与 demo `public_key` / `private_key` 配置槽位的对应关系；密钥材料已确认必须与 `X-Sign` 渠道签名密钥分离。
- token `expiration` 的精确格式、时区和官方刷新接口语义；同一账户在其他客户端登录时的冲突语义。
- IPO 改撤单接口的 `actionType` 枚举与普通股票委托不同，后续如接入 IPO 必须单独建模。
- 券商内部改单是原生修改还是券商侧 cancel + replace；本地 OMS 风险模型按 cancel + replace 处理。
- 订单明细 `orderStatus` 历史节点的完整枚举；已确认必须进入 OMS mapper，未知值进入 `unknown_by_official_doc`。
- 券商错误码完整枚举提取；项目策略已确认必须有完整 raw code catalog 和独立 gateway 错误码层。
- 美股碎股 `/odd-entrust` 的最小金额、最小股数、数量精度、订单状态和撤单细节；港股暗盘相关规则保留为后续设计项。
- 频率限制、IP 白名单生效规则。

## 17. 后续实现顺序

正式编码时按以下顺序推进，避免先写真实 transport 后才补安全边界：

1. 补齐交易开放 API 离线 DTO、枚举和 mapper：账户、资金、持仓、订单、成交、错误响应、状态响应。行情 DTO 属于 `quotation_kernel`，不在本文档实现。
2. 补齐 `CapabilityGuard` 的交易开放 API 只读能力判断：登录、交易状态查询、账户查询、持仓查询、订单查询、成交查询独立开关；`trade-login`、下单、改单、撤单仍默认阻断。
3. 实现 `uSmartRequestIdPolicy`、`uSmartTradeSensitiveFieldEncryptor`、`uSmartTradeAuthSigner` 的离线单元测试，不接真实账号。
4. 实现 dry-run adapter 的官方网页字段请求体构造，契约测试只断言字段和脱敏，不出网。
5. 实现 `uSmartMapper`，用官方示例和人工脱敏 fixture 覆盖成功、业务拒绝、未知状态、缺失字段。
6. 实现真实 HTTP transport，但默认配置仍为 `dry_run=true` 或 `mode=read_only`；没有用户明确配置时不能出网。
7. 用户已确认允许只读查询联调；实现时只开放真实登录、资产查询、持仓查询、今日订单、历史订单、订单明细、成交流水和行情查询，禁止 `trade-login` 和所有交易动作。申请材料截图仍不做真实登录。
8. 只有盈立明确确认 UAT / sandbox 不会产生真实委托时，才进入下单、改单、撤单链路验证；否则停在离线契约测试、真实登录和只读联调。
