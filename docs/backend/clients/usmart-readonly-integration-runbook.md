# uSmart 只读联调运行手册

版本：v0.1  
状态：设计草案，待实现时执行  
最后更新：2026-05-26

## 0. 目标

本文档定义第一批 uSmart / 盈立交易开放 API 只读联调的执行顺序和停机条件。它不替代接口 profile；实际断言以以下机器可读文件为准：

- [api/usmart-trade-endpoint-profiles.yaml](api/usmart-trade-endpoint-profiles.yaml)
- [api/usmart-trade-runtime-config-profile.yaml](api/usmart-trade-runtime-config-profile.yaml)
- [api/usmart-trade-readonly-acceptance-matrix.yaml](api/usmart-trade-readonly-acceptance-matrix.yaml)
- [../trading/broker-gateway-raw-record-profile.yaml](../trading/broker-gateway-raw-record-profile.yaml)

本轮只允许真实登录和只读查询：资产、持仓、今日订单、历史订单、订单明细、成交流水。`trade-login`、下单、改单、撤单、IPO 申购和 IPO 改单不得触达真实 HTTP。

## 1. 角色和前置确认

执行前必须确认：

- 操作者明确知道本轮不是交易联调。
- `USMART_API_BASE_URL` 已显式选择生产或官方测试环境；选择官方测试环境也不扩大本轮只读范围。
- IP 白名单、渠道号、登录 profile、key role 绑定和审计存储均已准备。
- `configs/broker/usmart.yaml` 仍为 `mode=read_only`、`trading_enabled=false`。
- `transport.allow_real_http_readonly=true` 只在真实只读联调配置中开启；申请材料截图配置必须保持 `false`。
- `capabilities.trade_login`、`place_order`、`odd_lot_order`、`modify_order`、`cancel_order`、`odd_lot_cancel` 全部为 `false`。

若以上任一项不满足，停止联调，保持 dry-run。

## 2. 执行顺序

### Step 0：离线配置和 profile 校验

先运行离线校验，且不得加载真实账号、密码、token 或券商下发密钥原文。

必须通过：

- endpoint profile 可解析，且第一批只读 endpoint 均为 `operation_kind=login|readonly`。
- runtime config profile 可解析，且 `usmart_readonly_integration_v1` 校验通过。
- key material profile 可解析，运行时只绑定 `trade_sign_private_key` 和 `sensitive_encrypt_public_key` 等语义角色。
- session/retry profile 可解析，只读 `max_retries=2`，交易动作 `max_retries=0`。
- raw record profile 可解析，`credential_secret` 和完整 HTTP 原文不可持久化。
- acceptance matrix 的全部 required offline contract cases 通过。

失败处理：记录 `trace_id`、失败 profile、失败 validation rule，停止，不允许安装真实 HTTP transport。

### Step 1：dry-run 安全回归

在真实 HTTP 关闭时运行：

- 登录 request builder dry-run。
- 资产/持仓 request builder dry-run。
- 今日订单、历史订单、订单明细、成交流水 request builder dry-run。
- 下单、碎股下单、改单、撤单、`trade-login` 阻断测试。

必须确认：

- dry-run suite 不产生任何真实 HTTP。
- 交易动作被 Gateway 或 capability guard 阻断。
- 普通日志不包含 token、密码、私钥、完整手机号、完整账号、完整资金和完整持仓市值。

失败处理：停止；不要尝试用真实只读 HTTP 排查 dry-run 基础错误。

### Step 2：启用真实只读 HTTP 配置

只在 Step 0 和 Step 1 都通过后，加载真实只读联调配置。

必须再次校验：

- runtime config validation 通过。
- audit store 可写入 `request_summary`。
- raw record profile validation 通过。
- `RealHttpTransport` 只对 login/readonly operation kind 可安装。
- 交易 endpoint 的 `real_http_allowed_in_readonly=false`。

失败处理：保持 dry-run 或启动失败；不得降级为“部分真实 HTTP”继续执行。

### Step 3：登录 smoke

执行密码登录 smoke。

必须记录：

- `trace_id`
- `broker_request_id`
- endpoint
- HTTP 状态码
- broker `code`
- token fingerprint
- `expiration` 原始值和解析结果
- `raw_hash`
- `raw_ref`

禁止记录：

- token 原文
- 手机号原文
- 登录密码
- 私钥
- 完整 HTTP response 文本

失败处理：

- 认证、签名、IP 白名单、base URL、渠道号错误时停止。
- 登录响应同时存在顶层 `token` 和 `data.token` 且不一致时，返回 `broker.response_invalid`，不安装 session。

### Step 4：资产和持仓 smoke

调用 `/asset-center-server/open-api/open-assetQuery/v1`。

必须确认：

- 可以生成 `AccountSnapshot` / `CashSnapshot`。
- 可以生成 `PositionSnapshot` 集合；无持仓时返回空集合而不是错误。
- `assetSingleInfoRespVOS` 和 `holdInfos` 的 mapper 输入保存为 redacted structured payload。
- 控制台只显示整理后的账户摘要和持仓表，不显示原始 JSON。

失败处理：

- 如果 endpoint 权限不可用，不静默切换到 `demo_stock_holding`。
- 如需启用 `/stock-order-server/open-api/stock-holding` fallback，必须先补 raw error catalog、endpoint profile 和单独审批。

### Step 5：订单和成交 smoke

按顺序执行：

1. 今日订单：`today-entrust`
2. 历史订单：`his-entrust`
3. 成交流水：`stock-record`
4. 订单明细：`order-detail`

分页规则：

- 默认 `pageNum=1`、`pageSize=10`。
- `pageSize` 最大 20。
- `today_entrust` 的 demo-compatible `pageNum=0` 默认不启用；若要验证，只能作为单独兼容实验记录。

订单明细规则：

- 只有当今日或历史订单返回可用 `entrustId` 或 `serialNo` 时才执行真实 `order-detail` smoke。
- 如果账户没有可用订单，记录 skip reason：`no_known_order_for_order_detail_smoke`。
- skip 不影响 Phase 2 退出，但 order-detail offline contract 必须通过。

失败处理：

- `code=0` 且 `data.list=[]` 映射为空 Page。
- `code=0` 但 `data` 缺失，或分页接口 `list` 缺失且未确认合法，映射为 `unknown_response`。
- 未知状态码或未知枚举保留 raw，内部映射为 `unknown_by_official_doc`，不得猜测。

### Step 6：401 / session 过期路径

优先用模拟或受控 fixture 验证；只有在不会触发异常账号安全策略时才用真实联调验证。

必须确认：

- 401 或 broker auth-expired 会把 session 标为 stale。
- 只读路径最多显式重登一次。
- 重登后的查询使用新的 `broker_request_id`。
- 失败请求 ID 不复用。
- 交易动作路径不做隐式重登。

失败处理：停止真实联调；这属于 session/retry 安全边界错误。

### Step 7：收尾和记录

联调结束后必须产出记录：

- 执行日期和操作者。
- base URL 是生产还是官方测试环境。
- profile 版本和配置哈希。
- 每个 endpoint 的结果：passed / failed / skipped。
- `order_detail` 若 skipped，记录 skip reason。
- 发现的官方文档差异和需要回填的 profile 字段。
- 审计存储抽查结果：能通过 `raw_ref` 查到受控结构化记录，普通日志不含 raw payload。

不允许在总结中粘贴真实资金、真实持仓、token、完整账号、手机号或 HTTP 原文。

## 3. 立即停止条件

出现任一情况，立即停止真实 HTTP：

- 任何交易 endpoint 被调用或即将被调用。
- `trade-login` 被调用或即将被调用。
- `trading_enabled=true`。
- 真实 HTTP 配置绕过 runtime config validation。
- 审计 `request_summary` 写入失败。
- 日志出现 token、密码、私钥、完整手机号、完整账号或完整 HTTP response。
- 登录响应 token 结构冲突。
- 只读 401 后复用失败 request id。
- mapper 把缺失 `data` 伪造成空成功结果。

## 4. 联调后必须回填

联调完成后更新：

- 登录 token / expiration 的真实包装路径、格式和时区。
- `open-assetQuery/v1` 是否完整覆盖资产和持仓需求。
- 每个分页接口的空结果结构。
- `today_entrust pageNum=0` 与 `pageNum=1` 的真实差异。
- `stock-record beginTime/endTime` 的闭区间和最大跨度。
- 订单明细 `orderStatus` 历史节点和状态流转枚举。
- uSmart raw code catalog 的缺口和新增映射。
