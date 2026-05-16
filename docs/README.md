# RobustQuant 设计文档

本目录用于沉淀 RobustQuant 的项目设计文档。这里的文档面向项目内部研发和长期维护，和 `券商API/盈立/申请资料/RobustQuant_使用者手冊.docx` 这种券商申请材料分开管理。

## 目录结构

```text
docs/
  README.md
  00-project/          项目总览、路线图、术语和待决策问题
  10-research-data/    研究 Agent 与数据源路线
  20-m1/               M1 范围、工程、数据模型、接口、CLI/API、服务和前端
  30-trading/          交易安全、券商接入和盈立 OpenAPI 官方资料解析
  40-ops/              审计、日志、可观测性和隐私规范
```

## 文档索引

### 00-project：项目总览

- [01-architecture.md](00-project/01-architecture.md)：系统架构设计，区分 M1 当前研究回测架构与长期交易架构，描述模块边界、数据流、风控和部署方式。
- [02-glossary.md](00-project/02-glossary.md)：量化和交易系统常用术语表，方便后续讨论时统一语言。
- [03-open-decisions.md](00-project/03-open-decisions.md)：待确认的架构决策和问题清单。
- [05-technical-roadmap.md](00-project/05-technical-roadmap.md)：总体技术路线规划，定义项目里程碑、模块主线、交付顺序和验收标准。

### 10-research-data：研究与数据

- [04-research-agent.md](10-research-data/04-research-agent.md)：内嵌研究回测 Agent 设计，描述自动选股、因子挖掘、训练、回测、归因分析、模拟和报告生成流程。
- [06-data-source-roadmap.md](10-research-data/06-data-source-roadmap.md)：A 股历史数据源专项路线，定义 AKShare 启动源、第二数据源交叉验证、数据网关、标准表和未来切换券商数据源的路径。

### 20-m1：M1 详细设计

- [10-m1-scope.md](20-m1/10-m1-scope.md)：M1 交付范围硬边界，明确做什么、不做什么、哪些只做预留。
- [11-m1-implementation-plan.md](20-m1/11-m1-implementation-plan.md)：M1 实施路线图，把范围拆成可执行任务、依赖、DoD 和风险登记。
- [07-m1-engineering-design.md](20-m1/07-m1-engineering-design.md)：M1 工程设计，定义主题股票池、本地 PostgreSQL、CLI、后台任务暂缓、回测库验证和 Markdown 报告。
- [08-m1-data-model.md](20-m1/08-m1-data-model.md)：M1 数据模型设计，定义 PostgreSQL 表、字段、约束、状态和 kernel 归属。
- [09-m1-kernel-interfaces.md](20-m1/09-m1-kernel-interfaces.md)：M1 Kernel 接口类设计，定义 DTO、Protocol、服务接口和 CLI/API 调用边界。
- [12-m1-api-cli-contract.md](20-m1/12-m1-api-cli-contract.md)：M1 CLI / API / DTO / 日志契约，定义命令、错误码、响应和入口边界。
- [13-m1-service-specs.md](20-m1/13-m1-service-specs.md)：M1 核心服务行为规范，定义数据网关、股票池、研究任务、回测、归因和报告服务。
- [16-frontend-console-spec.md](20-m1/16-frontend-console-spec.md)：前端控制台设计规范，定义 M1 只读控制台和后续交易监控 UI 边界。

### 30-trading：交易安全与券商接入

- [14-trading-safety-spec.md](30-trading/14-trading-safety-spec.md)：交易安全、风控、OMS 和券商网关规范，作为后续模拟盘和实盘前置设计。
- [17-yingli-openapi-reference.md](30-trading/17-yingli-openapi-reference.md)：盈立 OpenAPI 官方文档解析说明，记录官方 PDF、接口能力和后续正式接入前的安全边界。
- [18-broker-trading-gateway-design.md](30-trading/18-broker-trading-gateway-design.md)：TradingGateway 统一券商交易网关模块设计，定义统一交易门面、适配器基类、盈立/miniQMT/Ptrade 派生、能力模式、幂等、错误映射、日志脱敏和测试策略。

### 40-ops：运维审计

- [15-observability-audit-spec.md](40-ops/15-observability-audit-spec.md)：审计、日志、可观测性和隐私规范，定义 trace、日志、敏感信息红线和数据血缘。

## 按问题找文档

| 我想知道... | 去哪份文档 |
|---|---|
| M1 到底做什么、不做什么 | [10-m1-scope.md](20-m1/10-m1-scope.md) |
| M1 先做哪些任务、依赖关系是什么 | [11-m1-implementation-plan.md](20-m1/11-m1-implementation-plan.md) |
| 总体架构和长期模块边界 | [01-architecture.md](00-project/01-architecture.md) |
| M1 数据库表、字段、约束 | [08-m1-data-model.md](20-m1/08-m1-data-model.md) |
| M1 Python DTO、Protocol、Service 接口 | [09-m1-kernel-interfaces.md](20-m1/09-m1-kernel-interfaces.md) |
| CLI 命令、API 响应、错误码和日志入口 | [12-m1-api-cli-contract.md](20-m1/12-m1-api-cli-contract.md) |
| 数据导入、质量检查、股票池、研究、回测和报告服务怎么工作 | [13-m1-service-specs.md](20-m1/13-m1-service-specs.md) |
| 真实交易前必须满足哪些安全条件 | [14-trading-safety-spec.md](30-trading/14-trading-safety-spec.md) |
| 统一券商交易网关怎么设计、盈立和 miniQMT 如何接入 | [18-broker-trading-gateway-design.md](30-trading/18-broker-trading-gateway-design.md) |
| 日志、审计、trace_id、敏感信息怎么处理 | [15-observability-audit-spec.md](40-ops/15-observability-audit-spec.md) |
| React 控制台能做什么、不能做什么 | [16-frontend-console-spec.md](20-m1/16-frontend-console-spec.md) |
| 盈立 OpenAPI 官方 PDF 怎么解析和使用 | [17-yingli-openapi-reference.md](30-trading/17-yingli-openapi-reference.md) |
| 当前还有哪些待决策问题 | [03-open-decisions.md](00-project/03-open-decisions.md) |

## 设计原则

1. 先保证实盘安全，再追求策略复杂度。
2. 先支持低频、可解释、可回放的交易流程，再考虑高阶 AI/LLM 能力。
3. 将券商接入、策略逻辑、风控、账户状态和数据存储解耦，避免一个模块出问题拖垮整个系统。
4. 所有自动交易行为都要可审计、可暂停、可撤销、可复盘。

## 维护原则

1. 范围先看 [10-m1-scope.md](20-m1/10-m1-scope.md)，任务先看 [11-m1-implementation-plan.md](20-m1/11-m1-implementation-plan.md)。
2. 每个专项 spec 是对应模块的真相源，架构文档只保留摘要和指针。
3. 涉及交易、风控、账户、订单、券商适配器、数据模型或部署方式变更时，先更新对应文档，再编码。
4. 不确定的券商 API 行为、交易规则和订单状态，不猜测为事实，统一进入 [03-open-decisions.md](00-project/03-open-decisions.md)。
5. 运行产物、密钥、真实账号和真实资金隐私不进入文档和代码库。
