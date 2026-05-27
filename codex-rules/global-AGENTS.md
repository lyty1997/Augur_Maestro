# Augur_Maestro Codex 全局规范

本文是 Augur_Maestro 的 Codex 工作入口规范。开始任何任务前，必须先读取根目录 `AGENTS.md`，再按任务类型读取本目录下的相关规则和 `docs/README.md` 指向的设计文档。

## 优先级

1. 系统、开发者、用户的显式指令优先于本规范。
2. 根目录 `AGENTS.md` 是项目级最高规范。
3. `docs/` 是架构、交易链路、数据模型、风控、券商适配器和部署方式的真相源。
4. `codex-rules/` 是 Codex 执行任务时的操作规范，不能替代设计文档。

如规范之间存在冲突，默认选择更保守、更安全、更少影响真实资金的一项，并在回复中说明。

## 启动检查

每次任务开始时至少确认：

- 已读取 `AGENTS.md`。
- 已读取 `docs/README.md`。
- 若任务涉及交易、账户、订单、风控、券商、数据模型、部署或架构，已读取相关设计文档。
- 已检查 `codex-rules/known-issues.md` 和本次任务相关规则。
- 不写入、不打印 API Key、Secret、token、真实账户号、身份证明、真实资金或持仓隐私。

## 规则索引

- `rules/codex-workflow.md`：Codex 通用工作流。
- `rules/trading-safety-rules.md`：交易、风控、OMS、实盘安全规则。
- `rules/broker-openapi-rules.md`：券商 OpenAPI、miniQMT、盈立接口封装规则。
- `rules/python-coding-rules.md`：Python 编码规范。
- `rules/data-research-rules.md`：数据、研究、回测规范。
- `rules/frontend-react-rules.md`：React 前端和监控台规范。
- `rules/concurrency-resource-safety.md`：并发、资源生命周期和后台任务规范。
- `rules/markdown-docs.md`：Markdown 设计文档和图表规范。
- `rules/language.md`：语言、注释、解释风格规范。
- `rules/tool-failure.md`：工具失败处理规范。
- `rules/git-workflow.md`：Git 工作流规范。

## 交易安全底线

Augur_Maestro 的任何实盘相关能力都必须默认关闭。策略不得直接调用券商 API；真实下单、撤单、条件单、预埋单和任何改变券商侧订单状态的调用，必须先有设计文档、风控、OMS、人工确认入口、交易时间检查、账户/标的白名单、日志、对账和暂停机制。

M1 阶段默认只做研究、回测、数据采集、只读查询和干跑交易闭环。不得用真实下单或真实撤单接口做连通性探测、冒烟测试或权限测试。
