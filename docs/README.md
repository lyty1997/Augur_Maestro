# RobustQuant 设计文档

本目录用于沉淀 RobustQuant 的项目设计文档。这里的文档面向项目内部研发和长期维护，和 `券商API/盈立/申请资料/RobustQuant_使用者手冊.docx` 这种券商申请材料分开管理。

## 当前文档

- [01-architecture.md](./01-architecture.md)：系统架构设计，区分 M1 当前研究回测架构与长期交易架构，描述模块边界、数据流、风控和部署方式。
- [02-glossary.md](./02-glossary.md)：量化和交易系统常用术语表，方便后续讨论时统一语言。
- [03-open-decisions.md](./03-open-decisions.md)：待确认的架构决策和问题清单。
- [04-research-agent.md](./04-research-agent.md)：内嵌研究回测 Agent 设计，描述自动选股、因子挖掘、训练、回测、归因分析、模拟和报告生成流程。
- [05-technical-roadmap.md](./05-technical-roadmap.md)：总体技术路线规划，定义项目里程碑、模块主线、交付顺序和验收标准。
- [06-data-source-roadmap.md](./06-data-source-roadmap.md)：A 股历史数据源专项路线，定义 AKShare 启动源、数据网关、标准表和未来切换券商数据源的路径。
- [07-m1-engineering-design.md](./07-m1-engineering-design.md)：M1 工程设计，定义主题股票池、本地 PostgreSQL、CLI、后台任务暂缓、回测库验证和 Markdown 报告。
- [08-m1-data-model.md](./08-m1-data-model.md)：M1 数据模型设计，定义 PostgreSQL 表、字段、约束、状态和 kernel 归属。
- [09-m1-kernel-interfaces.md](./09-m1-kernel-interfaces.md)：M1 Kernel 接口类设计，定义 DTO、Protocol、服务接口和 CLI/API 调用边界。

## 设计原则

1. 先保证实盘安全，再追求策略复杂度。
2. 先支持低频、可解释、可回放的交易流程，再考虑高阶 AI/LLM 能力。
3. 将券商接入、策略逻辑、风控、账户状态和数据存储解耦，避免一个模块出问题拖垮整个系统。
4. 所有自动交易行为都要可审计、可暂停、可撤销、可复盘。
