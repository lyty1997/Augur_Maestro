# uSmart OpenAPI 调用栈全链路设计

版本：v0.1  
状态：设计草案，待用户确认  
最后更新：2026-05-19

## 0. 文档定位

本文档说明 RobustQuant 中“从本地入口到实际调用 uSmart OpenAPI server”的全链路代码层设计。它回答券商审核最关心的几个问题：

- 从 CLI / Web / 本地服务到 uSmart OpenAPI server，中间经过哪些层。
- 哪一层代码会发起到 uSmart OpenAPI 的 HTTP 请求。
- 登录、下单、改单、撤单分别调用哪些 endpoint。
- 请求 header、签名、`X-Request-Id`、token 如何生成和传递。
- 交易动作如何先经过 `TradingGateway` 安全门控。
- 日志和错误处理如何避免泄露账号、密码、token、密钥和真实资金隐私。

本文档是 [broker-trading-gateway.md](../trading/broker-trading-gateway.md) 的下层专项设计。`TradingGateway` 是统一交易安全门面；本文档描述从本地入口、应用服务、`TradingGateway`、`uSmartOpenApiTradingAdapter`、`uSmartOpenApiClient`、`uSmartAuthSigner`、HTTP transport 到 uSmart OpenAPI server 的完整调用栈。

登录、下单、改单、撤单四条链路的接口级 API 手册、输入输出、上下调用层和当前设计缺口见 [usmart-openapi-api-manual.md](usmart-openapi-api-manual.md)。

## 1. 调用链路

RobustQuant 本地系统与 uSmart OpenAPI 是 client-server 架构：

```mermaid
sequenceDiagram
    participant UI as CLI / Web / 任务
    participant App as RobustQuant 应用服务
    participant TG as TradingGateway
    participant AD as uSmartOpenApiTradingAdapter
    participant CL as uSmartOpenApiClient
    participant SG as uSmartAuthSigner
    participant HTTP as HTTP Transport
    participant API as uSmart OpenAPI Server

    UI->>App: 发起登录或订单动作
    App->>TG: 调用统一交易接口
    TG->>TG: 检查 mode / trading_enabled / capability
    alt 只读安全模式下的交易动作
        TG-->>App: broker.trading_disabled
    else 允许的只读动作或未来受控实盘动作
        TG->>AD: 调用适配器方法
        AD->>CL: 构造 endpoint + body
        CL->>SG: 生成 Authorization / X-Sign / X-Request-Id 等 header
        CL->>HTTP: POST JSON 请求
        HTTP->>API: HTTPS 调用 uSmart OpenAPI
        API-->>HTTP: OpenAPI 响应
        HTTP-->>CL: HTTP response
        CL-->>AD: 标准化原始响应摘要
        AD-->>TG: 映射为内部 DTO
        TG-->>App: 返回业务结果
    end
```

当前实现阶段：

- `TradingGateway` 已实现默认 `read_only` 交易阻断。
- `uSmartOpenApiTradingAdapter` 已保留登录、下单、改单、撤单方法外形；当前代码里的请求体仍是 dry-run 骨架，尚未按 PDF 字段完整映射。
- `uSmartOpenApiClient` 当前为 dry-run 外壳，不发真实 HTTP。
- `uSmartAuthSigner`、真实 HTTP transport、token 生命周期管理尚未实现。
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
| L6 | `uSmartOpenApiTradingAdapter` | 内部 DTO 与 uSmart endpoint/body 字段转换 | 是 | 否 |
| L7 | `uSmartOpenApiClient` | 生成 JSON、调用 signer、调用 HTTP transport、解析响应 | 是 | 否 |
| L8 | `uSmartAuthSigner` | 生成 `X-Sign`、`X-Request-Id`、认证 header | 是 | 否 |
| L9 | `uSmartHttpTransport` | 真实 HTTPS POST，处理 HTTP 状态和 timeout | 是 | 否 |
| L10 | uSmart OpenAPI Server | 券商服务端，处理登录、查询、委托、改单、撤单 | 是 | 券商侧执行 |

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
  -> uSmartOpenApiClient.post('/user-server/open-api/login')
  -> uSmartAuthSigner.build_headers
  -> uSmartHttpTransport.post_json
  -> uSmart OpenAPI Server
```

只读查询链路：

```text
CLI/FastAPI
  -> QueryService
  -> TradingGateway.get_positions / query_order / query_trades
  -> uSmartOpenApiTradingAdapter
  -> uSmartOpenApiClient
  -> uSmart OpenAPI Server
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
  -> 风控通过 + 交易时间通过 + 白名单通过 + 人工确认通过
  -> TradingGateway 允许
  -> uSmartOpenApiTradingAdapter
  -> uSmartOpenApiClient
  -> uSmartAuthSigner
  -> uSmartHttpTransport
  -> uSmart OpenAPI Server
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
uSmart 原始响应
  -> uSmartOpenApiResponse 脱敏摘要
  -> BrokerOrderAck / BrokerModifyAck / BrokerCancelAck
  -> OMS 状态
  -> ApplicationService 响应 DTO
  -> CLI/FastAPI 用户可见结果
```

禁止把 uSmart 原始响应直接返回给 CLI、Web 或报告。

### 1.4 本地 server 与券商 server 的关系

RobustQuant 后续可能有自己的 FastAPI server。它和 uSmart OpenAPI server 是两个不同角色：

| Server | 归属 | 作用 |
|---|---|---|
| RobustQuant FastAPI server | 本地系统 | 给 Web/CLI/任务提供本地接口，调用 `TradingGateway` |
| uSmart OpenAPI server | 券商 | 接收 HTTPS OpenAPI 请求，处理登录、查询、委托、改单、撤单 |

本地 FastAPI server 不直接拼接 uSmart 请求，也不保存私钥和 token 原文。真正与 uSmart server 通信的是 `uSmartOpenApiClient` + `uSmartHttpTransport`。

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
        client.py                   uSmartOpenApiClient
        auth.py                     uSmartAuthSigner
        transport.py                uSmartHttpTransport
        endpoints.py                endpoint 常量
        mapper.py                   OpenAPI 响应与内部 DTO 映射
        rate_limit.py               OpenAPI 频率限制
```

职责边界：

| 模块 | 职责 | 禁止事项 |
|---|---|---|
| `TradingGateway` | 检查能力模式、交易开关、调用来源，决定是否允许触达适配器 | 不拼接 uSmart 字段，不保存 token |
| `uSmartOpenApiTradingAdapter` | 将内部 DTO 转为 uSmart endpoint 和 body | 不绕过 `TradingGateway`，不自行决定真实交易是否允许 |
| `uSmartOpenApiClient` | 组织 header、签名、HTTP POST、响应解析 | 不包含策略、风控、OMS 逻辑 |
| `uSmartAuthSigner` | 生成 `X-Sign`、`X-Request-Id`、时间戳、认证 header | 不把私钥、密码、token 写入日志 |
| `uSmartHttpTransport` | 发起 HTTPS 请求、处理 timeout 和 HTTP 状态 | 不对下单/改单/撤单做自动重试 |
| `uSmartMapper` | 映射状态码、错误码、订单号和响应字段 | 不猜测 PDF 未说明的状态 |

## 3. Endpoint 范围

第一版只覆盖券商申请、只读联调、对账和交易网关最小闭环需要的接口。字段以官方 PDF 为准；本文只记录当前设计映射。

### 3.1 交易 API endpoint 分组

| 能力 | 方法 | endpoint | 当前允许触达 OpenAPI |
|---|---|---|---|
| 渠道密码登录 | POST | `/user-server/open-api/login` | 只读联调阶段可允许 |
| 渠道验证码登录 | POST | `/user-server/open-api/loginCaptcha` | 第一版不主动实现，保留扩展 |
| 获取手机验证码 | POST | `/user-server/open-api/send-phone-captcha` | 第一版不主动实现，避免短信验证码自动化 |
| 获取交易解锁状态 | POST | `/user-server/open-api/get-trade-status` | 只读联调阶段可允许 |
| 普通下单 | POST | `/stock-order-server/open-api/entrust-order` | 默认禁止，需 `live_guarded` |
| 委托改单 | POST | `/stock-order-server/open-api/modify-order` | 默认禁止，需 `live_guarded` |
| 委托撤单 | POST | `/stock-order-server/open-api/modify-order` | 默认禁止，需 `live_guarded` |
| 改单范围查询 | POST | `/stock-order-server/open-api/modified-range` | 只读联调阶段可允许，用于改单前校验 |
| 最大可买可卖数量 | POST | `/stock-order-server/open-api/trade-quantity` | 只读联调阶段可允许，用于风控辅助 |
| 今日订单查询 | POST | `/stock-order-server/open-api/today-entrust` | 只读联调阶段可允许 |
| 历史订单查询 | POST | `/stock-order-server/open-api/his-entrust` | 只读联调阶段可允许 |
| 订单明细查询 | POST | `/stock-order-server/open-api/order-detail` | 只读联调阶段可允许 |
| 成交流水查询 | POST | `/stock-order-server/open-api/stock-record` | 只读联调阶段可允许 |
| 持仓查询 | POST | `/stock-order-server/open-api/stock-holding` | 只读联调阶段可允许 |
| 资产查询 | POST | `/stock-order-server/open-api/stock-asset` | 只读联调阶段可允许 |
| 客户股票资产批量查询 | POST | `/stock-order-server/open-api/stock-asset-list` | 第一版可作为多账户只读扩展，不进入最小闭环 |
| 聚合资产查询 | POST | `/aggregation-server/open-api/user-asset-aggregation/v1` | 第一版可作为统一资产视图候选，不进入最小闭环 |
| 查询汇率 | POST | `/stock-capital-server/open-api/currency-exchange-info` | 第一版可作为多币种估值辅助，不进入交易决策硬依赖 |

不进入第一版：

- 修改、重置登录密码或交易密码。
- 交易解锁 `trade-login`。
- IPO 申购和 IPO 改单。
- 碎股下单和碎股撤单。
- 盘前盘后交易。
- 条件单、止盈止损、触发单。

`trade-login` 不是下单接口，但可能改变账户交易可用状态，因此不作为只读联调接口。

### 3.2 行情 API endpoint 分组

行情接口不挂在 `TradingGateway` 上，由 `QuotationDataGateway` 和后续 `uSmartQuotationAdapter` 承接。行情只读联调允许独立启用，但行情失败、延迟或权限不足时，未来实盘交易必须进入降级或暂停。

| 能力 | 方法 | endpoint / 入口 | 第一版用途 |
|---|---|---|---|
| 市场状态 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/marketstate` | 交易时间和市场状态参考 |
| 基础信息 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/basicinfo` | 标的信息补充 |
| 即时报价 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/realtime` | 只读行情快照 |
| 分时 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/timeline` | 只读行情序列 |
| K 线 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/kline` | 研究和校验辅助 |
| 逐笔 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/tick` | 第一版暂不作为交易依据 |
| 买卖盘 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/orderbook` | 只读盘口 |
| 行情推送 | WS | `wss://open-hz.yxzq.com/wss/v1` | `auth`、`sub`、`unsub`、`update`、`ping`、`pong` |

WebSocket 推送第一版只允许恢复行情订阅，不允许在重连、订阅恢复或 `update` 回调中触发任何交易动作。

## 4. 请求 header 设计

根据 PDF 初步解析，交易接口请求 header 包含：

| Header | 来源 | 说明 |
|---|---|---|
| `Authorization` | 登录后 token | 登录接口以外的交易和查询接口需要 |
| `Content-Type` | 固定 | `application/json; charset=utf-8` |
| `X-Lang` | 配置 | 语言类别，例如 `1` 表示简体 |
| `X-Channel` | uSmart 分配 | 渠道 ID |
| `X-Time` | 本地生成 | 时间戳或时间标记，格式以 PDF/券商确认为准 |
| `X-Dt` | 配置 | 设备类型，例如 Windows / Mac 等，具体值以 PDF 为准 |
| `X-Request-Id` | 本地生成 | 幂等防重 ID |
| `X-Sign` | `uSmartAuthSigner` 生成 | 对 body 内容签名/加密后的值 |

设计规则：

- `X-Request-Id` 必须由本地生成并写入订单审计记录。
- `X-Sign` 只由 `uSmartAuthSigner` 生成，其他模块不接触私钥。
- `Authorization` token 只保存在内存会话中，默认不落库。
- 日志只记录 header key 列表、`X-Request-Id` 和脱敏 token 摘要，不记录完整 token 或签名。
- `X-Type` 在交易 PDF 示例中出现，但字段含义和是否必填尚未从表格确认；第一版配置中保留 `x_type` 可选项，默认不猜值。
- `Content-Type` 统一由 client 注入，调用方不允许手工传入，避免签名 body 和实际 body 不一致。
- 同一请求的 header、body_json、endpoint 和 request_id 必须作为不可变对象进入签名流程，签名后不得再修改 body。

### 4.1 请求 ID 策略

PDF 中存在长度描述不一致：概述中 `X-Request-Id` 描述为 19 位数字，登录等接口章节又出现 30 位描述；下单 body 的 `serialNo` 明确为最长 19 位。设计上不猜测统一长度，先抽象为 `uSmartRequestIdPolicy`：

| 场景 | 字段 | 设计策略 |
|---|---|---|
| HTTP header 幂等 | `X-Request-Id` | 由 `RequestIdGenerator` 生成，长度按配置校验；默认标记为 `unknown_by_pdf`，正式联调前必须确认 |
| 下单 body 流水 | `serialNo` | 与本地 `broker_request_id` 建立映射，按 PDF 的最长 19 位约束处理 |
| 本地 OMS 订单 | `order_id` | RobustQuant 内部 ID，不直接暴露给券商 |
| 链路追踪 | `trace_id` | 可为 UUID/ULID，不参与券商幂等 |

映射关系：

```text
order_id -> broker_request_id -> X-Request-Id
broker_request_id -> serialNo
broker_order_id <- entrustId
```

规则：

- `broker_request_id` 必须在调用券商前持久化到审计记录；如果持久化失败，不允许触达 OpenAPI。
- 只读查询也要携带 `request_id`，但查询 request_id 不得复用交易 request_id。
- 交易请求超时后，不自动复用同一个 request_id 重发，也不生成新 request_id 补发。
- 如果券商对重复 `X-Request-Id` 的返回语义不清楚，统一标记为 `unknown_by_pdf`，不能依赖它做自动补偿。

## 5. 签名与认证设计

PDF 初步信息：

- 协议：HTTPS。
- 签名 header：`X-Sign`。
- 签名算法描述：`MD5withRSA`。
- 交易 API 概述描述签名内容为 Body 内容。
- 基础报价 API 描述签名原文为 `Authorization`、`X-Channel`、`X-Lang`、`X-Request-Id`、`X-Time` 头字段与 body 内容按序拼接。
- 编码方式：`safeBase64` / URL-safe Base64。
- 幂等字段：`X-Request-Id`。
- 访问控制：IP 白名单。

因此第一版不能把交易签名和行情签名硬编码成同一个实现，应拆成策略：

| 签名策略 | 适用范围 | 输入 |
|---|---|---|
| `TradeBodySignPolicy` | 交易开放 API | 稳定 JSON body，最终以交易 PDF/官方确认为准 |
| `QuoteHeaderBodySignPolicy` | 基础报价 HTTP API | `Authorization`、`X-Channel`、`X-Lang`、`X-Request-Id`、`X-Time`、body 的有序拼接 |
| `WebSocketAuthPolicy` | 报价推送 WebSocket | 以推送 PDF 的 `auth` 消息要求为准 |

目标接口：

```python
class uSmartAuthSigner:
    def build_headers(
        self,
        *,
        api_group: Literal["trade", "quote_http"],
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
2. 生成或接收 `X-Request-Id`。
3. 按 `api_group` 选择签名策略，生成签名前原文。
4. 对签名结果做 URL-safe Base64 编码，写入 `X-Sign`。
5. 组装 `Authorization`、`X-Lang`、`X-Channel`、`X-Time`、`X-Dt`、`X-Request-Id`、`X-Sign`。

隐私字段加密与签名分开处理：

- 登录手机号、登录密码、交易密码等字段使用 PDF 所说的“隐私资料加密公钥”，与 `X-Sign` 渠道私钥不是同一件事。
- `uSmartSensitiveFieldEncryptor` 负责加密 `phoneNumber`、`password`、交易密码等字段。
- `uSmartAuthSigner` 只负责请求签名，不接收明文密码和手机号。
- 明文敏感字段只能从本地密钥管理层读出后在内存中短暂存在，禁止进入 DTO、日志、异常消息和测试 fixture。

待确认项：

- `X-Time` 精确格式。
- `X-Dt` 可用枚举值。
- `X-Request-Id` 是 19 位还是 30 位，以最终 PDF/官方说明为准。
- `safeBase64` 是否需要去掉 padding。
- 登录密码、交易密码使用的 RSA 公钥是否与 `X-Sign` 私钥不同。
- 交易 API 的 `X-Sign` 是否仅签 body，还是也需要拼接 header 字段；基础报价 PDF 已写明 header+body 有序拼接，交易 PDF 当前摘录以 body 为主。

## 6. uSmartOpenApiClient 设计

目标接口：

```python
class uSmartOpenApiClient:
    def post(
        self,
        endpoint: str,
        body: dict[str, Any],
        *,
        api_group: Literal["trade", "quote_http"],
        trace_id: str,
        request_id: str,
        token_required: bool,
        operation_kind: Literal["readonly", "trade_action"],
    ) -> uSmartOpenApiResponse:
        ...
```

内部流程：

1. 校验 endpoint 是否在白名单常量中。
2. 生成稳定 body JSON。
3. 按 `api_group` 调用 `uSmartAuthSigner.build_headers(...)`。
4. 通过 `uSmartHttpTransport.post_json(...)` 发起 HTTPS 请求。
5. 解析 HTTP 状态码和 JSON 响应。
6. 生成脱敏响应摘要。
7. 返回 `uSmartOpenApiResponse` 给 adapter。

重试边界：

- `operation_kind="readonly"` 可以按 `RateLimiter` 和退避策略有限重试。
- `operation_kind="trade_action"` 不允许由 client 自动重试；timeout、连接中断、未知响应统一向上抛出可审计错误，由 OMS 进入 `unknown`。
- client 只能重试传输层未出网的只读请求；是否“未出网”不能确定时，按已可能触达券商处理。

`uSmartOpenApiResponse` 建议字段：

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

方法：

```python
class uSmartOpenApiTradingAdapter:
    def connect(self, account_ref: AccountRef | None = None) -> BrokerSession:
        ...
```

OpenAPI：

```text
POST /user-server/open-api/login
```

请求 body 设计：

| 字段 | 来源 | 说明 |
|---|---|---|
| `areaCode` | 配置 | 区号 |
| `phoneNumber` | 本地密钥配置 | PDF 登录接口字段，需使用隐私资料公钥 RSA 加密 |
| `password` | 本地密钥配置 | RSA 加密后的登录密码 |

响应处理：

- 成功后提取 token。
- 记录 token 过期时间 `expiration`，但不记录 token 原文。
- 读取 `tradePassword`、`openedAccount`、`extendStatusBit` 作为权限和账户状态摘要；仅保存脱敏布尔值或摘要，不保存完整用户资料。
- token 存入内存 `uSmartSession`。
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
| `request.limit_price` | `entrustPrice` | 委托价格，竞价单传 0 |
| `request.price_type` + `market` | `entrustProp` | 委托属性，枚举见下表 |
| `request.side` | `entrustType` | 0 买，1 卖 |
| `request.market` | `exchangeType` | 0 港股，5 美股，6 沪港通，7 深港通 |
| `request.symbol` | `stockCode` | 股票代码 |
| `request.name` | `stockName` | 可选 |
| 交易密码 | `password` | 可选，是否需要以官方要求为准 |
| 是否强制委托 | `forceEntrustFlag` | 默认不启用 |
| 交易阶段 | `sessionType` | 默认不传或正常交易 |

市场映射：

| 内部市场 | `exchangeType` | 第一版策略 |
|---|---|---|
| `HK` | `0` | 可作为港股只读和未来受控交易候选 |
| `US` | `5` | 可作为美股只读和未来受控交易候选 |
| `SH_HK_CONNECT` | `6` | 第一版不启用真实交易 |
| `SZ_HK_CONNECT` | `7` | 第一版不启用真实交易 |
| `ALL` | `100` | 仅查询接口使用，不允许下单 |

订单方向映射：

| 内部方向 | `entrustType` |
|---|---|
| `buy` | `0` |
| `sell` | `1` |

委托属性映射：

| `entrustProp` | PDF 含义 | 第一版策略 |
|---|---|---|
| `0` | 美股限价单 / 暗盘委托 limit order | 默认不启用暗盘；美股限价单需进一步确认 |
| `d` | 竞价单 | 默认不启用 |
| `e` | 增强限价单 | 港股第一版候选限价类型，需确认适用市场 |
| `g` | 竞价限价单 | 默认不启用 |
| `h` | 港股限价单 | 第一版候选限价类型，需确认与 `e` 的差异 |
| `j` | 特殊限价单 | 默认不启用 |
| `u` | 碎股单 | 不进入第一版 |

`OrderType.MARKET`、盘前盘后、暗盘、碎股和 `forceEntrustFlag=true` 默认全部拒绝。若后续需要支持，必须先更新风控和订单类型设计。

响应处理目标：

| uSmart 响应字段 | 内部字段 | 说明 |
|---|---|---|
| `code` | `broker_response_code` | 业务状态码 |
| `msg` | `broker_message` | 脱敏后消息 |
| `data.entrustId` | `broker_order_id` | PDF 说明可用于查询订单、修改订单、取消订单 |
| `data.status` | `broker_status_raw` | 状态码，完整枚举待确认 |
| `data.statusName` | `broker_status_name_raw` | 状态名摘要，日志需脱敏 |

- `code=0` 且存在 `data.entrustId` 时，才能认为券商返回了可追踪订单号。
- `code=0` 但缺少 `entrustId` 时，进入 `unknown_response`，内部状态为 `unknown`。
- HTTP 2xx 不等于业务成功，必须同时检查业务 `code`。

安全规则：

- 默认 `read_only` 下，`TradingGateway.place_order` 直接返回/抛出 `broker.trading_disabled`，不会触达本方法。
- 未来即使允许调用，也必须由 OMS 发起，并携带 `order_id`、`risk_check_id`、`trace_id`。
- 下单 HTTP timeout、网络异常或未知响应时，内部订单进入 `unknown`，不得自动重试。
- 默认不启用 `forceEntrustFlag`。
- 默认不支持盘前、盘后、暗盘，`sessionType` 不传或只允许正常交易。

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

PDF 初步显示 `actionType=1` 表示改单。

内部字段映射：

| 内部字段 | uSmart body 字段 | 说明 |
|---|---|---|
| 固定值 | `actionType=1` | 改单 |
| `request.new_quantity` | `entrustAmount` | 新委托数量 |
| `request.broker_order_id` | `entrustId` | 原委托 ID |
| `request.new_limit_price` | `entrustPrice` | 新委托价格 |
| 交易密码 | `password` | 可选，是否需要以官方要求为准 |
| 是否强制委托 | `forceEntrustFlag` | 默认不启用 |

响应处理目标：

| uSmart 响应字段 | 内部字段 | 说明 |
|---|---|---|
| `code` | `broker_response_code` | 业务状态码 |
| `msg` | `broker_message` | 脱敏后消息 |
| `data.entrustId` | `broker_order_id` | 改单申请编号或原委托 ID，需以 PDF/官方确认语义 |
| `data.status` | `broker_status_raw` | 示例中 `5` 为等待改单，但完整枚举待确认 |
| `data.statusName` | `broker_status_name_raw` | 状态名摘要 |

改单前置校验：

- 如果接口可用，应先调用 `/stock-order-server/open-api/modified-range` 获取可改数量上下限。
- `new_quantity` 必须在可改范围内，`new_limit_price` 必须通过价格偏离和订单类型检查。
- 如果 `modified-range` 查询失败，不得继续提交真实改单。

安全规则：

- 默认 `read_only` 下，`TradingGateway.modify_order` 阻断，不触达 OpenAPI。
- 改单语义必须确认：是原生 modify，还是 cancel + replace。
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

PDF 初步显示 `actionType=0` 表示撤单。

内部字段映射：

| 内部字段 | uSmart body 字段 | 说明 |
|---|---|---|
| 固定值 | `actionType=0` | 撤单 |
| 固定值 | `entrustAmount=0` | 撤单时传 0 |
| `request.broker_order_id` | `entrustId` | 原委托 ID |
| 固定值 | `entrustPrice=0` | 撤单时传 0 |
| 交易密码 | `password` | 可选，是否需要以官方要求为准 |

响应处理目标：

| uSmart 响应字段 | 内部字段 | 说明 |
|---|---|---|
| `code` | `broker_response_code` | 业务状态码 |
| `msg` | `broker_message` | 脱敏后消息 |
| `data.entrustId` | `broker_order_id` | 原委托 ID 或撤单申请编号，需以 PDF/官方确认语义 |
| `data.status` | `broker_status_raw` | 撤单状态码，完整枚举待确认 |
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

PDF 字段映射：

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
| `orderStatus` / `status` | `broker_status_raw` | 原始状态码，需经 mapper 转内部状态 |
| `finalStateFlag` | `final_state_flag` | 是否最终状态，语义需确认 |
| `businessAmount` | `filled_quantity` / `trade_quantity` | 成交数量 |
| `businessAveragePrice` / `businessPrice` | `avg_fill_price` / `trade_price` | 成交均价或成交价 |
| `businessBalance` | `trade_amount` | 成交金额 |
| `businessStatus` | `trade_status_raw` | 1 成交成功、2 成交取消 |

规则：

- 只读查询可以在 `read_only` 模式下触达 OpenAPI。
- 查询失败可以按限流策略做有限重试。
- 查询结果中的真实资金、持仓市值、完整账号不得写入普通日志。
- 对账和风控只能使用结构化结果，不直接传播券商原始响应。
- 查询接口分页必须显式传入 `page_num`、`page_size` 或使用配置默认值；不得无限翻页。
- 多市场 `exchangeType=100` 只允许用于查询，不允许流入下单请求。
- 只读查询结果可以用于风控辅助，但不能替代对账状态；对账异常时必须暂停相关自动交易。

## 12. 错误处理

错误分类：

| 类型 | 示例 | 处理 |
|---|---|---|
| `transport_error` | DNS、TLS、connect timeout、read timeout | 交易动作进入 `unknown`，查询可有限重试 |
| `http_error` | 401、403、404、5xx | 映射统一错误码，记录脱敏摘要 |
| `auth_error` | token 失效、签名失败、IP 白名单拒绝 | 停止交易动作，提示人工检查 |
| `rate_limited` | 频率限制 | 查询退避重试，交易不自动补偿 |
| `business_reject` | 资金不足、数量错误、市场规则拒绝 | 映射为 `broker_rejected` |
| `unknown_response` | 缺少订单号、状态码未知、响应结构不匹配 | 进入 `unknown_by_pdf` 或 `unknown` |

交易动作统一原则：

- 下单、改单、撤单不做自动重试。
- HTTP timeout 不等于券商未收到请求。
- `unknown` 状态必须通过订单查询、成交查询、对账或人工确认转出。

### 12.1 状态映射初稿

以下只来自当前 PDF 摘录和示例，不能视为完整枚举。没有列出的状态码一律映射为 `unknown_by_pdf`，并保留原始状态摘要供人工确认。

| 来源字段 | PDF 示例值 | PDF 示例状态名 | 内部建议状态 | 说明 |
|---|---|---|---|---|
| 下单响应 `data.status` | `1` | 等待提交 | `submitted` 或 `accepted` 待确认 | 是否已被券商/交易所接受需官方确认 |
| 改单响应 `data.status` | `5` | 等待改单 | `submitted` 或 `unknown` 待确认 | 只表示改单申请状态，不等同最终改单成功 |
| 订单明细 `orderStatus` | `11` | 委托下单 | `submitted` 或 `accepted` 待确认 | 示例历史节点 |
| 订单明细 `orderStatus` | `21` | 改单（最新订单） | `accepted` 或 `unknown` 待确认 | 示例历史节点 |
| 订单明细 `orderStatus` | `0` | 全部成交（订单结束） | `filled` | 示例显示为最终成交 |
| 成交流水 `businessStatus` | `1` | 成交成功 | `filled_event` | 成交流水事件，不直接作为订单总状态 |
| 成交流水 `businessStatus` | `2` | 成交取消 | `trade_cancelled_event` | 成交流水事件，不直接作为订单总状态 |

状态映射规则：

- 下单、改单、撤单响应里的 `status` 只能表示本次申请状态，不能单独作为最终订单状态。
- 订单最终状态以订单明细、今日/历史订单、成交流水和对账综合确认。
- `finalStateFlag` 若为最终状态标识，必须先确认枚举含义；未确认前不得用它自动结束 OMS 订单。
- 任意状态名文本只能做审计辅助，不能作为唯一状态判断依据。

## 13. 配置和密钥

`.env` 或本地密钥配置示例，禁止进入 Git：

```text
USMART_API_BASE_URL=...
USMART_QUOTE_BASE_URL=https://open-hz.yxzq.com/quotes-openservice/api/v1
USMART_WS_URL=wss://open-hz.yxzq.com/wss/v1
USMART_CHANNEL_ID=...
USMART_ACCOUNT_REF=...
USMART_PRIVATE_KEY_PATH=...
USMART_PUBLIC_KEY_PATH=...
USMART_PASSWORD_PUBLIC_KEY_PATH=...
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
  x_dt: "t4"
  x_type: null

capabilities:
  login: true
  trade_status_query: true
  account_query: true
  position_query: true
  order_query: true
  trade_query: true
  trade_quantity_query: true
  modify_range_query: true
  quote_http: true
  quote_ws: true
  place_order: false
  modify_order: false
  cancel_order: false
  odd_lot_order: false
  ipo: false
  prepost_market: false

request_id:
  header_length: unknown_by_pdf
  serial_no_length: 19
  generator: snowflake_or_compatible

safety:
  block_trade_login_in_read_only: true
  block_force_entrust: true
  block_session_type_prepost: true
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
- 被阻断时，`uSmartOpenApiClient` 不应收到调用。
- `uSmartOpenApiTradingAdapter` 能按 PDF 字段构造登录、下单、改单、撤单请求体。
- 下单请求体必须包含 `serialNo`、`entrustAmount`、`entrustPrice`、`entrustProp`、`entrustType`、`exchangeType`、`stockCode`。
- 改单请求体必须包含 `actionType=1`、`entrustAmount`、`entrustId`、`entrustPrice`。
- 撤单请求体必须包含 `actionType=0`、`entrustAmount=0`、`entrustId`、`entrustPrice=0`。
- 只读查询 DTO 能映射 `stock-asset`、`stock-holding`、`today-entrust`、`his-entrust`、`order-detail`、`stock-record` 的脱敏响应。
- `uSmartAuthSigner` 使用固定测试 key 生成可重复签名。
- 日志脱敏测试确认不输出 token、密码、私钥、完整账号。
- 对 PDF 示例状态 `1`、`5`、`11`、`21`、`0` 建立 mapper 单元测试；未识别状态必须进入 `unknown_by_pdf`。
- 对 `X-Request-Id` 和 `serialNo` 生成、长度校验、审计映射建立单元测试。

只读联调测试：

- 只允许登录、账户、持仓、订单、成交查询。
- 不允许 `trade-login`。
- 不允许触达下单、改单、撤单 endpoint。
- 所有输出脱敏。

受控实盘前测试：

- 必须先确认 sandbox 或 paper trading 环境。
- 没有 sandbox 时，不执行真实下单、改单、撤单测试。
- 交易接口必须经过 OMS、风控、交易时间、白名单和人工确认。

## 16. 待确认问题

需要从 PDF 或 uSmart 官方确认：

- 交易 API base URL。
- `X-Time` 格式。
- `X-Dt` 可用枚举。
- `X-Type` 是否必填及可用枚举。
- `X-Request-Id` 长度和重复请求返回语义。
- `X-Sign` 的精确签名输入、输出编码和 padding 规则。
- 交易 API 签名是否只签 body，还是像基础报价 API 一样需要 header+body 有序拼接。
- 登录手机号字段名、是否需要 RSA 加密、使用哪把公钥。
- 登录密码和交易密码是否使用与 `X-Sign` 不同的 RSA 公钥。
- token 有效期、刷新方式、多会话冲突语义。
- 下单返回的 `data.entrustId` 是否稳定作为券商订单号。
- `modify-order` 的 `actionType=0/1` 是否分别稳定表示撤单/改单。
- `modify-order` 的 `data.entrustId` 是原委托 ID、申请编号，还是新委托 ID。
- 改单是原生修改还是券商侧 cancel + replace。
- 订单状态码、错误码完整枚举。
- `finalStateFlag` 的完整枚举和是否可作为 OMS 订单终态判断依据。
- `exchangeType` 在不同接口中的枚举差异，尤其是查询接口里的 `67-A 股` 和下单接口里的沪深港通枚举。
- `entrustProp` 中 `e`、`h`、`0` 对港股/美股限价单的适用规则。
- `sessionType` 的盘前、盘后、暗盘规则，以及是否会形成非交易时间挂单。
- 频率限制、IP 白名单生效规则。

## 17. 后续实现顺序

正式编码时按以下顺序推进，避免先写真实 transport 后才补安全边界：

1. 补齐离线 DTO、枚举和 mapper：账户、资金、持仓、订单、成交、行情快照、错误响应、状态响应。
2. 补齐 `CapabilityGuard` 的只读能力判断：登录、交易状态查询、账户查询、持仓查询、订单查询、成交查询、行情查询独立开关；`trade-login`、下单、改单、撤单仍默认阻断。
3. 实现 `uSmartRequestIdPolicy`、`uSmartSensitiveFieldEncryptor`、`uSmartAuthSigner` 的离线单元测试，不接真实账号。
4. 实现 dry-run adapter 的 PDF 字段请求体构造，契约测试只断言字段和脱敏，不出网。
5. 实现 `uSmartMapper`，用 PDF 示例和人工脱敏 fixture 覆盖成功、业务拒绝、未知状态、缺失字段。
6. 实现真实 HTTP transport，但默认配置仍为 `dry_run=true` 或 `mode=read_only`；没有用户明确配置时不能出网。
7. 若用户确认只读联调，再只开放登录、账户、持仓、订单、成交和行情查询；禁止 `trade-login` 和所有交易动作。
8. 只有官方 sandbox 明确存在且不会产生真实委托时，才进入下单、改单、撤单链路验证；否则停在离线契约测试和只读联调。
