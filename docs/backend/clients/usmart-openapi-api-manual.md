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

本地网页转换稿保存于 `API_manual/uSmart/API_manual/`。官方 Python demo `API_manual/uSmart/openapi-demo-py/` 只作为签名、加密、序列化和连接流程参考，不替代网页字段表；不得提交或复制 demo 中的账号、密码、token、私钥或配置。交易响应状态 catalog 由 `src/scripts/docs/extract_usmart_trade_error_codes.py` 从本地网页转换稿生成到 `docs/backend/clients/api/usmart-trade-error-codes.draft.yaml`，并按 `endpoint` / 手册章节分组，接口实现只能读取当前 endpoint 对应的响应状态。逐接口 HTTP 语义 profile 维护在 `docs/backend/clients/api/usmart-trade-endpoint-profiles.yaml`，用于约束 header、签名、body 序列化、分页、流水号和响应 envelope。

## 1. 现有设计缺口

对照当前两份设计文档和代码，实现前必须补齐以下缺口。2026-05-25 用户确认当前已存在的 uSmart 相关代码未经设计确认，不作为实现基线；后续实现可以放弃或替换这些草稿代码，不能为了兼容旧代码而降低下列缺口要求：

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

> 本节是申请材料视角的聚合调用栈。分层层号与职责的唯一真相源是 [usmart-openapi-call-design.md](usmart-openapi-call-design.md) §1.1（L0–L10）。层号映射：本节 L1（BrokerApplicationService）合并设计的 L1（FastAPI Router / CLI command）与 L2（Application Service）；本节 L2 = 设计 L3（OMS/Risk）；本节 L3 起依次对应设计 L4 及之后；本节 L7 合并设计 L8（signer）与 encryptor、RequestIdPolicy。实现时层号以设计文档为准。

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
        auth.py                   交易开放 API X-Sign、Authorization、端点级 header profile
        encryptor.py              交易开放 API 手机号、登录密码、交易密码加密
        transport.py              HTTPS POST / dry-run transport
        mapper.py                 响应、状态、错误映射
        endpoints.py              endpoint 常量
        request_id.py             X-Request-Id / serialNo 策略
        session.py                token 内存会话
```

申请材料第一批代码可以只实现 `dry_run` transport 和 request builder，但文件和调用层必须按上述结构落位，避免后续真实接入时重写。

## 4. 对外本地 API 清单

本地 API 是 Augur_Maestro 自己暴露给 CLI / Web / 任务的接口，不是直接暴露券商 OpenAPI。

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

2026-05-25 用户确认 DTO 决策：

- `TradingGateway.connect` 改为接收 `BrokerLoginRequest`，不再只接收 `AccountRef`；手机号、登录密码、验证码和 token 原文仍只能通过密钥配置、人工输入或 session 管理层间接处理，不进入 Gateway DTO。
- 订单查询统一使用一个 `OrderQueryRequest`，通过 `scope=today|history|detail` 区分今日订单、历史订单和订单明细；分页规则统一按官方手册处理，`page_num` 从 1 开始，`page_size` 默认 10、最大 20。
- `AccountSnapshot`、`CashSnapshot`、`PositionSnapshot` 等程序内部 DTO 可以保留完整 `Decimal` 金额和数量；普通日志、控制台和 Web 展示层负责脱敏、摘要或格式化，不直接输出完整敏感资金和持仓隐私。
- 原始券商结构化字段不直接挂在用户可见 DTO 上；DTO 只携带 `raw_hash` 和 `BrokerRawRecordRef`，需要排查或对账细节时再通过引用查询受控审计存储。
- Gateway 以上层只能依赖统一 Broker 抽象和统一 DTO；uSmart、miniQMT、Ptrade 都是从统一 `BrokerTradingAdapter` 基类或 Protocol 派生的后端实现，不能让上层服务依赖具体券商字段或类名。


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
```

字段说明：

| 字段 | 来源 | 说明 |
|---|---|---|
| `account_ref` | 本地配置 | 脱敏账户引用，不是完整账号 |
| `method` | 入口参数 | `password` 为渠道密码登录；`captcha` 为手机验证码登录 |
| `login_profile_ref` | 本地密钥配置 | 指向区号、手机号、`login_password_secret_ref` 的引用 |
| `request_id` | L1/L3 | 本地审计 ID；仅在端点 header profile 要求时外发为 `X-Request-Id` |

真实 HTTP 是否允许由 broker 配置中的 `mode`、capability、`transport.allow_real_http_readonly` 和 [api/usmart-trade-runtime-config-profile.yaml](api/usmart-trade-runtime-config-profile.yaml) 的 runtime validation 共同决定，不进入 `BrokerLoginRequest`。

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
| `request_id` | 是 | 本地请求 ID；用于审计和派生券商流水，是否映射到 header 由端点 profile 决定 |
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
- 交易开放 API 的 `X-Sign` 签名原文只使用最终发送的同一 JSON body 字符串，不拼接 header 字段。
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
| `login_profile.login_password_secret_ref` | `password` | 读取登录密码 secret 后使用隐私资料加密密钥材料处理，最终写入盈立官方登录 body 字段 `password` |
| 固定值 | `type` | 仅用于 `/send-phone-captcha`，`106` 表示短信登录验证码 |
| 用户输入 / 人工流程 | `captcha` | 仅用于 `/loginCaptcha`，不写日志 |
| `request.request_id` | 内部审计 ID / 可选 `X-Request-Id` | 始终保留本地审计；只有端点 header profile 要求时外发为 header |
| channel 配置 | `X-Channel` | header |
| signer | `X-Sign` | header |

登录手机号字段名确认使用 `phoneNumber`，不使用 `mobile`、`phone` 或 `telephone`。

`loginCaptcha` 参数表只列出 `areaCode`、`captcha`、`phoneNumber` 三个 body 字段；请求 body 示例里出现了 `modifyUserConfigParam`。第一版不主动发送 `modifyUserConfigParam`，除非盈立确认该示例字段在当前渠道必填。

### 7.4 输出映射

登录响应结构存在官方资料差异：网页版手册示例为顶层对象直接包含 `token`、`expiration`、`tradePassword`、`openedAccount` 等字段；官方 Python demo 读取 `res["data"]["token"]`。第一版 mapper 必须兼容顶层和 `data` 包装两种结构。

| uSmart 顶层响应字段 | 内部字段 | 说明 |
|---|---|---|
| `token` / `data.token` | `uSmartSession.token` | 仅内存保存，不进日志；两处同时存在且不一致时返回 `broker.response_invalid` |
| `expiration` / `data.expiration` | `expires_at` | 过期时间 |
| `tradePassword` | `metadata.trade_password_enabled` | 布尔或摘要 |
| `openedAccount` | `metadata.opened_account` | 布尔或摘要 |
| 原始响应 | `raw_hash` | 哈希，不保存全文 |

登录成功只表示已建立只读会话，不表示允许交易。

会话策略由 [api/usmart-trade-session-retry-profiles.yaml](api/usmart-trade-session-retry-profiles.yaml) 约束：

- 第一版只维护单账户单 session，token 只保存在进程内存，默认不落库。
- `expiration` 解析为 `expires_at`，但官方精确格式、时区和包装路径仍需联调确认；解析失败时不得假设长期有效。
- 登录 endpoint 使用 `login_no_authorization` 和 `login_single_attempt`；登录请求不得发送 `Authorization`。
- 只读查询使用 `token_required_readonly` 和 `readonly_bounded_backoff_v1`；遇到 token 过期或 401 时，可以显式重新登录后用新的 `request_id` 重新发起查询。
- `readonly_bounded_backoff_v1.max_retries=2`，表示最多 3 次总尝试；每次尝试必须生成新的 `broker_request_id`，失败请求 ID 不得复用。
- 下单、改单、撤单使用 `token_required_trade_action` 和 `trade_action_no_retry_v1`；遇到 token 过期、401 或权限错误时，不允许隐式刷新 token 后继续提交，必须返回认证错误并让 OMS 重新进入可审计流程。

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
| `request.request_id` 派生 | `serialNo` | 最长 19 位；与本地 `broker_request_id` 建立审计映射，普通下单不强制外发 header `X-Request-Id` |
| `request.quantity` | `entrustAmount` | 按数字写入 JSON body |
| `request.limit_price` | `entrustPrice` | 限价必填且必须大于 0；市价第一版拒绝 |
| `request.price_type` + `market` | `entrustProp` | 用户已确认第一版美股盘中普通限价单使用 `0`；其他枚举不允许真实交易 |
| `request.side` | `entrustType` | `buy -> 0`，`sell -> 1` |
| `request.market` | `exchangeType` | `US -> 5` 为第一批普通真实交易范围；`HK -> 0` 仅保留港股暗盘设计；沪深港通先禁用真实交易 |
| `request.symbol` | `stockCode` | 股票代码 |
| 可选名称 | `stockName` | 非主键，可不传 |
| `trade_password_secret_ref` | `password` | 读取交易密码 secret 后加密，最终写入盈立交易 API body 字段 `password`；官方网页普通下单字段为可选；第一版 `trade_password_required=false`，默认不发送 |
| 固定安全默认 | `forceEntrustFlag` | 默认不启用 |
| `request.session` | `sessionType` | 第一批只做正常盘中交易 `0` / 不传；港股暗盘候选为 `3` 但仅保留设计；美股盘前盘后不进第一批 |

第一版普通真实下单白名单：`market=US`、`exchangeType=5`、`order_type=LIMIT`、`entrustProp=0`、`entrustType` 为买 `0` 或卖 `1`、`entrustPrice>0`、`sessionType=0` 或不传。账户能力按现金账户正股多头交易设计，`TradingGateway` 只承接正股买入卖出执行，止盈止损由策略模块产生普通交易意图；不启用自动对冲、做空、融资融券、保证金交易或美股期权。任何字段无法明确映射时，request builder 只能生成 dry-run 或返回不支持，不能触达真实交易接口。

### 8.4 输出映射

### 8.4 美股碎股输入映射

碎股使用专用 endpoint：

```text
POST /stock-order-server/open-api/odd-entrust
```

第一版启用美股碎股买入和卖出；内部按金额建模，不让策略直接提交券商碎股数量。

| 内部字段 | uSmart body 字段 | 第一版规则 |
|---|---|---|
| `request.notional_amount / request.limit_price` | `entrustAmount` | 小数股数，按委托金额除以限价换算；内部使用 `Decimal`，HTTP JSON 边界序列化为券商接受的 number |
| `request.limit_price` | `entrustPrice` | 限价，必须大于 0 |
| `request.side` | `entrustType` | `buy -> 0`，`sell -> 1` |
| 固定值 | `exchangeType` | `5`，美股 |
| `request.symbol` | `stockCode` | 股票代码 |

卖出碎股前必须校验持仓或最大可卖返回的可卖碎股数量，不能只按目标金额发单。最小金额、最小股数和数量精度按后续联调结果配置。

### 8.5 输出映射

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
| `trade_password_secret_ref` | `password` | 读取交易密码 secret 后加密，最终写入盈立交易 API body 字段 `password`；官方网页改单字段为可选；第一版 `trade_password_required=false`，默认不发送 |
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
| `trade_password_secret_ref` | `password` | 读取交易密码 secret 后加密，最终写入盈立交易 API body 字段 `password`；官方网页撤单字段为可选；第一版 `trade_password_required=false`，默认不发送 |

### 10.4 输出映射

| uSmart 响应 | 内部字段 | 处理 |
|---|---|---|
| `code` | `broker_response_code` | 业务返回码 |
| `msg` | `broker_message` | 脱敏 |
| `data.entrustId` | `broker_apply_id` | 官方网页回应参数说明为“申请编号”；不得覆盖原始 `broker_order_id` |
| `data.status` | `broker_status_raw` | 不能单独判断终态 |
| `data.statusName` | `broker_status_name_raw` | 审计辅助 |

撤单也是交易动作。撤单 timeout 或未知响应必须进入 `unknown`，只能通过订单查询、成交查询、对账或人工确认转出。


## 11. 只读查询 API 设计

本节按 2026-05-26 核对的 uSmart / 盈立网页版交易 OPEN API 手册补齐第一批只读联调的 request builder 和 response mapper。当前网页版手册中，资产和持仓不再按历史草稿里的 `/stock-order-server/open-api/stock-asset`、`/stock-order-server/open-api/stock-holding` 两个独立 endpoint 建模；网页版手册的“查询资产” endpoint 为 `/asset-center-server/open-api/open-assetQuery/v1`，响应同时包含账户资产明细 `assetSingleInfoRespVOS` 和持仓明细 `holdInfos`。因此本轮实现以 `open-assetQuery/v1` 为事实源构造 `AccountSnapshot`、`CashSnapshot` 和 `PositionSnapshot`；旧 `stock-asset` / `stock-holding` 名称只作为历史草稿，不进入本轮 request builder。

### 11.1 通用只读请求规则

| 项 | 规则 |
|---|---|
| HTTP method | 全部为 `POST` |
| `operation_kind` | 全部为 `readonly` |
| token | 除登录外均要求内存 `uSmartSession.token`，映射到 `Authorization` header |
| 签名 | 使用交易开放 API signer；按 endpoint profile 先生成最终 body 字符串，再对同一字符串签名并发送 |
| 出网开关 | 只有 `mode=read_only`、对应只读 capability 开启且 `transport.allow_real_http_readonly=true` 才允许真实 HTTP |
| 重试 | 只读查询 `max_retries=2`，最多 3 次总尝试；每次尝试生成新的 `broker_request_id`，不能复用失败请求的 `request_id` |
| 原始响应 | 不直接返回给 CLI/Web；按 [../trading/broker-gateway-raw-record-profile.yaml](../trading/broker-gateway-raw-record-profile.yaml) 存入受控审计存储并返回 `raw_hash` / `BrokerRawRecordRef` |
| 数字 | 金额、价格、数量统一解析为 `Decimal`；官方返回 number 或数字字符串都按 `Decimal(str(value))` 处理 |
| ID | `entrustId`、`serialNo`、`recordId` 等统一在内部按字符串保存，避免 int64 精度损失 |
| 空值 | 缺失、`null`、空字符串按字段语义映射为 `None`；必需字段缺失进入 `unknown_response` |

分页规则：内部 `page_num` 从 1 开始，默认 1；`page_size` 默认 10，第一版最大 20。超过 20 时 request builder 在本地截断为 20 并记录审计摘要，不依赖服务端截断。官方 Python demo 的 `today_entrust` 默认 `pageNum="0"`、`pageSize="20"`，与网页手册冲突；只有 endpoint profile 显式启用 demo-compatible 模式时才允许 HTTP 层发送 `pageNum=0`，内部 DTO 不引入 0-based 分页。

市场枚举按查询语义处理：`HK -> 0`、`US -> 5`、`A -> 67`、`ALL -> 100`。`ALL` 只能用于查询，不能流入任何交易 request builder。成交流水响应中的 `exchangeType` 字段说明更细，可能出现 `1/2/3/4/6/7` 等 A/B 股或港股通值；mapper 必须保留原始值，无法映射到内部市场时标记为 `unknown_by_official_doc`。

币种枚举按网页版手册当前字段说明处理：`moneyType=0 -> CNY`、`1 -> USD`、`2 -> HKD`。如联调发现接口返回其他值，保留 raw 并映射为 `unknown_currency`。

时间字段规则：官方手册同时出现 `yyyy-MM-dd`、`HH:mm:ss`、`yyyy-MM-dd HH:mm:ss` 和 ISO-like `2019-06-14T09:12:49.000+0000`。DTO 中保留原始时间字符串，并尽力解析为 timezone-aware `datetime`；无法确定时区时不猜，解析字段置空并把 raw time 放入 `raw_ref` 指向的原始结构化记录。

### 11.2 Endpoint 与 Gateway 方法

| Gateway 方法 | uSmart endpoint | 网页版手册章节 | 返回 DTO |
|---|---|---|---|
| `get_account` / `get_cash` | `/asset-center-server/open-api/open-assetQuery/v1` | `2.11 查询资产` | `AccountSnapshot` / `CashSnapshot` |
| `get_positions` | `/asset-center-server/open-api/open-assetQuery/v1` | `2.11 查询资产` 的 `holdInfos` | `list[PositionSnapshot]` |
| `query_orders(scope=today)` | `/stock-order-server/open-api/today-entrust` | `2.7 今日订单-分页查询` | `Page[BrokerOrderSnapshot]` |
| `query_orders(scope=history)` | `/stock-order-server/open-api/his-entrust` | `2.8 全部订单-分页查询` | `Page[BrokerOrderSnapshot]` |
| `query_orders(scope=detail)` | `/stock-order-server/open-api/order-detail` | `2.9 查询订单明细` | `BrokerOrderDetailSnapshot` |
| `query_trades` | `/stock-order-server/open-api/stock-record` | `2.10 查询成交流水-分页查询` | `Page[BrokerTradeSnapshot]` |

`OrderQueryRequest.scope` 只允许 `today`、`history`、`detail`。`scope=detail` 不分页，必须提供 `broker_order_id` 或 `serial_no` 至少一个；`scope=today/history` 使用分页返回。

### 11.3 Request Builder 表

#### 11.3.1 资产和持仓：`open-assetQuery/v1`

| Gateway 字段 | uSmart body 字段 | 必填 | 规则 |
|---|---|---|---|
| `currency` | `moneyType` | 否 | `CNY=0`、`USD=1`、`HKD=2`；为空时不传，查询所有官方默认范围 |
| `account_ref` | 不进入 body | 否 | 只用于本地审计和 session 选择 |
| `request_id` | header profile 可选 | 是 | 内部必有；是否外发由交易 API header profile 控制 |

Builder 输出示例：`{}` 或 `{"moneyType": 1}`。不发送 `exchangeType`，因为网页版 `open-assetQuery/v1` 请求参数只列出 `moneyType`。

#### 11.3.2 今日订单：`today-entrust`

| Gateway 字段 | uSmart body 字段 | 必填 | 规则 |
|---|---|---|---|
| `market` | `exchangeType` | 是 | `HK=0`、`US=5`、`A=67`、`ALL=100`；默认第一批可用 `ALL=100` 做只读查询 |
| `page_num` | `pageNum` | 否 | 内部默认 1、最小 1；HTTP 默认 1，demo-compatible profile 可发送 0 |
| `page_size` | `pageSize` | 否 | 默认 10，最大 20；demo-compatible profile 可默认 20 |
| `symbol` | `stockCode` | 否 | 为空不传；不发送空字符串 |
| `name` | `stockName` | 否 | 第一版不作为主筛选条件；为空不传 |

#### 11.3.3 历史订单：`his-entrust`

| Gateway 字段 | uSmart body 字段 | 必填 | 规则 |
|---|---|---|---|
| `date_range_mode` | `dateFlag` | 是 | 默认 `1` 一周；自定义日期时使用 `6`；查询全部使用 `7` 需显式配置允许 |
| `market` | `exchangeType` | 是 | 同今日订单 |
| `start_date` | `entrustBeginDate` | 否 | `yyyy-MM-dd`；仅 `dateFlag=6` 时发送 |
| `end_date` | `entrustEndDate` | 否 | `yyyy-MM-dd`；仅 `dateFlag=6` 时发送 |
| `page_num` | `pageNum` | 否 | 默认 1，最小 1 |
| `page_size` | `pageSize` | 否 | 默认 10，最大 20 |
| `symbol` | `stockCode` | 否 | 为空不传 |

`dateFlag` 官方枚举：`1` 一周、`2` 一个月、`3` 三个月、`4` 近一年、`5` 今年、`6` 自选时间、`7` 查询全部。第一版默认不使用 `7`，避免无界分页。

#### 11.3.4 订单明细：`order-detail`

| Gateway 字段 | uSmart body 字段 | 必填 | 规则 |
|---|---|---|---|
| `serial_no` | `serialNo` | 条件必填 | 与 `broker_order_id` 至少一个非空；内部按字符串保存，HTTP JSON 边界按官方 int64 可配置序列化 |
| `broker_order_id` | `entrustId` | 条件必填 | 与 `serial_no` 至少一个非空；优先使用 `broker_order_id` |

Builder 不发送 `pageNum` / `pageSize`，因为订单明细不是分页接口。

#### 11.3.5 成交流水：`stock-record`

| Gateway 字段 | uSmart body 字段 | 必填 | 规则 |
|---|---|---|---|
| `market` | `exchangeType` | 是 | `HK=0`、`US=5`、`A=67`、`ALL=100` |
| `symbol` | `stockCode` | 否 | 为空不传 |
| `broker_order_id` | `entrustId` | 否 | 内部字符串；HTTP JSON 边界按官方 int64 可配置序列化 |
| `start_date` | `beginTime` | 否 | `yyyy-MM-dd` |
| `end_date` | `endTime` | 否 | `yyyy-MM-dd` |
| `page_num` | `pageNum` | 否 | 默认 1，最小 1 |
| `page_size` | `pageSize` | 否 | 默认 10，最大 20 |

### 11.4 Response Mapper 表

#### 11.4.1 资产和资金 mapper

响应路径：`data.assetSingleInfoRespVOS[]`。

| uSmart 字段 | 内部字段 | 规则 |
|---|---|---|
| `fundAccount` | `account_ref` / `broker_account_ref_masked` | 只保存脱敏或引用，不在普通日志输出完整值 |
| `fundAccountType` | `fund_account_type_raw` | 保留原始枚举 |
| `multiAssetBusinessType` | `asset_business_type_raw` | 保留原始枚举，用于区分港股、美股、碎股、期权等资产业务 |
| `moneyType` | `currency` | `0=CNY`、`1=USD`、`2=HKD` |
| `asset` | `total_asset` | `Decimal` |
| `cashBalance` | `cash` | `Decimal` |
| `availableBalance` | `available_cash` | `Decimal` |
| `frozenBalance` | `frozen_cash` | `Decimal` |
| `marketValue` | `market_value` | `Decimal` |
| `purchasePower` | `purchasing_power` | `Decimal`，只作风控辅助 |
| `borrowAmount` | `borrow_amount_raw` | 第一版现金账户只保留 raw，不启用融资逻辑 |
| `riskStatusCode` / `mvRate` / `mvLevelDesc` | `broker_risk_raw` | 保留给审计和后续风控，不直接触发交易 |

同一响应可能包含多个 `assetSingleInfoRespVOS`。`AccountSnapshot` 可以按 `moneyType` / `multiAssetBusinessType` 生成多条现金和资产记录；展示层再汇总。

#### 11.4.2 持仓 mapper

响应路径：`data.assetSingleInfoRespVOS[].holdInfos[]`。

| uSmart 字段 | 内部字段 | 规则 |
|---|---|---|
| `code` | `symbol` | 字符串 |
| `name` | `name` | 字符串，可为空 |
| `exchangeType` | `market` | `0=HK`、`5=US`，其他保留 raw |
| `moneyType` | `currency` | 若持仓项缺失，则继承所属 asset item 的 `moneyType` |
| `curHoldNum` | `quantity` | `Decimal` |
| `marketValue` | `market_value` | `Decimal` |
| `costPrice` | `cost_price` | `Decimal` |
| `costBalance` | `cost_amount` | `Decimal` |
| `holdProfit` | `unrealized_pnl` | `Decimal` |
| `holdProfitPercent` | `unrealized_pnl_pct` | `Decimal`，不转百分号字符串 |
| `sessionType` | `session_type_raw` | 保留 raw |
| `fundAccountType` | `fund_account_type_raw` | 保留 raw |
| `id` | `broker_position_id` | 字符串 |

网页版 `open-assetQuery/v1` 的 `holdInfos` 未提供明确 `available_quantity`、`frozen_quantity`、`odd_quantity` 字段；第一版这些字段置为 `None`，并在 DTO 中保留 `raw_ref`。如果后续需要可卖数量，用 `query_trade_quantity` 或券商补充接口，不从持仓数量猜。

#### 11.4.3 今日/历史订单 mapper

今日订单响应路径：`data.list[]`，历史订单响应路径：`data.list[]`。

| uSmart 字段 | 内部字段 | 规则 |
|---|---|---|
| `entrustId` | `broker_order_id` | 字符串 |
| `entrustNo` | `broker_order_no` | 字符串，可为空 |
| `serialNo` | `broker_serial_no` | 字符串，避免 int64 精度损失 |
| `exchangeType` | `market` | `0=HK`、`5=US`，其他保留 raw |
| `stockCode` | `symbol` | 字符串 |
| `stockName` | `name` | 字符串 |
| `entrustType` | `side` | `0=buy`、`1=sell`；其他值保留 raw，不映射方向 |
| `entrustProp` | `broker_order_type_raw` | 保留 raw，不反推内部交易能力 |
| `entrustAmount` | `quantity` | `Decimal` |
| `businessAmount` | `filled_quantity` | `Decimal` |
| `entrustPrice` | `limit_price` | `Decimal` |
| `businessAveragePrice` | `avg_fill_price` | `Decimal` |
| `status` | `broker_status_raw` | 必须进入 OMS mapper |
| `statusName` | `broker_status_name_raw` | 仅审计辅助 |
| `moneyType` | `currency` | `0=CNY`、`1=USD`、`2=HKD` |
| `createTime` | `submitted_time_raw` | 今日订单通常只有时间字符串 |
| `createDate` | `submitted_date_raw` | 历史订单可能返回 `yyyyMMdd` |
| `flag` | `broker_order_flag_raw` | 订单类别 raw，不作为交易能力开关 |
| `sessionType` | `session_type_raw` | 保留 raw |

今日/历史列表不稳定提供 `finalStateFlag`；因此列表 mapper 不单独把订单置为最终状态。最终状态判断优先结合订单明细 `finalStateFlag`、成交流水和对账结果。

#### 11.4.4 订单明细 mapper

响应路径：顶层订单字段在 `data`，历史节点在 `data.appEntrustRecordDetailInfoList[]`。

| uSmart 字段 | 内部字段 | 规则 |
|---|---|---|
| `data.entrustId` | `broker_order_id` | 字符串 |
| `data.exchangeType` | `market` | 内部市场映射；无法识别保留 raw |
| `data.stockCode` / `data.stockName` | `symbol` / `name` | 字符串 |
| `data.entrustType` | `side` | `0=buy`、`1=sell` |
| `data.status` | `broker_status_raw` | 普通订单状态 raw |
| `data.statusName` | `broker_status_name_raw` | 审计辅助 |
| `data.finalStateFlag` | `final_state_flag` | 接受字符串或数字；`1=True`、`0=False`，其他进入 `unknown_by_official_doc` |
| `detail.orderStatus` | `order_status_raw` | 历史节点状态 raw，必须进入 OMS mapper |
| `detail.orderStatusName` | `order_status_name_raw` | 审计辅助 |
| `detail.createTime` | `event_time_raw` | 尽力解析，保留 raw |
| `detail.businessAmount` | `filled_quantity_at_event` | `Decimal` |
| `detail.businessAveragePrice` | `avg_fill_price_at_event` | `Decimal` |
| `detail.businessBalance` | `filled_amount_at_event` | `Decimal` |
| `detail.commissionFee` 等费用字段 | `fee_items_raw` | 字符串或 `Decimal`，第一版只保留 raw/ref，不做费用归因 |

`OrderQueryRequest(scope=detail)` 返回 `BrokerOrderDetailSnapshot`，其中包含当前订单摘要和 `events: list[BrokerOrderEventSnapshot]`。未知 `orderStatus` 或 `finalStateFlag` 冲突时，订单状态进入 `unknown_by_official_doc`。

#### 11.4.5 成交流水 mapper

响应路径：`data.list[]`。

| uSmart 字段 | 内部字段 | 规则 |
|---|---|---|
| `recordId` | `broker_trade_id` | 优先使用；缺失时可退到 `id`，并记录 `trade_id_source` |
| `id` | `broker_trade_row_id_raw` | 保留 raw |
| `entrustId` | `broker_order_id` | 字符串 |
| `exchangeType` | `market` | 按查询枚举映射，无法识别保留 raw |
| `stockCode` / `stockName` | `symbol` / `name` | 字符串 |
| `entrustType` | `side_or_trade_type_raw` | 成交流水里含买、卖、查询、撤单、补单、改单、转入、转出、成交取消等类型；只有 `0/1` 可映射为买卖方向 |
| `businessAmount` | `quantity` | `Decimal` |
| `businessPrice` | `price` | `Decimal` |
| `businessBalance` | `amount` | `Decimal` |
| `moneyType` | `currency` | `0=CNY`、`1=USD`、`2=HKD` |
| `businessStatus` | `business_status_raw` | `1=成交成功`、`2=成交取消`；不直接覆盖订单总状态 |
| `businessTime` | `business_time` / `business_time_raw` | 尽力解析 timezone-aware datetime，保留 raw |
| `createTime` / `updateTime` | `created_at_raw` / `updated_at_raw` | 保留 raw |

### 11.5 空响应和异常结构处理

| 场景 | 处理 |
|---|---|
| HTTP 2xx 但 `code != 0` | 映射 gateway 错误码，保留 endpoint 对应 raw code/msg |
| `code=0` 且分页接口 `data.list=[]` | 返回空 `Page`，`total` 取官方字段或 0 |
| `code=0` 但 `data` 缺失 | `unknown_response`，不伪造空结果 |
| 分页接口 `data` 存在但 `list` 缺失 | `unknown_response`，除非 `total=0` 且联调确认该结构合法 |
| 数字字段为空字符串 | 映射 `None`，并在 raw record 中保留原值 |
| 必需 ID 缺失 | 对应订单或成交记录进入 `unknown_by_official_doc`，不生成可追踪业务 ID |
| 未知枚举 | 保留 raw，内部枚举置为 `UNKNOWN` 或 `None`，不猜 |

uSmart 错误响应统一进入 `BrokerGatewayError`：

| 输入来源 | mapper 规则 |
|---|---|
| HTTP 2xx 且 `code=0` | 正常 mapper，不生成错误 DTO |
| HTTP 2xx 且 `code!=0` | 用当前 endpoint 在 `usmart-trade-error-codes.draft.yaml` 查 `response_statuses[].gateway_error`；查不到映射为 `broker.unclassified` |
| HTTP 401/403 | 优先映射 `broker.auth_expired`、`broker.permission_denied`、`broker.ip_not_allowed`；具体 raw HTTP 摘要写入 `raw_ref` |
| HTTP 404 | 映射 `broker.endpoint_not_found` |
| HTTP 429 | 映射 `broker.rate_limited` |
| HTTP 5xx | 映射 `broker.service_unavailable` 或 `broker.transport_error` |
| connect/read timeout | 查询可映射 `broker.timeout` 并按策略重试；交易动作必须进入未知/待对账流程 |
| 响应 JSON 无法解析或结构不匹配 | 映射 `broker.response_invalid`，不得伪造空成功 |

`uSmartErrorMapper` 必须填充 `broker="usmart"`、`endpoint`、`trace_id`、`request_id`、`http_status`、`raw_code`、`raw_message_hash` 和 `raw_ref`。`raw_message` 原文只允许进入受控审计存储，不进入 CLI/FastAPI/普通日志。

### 11.6 仍需联调确认项

以下不阻塞 request builder 和 mapper 初版，但只读联调后必须回填：

- `open-assetQuery/v1` 是否完全替代旧 `stock-asset` / `stock-holding`，以及渠道权限是否默认开放该 endpoint；网页版转换稿变更记录提到 `stock-holding`，但当前正文缺少可实现级别的 endpoint 章节；官方 Python demo 提供 `stock_holding(exchangeType)` 示例。若要作为 fallback 候选，必须先补齐 endpoint profile、raw error catalog 和联调确认。
- `open-assetQuery/v1` 返回多账户、多币种、多业务类型时，是否存在同一市场多条资产记录需要合并。
- `holdInfos` 是否可能返回可卖数量、冻结数量或碎股数量的隐藏字段；网页版字段表当前未列出。
- `exchangeType=100` 在今日订单、历史订单、成交流水中是否稳定支持；资产接口不使用 `exchangeType`。
- 历史订单 `dateFlag=7` 查询全部的最大跨度、最大页数和限流语义。
- 成交流水 `beginTime` / `endTime` 是否闭区间，以及最大查询跨度。
- 订单列表与订单明细时间字段的实际时区；成交流水 ISO-like 时间是否始终带 `+0000`。
- 订单明细 `orderStatus` 完整枚举和状态流转；未知状态继续进入 `unknown_by_official_doc`。

## 12. Client、Signer、Transport API

### 12.1 交易开放 API Client

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

1. 校验 endpoint 在白名单常量中。交易标的的人工发布白名单校验属于 OMS/Risk 与 `TradingGateway` 的职责（命中失败在进入网关前返回 `risk.symbol_not_whitelisted`），不在 client 层重复执行；client 不含 OMS/风控逻辑。
2. 稳定序列化 body。
3. 对交易开放 API 敏感 body 字段调用 encryptor。
4. 调用交易开放 API signer 生成 header。
5. 调用 transport；`dry_run=True` 时只返回脱敏请求摘要。
6. 解析响应，生成 `raw_hash`。
7. 返回 `uSmartTradeOpenApiResponse`。

### 12.2 交易开放 API Signer

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

输出 header 按端点 profile 生成。交易 API 第一版跟随官方 Python demo，默认交易 helper 至少包含：

- `Content-Type`
- `Authorization`，登录接口按 endpoint profile 不发送，登录后接口必填
- `X-Lang`
- `X-Channel`
- `X-Sign`

端点 profile 可额外启用：

- `X-Time`，Unix epoch milliseconds 字符串；交易 demo 默认 helper 未携带，不作为全局必填。
- `X-Dt`，设备类型数字字符串，默认 `"4"` 表示 Windows。
- `X-Type`，APP 类别数字字符串，默认 `"1"` 表示大陆版。
- `X-Request-Id`，官方 demo 在 `modify-order` 示例显式携带；`entrust-order` 不强制携带，依赖 body `serialNo` 和内部审计映射。

基础报价 API 和报价推送 API 不使用这个 signer；后续分别实现独立的报价 HTTP signer 和报价 WS auth。

### 12.3 Transport

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

## 13. 审计、日志和截图边界

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

## 14. 第一批实现验收

为了满足申请材料源码截图，同时不突破交易安全边界，第一批实现必须达到：

1. 有本地入口或应用服务方法：登录、下单、改单、撤单四个方法清晰存在。
2. 有 `TradingGateway` 层：交易动作默认在 `read_only` 被阻断。
3. 有 `uSmartOpenApiTradingAdapter` 层：能构造四类 endpoint 和 body。
4. 有交易开放 API client 层：能组装 request、调用交易 signer、调用 dry-run transport。
5. 有交易开放 API signer 接口：即使先用固定测试 key，也要展示交易 header 生成边界。
6. 有 `uSmartSensitiveFieldEncryptor` 接口：登录手机号、密码不以明文进入最终 request builder。
7. 有 `uSmartRequestIdPolicy`：生成或校验内部 `broker_request_id`、端点级 `X-Request-Id` 与 `serialNo`。
8. 有离线测试：断言登录、下单、改单、撤单请求体字段完整，且 read-only 下交易动作不出网。
9. 有脱敏测试：日志或 response summary 不包含 token、密码、手机号、私钥。
10. 默认配置不出网；真实 HTTP transport 必须显式配置并通过 [api/usmart-trade-runtime-config-profile.yaml](api/usmart-trade-runtime-config-profile.yaml) 校验才可启用。
11. 只读查询 request builder 和 mapper 覆盖 `open-assetQuery/v1`、`today-entrust`、`his-entrust`、`order-detail`、`stock-record`，并按 [api/usmart-trade-readonly-acceptance-matrix.yaml](api/usmart-trade-readonly-acceptance-matrix.yaml) 和 [usmart-readonly-integration-runbook.md](usmart-readonly-integration-runbook.md) 覆盖 endpoint profile、分页、空结果、未知枚举、`raw_ref`、401 显式重登和错误码映射。

## 15. 待官方确认项

以下事项不能靠代码猜测，必须从官方网页文档或盈立官方确认：

- 交易 API base URL：网页版官方文档给出生产 `https://open-jy.yxzq.com`、测试 `http://open-jy-uat.yxzq.com`，官方 Python demo 使用测试 `https://open-jy-uat.yxzq.com`；实现仍必须通过 `USMART_API_BASE_URL` 配置显式选择，默认 dry-run 不出网。
- 用户已确认：官方“测试环境接口地址”就是非生产测试环境，可用于联调且不触达生产交易/登录；本轮因项目范围仍只开放真实登录和只读查询，交易动作继续 dry-run。
- 项目策略已确认：第一版交易 API header 跟随官方 Python demo，`X-Time` 和 `X-Request-Id` 不作为全局必填；`modify-order` 额外携带 `X-Request-Id`；`entrust-order` 使用 body `serialNo` 和内部审计映射。`X-Request-Id` 长度按 30 位可配置字符串实现；下单 body `serialNo` 严格按最长 19 位实现。重复请求返回语义仍需官方确认。
- `X-Sign` 输出编码默认跟随官方 Python demo 使用标准 Base64，并通过配置允许切换 URL-safe Base64 和控制 `=` padding；签名原文已确认只使用最终发送的同一 JSON body 字符串，不拼接 header 字段。
- 隐私资料加密按官方 Python demo 的 `rsa_encrypt` transform 实现：RSA `PKCS1_v1_5` 加密后 URL-safe Base64；官方 demo README 和代码用法对应为 `public_key` -> `sensitive_encrypt_public_key`、`private_key` -> `trade_sign_private_key`。`common/utils.py` 的 PEM 包装反直觉，工程实现必须按 key role 校验，不照抄包装。它必须和 `X-Sign` 渠道签名密钥材料分离。
- uSmart 密钥角色、demo 槽位、env ref 和校验规则落盘在 [api/usmart-trade-key-material-profiles.yaml](api/usmart-trade-key-material-profiles.yaml)；官方来源材料可以来自 demo `public_key` / `private_key` 同名槽位，但运行时只按 `trade_sign_private_key`、`sensitive_encrypt_public_key` 等语义角色取 secret ref。
- 交易密码 `password` 指盈立交易 API request body 中的交易密码字段；普通下单、改单、撤单手册字段为可选。第一版保留字段抽象和加密能力，默认不发送，只有配置显式要求时才从 secret 读取并加密写入 body。
- 第一版 `trade_password_required=false`，因此默认不读取 `trade_password_secret_ref`，也不写入下单、改单、撤单 body；遇到券商要求交易密码、交易解锁或交易锁定时，订单进入 `blocked_by_broker_trade_lock`，停止自动交易并进入人工确认流程。
- 配置和代码变量名必须区分登录密码和交易密码：登录使用 `login_password_secret_ref` / `loginPasswordEncrypted`，交易使用 `trade_password_secret_ref` / `tradePasswordEncrypted`。只有最终映射到盈立官方 request body 时才使用官方字段名 `password`。
- token `expiration` 的精确格式、时区、包装路径（顶层或 `data`）和官方刷新接口语义；第一版项目策略已确认：内存 session、只读可显式重登、交易动作不隐式刷新、单账户单 session。
- IPO 改撤单接口的 `actionType` 枚举与普通股票委托不同，后续如接入 IPO 必须单独建模。
- 券商内部改单是原生修改还是 cancel + replace；本地 OMS 风险模型按 cancel + replace 处理。
- 订单明细 `orderStatus` 历史节点的完整枚举；已确认 `status` / `orderStatus` 和 `finalStateFlag` 都必须进入 OMS mapper，未知或冲突状态进入 `unknown_by_official_doc`。
- 券商响应状态完整提取；项目策略已确认必须按 endpoint 分组保留券商 raw code catalog，并映射到 Augur_Maestro gateway 错误码层。
- 美股碎股使用 `/stock-order-server/open-api/odd-entrust` 专用接口，不通过普通下单 `entrustProp` 建模；第一版内部按金额建模，发送给券商的 `entrustAmount` 为金额除以限价换算出的小数股数。最小金额、最小股数、数量精度、订单状态和撤单细节仍需后续按网页手册和 demo 继续细化。
- 第一版先按现金账户正股多头交易设计，`TradingGateway` 只承接正股买入卖出执行，止盈止损由策略模块产生普通交易意图；不启用自动对冲、做空、融资融券、保证金交易或美股期权；后续迭代再加入对冲、做空和美股期权。
