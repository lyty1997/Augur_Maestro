# RobustQuant 设计文档

本目录用于沉淀 RobustQuant 的项目设计文档。这里的文档面向项目内部研发和长期维护，和 `券商API/盈立/申请资料/RobustQuant_使用者手冊.docx` 这种券商申请材料分开管理。

## 目录结构

```text
docs/
├── README.md
├── architecture/                       架构、安全边界、术语和待决策问题
│   ├── overview.md
│   ├── trading-safety.md
│   ├── glossary.md
│   └── open-decisions.md
├── frontend/                           前端控制台和交互规范
│   └── console-spec.md
├── backend/                            后端工程、API、数据、Kernel、服务、客户端、交易网关和审计
│   ├── engineering-design.md
│   ├── observability-audit.md
│   ├── api/
│   │   └── api-cli-contract.md
│   ├── clients/
│   │   ├── yingli-openapi-reference.md
│   │   └── usmart-openapi-call-design.md
│   ├── data/
│   │   ├── data-model.md
│   │   └── data-source-roadmap.md
│   ├── kernel/
│   │   └── kernel-interfaces.md
│   ├── services/
│   │   ├── service-specs.md
│   │   └── research-agent.md
│   └── trading/
│       └── broker-trading-gateway.md
└── project-progress/                   项目范围、路线图和实施进度
    ├── m1-scope.md
    ├── implementation-plan.md
    └── technical-roadmap.md
```

## 文档索引

### 架构

- [overview.md](architecture/overview.md)：系统架构设计，区分 M1 当前研究回测架构与长期交易架构，描述模块边界、数据流、风控和部署方式。
- [trading-safety.md](architecture/trading-safety.md)：交易安全、风控、OMS 和券商网关规范，作为后续模拟盘和实盘前置设计。
- [glossary.md](architecture/glossary.md)：量化和交易系统常用术语表，方便后续讨论时统一语言。
- [open-decisions.md](architecture/open-decisions.md)：待确认的架构决策和问题清单。

### 前端

- [console-spec.md](frontend/console-spec.md)：前端控制台设计规范，定义 M1 只读控制台和后续交易监控 UI 边界。

### 后端

- [engineering-design.md](backend/engineering-design.md)：M1 工程设计，定义主题股票池、本地 PostgreSQL、CLI、后台任务暂缓、回测库验证和 Markdown 报告。
- [api-cli-contract.md](backend/api/api-cli-contract.md)：M1 CLI / API / DTO / 日志契约，定义命令、错误码、响应和入口边界。
- [data-model.md](backend/data/data-model.md)：M1 数据模型设计，定义 PostgreSQL 表、字段、约束、状态和 kernel 归属。
- [data-source-roadmap.md](backend/data/data-source-roadmap.md)：A 股历史数据源专项路线，定义 AKShare 启动源、第二数据源交叉验证、数据网关、标准表和未来切换券商数据源的路径。
- [kernel-interfaces.md](backend/kernel/kernel-interfaces.md)：M1 Kernel 接口类设计，定义 DTO、Protocol、服务接口和 CLI/API 调用边界。
- [broker-trading-gateway.md](backend/trading/broker-trading-gateway.md)：TradingGateway 统一券商交易网关模块设计，定义统一交易门面、适配器基类、uSmart/miniQMT/Ptrade 派生、能力模式、幂等、错误映射、日志脱敏和测试策略。
- [observability-audit.md](backend/observability-audit.md)：审计、日志、可观测性和隐私规范，定义 trace、日志、敏感信息红线和数据血缘。

### 服务

- [research-agent.md](backend/services/research-agent.md)：内嵌研究回测 Agent 设计，描述自动选股、因子挖掘、训练、回测、归因分析、模拟和报告生成流程。
- [service-specs.md](backend/services/service-specs.md)：M1 核心服务行为规范，定义数据网关、股票池、研究任务、回测、归因和报告服务。

### 客户端

- [yingli-openapi-reference.md](backend/clients/yingli-openapi-reference.md)：盈立 OpenAPI 官方文档解析说明，记录官方 PDF、接口能力和后续正式接入前的安全边界。
- [usmart-openapi-call-design.md](backend/clients/usmart-openapi-call-design.md)：uSmart OpenAPI 调用栈全链路设计，定义从本地入口到券商 server 的完整调用层、签名认证、登录、下单、改单、撤单、只读查询和错误处理。

### 项目进度

- [m1-scope.md](project-progress/m1-scope.md)：M1 交付范围硬边界，明确做什么、不做什么、哪些只做预留。
- [implementation-plan.md](project-progress/implementation-plan.md)：M1 实施路线图，把范围拆成可执行任务、依赖、DoD 和风险登记。
- [technical-roadmap.md](project-progress/technical-roadmap.md)：总体技术路线规划，定义项目里程碑、模块主线、交付顺序和验收标准。

## 按问题找文档

| 我想知道... | 去哪份文档 |
|---|---|
| M1 到底做什么、不做什么 | [m1-scope.md](project-progress/m1-scope.md) |
| M1 先做哪些任务、依赖关系是什么 | [implementation-plan.md](project-progress/implementation-plan.md) |
| 总体架构和长期模块边界 | [overview.md](architecture/overview.md) |
| M1 数据库表、字段、约束 | [data-model.md](backend/data/data-model.md) |
| M1 Python DTO、Protocol、Service 接口 | [kernel-interfaces.md](backend/kernel/kernel-interfaces.md) |
| CLI 命令、API 响应、错误码和日志入口 | [api-cli-contract.md](backend/api/api-cli-contract.md) |
| 数据导入、质量检查、股票池、研究、回测和报告服务怎么工作 | [service-specs.md](backend/services/service-specs.md) |
| 真实交易前必须满足哪些安全条件 | [trading-safety.md](architecture/trading-safety.md) |
| 统一券商交易网关怎么设计、uSmart 和 miniQMT 如何接入 | [broker-trading-gateway.md](backend/trading/broker-trading-gateway.md) |
| uSmart OpenAPI 全链路怎么调用、怎么签名 | [usmart-openapi-call-design.md](backend/clients/usmart-openapi-call-design.md) |
| 日志、审计、trace_id、敏感信息怎么处理 | [observability-audit.md](backend/observability-audit.md) |
| React 控制台能做什么、不能做什么 | [console-spec.md](frontend/console-spec.md) |
| 盈立 OpenAPI 官方 PDF 怎么解析和使用 | [yingli-openapi-reference.md](backend/clients/yingli-openapi-reference.md) |
| 当前还有哪些待决策问题 | [open-decisions.md](architecture/open-decisions.md) |

## 设计原则

1. 先保证实盘安全，再追求策略复杂度。
2. 先支持低频、可解释、可回放的交易流程，再考虑高阶 AI/LLM 能力。
3. 将券商接入、策略逻辑、风控、账户状态和数据存储解耦，避免一个模块出问题拖垮整个系统。
4. 所有自动交易行为都要可审计、可暂停、可撤销、可复盘。

## 维护原则

1. 范围先看 [m1-scope.md](project-progress/m1-scope.md)，任务先看 [implementation-plan.md](project-progress/implementation-plan.md)。
2. 每个专项 spec 是对应模块的真相源，架构文档只保留摘要和指针。
3. 涉及交易、风控、账户、订单、券商适配器、数据模型或部署方式变更时，先更新对应文档，再编码。
4. 不确定的券商 API 行为、交易规则和订单状态，不猜测为事实，统一进入 [open-decisions.md](architecture/open-decisions.md)。
5. 运行产物、密钥、真实账号和真实资金隐私不进入文档和代码库。

## 实现期对照

| 实现任务 | 对应真相源 |
|---|---|
| 架构、模块边界、部署方式 | [overview.md](architecture/overview.md) |
| M1 范围和验收标准 | [m1-scope.md](project-progress/m1-scope.md) |
| 任务拆解和进度维护 | [implementation-plan.md](project-progress/implementation-plan.md) |
| FastAPI / CLI / DTO / 错误码 | [api-cli-contract.md](backend/api/api-cli-contract.md) |
| PostgreSQL 表、字段和迁移顺序 | [data-model.md](backend/data/data-model.md) |
| Kernel DTO、Protocol 和服务接口 | [kernel-interfaces.md](backend/kernel/kernel-interfaces.md) |
| 数据导入、质量检查、股票池、回测和报告服务 | [service-specs.md](backend/services/service-specs.md) |
| React 只读控制台 | [console-spec.md](frontend/console-spec.md) |
| 统一券商交易网关 | [broker-trading-gateway.md](backend/trading/broker-trading-gateway.md) |
| uSmart / 盈立 OpenAPI 客户端资料 | [backend/clients/](backend/clients/) |
| 交易安全、风控、OMS、对账边界 | [trading-safety.md](architecture/trading-safety.md) |
