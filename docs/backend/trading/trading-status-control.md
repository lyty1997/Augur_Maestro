# 交易模块状态控制枚举

版本：v0.1  
状态：设计草案，待用户确认  
最后更新：2026-05-28

## 0. 文档定位

本文档只定义交易模块的状态控制枚举、归属层级和流转约束，不定义 broker 官方错误码，也不定义 Augur_Maestro Gateway 错误码。

错误码的职责是说明“为什么失败或被阻断”；状态控制枚举的职责是说明“交易对象现在处于什么阶段，下一步允许做什么”。两者可以关联，但不能互相替代。

适用范围：

- 交易意图。
- 风控结果。
- OMS 本地订单。
- Gateway 请求生命周期。
- Broker 会话和交易解锁状态。
- Broker 订单状态映射结果。
- 对账状态。

不适用范围：

- M1 研究、数据导入、回测和报告状态。
- 券商官方 raw code catalog。
- `broker.*` Gateway 错误码 catalog。
- 行情基础报价 API 和报价推送 API 的订阅状态；它们后续由 `QuotationDataGateway` 单独定义。

## 0.1 实现阶段标签

本文档定义的所有状态枚举默认在 M2 模拟盘启用时全部进入实现范围（OMS、Gateway、风控、对账等模块的接口、DTO 和单元测试同步覆盖）。仅以下枚举值在第一版接口/DTO 中可以预留为 long-tail，等具体 broker 能力启用时再补实现与测试：

| 枚举 | 推迟项 | 推迟原因与启用条件 |
|---|---|---|
| `OmsOrderStatus` | `modify_requested` / `modify_pending` / `modify_rejected` | broker-trading-gateway.md §4 第一版默认禁用改单 capability，风险模型采用 cancel + replace；待 M3 改单 capability 启用、且对应 broker 改单语义官方确认后再实现 |
| `BrokerTradeUnlockStatus` | `requires_trade_login` 分支的自动处理逻辑 | 第一版不自动调用 `trade-login`，订单进入 `blocked_by_broker_trade_lock` 等人工；状态值本身保留，但状态机自动转出逻辑推迟 |

其它所有状态值都按 core 处理，自 M2 模拟盘第一版起接口和测试必须覆盖。

## 1. 分层原则

交易状态按对象归属分层，不能用一个大枚举混用所有状态。

| 层级 | 枚举 | 归属模块 | 说明 |
|---|---|---|---|
| 策略到交易链路入口 | `TradeIntentStatus` | strategy / risk 前置边界 | 交易意图状态，不代表订单 |
| 风控 | `RiskCheckStatus` | risk | 风控检查结果 |
| OMS | `OmsOrderStatus` | OMS | 本地订单状态，是交易主状态机 |
| Gateway 请求 | `GatewayRequestStatus` | TradingGateway | 单次 broker 请求生命周期 |
| Broker 会话 | `BrokerSessionStatus` | BrokerTradingAdapter | 登录态、连接态和认证状态 |
| Broker 交易解锁 | `BrokerTradeUnlockStatus` | BrokerTradingAdapter / OMS | 券商交易权限是否可用 |
| Broker 订单映射 | `BrokerOrderMappingStatus` | mapper | 券商订单状态映射结果 |
| 对账 | `ReconciliationStatus` | reconciliation | 本地记录与券商事实是否一致 |

代码实现时建议放在：

```text
src/
  rq_core/
    broker_kernel/
      statuses.py
```

`statuses.py` 只包含稳定状态枚举和流转辅助函数，不读取配置、不调用券商、不包含错误码映射表。

## 2. 交易意图状态

`TradeIntentStatus` 表示策略或人工流程产生的交易意图所处阶段。交易意图不是订单，不能直接发给券商。

| 状态 | 含义 | 是否终态 |
|---|---|---|
| `created` | 意图已创建，尚未进入风控 | 否 |
| `pending_review` | 等待人工审核或等待交易窗口重新检查 | 否 |
| `risk_rejected` | 被风控拒绝 | 是 |
| `approved` | 风控通过，允许进入 OMS 创建订单 | 否 |
| `converted_to_order` | 已生成本地 OMS 订单 | 是 |
| `expired` | 意图过期，不能继续使用 | 是 |
| `cancelled` | 用户或系统取消意图 | 是 |

规则：

- 非交易时间触发的策略信号只能进入 `pending_review`，不能直接进入 `approved`。
- `approved` 必须有有效期；过期后进入 `expired`，不能复用旧风控结果。
- `converted_to_order` 之后由 OMS 订单状态接管。

## 3. 风控结果状态

`RiskCheckStatus` 表示一次风控检查结果。

| 状态 | 含义 | 是否允许继续 |
|---|---|---|
| `approved` | 风控通过 | 是 |
| `rejected` | 明确拒绝 | 否 |
| `requires_manual_review` | 需要人工复核 | 否 |
| `degraded` | 降级通过或仅允许降低风险暴露 | 条件允许 |
| `paused` | 全局、账户或策略暂停 | 否 |

规则：

- `requires_manual_review` 不能被程序自动转为 `approved`。
- `degraded` 必须携带限制条件，例如只允许减仓、禁止开仓、缩小订单金额。
- 风控状态不是 OMS 订单状态；风控拒绝后，如果已经有本地订单，订单状态应进入 `risk_rejected`。

## 4. OMS 本地订单状态

`OmsOrderStatus` 是交易模块的主状态机。所有真实下单、改单、撤单都必须围绕本地订单状态推进。

| 状态 | 含义 | 是否终态 |
|---|---|---|
| `created` | 本地订单已创建，未触达券商 | 否 |
| `risk_rejected` | 本地订单被风控拒绝 | 是 |
| `manual_review_required` | 需要人工确认，未允许提交券商 | 否 |
| `ready_to_submit` | 已满足提交前置条件 | 否 |
| `submitting` | 正在提交券商 | 否 |
| `submitted` | 请求已发出，但券商是否接受仍待确认 | 否 |
| `accepted` | 券商已接受委托 | 否 |
| `partial_filled` | 部分成交 | 否 |
| `filled` | 全部成交 | 是 |
| `cancel_requested` | 撤单请求已发起 | 否 |
| `cancel_pending` | 券商已收到或订单查询显示正在等待撤单 | 否 |
| `cancelled` | 券商确认撤单 | 是 |
| `cancel_rejected` | 券商拒绝撤单，原订单仍需继续跟踪 | 否 |
| `modify_requested` | 改单请求已发起 | 否 |
| `modify_pending` | 券商已收到或订单查询显示正在等待改单 | 否 |
| `modify_rejected` | 券商拒绝改单，原订单仍需继续跟踪 | 否 |
| `partial_cancelled` | 部分成交后剩余数量已撤销 | 是 |
| `broker_rejected` | 券商明确拒绝委托 | 是 |
| `blocked_by_broker_trade_lock` | 券商要求交易解锁或账户交易锁定 | 否 |
| `failed` | 本地系统或提交前检查失败，确认未形成有效券商委托 | 是 |
| `unknown` | 状态未知，需要查询、对账或人工确认 | 否 |

流转原则：

- 本地请求驱动流转：由 OMS、风控或 Gateway 调用前置检查推动，例如 `ready_to_submit -> submitting`、`accepted -> cancel_requested`。
- 券商事实驱动流转：由订单查询、成交查询、对账或人工确认推动。券商事实可以跳过中间态，例如本地 `submitted` 后直接查到 `filled`。
- 权威券商事实优先于本地预期，但未知、缺失或冲突的券商状态不能猜测，必须进入 `unknown`。
- `cancel_pending` 和 `modify_pending` 表示券商侧异步处理中的订单，不表示撤单或改单已经成功。
- `partial_cancelled` 表示订单生命周期结束，但已经发生部分成交；后续持仓、资金和成交记录必须按已成交部分入账。

允许流转：

```text
created
  -> risk_rejected
  -> manual_review_required
  -> ready_to_submit

manual_review_required
  -> ready_to_submit
  -> risk_rejected
  -> failed

ready_to_submit
  -> submitting
  -> manual_review_required
  -> blocked_by_broker_trade_lock
  -> failed

submitting
  -> submitted
  -> accepted
  -> partial_filled
  -> filled
  -> broker_rejected
  -> blocked_by_broker_trade_lock
  -> failed
  -> unknown

submitted
  -> accepted
  -> partial_filled
  -> filled
  -> cancelled
  -> partial_cancelled
  -> broker_rejected
  -> unknown

accepted
  -> partial_filled
  -> filled
  -> cancel_requested
  -> modify_requested
  -> broker_rejected
  -> unknown

partial_filled
  -> cancel_requested
  -> modify_requested
  -> filled
  -> partial_cancelled
  -> unknown

cancel_requested
  -> cancel_pending
  -> cancelled
  -> partial_cancelled
  -> cancel_rejected
  -> partial_filled
  -> filled
  -> unknown

cancel_pending
  -> cancelled
  -> partial_cancelled
  -> cancel_rejected
  -> partial_filled
  -> filled
  -> unknown

cancel_rejected
  -> accepted
  -> partial_filled
  -> filled
  -> cancel_requested
  -> modify_requested
  -> unknown

modify_requested
  -> modify_pending
  -> accepted
  -> partial_filled
  -> filled
  -> modify_rejected
  -> unknown

modify_pending
  -> accepted
  -> partial_filled
  -> filled
  -> partial_cancelled
  -> modify_rejected
  -> unknown

modify_rejected
  -> accepted
  -> partial_filled
  -> filled
  -> cancel_requested
  -> modify_requested
  -> unknown

blocked_by_broker_trade_lock
  -> manual_review_required
  -> failed
  -> unknown

unknown
  -> submitted
  -> accepted
  -> partial_filled
  -> filled
  -> cancel_pending
  -> cancelled
  -> cancel_rejected
  -> modify_pending
  -> modify_rejected
  -> partial_cancelled
  -> broker_rejected
  -> blocked_by_broker_trade_lock
  -> failed
```

禁止流转：

- `filled`、`cancelled`、`partial_cancelled`、`broker_rejected`、`risk_rejected`、`failed` 作为终态，不能自动回到可提交状态。
- `unknown` 不能自动重试下单、改单或撤单；只能通过订单查询、成交查询、对账或人工确认转出。
- `cancel_rejected` 和 `modify_rejected` 不是终态；原订单仍可能继续成交或再次进入人工处理。
- `cancel_pending` 不能再次自动发起撤单；必须等待查询、对账或人工确认。
- `modify_pending` 不能再次自动发起改单；必须等待查询、对账或人工确认。
- `blocked_by_broker_trade_lock` 不能自动调用 `trade-login` 解除；必须进入人工确认或重新授权流程。

动作约束：

| 当前状态 | 允许自动提交下单 | 允许发起撤单 | 允许发起改单 | 处理要求 |
|---|---|---|---|---|
| `created`、`manual_review_required`、`ready_to_submit` | 仅 `ready_to_submit` 可提交 | 否 | 否 | 提交前重新检查风控、交易时间、白名单和对账 |
| `submitting`、`submitted`、`unknown` | 否 | 否 | 否 | 等待 Gateway 结果、查询、对账或人工确认 |
| `accepted`、`partial_filled` | 否 | 条件允许 | 条件允许 | 撤单或改单前重新检查交易时间、券商状态和权限 |
| `cancel_requested`、`cancel_pending` | 否 | 否 | 否 | 等待撤单结果；不能重复撤单 |
| `cancel_rejected` | 否 | 条件允许 | 条件允许 | 原订单继续跟踪；再次操作必须重新检查 |
| `modify_requested`、`modify_pending` | 否 | 否 | 否 | 等待改单结果；不能重复改单 |
| `modify_rejected` | 否 | 条件允许 | 条件允许 | 原订单继续跟踪；再次操作必须重新检查 |
| `blocked_by_broker_trade_lock` | 否 | 否 | 否 | 人工确认或重新授权后才能重新进入提交前状态 |
| 终态 | 否 | 否 | 否 | 只能用于查询、对账、复盘和审计 |

改单规则：

- 第一版默认按保守的 cancel + replace 风险模型理解改单：改单失败时原订单继续有效，不能假设原订单已经撤销。
- 若某个 broker 官方确认支持原生改单，OMS 仍必须保留原委托 ID、改单申请 request_id、改单前后价格和数量。
- 若改单成功后 broker 返回新的委托 ID，必须创建或关联新的本地订单记录，原订单进入对应终态或关联状态；在该行为被官方确认前，相关状态进入 `unknown` 或 `modify_pending`，不得猜测。
- 部分成交订单改单时，风控必须按剩余未成交数量计算，不得按原始委托数量重复计算。

## 5. Gateway 请求生命周期状态

`GatewayRequestStatus` 表示单次 Gateway 调用或单次 broker HTTP / SDK 请求的生命周期。它不等同于订单状态。**只保留调用方、审计和 UI 需要 switch 的可观察状态**；client 内部 pipeline 的签名、序列化、HTTP 发送、响应解析、mapper 映射等处理阶段不作为顶层枚举，统一通过审计事件 metadata（trace span 时间戳 + `phase` 标签）观察。

| 状态 | 含义 | 是否终态 |
|---|---|---|
| `created` | Gateway 请求对象已创建 | 否 |
| `guard_blocked` | 被 mode、capability、transport 或 caller guard 阻断，请求未触达适配器/broker | 是 |
| `sending` | 已通过 guard，正在调用适配器/transport，等待响应 | 否 |
| `succeeded` | 请求成功完成并已映射 | 是 |
| `failed` | 请求明确失败（含本地构造错、broker 业务拒绝、响应不可解析等） | 是 |
| `unknown` | 是否到达 broker 或业务状态无法判断 | 是 |

规则：

- 交易动作的 `unknown` 必须推动对应 OMS 订单进入 `unknown`。
- 只读查询的 `failed` 或 `unknown` 不能改变本地订单终态，只能记录审计和告警。
- `guard_blocked` 表示请求未触达适配器或 broker。
- 签名、序列化、HTTP 发送、响应解析、mapper 映射等内部 phase 不进入本枚举；它们作为审计事件的 `metadata.phase` 标签和 trace span 时间戳记录，便于排查但不参与业务流转判断。

## 6. Broker 会话状态

`BrokerSessionStatus` 表示 broker 适配器维护的登录和连接状态。

| 状态 | 含义 |
|---|---|
| `disconnected` | 未连接或本地 session 已清理 |
| `connecting` | 正在登录或连接 |
| `connected` | 已建立可用 session |
| `auth_expired` | token 或登录态过期 |
| `auth_failed` | 登录失败或凭证错误 |
| `permission_denied` | 账号、IP 白名单或 API 权限不足 |
| `restricted` | 账户受限 |
| `unknown` | 无法确认 session 状态 |

规则：

- 只读查询遇到 `auth_expired` 可以按 profile 显式重新登录并使用新的 request_id。
- 交易动作过程中不能隐式刷新登录后继续提交；必须回到 OMS 可审计流程。
- `permission_denied`、`restricted` 和 `unknown` 默认阻断交易动作。

## 7. Broker 交易解锁状态

`BrokerTradeUnlockStatus` 表示券商侧交易权限或交易密码解锁状态。

| 状态 | 含义 |
|---|---|
| `not_required` | 当前 broker 或账户不要求额外交易解锁 |
| `unlocked` | 已解锁，可继续走后续风控和 OMS |
| `locked` | 交易被锁定 |
| `requires_trade_login` | 需要交易密码或交易解锁动作 |
| `unknown` | 无法确认 |

规则：

- `requires_trade_login` 不等于允许自动调用 `trade-login`。
- `locked`、`requires_trade_login`、`unknown` 必须阻断真实下单、改单和撤单。
- 对应 OMS 订单状态进入 `blocked_by_broker_trade_lock`，并记录人工处理原因。

## 8. Broker 订单映射状态

`BrokerOrderMappingStatus` 表示 mapper 对券商订单状态字段的理解结果。它不是 broker 官方 raw status，也不是 Gateway 错误码。

| 状态 | 含义 |
|---|---|
| `mapped` | 已按官方文档或已确认 profile 映射到 `OmsOrderStatus` |
| `raw_status_unknown` | 券商返回了未知 raw status |
| `raw_status_conflict` | `status`、`orderStatus`、`finalStateFlag` 冲突 |
| `raw_status_missing` | 必要状态字段缺失 |
| `unknown_by_official_doc` | 官方文档未确认语义，不能猜测 |

规则：

- `mapped` 才能推动 OMS 订单进入明确状态。
- 其他状态必须推动 OMS 订单进入 `unknown`，并把具体原因写入 `unknown_reason` 或审计 metadata。
- `unknown_by_official_doc` 是映射原因，不是 OMS 订单状态；OMS 对外状态仍然是 `unknown`。
- `finalStateFlag=1` 只能作为终态辅助条件，不能单独决定本地订单终态。

## 9. 对账状态

`ReconciliationStatus` 表示本地记录与券商事实的对账结果。

| 状态 | 含义 | 是否允许自动交易 |
|---|---|---|
| `not_checked` | 尚未完成对账 | 受限 |
| `matched` | 本地与券商一致 | 允许 |
| `mismatch_detected` | 发现订单、成交、持仓或资金不一致 | 不允许 |
| `broker_state_unknown` | 券商侧状态无法确认 | 不允许 |
| `manual_review_required` | 需要人工确认 | 不允许 |
| `manual_confirmed` | 人工已确认处理结论 | 视处理结论 |

规则：

- `mismatch_detected`、`broker_state_unknown` 和 `manual_review_required` 默认暂停相关账户、标的或策略的自动交易。
- 人工确认后不能直接恢复全局交易；必须明确恢复范围和恢复原因。

## 10. DTO 字段约定

交易模块 DTO 应使用上述枚举，不使用裸字符串表达核心状态。

示例：

```python
from enum import Enum


class OmsOrderStatus(str, Enum):
    CREATED = "created"
    RISK_REJECTED = "risk_rejected"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"
    READY_TO_SUBMIT = "ready_to_submit"
    SUBMITTING = "submitting"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    PARTIAL_FILLED = "partial_filled"
    FILLED = "filled"
    CANCEL_REQUESTED = "cancel_requested"
    CANCEL_PENDING = "cancel_pending"
    CANCELLED = "cancelled"
    CANCEL_REJECTED = "cancel_rejected"
    MODIFY_REQUESTED = "modify_requested"
    MODIFY_PENDING = "modify_pending"
    MODIFY_REJECTED = "modify_rejected"
    PARTIAL_CANCELLED = "partial_cancelled"
    BROKER_REJECTED = "broker_rejected"
    BLOCKED_BY_BROKER_TRADE_LOCK = "blocked_by_broker_trade_lock"
    FAILED = "failed"
    UNKNOWN = "unknown"
```

DTO 规则：

- `BrokerOrderAck.status` 使用 `OmsOrderStatus`。
- `BrokerOrderSnapshot.status` 使用 `OmsOrderStatus`，并保留 `broker_status_raw` 和 `final_state_flag`。
- `BrokerTradeUnlockStatus` 使用同名枚举，不用布尔值表达。
- 单次请求审计记录使用 `GatewayRequestStatus`。
- `unknown` 必须携带 `unknown_reason`、`raw_ref` 或可审计 metadata。

## 11. 和错误码的关系

错误码可以解释状态变化原因，但不能替代状态字段。状态字段用于控制下一步动作；错误码用于排查、展示和调用方处理建议。broker 官方 raw code 只能进入 raw catalog 或映射上下文，不能直接作为内部状态控制枚举。

下表按 [broker-gateway-error-codes.yaml](broker-gateway-error-codes.yaml) 的 category 列出全部 24 个稳定 gateway 错误码到状态控制枚举的映射。`OmsOrderStatus` 列只适用于"该错误码对应的请求正在驱动一个 OMS 订单"的场景；只读查询、登录、对账等非订单请求只更新 `GatewayRequestStatus`，不变更订单状态。

### 11.1 success

| Gateway 错误码 | GatewayRequestStatus | OmsOrderStatus | 说明 |
|---|---|---|---|
| `broker.ok` | `succeeded` | 按 broker 返回推进到 `submitted` / `accepted` / `partial_filled` / `filled` / `cancelled` 等；下单 HTTP 成功 ≠ 订单终态 | 正常成功 |

### 11.2 capability_guard（请求未触达适配器或 broker）

| Gateway 错误码 | GatewayRequestStatus | OmsOrderStatus | 说明 |
|---|---|---|---|
| `broker.disabled` | `guard_blocked` | 保持当前状态 | `mode=disabled` |
| `broker.trading_disabled` | `guard_blocked` | Gateway 不直接改 OMS；OMS 可基于阻断结果显式进入 `manual_review_required` | `mode != live_guarded` 或 `trading_enabled=false` |
| `broker.capability_disabled` | `guard_blocked` | Gateway 不直接改 OMS；OMS 可显式进入 `manual_review_required` | capability 为 false |
| `broker.unsupported_capability` | `guard_blocked` | Gateway 不直接改 OMS；OMS 可显式进入 `manual_review_required` | broker 适配器声明不支持 |
| `broker.real_http_disabled` | `guard_blocked` | Gateway 不直接改 OMS；OMS 可显式进入 `manual_review_required` | transport 出网开关未开 |
| `broker.caller_not_allowed` | `guard_blocked` | Gateway 不直接改 OMS；OMS 可显式进入 `manual_review_required` 或安全失败状态 | 调用方不是允许的应用服务/OMS |

### 11.3 auth

| Gateway 错误码 | GatewayRequestStatus | OmsOrderStatus | 说明 |
|---|---|---|---|
| `broker.auth_missing` | `failed` | 交易动作 `failed`（请求未触达 broker） | 会话或凭证引用缺失 |
| `broker.auth_expired` | 只读：`failed` 后允许显式重登一次再发新请求；交易：`failed` | 只读查询不变更订单 | 401 + 只读 endpoint；下单类 endpoint 的 401 见 `broker.order_state_unknown` |
| `broker.auth_failed` | `failed` | 交易动作 `failed`（请求未触达） | 凭证错 |
| `broker.captcha_required` | `failed` | 订单进入 `manual_review_required`，等人工启动验证码流程 | 需短信验证码 |
| `broker.trade_locked` | `failed` | `blocked_by_broker_trade_lock`，同时 `BrokerTradeUnlockStatus.requires_trade_login` | 券商要求交易解锁；不自动调 `trade-login` |
| `broker.permission_denied` | `failed` | 交易动作 `failed`（请求被 broker 拒、未形成委托） | 权限不足 |
| `broker.account_restricted` | `failed` | 交易动作 `failed`；OMS/Risk 阻断该账户后续自动交易 | 账户受限或被锁；含验证码次数超限的账号级锁 |
| `broker.ip_not_allowed` | `failed` | 交易动作 `failed`（请求被 broker 拒） | IP 白名单 |

### 11.4 request（本地构造错误，请求未触达 broker）

| Gateway 错误码 | GatewayRequestStatus | OmsOrderStatus | 说明 |
|---|---|---|---|
| `broker.sign_failed` | `failed` | 交易动作 `failed` | 密钥配置或签名规则错 |
| `broker.bad_request` | `failed` | 交易动作 `failed` | DTO/字段映射/参数错 |
| `broker.unsupported_order_type` | `failed` | 交易动作 `failed`（Gateway 阻断） | 订单类型超出 capability 允许范围 |
| `broker.endpoint_not_found` | `failed` | 交易动作 `failed` | endpoint 拼错或环境错 |

### 11.5 rate_limit

| Gateway 错误码 | GatewayRequestStatus | OmsOrderStatus | 说明 |
|---|---|---|---|
| `broker.rate_limited` | 只读：`failed` 后按 retry profile 退避重试；交易：`failed`（绝不自动重试） | 不变（交易动作此码意味着未真正发出或被 gateway 拦截） | 请求级频控；账号级锁定走 `broker.account_restricted` |

### 11.6 transport（无法判断请求是否抵达 broker，必须保守）

| Gateway 错误码 | GatewayRequestStatus | OmsOrderStatus | 说明 |
|---|---|---|---|
| `broker.transport_error` | `unknown` | 交易动作进 `unknown`，必须对账 | DNS/连接/TLS 错 |
| `broker.timeout` | `unknown` | 交易动作进 `unknown`，必须对账 | 超时 |
| `broker.service_unavailable` | 只读：`failed`；交易：`unknown` | 交易动作进 `unknown` | broker 服务不可用 |

### 11.7 broker_business

| Gateway 错误码 | GatewayRequestStatus | OmsOrderStatus | 说明 |
|---|---|---|---|
| `broker.order_rejected` | `failed`（已 mapped） | `broker_rejected` | broker 明确拒单，已形成响应 |

### 11.8 response_mapping

| Gateway 错误码 | GatewayRequestStatus | OmsOrderStatus | 说明 |
|---|---|---|---|
| `broker.response_invalid` | `failed`（mapper 无法解析） | `unknown`，关联 `BrokerOrderMappingStatus.raw_status_missing` 或 `raw_status_conflict` | 响应缺字段/结构错，订单实际状态不可知 |
| `broker.order_state_unknown` | `unknown` | `unknown` | 下单类 endpoint 的 401 / 终态字段冲突 / 状态无法判定 |
| `broker.unclassified` | `failed`（兜底） | `unknown`（保守） | 未映射的 raw 响应；保留 `raw_ref` 供后续审计补映射 |

### 11.9 跨层一致性约束

- 所有 `OmsOrderStatus = unknown` 路径必须同时关联 `GatewayRequestStatus = unknown` 或带 `unknown_reason` 元数据。
- 所有 `GatewayRequestStatus = guard_blocked` 的请求一定未触达 broker；Gateway 层不得直接变更 OMS。若需要把订单转入 `manual_review_required` 或其他安全状态，必须由 OMS 在接收 guard 结果后显式执行本地状态流转，并记录独立审计事件。
- 交易动作的错误码即使 retryable=true，也必须由 OMS 显式发起新请求（带新 `order_id` 或新 `broker_request_id`），不由 client/transport 自动补偿。
- raw code 到 gateway 错误码的映射由 [usmart-trade-error-codes.draft.yaml](../clients/api/usmart-trade-error-codes.draft.yaml) 维护；其 `endpoint_scoping_invariants` 段列出已激活的按 endpoint 差异化规则（当前仅 HTTP 401 区分写动作 endpoint，写动作 401 映射到 `broker.order_state_unknown`）。
