# M1 工程设计

版本：v0.1  
状态：部分确认  
最后更新：2026-05-15

## 1. 文档定位

本文档定义 RobustQuant M1 的工程落地方案。M1 的目标不是做完整量化平台，而是先跑通 A 股主题股票池的历史数据导入、标准化落库、质量检查、最小回测验证、归因分析和报告闭环。

上位路线见 [05-technical-roadmap.md](../00-project/05-technical-roadmap.md)，历史数据源专项路线见 [06-data-source-roadmap.md](../10-research-data/06-data-source-roadmap.md)。

M1 的具体 PostgreSQL 表、字段、约束和迁移顺序见 [08-m1-data-model.md](08-m1-data-model.md)。

M1 的 Python DTO、Protocol、服务接口和 CLI/API 调用边界见 [09-m1-kernel-interfaces.md](09-m1-kernel-interfaces.md)。

## 2. 已确认决策

- M1 不导入全 A 股，先导入用户熟悉主题相关标的。
- M1 可以前置 AI 辅助选股，也允许 AI 扩展候选清单，但只用于生成候选股票池，不能直接进入交易。
- 股票展示使用“代码 + 名称”的表达法，例如 `688981.SH 中芯国际`；内部主键仍以标准代码为准。
- 历史数据源使用 AKShare。
- M1 需要加入第二数据源，对 AKShare 关键字段做交叉验证。
- 数据导入时间范围默认最近 10 年；最近 1 年作为模拟数据，之前数据按时间顺序 8:2 切分为建模数据和回测数据。
- 数据库使用 PostgreSQL，本地部署。
- Python 项目管理先使用普通虚拟环境 `venv` + `requirements.txt`。
- 第一版任务入口使用命令行 CLI。
- CLI 框架使用 Typer。
- CLI 必须提供完整 `--help`。
- 项目 README 必须写清楚常用命令、配置文件示例和运行顺序。
- 数据库访问使用 SQLAlchemy 2.x，数据库迁移使用 Alembic。
- M1 不引入 Redis、Celery、Dramatiq 等后台任务队列。
- 回测库先并行最小验证 Qlib 和 VectorBT，再选择最适合的主执行器。
- M1 报告必须包含基础归因分析，用来解释主要收益和亏损来自哪里。
- 配置文件分为 `.env` 和 `configs/*.yaml`：`.env` 保存本机敏感配置，不进入 Git；`configs/*.yaml` 保存研究配置和股票池配置，可以进入 Git。
- 第一版报告使用 Markdown。
- 中间产物和输出目录不进入代码库。
- 代码架构采用拆分 kernel 的方式，尽可能保证高内聚、低耦合。
- M1 第一条关键路径先跑通 CLI；React 只读控制台后置，若实现也只做研究展示。

## 3. M1 股票池

M1 只导入用户熟悉的主题方向，避免一开始全市场铺开导致数据量、行业分类和质量检查复杂度过高。

主题范围：

- 算力。
- 电力。
- 半导体。
- 人工智能。
- 芯片。
- 电池。
- 通信。
- 银行。
- CPO。
- 机器人。
- 存储。
- 有色金属。
- 影视院线。

股票池设计：

- 建立 `research_universes` 表记录股票池定义。
- 建立 `research_universe_members` 表记录股票池成员。
- 每个成员必须记录 `symbol`、`name`、`theme`、`source`、`reason`、`added_at`、`is_active`。
- 第一版不要求用户一只只股票手工输入。可以用 AKShare 概念板块、行业分类、公开资料和 AI 辅助生成或扩展候选清单，再由用户确认后写入正式股票池。
- AI 辅助选股只能生成候选池，必须输出候选理由、来源、主题归属和置信度，不能自动加入正式股票池或实盘交易链路。
- 同一股票可以属于多个主题，例如半导体、芯片、存储。
- 正式研究池需要排除表现异常、容易被大资金操纵的小票股。
- 换手率低、成交额低、长期停牌、流动性差的标的不进入正式研究池。
- 具体过滤阈值放在 `configs/universe/*.yaml`，例如最小上市天数、最小日均成交额、最小换手率、市值下限和最大停牌天数。

注意：如果使用当前概念板块成分作为历史回测股票池，可能产生幸存者偏差。简单说，就是只看今天还在板块里的股票，会漏掉过去已经退出、退市或表现很差的股票，回测结果可能偏乐观。M1 的结果只能用于工程验证和研究探索，不能直接当实盘依据。

消息面或 AI 选股还必须遵守“不能仅凭关键词匹配”的原则。比如新闻里出现“天坛”，不能因为某只股票名字里带“天坛”就把它选入交易候选。系统必须判断新闻实体、上市公司主体、行业链条和事件影响之间是否存在真实关联。

## 4. 本地数据库设计说明

数据库可以理解为系统的“账本”和“资料库”。Excel 也能存表格，但量化系统需要长期保存大量行情、实验参数、导入批次、回测结果和错误原因，还要支持查询、去重、约束和追踪，因此需要数据库。

RobustQuant M1 使用 PostgreSQL，原因是：

- 它是成熟稳定的关系型数据库。
- 适合保存结构化表，例如股票、日线行情、研究任务、回测结果。
- 能通过唯一约束避免重复数据。
- 能通过索引加快按股票和日期查询。
- 后续从本地研究迁移到实盘服务时，不需要更换数据库方向。

几个核心概念：

- 表：类似 Excel 里的一个工作表，例如 `daily_bars` 存日线行情。
- 行：一条记录，例如某只股票某一天的一根 K 线。
- 列：字段，例如开盘价、收盘价、成交量。
- 主键：每行记录的唯一身份。
- 唯一约束：防止同一只股票同一天同一复权类型重复入库。
- 索引：类似目录，帮助数据库更快找到某只股票某段时间的数据。
- 迁移：表结构变化的版本记录，例如新增一个字段或新建一张表。

M1 建议本地部署方式：

- 优先使用 Docker Compose 在本机启动 PostgreSQL。
- 如果本机不方便使用 Docker，再使用本机原生 PostgreSQL 服务。
- 数据库连接信息只写入 `.env` 或本地配置，不提交到 Git。

数据库访问方式：

- SQLAlchemy 2.x 负责在 Python 代码里读写数据库表。
- Alembic 负责管理表结构迁移，例如新增表、增加字段、建立索引。
- 表结构变化必须通过迁移脚本记录，不能只靠手工改数据库。

## 5. 数据模型补充

本节只保留 M1 股票池相关表的摘要。完整数据模型见 [08-m1-data-model.md](08-m1-data-model.md)。

### 5.1 研究股票池表

表名建议：`research_universes`

核心字段：

- `universe_id`：股票池 ID。
- `name`：股票池名称，例如 `m1_theme_universe`。
- `description`：说明。
- `created_by`：创建来源，例如 `manual`。
- `created_at`：创建时间。
- `updated_at`：更新时间。

### 5.2 股票池成员表

表名建议：`research_universe_members`

核心字段：

- `universe_id`：股票池 ID。
- `symbol`：内部统一证券代码。
- `name`：证券名称。
- `theme`：主题，例如 `semiconductor`、`bank`。
- `source`：来源，例如 `manual`、`akshare_concept`。
- `reason`：进入候选池或正式池的理由。
- `confidence`：候选置信度，可为空。
- `is_active`：是否启用。
- `added_at`：加入时间。
- `removed_at`：移除时间，可为空。

唯一约束建议：

```text
(universe_id, symbol, theme)
```

## 6. 命令行入口设计

M1 使用 CLI 作为主要操作入口，CLI 框架使用 Typer。CLI 的目的不是炫技，而是让每个动作都可复现、可记录、可写进 README。

建议命令命名：

```bash
robustquant --help
robustquant data --help
robustquant data init-db --help
robustquant data import-symbols --help
robustquant data import-daily-bars --help
robustquant data validate --help
robustquant research --help
robustquant research run-backtest --help
robustquant research analyze-attribution --help
robustquant universe --help
robustquant universe build-candidates --help
robustquant universe approve --help
```

README 必须说明：

- 如何创建 Python 虚拟环境。
- 如何配置 `.env`。
- 如何启动本地 PostgreSQL。
- 如何初始化数据库。
- 如何导入主题股票池。
- 如何用 AI/规则生成候选股票池并人工确认。
- 如何导入日线行情。
- 如何运行数据质量检查。
- 如何运行最小回测。
- 如何运行归因分析。
- 输出报告在哪里。

CLI 基本要求：

- 每个命令都有 `--help`。
- 关键参数必须有清晰说明和默认值。
- 导入任务必须打印导入批次 ID。
- 失败时必须返回非 0 退出码。
- 错误信息必须能指导下一步排查。

## 7. 配置、数据区间和输出目录

配置文件分两类：

- `.env`：保存本机敏感配置，例如数据库连接字符串，不进入 Git。
- `configs/*.yaml`：保存研究配置、股票池配置、回测配置，可以进入 Git。

数据区间默认规则：

- 默认导入最近 10 年日线数据。
- 如果标的上市不足 10 年，从上市日或可获得数据首日开始。
- 最近 1 年作为模拟数据，用于离线模拟或后续 paper trading 对比。
- 剩余历史数据按时间顺序 8:2 切分：前 80% 用于建模和参数选择，后 20% 用于回测验证。
- 切分必须按时间顺序，不能随机打乱，避免偷看未来数据。

输出目录：

```text
outputs/
  reports/
  backtests/
  attribution/
  data_quality/
  universe_candidates/
```

`outputs/`、缓存和中间产物不进入代码库。需要长期留存的研究结论可以挑选 Markdown 报告进入文档或单独归档，但默认运行产物不提交。

## 8. 后台任务暂缓说明

后台任务框架解决的是“任务很多、任务很慢、需要排队、需要失败重试、需要定时运行”的问题。

常见选择：

- APScheduler：适合简单定时任务。
- Dramatiq：适合较轻量的任务队列。
- Celery：功能强，但依赖和运维复杂度更高，通常需要 Redis 或 RabbitMQ。
- Redis：常用作缓存、任务队列中间件或轻量消息协调。

M1 暂不引入这些组件，原因是：

- 当前只有数据导入、质量检查、最小回测，CLI 同步执行更容易调试。
- 过早引入任务队列会增加部署和排错复杂度。
- 研究期最重要的是先确认数据、模型和回测链路正确。

触发引入后台任务的条件：

- 数据导入耗时明显变长，需要异步执行。
- 需要每天自动更新行情。
- 需要多个回测任务排队运行。
- 需要 Web 页面发起任务后后台执行。
- 需要任务失败状态、重跑和进度查询。

## 9. 回测库验证方案

M1 优先验证：

- Qlib。
- VectorBT。

验证目标：

- 两者都能读取 RobustQuant 标准化日线数据。
- 能运行一个简单日频策略。
- 能输出收益、回撤、换手率等基础指标。
- 能输出基础归因结果，至少覆盖标的贡献、主题贡献、交易成本贡献和主要回撤片段。
- 能把结果转成 RobustQuant Markdown 报告。
- 形成主执行器选择建议，说明未被选中的库是否保留为对照验证工具。

暂缓：

- Backtrader。
- Zipline/Zipline Reloaded。

暂缓原因不是它们不能用，而是 M1 更需要快速验证因子、选股和日频研究链路。Backtrader 更偏事件驱动交易模拟，Zipline 接 A 股自定义数据和交易规则可能需要更多适配。

## 10. Markdown 报告

第一版报告只输出 Markdown。

报告至少包含：

- 研究任务名称。
- 股票池名称和主题范围。
- 数据源和导入批次。
- 数据时间范围。
- 数据切分方式：建模、回测、模拟。
- 复权方式。
- 策略参数。
- 回测指标。
- 归因分析：主要收益和亏损来自哪些标的、主题、时间窗口、交易成本和回撤片段。
- 数据质量问题摘要。
- 风险提示。

报告必须明确标注：

- M1 结果只用于工程验证和研究探索。
- 主题股票池可能存在幸存者偏差。
- AKShare 不是最终生产真相源。
- 结果不能直接作为实盘建议。

## 11. Kernel 拆分架构

M1 采用拆分 kernel 的核心架构。这里的 kernel 指高度内聚的领域核心模块，每个 kernel 管自己的模型、规则和服务，通过明确接口和其他模块协作。

接口类按 `records.py`、`ports.py`、`services.py` 拆分：`records.py` 放 kernel 对外传递的 DTO，`ports.py` 放外部依赖和仓储 Protocol，`services.py` 放业务编排服务。具体接口定义见 [09-m1-kernel-interfaces.md](09-m1-kernel-interfaces.md)。

建议拆分：

```text
rq_core/
  data_kernel/
  universe_kernel/
  research_kernel/
  backtest_kernel/
  report_kernel/
  common/
backend/
cli/
configs/
tests/
```

职责边界：

- `data_kernel`：数据源 Provider、标准化、落库、质量检查。
- `universe_kernel`：主题股票池、AI 候选池、人工确认。
- `research_kernel`：研究任务、数据切分、实验记录。
- `backtest_kernel`：Qlib/VectorBT 适配、回测执行、指标计算、归因分析。
- `report_kernel`：Markdown 报告生成。
- `backend`：FastAPI 接口层，不写核心研究逻辑。
- `cli`：命令行入口，只调用 kernel 暴露的服务。

约束：

- kernel 之间通过接口或数据模型协作，避免互相直接读写内部细节。
- `backend` 和 `cli` 都是入口层，不能沉淀核心业务规则。
- 策略、回测和研究 Agent 不能直接调用 AKShare。
- SQLAlchemy ORM 模型只在基础设施层使用，不能直接作为 kernel 之间的传输对象。

## 12. 开源协议初步检查

M1 计划使用的 Typer、SQLAlchemy、Alembic 都是宽松开源许可证，初步看不构成个人研究项目使用障碍。

- Typer：MIT License。
- SQLAlchemy：MIT License。
- Alembic：MIT License。

后续真正锁定依赖版本时，需要在 `requirements.txt` 或依赖清单中记录版本，并保留许可证检查结果。若引入 Qlib、VectorBT 或其他回测库，也要单独检查许可证和商业使用限制。

## 13. M1 验收标准

- 能在本地启动 PostgreSQL。
- 能通过 CLI 初始化数据库。
- 能按 [09-m1-kernel-interfaces.md](09-m1-kernel-interfaces.md) 建立 M1 kernel 接口类，并保持 `rq_core` 不依赖 FastAPI、Typer、SQLAlchemy、AKShare、Qlib 或 VectorBT。
- 能通过 AI/规则生成候选股票池，并由用户确认后导入正式主题股票池。
- 能按配置过滤 ST、低成交额、低换手率、长期停牌、流动性差和疑似易被操纵的小票股。
- 能通过 AKShare 导入股票池日线数据。
- 能通过第二数据源生成关键字段交叉验证差异摘要。
- 能保存不复权和前复权数据。
- 能按最近 10 年、最近 1 年模拟、此前数据 8:2 建模/回测的规则切分数据。
- 能生成导入批次记录。
- 能运行基础数据质量检查。
- 能用 Qlib 和 VectorBT 并行跑通最小验证，并选择一个更适合的主执行器。
- 能生成基础归因分析结果，回答主要收益和亏损来自哪里。
- 能输出 Markdown 报告。
- README 能让用户按步骤复现整个流程。
