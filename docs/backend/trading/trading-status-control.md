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
| `risk_checking` | 正在执行风控检查 | 否 |
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
| `cancelled` | 券商确认撤单 | 是 |
| `cancel_rejected` | 券商拒绝撤单，原订单仍需继续跟踪 | 否 |
| `broker_rejected` | 券商明确拒绝委托 | 是 |
| `blocked_by_broker_trade_lock` | 券商要求交易解锁或账户交易锁定 | 否 |
| `failed` | 本地系统或提交前检查失败，确认未形成有效券商委托 | 是 |
| `unknown` | 状态未知，需要查询、对账或人工确认 | 否 |

允许流转：

```text
created
  -> risk_rejected
  -> manual_review_required
  -> ready_to_submit
  -> submitting
  -> submitted
  -> accepted
  -> partial_filled
  -> filled

accepted
  -> cancel_requested
  -> cancelled
  -> cancel_rejected

partial_filled
  -> cancel_requested
  -> cancelled
  -> filled

submitting
  -> submitted
  -> broker_rejected
  -> blocked_by_broker_trade_lock
  -> failed
  -> unknown

submitted
  -> accepted
  -> broker_rejected
  -> unknown

unknown
  -> submitted
  -> accepted
  -> partial_filled
  -> filled
  -> cancelled
  -> broker_rejected
  -> failed
```

禁止流转：

- `filled`、`cancelled`、`broker_rejected`、`risk_rejected`、`failed` 作为终态，不能自动回到可提交状态。
- `unknown` 不能自动重试下单或撤单；只能通过订单查询、成交查询、对账或人工确认转出。
- `cancel_rejected` 不是终态；订单仍可能继续成交或再次进入人工处理。
- `blocked_by_broker_trade_lock` 不能自动调用 `trade-login` 解除；必须进入人工确认或重新授权流程。

## 5. Gateway 请求生命周期状态

`GatewayRequestStatus` 表示单次 Gateway 调用或单次 broker HTTP / SDK 请求的生命周期。它不等同于订单状态。

| 状态 | 含义 | 是否终态 |
|---|---|---|
| `created` | Gateway 请求对象已创建 | 否 |
| `guard_blocked` | 被 mode、capability、transport 或 caller guard 阻断 | 是 |
| `signing` | 正在签名或构造请求 | 否 |
| `ready_to_send` | 请求已构造完成，准备发送 | 否 |
| `sending` | 正在发送到 broker transport | 否 |
| `sent` | 请求已发出，等待响应 | 否 |
| `response_received` | 收到 broker 或 transport 响应 | 否 |
| `mapped` | 响应已映射成内部 DTO 或错误 | 否 |
| `succeeded` | 请求成功完成 | 是 |
| `failed` | 请求明确失败 | 是 |
| `unknown` | 是否到达 broker 或业务状态无法判断 | 是 |

规则：

- 交易动作的 `unknown` 必须推动对应 OMS 订单进入 `unknown`。
- 只读查询的 `failed` 或 `unknown` 不能改变本地订单终态，只能记录审计和告警。
- `guard_blocked` 表示请求未触达适配器或 broker。

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
    CANCELLED = "cancelled"
    CANCEL_REJECTED = "cancel_rejected"
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

状态和错误码的关系示例：

| 场景 | 状态控制 | 错误码 |
|---|---|---|
| `read_only` 模式调用真实下单 | `GatewayRequestStatus.guard_blocked`，订单保持 `created` 或进入 `manual_review_required` | `broker.trading_disabled` |
| capability 关闭 | `GatewayRequestStatus.guard_blocked` | `broker.capability_disabled` |
| 下单请求超时，无法判断是否到达券商 | `GatewayRequestStatus.unknown`，`OmsOrderStatus.unknown` | `broker.timeout` |
| 券商明确废单或拒绝 | `OmsOrderStatus.broker_rejected` | `broker.order_rejected` |
| 券商状态字段缺失 | `BrokerOrderMappingStatus.raw_status_missing`，`OmsOrderStatus.unknown` | `broker.response_invalid` 或 `broker.order_state_unknown` |
| 需要交易解锁 | `BrokerTradeUnlockStatus.requires_trade_login`，`OmsOrderStatus.blocked_by_broker_trade_lock` | `broker.trade_locked` |

规则：

- 错误码可以解释状态变化原因，但不能替代状态字段。
- 状态字段用于控制下一步动作；错误码用于排查、展示和调用方处理建议。
- broker 官方 raw code 只能进入 raw catalog 或映射上下文，不能直接作为内部状态控制枚举。
