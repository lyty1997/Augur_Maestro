# RobustQuant 已知问题与注意事项

## PowerShell 与中文文件

Windows PowerShell 读取中文 Markdown、PDF 提取文本或券商文档时，优先显式指定 UTF-8：

```powershell
Get-Content -Encoding UTF8 docs/README.md
```

若输出出现乱码，先判断编码问题，不要直接修改原文件内容。

## 搜索与文件读取

- 优先使用 `rg` 和 `rg --files`。
- 如果 `rg` 不可用，再使用 PowerShell 的 `Get-ChildItem`、`Select-String`。
- 不要把大量无关文件一次性读入上下文；先通过目录和关键词定位。

## 券商官方资料与提取文本

券商网页、PDF、Markdown 转写文本、OCR 文本可能存在表格错位、字段遗漏、版本差异或繁简混杂。设计中引用券商行为时：

- 以当前指定的官方真相源为最终依据。
- uSmart / 盈立 OpenAPI 当前以官方网页文档为真相源，本地转换稿位于 `API_manual/uSmart/API_manual/`；历史 PDF/MinerU 转换稿不再作为当前依据。
- 官方 Python demo 只用于核对签名、加密、序列化和连接流程，不替代网页字段表；demo 配置中的账号、密码、token、私钥不得进入仓库提交。
- 无法从官方真相源确认的行为必须标记为 `待确认` 或 `unknown_by_official_doc`。
- 不得用猜测补齐签名、状态机、错误码、交易规则或真实接口地址。

## 盈立 OpenAPI 待确认项

当前已知文档存在或仍需确认的事项：

- `X-Request-Id` 与下单 body `serialNo` 是两类字段：`serialNo` 按最长 19 位处理，`X-Request-Id` 按端点 profile 决定是否外发；其有效期、重复请求返回语义和官方关系仍需券商确认。
- 交易开放 API、基础报价 API、报价推送 API 是三套独立 API；交易 signer 已按“稳定 JSON body 签名”建模，报价 HTTP / WS signer 仍需在各自文档中单独设计和验证。
- 普通下单响应 `data.entrustId` 已按订单 ID 建模；改单/撤单响应中的 `data.entrustId` 按申请编号处理，不覆盖原委托 ID。最终订单状态仍必须通过订单查询、成交流水、对账和 `finalStateFlag` 综合确认。
- 普通订单 `status` 已有官方枚举；订单明细 `orderStatus` 历史节点完整枚举、券商错误码 catalog 覆盖率、频率限制、IP 白名单、token `expiration` 格式和刷新语义仍需补充或联调确认。
- UAT 测试地址不自动等同 sandbox / paper trading；未获得盈立明确确认前，不运行真实下单、改单、撤单。

这些事项未确认前，不得把实现标记为完整生产可用。

## 实盘接口

不得调用真实下单、真实撤单、真实改单、条件单、预埋单或任何会改变券商侧状态的接口做测试。只读接口也需要保护账户隐私，日志和测试夹具必须脱敏。

## 文档状态

若发现 `docs/` 与代码或券商文档不一致，先更新设计文档并标记决策状态，再进入实现。
