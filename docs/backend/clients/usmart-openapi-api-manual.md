# uSmart / 盈立 OpenAPI 登录与订单 API 调用栈设计手册

版本：v0.1  
状态：申请材料优先实现设计  
最后更新：2026-05-21

## 0. 文档定位

本文档面向“盈立 OpenAPI 申请材料需要源码截图”的紧急任务，定义交易开放 API 中登录、下单、改单、撤单四条链路从本地入口到券商交易开放 API 的完整设计。它补足 [broker-trading-gateway.md](../trading/broker-trading-gateway.md) 和 [usmart-openapi-call-design.md](usmart-openapi-call-design.md) 中仍停留在总体设计、缺少接口级手册的部分。

本文档只定义调用栈、模块 API、输入输出、字段映射、审计和安全边界。申请材料代码可以实现 dry-run / offline request builder 和完整调用链截图，但不得为了截图触达真实登录、真实下单、改单、撤单接口。

命名说明：项目文档中 `uSmart`、`盈立` 指同一 OpenAPI 接入方向；代码命名暂沿用 `usmart` 包名，文档面向券商申请时使用“盈立 OpenAPI”。

盈立官方资料拆成三套不同 API。本文档只覆盖交易开放 API；基础报价 API 和报价推送 API 不在本文档实现范围内，后续应在 `quotation_kernel` 下分别设计。

| API | 官方文档 | 协议 | 本文档是否覆盖 |
|---|---|---|---|
| 交易开放 API | `https://api-doc.usmart8.com/zh-cn/trade.html` | HTTPS POST | 是 |
| 基础报价 API | `https://api-doc.usmart8.com/zh-cn/quote-base.html` | HTTPS POST | 否 |
| 报价推送 API | `https://api-doc.usmart8.com/zh-cn/quote-push.html` | WebSocket | 否 |

本地网页转换稿保存于 `API_manual/uSmart/API_manual/`。官方 Python demo `API_manual/uSmart/openapi-demo-py/` 只作为签名、加密、序列化和连接流程参考，不替代网页字段表；不得提交或复制 demo 中的账号、密码、token、私钥或配置。

## 1. 现有设计缺口

对照当前两份设计文档和代码，实现前必须补齐以下缺口：

| 缺口 | 当前状态 | 对申请材料的影响 | 补齐方式 |
|---|---|---|---|
| 本地入口层缺失 | `src/backend`、`src/cli` 只有 README | 截图无法展示从 CLI/API 到网关的调用链 | 增加 `BrokerApplicationService`、CLI/API handler 设计和 dry-run 调用示例 |
| 登录 DTO 不完整 | `TradingGateway.connect(account_ref)` 只有账户引用 | 无法表达手机号、区号、密码密钥引用、token 会话 | 增加 `BrokerLoginRequest`、`BrokerLoginResult`、`uSmartSession` |
| 交易 DTO 与官方网页字段未完全对齐 | 当前 adapter body 仍是内部字段外形 | 截图无法证明对接 `serialNo`、`entrustAmount`、`actionType` 等字段 | 增加专门的 request builder 和字段映射测试 |
| 认证签名层缺失 | 没有 `auth.py`、`encryptor.py`、`transport.py` | 无法展示交易开放 API header、签名、加密、token 传递层 | 定义交易开放 API signer、交易敏感字段 encryptor、交易 HTTP transport |
| 请求 ID 与流水映射缺失 | 只有 `request_id` 字符串 | 无法证明 `X-Request-Id`、`serialNo`、本地订单 ID 的关系 | 增加 `uSmartRequestIdPolicy` 和审计映射 |
| 响应 mapper 缺失 | adapter 直接返回 `UNKNOWN` | 无法展示券商响应如何变成本地 ACK | 增加 `uSmartOrderMapper`、`uSmartErrorMapper` |
| 安全门控不够细 | 只拦截交易动作，未细分登录/只读查询/trade-login | 只读联调和申请截图容易边界不清 | 扩展 capability：login、trade_status、account、order、trade_action |
| 审计与脱敏未落代码接口 | 文档有规则，代码没有 API | 截图无法展示敏感字段不落日志 | 增加 `BrokerAuditLogger`、`Redactor` 接口 |
| 测试验收缺少申请材料目标 | 当前只测 read-only 阻断和一个 body 片段 | 无法稳定证明登录/下单/改单/撤单四条链路 | 增加四条链路 dry-run 契约测试 |

## 2. 完整调用栈

四条申请材料核心链路共用同一条分层调用栈：

```text
L0 CLI / FastAPI / 本地任务
  -> L1 BrokerApplicationService
  -> L2 OMS / Risk / SafetyPolicy
  -> L3 TradingGateway
  -> L4 BrokerTradingAdapter
  -> L5 uSmartOpenApiTradingAdapter
  -> L6 uSmartTradeOpenApiClient
  -> L7 uSmartTradeAuthSigner + uSmartTradeSensitiveFieldEncryptor + uSmartRequestIdPolicy
  -> L8 uSmartHttpTransport
  -> L9 uSmart OpenAPI Server
```

| 层 | 允许知道的字段 | 输入 | 输出 | 禁止事项 |
|---|---|---|---|---|
| L0 入口 | 本地参数、账户引用 | CLI args / HTTP body | 用户可见 DTO | 不出现券商私钥、token、完整密码 |
| L1 应用服务 | 内部 DTO、trace_id | command DTO | application result | 不拼接 uSmart body |
| L2 OMS/Risk | 订单、风控、人工确认 | order intent | gateway request | 不直接调用 adapter/client |
| L3 `TradingGateway` | 统一 DTO、能力模式 | `Broker*Request` | `Broker*Ack` | 不出现 uSmart endpoint |
| L4 基类 | 抽象接口 | 统一 DTO | 统一 DTO | 不做券商字段判断 |
| L5 uSmart adapter | uSmart endpoint/body | 统一 DTO | 统一 ACK | 不决定是否允许真实交易 |
| L6 trade client | 交易开放 API HTTP request/response | endpoint + body | `uSmartTradeOpenApiResponse` | 不含 OMS/风控逻辑；不处理基础报价或报价推送 |
| L7 trade signer/encryptor/id | 交易开放 API header、签名、加密字段 | stable JSON + secrets ref | headers + encrypted body | 不写日志输出秘密；不复用基础报价或报价推送规则 |
| L8 transport | HTTPS | `uSmartHttpRequest` | `uSmartHttpResponse` | 交易动作不自动重试 |
| L9 broker server | OpenAPI 协议 | HTTP request | OpenAPI response | 不受本地代码控制 |

## 3. 目标模块与文件

```text
src/
  backend/
    broker_api.py                 FastAPI handler，占位或后续实现
  cli/
    broker_commands.py            CLI handler，占位或后续实现
  rq_core/
    broker_kernel/
      contracts.py                统一 DTO、ACK、枚举、适配器基类
      gateway.py                  TradingGateway 安全门面
      capability.py               mode / capability / caller 检查
      audit.py                    审计事件接口
      redaction.py                脱敏工具
      idempotency.py              本地 request_id / broker_request_id
      application_service.py      本地应用服务编排
      usmart/
        adapter.py                内部 DTO -> uSmart endpoint/body
        client.py                 交易开放 API header、签名、transport、响应摘要
        auth.py                   交易开放 API X-Sign、Authorization、X-Time、X-Request-Id
        encryptor.py              交易开放 API 手机号、登录密码、交易密码加密
        transport.py              HTTPS POST / dry-run transport
        mapper.py                 响应、状态、错误映射
        endpoints.py              endpoint 常量
        request_id.py             X-Request-Id / serialNo 策略
        session.py                token 内存会话
```

申请材料第一批代码可以只实现 `dry_run` transport 和 request builder，但文件和调用层必须按上述结构落位，避免后续真实接入时重写。

## 4. 对外本地 API 清单

本地 API 是 RobustQuant 自己暴露给 CLI / Web / 任务的接口，不是直接暴露券商 OpenAPI。

| 本地能力 | 本地入口 | 应用服务方法 | 网关方法 | 券商 endpoint | 默认模式 |
|---|---|---|---|---|---|
| 登录 | `broker login` / `POST /broker/usmart/login` | `connect_broker` | `connect` | `/user-server/open-api/login` | 申请材料只 dry-run；只读联调需显式开启真实 HTTP |
| 下单 | `broker dry-run-place-order` / `POST /broker/usmart/orders` | `place_order` | `place_order` | `/stock-order-server/open-api/entrust-order` | 默认阻断；dry-run 只构造请求 |
| 改单 | `broker dry-run-modify-order` / `PATCH /broker/usmart/orders/{id}` | `modify_order` | `modify_order` | `/stock-order-server/open-api/modify-order` | 默认阻断；dry-run 只构造请求 |
| 撤单 | `broker dry-run-cancel-order` / `POST /broker/usmart/orders/{id}/cancel` | `cancel_order` | `cancel_order` | `/stock-order-server/open-api/modify-order` | 默认阻断；dry-run 只构造请求 |

本地接口统一返回 `ApplicationResult`：

| 字段 | 类型 | 说明 |
|---|---|---|
| `ok` | `bool` | 是否在本地流程成功完成 |
| `trace_id` | `str` | 链路 ID |
| `request_id` | `str | None` | 本地请求 ID |
| `status` | `str` | `connected`、`blocked`、`dry_run_built`、`unknown` 等 |
| `data` | `dict` | 脱敏业务结果 |
| `error` | `ErrorDTO | None` | 统一错误 |

## 5. 统一 DTO 设计

### 5.1 登录 DTO

```python
@dataclass(frozen=True)
class BrokerLoginRequest:
    broker: BrokerName
    account_ref: AccountRef
    method: Literal["password", "captcha"]
    login_profile_ref: str
    trace_id: str
    request_id: str
    allow_real_http: bool = False
```

字段说明：

| 字段 | 来源 | 说明 |
|---|---|---|
| `account_ref` | 本地配置 | 脱敏账户引用，不是完整账号 |
| `method` | 入口参数 | `password` 为渠道密码登录；`captcha` 为手机验证码登录 |
| `login_profile_ref` | 本地密钥配置 | 指向区号、手机号、登录密码 secret 的引用 |
| `request_id` | L1/L3 | 用于 `X-Request-Id` |
| `allow_real_http` | 运行配置 | 默认 `False`；申请截图代码必须使用 dry-run，不做真实登录 |

登录输出：

```python
@dataclass(frozen=True)
class BrokerLoginResult:
    broker: BrokerName
    account_ref: AccountRef
    connected: bool
    session_id_masked: str | None
    expires_at: datetime | None
    token_fingerprint: str | None
    raw_hash: str | None
```

### 5.2 下单 DTO

当前 `BrokerOrderRequest` 可以继续作为核心输入，但申请材料链路需要明确以下字段不能缺失：

| 字段 | 必填 | 说明 |
|---|---|---|
| `order_id` | 是 | 本地 OMS 订单 ID |
| `intent_id` | 是 | 交易意图 ID |
| `account_ref` | 是 | 脱敏账户引用 |
| `market` | 是 | `HK`、`US` 等内部市场 |
| `symbol` | 是 | 股票代码 |
| `side` | 是 | `buy` / `sell` |
| `order_type` | 是 | 第一版只允许 `LIMIT` 进入真实候选 |
| `price_type` | 是 | 第一版只允许安全映射后的限价类型 |
| `quantity` | 是 | 委托数量 |
| `limit_price` | 限价必填 | 委托价格 |
| `request_id` | 是 | 本地请求 ID，映射到 header |
| `risk_check_id` | 是 | 风控结果 ID |
| `manual_confirm_id` | 受控实盘必填 | 人工确认 ID |

### 5.3 改单 DTO

`BrokerModifyRequest` 必须满足：

- `broker_order_id` 必填。
- `new_quantity` 和 `new_limit_price` 至少一个非空。
- 真实改单前必须存在 `risk_check_id` 和 OMS 状态校验结果。
- 若 `modified-range` 查询失败，不允许进入真实改单。

### 5.4 撤单 DTO

`BrokerCancelRequest` 必须满足：

- `broker_order_id` 必填。
- `risk_check_id` 必填。
- OMS 订单状态必须允许撤单。
- 撤单超时不得自动重复撤单。

## 6. uSmart HTTP 请求对象

adapter 不直接调用 transport，而是先构造不可变请求对象：

```python
@dataclass(frozen=True)
class uSmartOpenApiRequest:
    endpoint: str
    operation_kind: Literal["readonly", "trade_action"]
    method: Literal["POST"]
    body: Mapping[str, Any]
    request_id: str
    serial_no: str | None
    trace_id: str
    token_required: bool
```

client 输出：

```python
@dataclass(frozen=True)
class uSmartTradeOpenApiResponse:
    endpoint: str
    http_status: int | None
    request_id: str
    broker_code: str | None
    broker_message: str | None
    data: Mapping[str, Any]
    raw_hash: str | None
    duration_ms: int | None
    dry_run: bool
```

规则：

- `body` 必须先稳定 JSON 序列化，再签名。
- 交易开放 API 的 `X-Sign` 签名原文只使用稳定 JSON body，不拼接 header 字段。
- 签名完成后 body 不得再修改。
- `raw_hash` 用于审计，不保存完整原始响应。
- 申请材料截图可以展示 `dry_run=True` 的 `uSmartOpenApiRequest` 和脱敏 response。

## 7. 登录调用栈 API

### 7.1 上下层关系

```text
CLI/FastAPI
  -> BrokerApplicationService.connect_broker(BrokerLoginRequest)
  -> TradingGateway.connect(account_ref)
  -> uSmartOpenApiTradingAdapter.connect(account_ref)
  -> uSmartLoginRequestBuilder.build(...)
  -> uSmartTradeOpenApiClient.post(...)
  -> uSmartTradeSensitiveFieldEncryptor.encrypt_login_fields(...)
  -> uSmartTradeAuthSigner.build_headers(...)
  -> uSmartHttpTransport.post_json(...)
```

### 7.2 uSmart endpoint

```text
POST /user-server/open-api/login
```

验证码登录使用：

```text
POST /user-server/open-api/send-phone-captcha
POST /user-server/open-api/loginCaptcha
```

### 7.3 输入映射

| 来源 | uSmart 字段 | 处理 |
|---|---|---|
| `login_profile.area_code` | `areaCode` | 配置读取 |
| `login_profile.phone_number` | `phoneNumber` | 使用隐私资料加密密钥材料处理后写入 body，默认按公钥加密 |
| `login_profile.password` | `password` | 使用隐私资料加密密钥材料处理后写入 body，默认按公钥加密 |
| 固定值 | `type` | 仅用于 `/send-phone-captcha`，`106` 表示短信登录验证码 |
| 用户输入 / 人工流程 | `captcha` | 仅用于 `/loginCaptcha`，不写日志 |
| `request.request_id` | `X-Request-Id` | header |
| channel 配置 | `X-Channel` | header |
| signer | `X-Sign` | header |

登录手机号字段名确认使用 `phoneNumber`，不使用 `mobile`、`phone` 或 `telephone`。

`loginCaptcha` 参数表只列出 `areaCode`、`captcha`、`phoneNumber` 三个 body 字段；请求 body 示例里出现了 `modifyUserConfigParam`。第一版不主动发送 `modifyUserConfigParam`，除非盈立确认该示例字段在当前渠道必填。

### 7.4 输出映射

登录响应不是 `data.token` 包装结构；手册示例为顶层对象直接包含 `token`、`expiration`、`tradePassword`、`openedAccount` 等字段。

| uSmart 顶层响应字段 | 内部字段 | 说明 |
|---|---|---|
| `token` | `uSmartSession.token` | 仅内存保存，不进日志 |
| `expiration` | `expires_at` | 过期时间 |
| `tradePassword` | `metadata.trade_password_enabled` | 布尔或摘要 |
| `openedAccount` | `metadata.opened_account` | 布尔或摘要 |
| 原始响应 | `raw_hash` | 哈希，不保存全文 |

登录成功只表示已建立只读会话，不表示允许交易。

## 8. 下单调用栈 API

### 8.1 上下层关系

```text
OMS
  -> BrokerApplicationService.place_order(BrokerOrderRequest)
  -> Risk / SafetyPolicy 校验
  -> TradingGateway.place_order(request)
  -> CapabilityGuard.ensure_allowed(PLACE_ORDER)
  -> uSmartOpenApiTradingAdapter.place_order(request)
  -> uSmartOrderRequestBuilder.build_place_order(request)
  -> uSmartTradeOpenApiClient.post(... operation_kind="trade_action")
```

`read_only` 默认模式下链路停在 `CapabilityGuard`，返回 `broker.trading_disabled`，不会进入 adapter。申请材料可以通过单独的 dry-run builder 测试展示将要发出的请求体。

### 8.2 uSmart endpoint

```text
POST /stock-order-server/open-api/entrust-order
```

### 8.3 输入映射

| 内部字段 | uSmart body 字段 | 第一版规则 |
|---|---|---|
| `request.request_id` 派生 | `serialNo` | 最长 19 位；与 `X-Request-Id` 建立审计映射 |
| `request.quantity` | `entrustAmount` | 按数字写入 JSON body |
| `request.limit_price` | `entrustPrice` | 限价必填；市价第一版拒绝 |
| `request.price_type` + `market` | `entrustProp` | 只允许明确白名单映射 |
| `request.side` | `entrustType` | `buy -> 0`，`sell -> 1` |
| `request.market` | `exchangeType` | `US -> 5` 为主要交易市场和第一批真实交易范围；`HK -> 0` 仅保留港股暗盘设计；沪深港通先禁用真实交易 |
| `request.symbol` | `stockCode` | 股票代码 |
| 可选名称 | `stockName` | 非主键，可不传 |
| 交易密码 secret | `password` | 若官方网页要求，则加密后传 |
| 固定安全默认 | `forceEntrustFlag` | 默认不启用 |
| `request.session` | `sessionType` | 第一批只做正常盘中交易 `0` / 不传；港股暗盘候选为 `3` 但仅保留设计；美股盘前盘后不进第一批 |

### 8.4 输出映射

| uSmart 响应 | 内部字段 | 处理 |
|---|---|---|
| `code` | `broker_response_code` | `0` 才可能业务成功 |
| `msg` | `broker_message` | 脱敏 |
| `data.entrustId` | `broker_order_id` | 缺失则 `unknown_response` |
| `data.status` | `broker_status_raw` | 未确认枚举前不猜最终状态 |
| `data.statusName` | `broker_status_name_raw` | 审计辅助 |

内部返回 `BrokerOrderAck`。如果 HTTP timeout、网络异常、业务成功但缺字段，状态进入 `unknown`，不得自动重试。

## 9. 改单调用栈 API

### 9.1 上下层关系

```text
OMS
  -> BrokerApplicationService.modify_order(BrokerModifyRequest)
  -> query_modify_range / Risk / OMS 状态校验
  -> TradingGateway.modify_order(request)
  -> CapabilityGuard.ensure_allowed(MODIFY_ORDER)
  -> uSmartOpenApiTradingAdapter.modify_order(request)
  -> uSmartOrderRequestBuilder.build_modify_order(request)
  -> uSmartTradeOpenApiClient.post(... operation_kind="trade_action")
```

### 9.2 uSmart endpoint

```text
POST /stock-order-server/open-api/modify-order
```

### 9.3 输入映射

| 内部字段 | uSmart body 字段 | 第一版规则 |
|---|---|---|
| 固定值 | `actionType` | 普通股票委托 `1` 表示改单；IPO 改撤单接口枚举不同，不得复用 |
| `request.new_quantity` | `entrustAmount` | 未改数量时按官方网页要求处理；不能猜默认 |
| `request.broker_order_id` | `entrustId` | 原委托 ID |
| `request.new_limit_price` | `entrustPrice` | 未改价格时按官方网页要求处理；不能猜默认 |
| 交易密码 secret | `password` | 若官方网页要求，则加密后传 |
| 固定安全默认 | `forceEntrustFlag` | 默认不启用 |

### 9.4 输出映射

| uSmart 响应 | 内部字段 | 处理 |
|---|---|---|
| `code` | `broker_response_code` | 业务返回码 |
| `msg` | `broker_message` | 脱敏 |
| `data.entrustId` | `broker_apply_id` | 官方网页回应参数说明为“申请编号”；不得覆盖原始 `broker_order_id` |
| `data.status` | `broker_status_raw` | 不能单独判断终态 |
| `data.statusName` | `broker_status_name_raw` | 审计辅助 |

改单前如果无法查询或验证 `modified-range`，不得进入真实改单。改单 timeout 进入 `unknown`，不得自动再次改单。

## 10. 撤单调用栈 API

### 10.1 上下层关系

```text
OMS
  -> BrokerApplicationService.cancel_order(BrokerCancelRequest)
  -> OMS 状态校验
  -> TradingGateway.cancel_order(request)
  -> CapabilityGuard.ensure_allowed(CANCEL_ORDER)
  -> uSmartOpenApiTradingAdapter.cancel_order(request)
  -> uSmartOrderRequestBuilder.build_cancel_order(request)
  -> uSmartTradeOpenApiClient.post(... operation_kind="trade_action")
```

### 10.2 uSmart endpoint

```text
POST /stock-order-server/open-api/modify-order
```

### 10.3 输入映射

| 内部字段 | uSmart body 字段 | 第一版规则 |
|---|---|---|
| 固定值 | `actionType` | 普通股票委托 `0` 表示撤单；IPO 改撤单接口枚举不同，不得复用 |
| 固定值 | `entrustAmount` | `0` |
| `request.broker_order_id` | `entrustId` | 原委托 ID |
| 固定值 | `entrustPrice` | `0` |
| 交易密码 secret | `password` | 若官方网页要求，则加密后传 |

### 10.4 输出映射

| uSmart 响应 | 内部字段 | 处理 |
|---|---|---|
| `code` | `broker_response_code` | 业务返回码 |
| `msg` | `broker_message` | 脱敏 |
| `data.entrustId` | `broker_apply_id` | 官方网页回应参数说明为“申请编号”；不得覆盖原始 `broker_order_id` |
| `data.status` | `broker_status_raw` | 不能单独判断终态 |
| `data.statusName` | `broker_status_name_raw` | 审计辅助 |

撤单也是交易动作。撤单 timeout 或未知响应必须进入 `unknown`，只能通过订单查询、成交查询、对账或人工确认转出。

## 11. Client、Signer、Transport API

### 11.1 交易开放 API Client

```python
class uSmartTradeOpenApiClient:
    def post(
        self,
        request: uSmartOpenApiRequest,
        *,
        token_required: bool,
    ) -> uSmartTradeOpenApiResponse:
        ...
```

处理步骤：

1. 校验 endpoint 在白名单中。
2. 稳定序列化 body。
3. 对交易开放 API 敏感 body 字段调用 encryptor。
4. 调用交易开放 API signer 生成 header。
5. 调用 transport；`dry_run=True` 时只返回脱敏请求摘要。
6. 解析响应，生成 `raw_hash`。
7. 返回 `uSmartTradeOpenApiResponse`。

### 11.2 交易开放 API Signer

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
    ) -> Mapping[str, str]:
        ...
```

输出 header 至少包含：

- `Content-Type`
- `Authorization`，登录接口可为空
- `X-Lang`
- `X-Channel`
- `X-Time`，Unix epoch milliseconds 字符串
- `X-Dt`，设备类型数字字符串，默认 `"4"` 表示 Windows
- `X-Type`，APP 类别数字字符串，默认 `"1"` 表示大陆版
- `X-Request-Id`
- `X-Sign`

基础报价 API 和报价推送 API 不使用这个 signer；后续分别实现独立的报价 HTTP signer 和报价 WS auth。

### 11.3 Transport

```python
class uSmartHttpTransport:
    def post_json(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        body_json: str,
        timeout: TimeoutConfig,
        operation_kind: Literal["readonly", "trade_action"],
    ) -> uSmartHttpResponse:
        ...
```

规则：

- `operation_kind="trade_action"` 不自动重试。
- timeout 不能被解释为未触达券商。
- 申请材料和默认开发环境使用 `DryRunTransport`。

## 12. 审计、日志和截图边界

四条链路都必须产出审计事件：

| 事件 | 触发点 | 记录 |
|---|---|---|
| `broker.login_requested` | L1 | `trace_id`、脱敏账户 |
| `broker.login_completed` | L6 | `trace_id`、request_id、token 指纹 |
| `broker.order_submit_requested` | L2 | `order_id`、risk_check_id |
| `broker.order_submit_blocked` | L3 | 阻断原因 |
| `broker.modify_requested` | L2 | `order_id`、broker_order_id 脱敏 |
| `broker.modify_blocked` | L3 | 阻断原因 |
| `broker.cancel_requested` | L2 | `order_id`、broker_order_id 脱敏 |
| `broker.cancel_blocked` | L3 | 阻断原因 |
| `usmart.request_built` | L5 | endpoint、body 字段名、request_id |
| `usmart.request_signed` | L7 | header key 列表，不含签名值 |

申请材料截图允许展示：

- 文件结构和类名。
- endpoint 常量。
- dry-run request builder。
- DTO 字段。
- `TradingGateway` 阻断交易动作的代码。
- `DryRunTransport` 不出网的代码。

申请材料截图禁止展示：

- 真实手机号、密码、token、私钥。
- 真实账户号、真实资金、真实持仓。
- 任何真实下单、改单、撤单运行结果。

## 13. 第一批实现验收

为了满足申请材料源码截图，同时不突破交易安全边界，第一批实现必须达到：

1. 有本地入口或应用服务方法：登录、下单、改单、撤单四个方法清晰存在。
2. 有 `TradingGateway` 层：交易动作默认在 `read_only` 被阻断。
3. 有 `uSmartOpenApiTradingAdapter` 层：能构造四类 endpoint 和 body。
4. 有交易开放 API client 层：能组装 request、调用交易 signer、调用 dry-run transport。
5. 有交易开放 API signer 接口：即使先用固定测试 key，也要展示交易 header 生成边界。
6. 有 `uSmartSensitiveFieldEncryptor` 接口：登录手机号、密码不以明文进入最终 request builder。
7. 有 `uSmartRequestIdPolicy`：生成或校验 `X-Request-Id` 与 `serialNo`。
8. 有离线测试：断言登录、下单、改单、撤单请求体字段完整，且 read-only 下交易动作不出网。
9. 有脱敏测试：日志或 response summary 不包含 token、密码、手机号、私钥。
10. 默认配置不出网；真实 HTTP transport 必须显式配置才可启用。

## 14. 待官方确认项

以下事项不能靠代码猜测，必须从官方网页文档或盈立官方确认：

- 交易 API base URL：网页版官方文档给出生产 `https://open-jy.yxzq.com`、测试 `http://open-jy-uat.yxzq.com`；实现仍必须通过 `USMART_API_BASE_URL` 配置显式选择，默认 dry-run 不出网。
- 用户已确认项目策略：UAT 测试地址不自动等同 sandbox / paper trading；是否保证下单、改单、撤单不产生真实委托仍需券商确认，确认前交易动作继续 dry-run。
- `X-Request-Id` 长度按 30 位可配置字符串实现；下单 body `serialNo` 严格按最长 19 位实现。重复请求返回语义仍需官方确认。
- `X-Sign` 输出编码默认跟随官方 Python demo 使用标准 Base64，并通过配置允许切换 URL-safe Base64 和控制 `=` padding；签名原文已确认只使用稳定 JSON body，不拼接 header 字段。
- 隐私资料加密按官方 Python demo 的 `rsa_encrypt` transform 实现：RSA `PKCS1_v1_5` 加密后 URL-safe Base64；仍需确认券商最终下发密钥材料与 demo `public_key` / `private_key` 配置槽位的对应关系。它必须和 `X-Sign` 渠道签名密钥材料分离。
- token 有效期、刷新机制。
- IPO 改撤单接口的 `actionType` 枚举与普通股票委托不同，后续如接入 IPO 必须单独建模。
- 券商内部改单是原生修改还是 cancel + replace；本地 OMS 风险模型按 cancel + replace 处理。
- 订单明细 `orderStatus` 历史节点的完整枚举。
- 错误码完整枚举。
- `entrustProp` 中 `0` 在美股盘中限价单上的精确适用规则；港股暗盘和盘前盘后后置。美股碎股使用 `/stock-order-server/open-api/odd-entrust` 专用接口，不通过普通下单 `entrustProp` 建模。
