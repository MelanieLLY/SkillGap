## 团队分工与贡献说明（Team Contributions）

项目名称：**Tech Stack Skill Gap Analyzer（SkillGap）**  
团队成员：**Liuyi (MelanieLLY)**、**Jing**

> 本文档由 AI 助手基于完整的 GitHub commit 历史、GitHub Issues / Project Board 元数据以及内部 planning note 自动整理，并再由 Liuyi 进行人工校对与补充。  
> 重点不是「单纯的 commit 数量」，而是结合 Issue 归属、模块 ownership 和时间轴，还原每位成员在各个 Sprint 中的真实职责与代表性贡献。  
> **说明**：整个 documentation package（包括 API docs、Scrum 文档、AI 相关文档、code-architecture 等）的整理工作体量很大，且在项目期间是持续演进的，参与者涵盖两位成员与多轮 AI 协作，因此没有在本文件中逐项细分到个人层级；可以简单理解为两位成员在文档工作上是「共同负责 + 合理分工」，本文件主要聚焦于代码与工程侧的代表性贡献。

---

## 1. Liuyi (MelanieLLY)：核心功能实现、后端架构、CI/CD、AI 集成与质量保障

### 1.1 主要职责

- 负责后端 FastAPI 服务的整体架构与稳定性。  
- 负责云端 PostgreSQL 数据库的统一配置与迁移策略。  
- 参与并主导多项**核心业务功能**实现（包括早期 skill extraction 与 matching 优化、History 与 Roadmap 后端逻辑等）。  
- 设计并实现多阶段 CI/CD 流水线，确保测试与覆盖率达标。  
- 主导 Claude AI 学习路线的集成与 AI Eval Suite 的实现。  
- 统筹项目级文档（API 文档、代码架构说明、Eval Dashboard 等）。

### 1.2 关键技术贡献（示例）

> 以下示例来自 `internal_working_planning_note/GitHub commit history copy from github.md`，只列出部分代表性提交。

- **CI/CD 与测试基础设施**  
  - `feat(#14): implement backend test suite and multi-stage ci workflow`  
  - `chore: streamline CI to focus on security and coverage requirements`  
  - `test(#29): add unit tests for migrate_roadmap.py`  
  - `docs: implement evaluation dashboard and generate test coverage reports`（对应 Issue #9 Eval Dashboard）  
  - `fix(ci): correct node cache path and package-lock location for workspaces`  
  - 这些提交建立了后端 pytest、覆盖率门槛以及前后端联合 CI，并通过 Eval Dashboard 把测试与覆盖率结果文档化，使得后续所有 PR 都在明确的质量与可观测性门槛下进行。

- **AI 路线集成与 Roadmap 功能**  
  - `feat(#21): setup Claude AI scaffolding with dummy service and integration tests`  
  - `feat(#7): implement Claude-powered learning roadmap with TDD and frontend integration`  
  - `feat(#7): implement roadmap and dashboard state persistence`  
  - 负责 `roadmap/services.py` 与 `/api/roadmap/generate` 的实现，以及与前端 Dashboard 的状态管理和持久化联动。

- **安全与数据库可靠性**  
  - `refactor(#15): implement global db error handler and debug logs`  
  - `fix(#16): fix mac environment bugs and unify postgresql database`  
  - 通过统一使用云端 PostgreSQL、增加全局 SQLAlchemy 异常处理器等方式，提升系统在真实部署环境下的稳定性与可观测性。

- **部署与仓库结构优化（DevOps）**  
  - `enhancement(#35): separate client and server structure for independent deployment`  
  - `chore(deploy): (#37) configure FastAPI backend deployment on Render`  
  - 对应 GitHub Issue #35/#37/#38 等一系列 DevOps / 部署任务，完成了前后端分离部署结构的整理，以及 Render 后端与 Netlify 前端的生产部署配置。每次 PR 除 GitHub Actions（Lint / Test / Build）外，还会触发 Netlify 的 Deploy Preview 及站点规则检查（Header rules、Pages changed、Redirect rules），见 [每次PR的自动化检测CI和部署平台.png](../internal_working_planning_note/screenshot%20during%20dev/每次PR的自动化检测CI和部署平台.png)。

- **前端测试与 UI Polish 支持**  
  - `feat(#14): setup vitest testing environment and core unit tests`  
  - `feat(#29): improve frontend line coverage to 87% and fix component accessibility`  
  - `feat(#10): implement learning roadmap skeletons and framer-motion animations`  
  - `fix(test): resolve CI lint errors and React scope in test setup`  
  - 为前端搭建 Vitest 测试框架并将覆盖率提升到 80%+，同时在 UI 动画、骨架屏和可访问性（a11y）方面进行多次优化，使 Dashboard 体验更丝滑且更易用。

- **文档与项目管理**  
  - 牵头整理 `PROJECT2_MASTER_PLAN.md` 最终版本，将课程 rubric 抽象为可执行路线。  
  - 撰写/补全 `docs/api-docs.md`、`docs/code-architecture.md`、`docs/ai-modalities-usage.md`、`docs/ai-reflection.md` 等核心文档。

### 1.3 对团队协作的影响

- Liuyi (MelanieLLY) 在项目中类似「后端 Tech Lead + DevOps Engineer」的角色：  
  - 把握整体系统架构与质量边界。  
  - 通过 CI 与测试为队友的前端与规则引擎工作提供稳定的运行基础。  
  - 在课程要求的 AI Mastery、CI/CD、Documentation 等维度上提供系统性支撑。

---

## 2. Jing：核心功能实现、前端体验与提取引擎

### 2.1 主要职责

- 负责应用的核心功能闭环：认证流、技能档案管理、JD 技能提取与前端主流程。  
- 设计并实现匹配度环形动画、三列技能对比 UI 等关键用户体验。  
- 主导 `extraction` 引擎与前端 Dashboard 交互，保证规则引擎结果在 UI 中准确呈现。  
- 参与 Sprint 规划、规则文件（`.antigravityrules`、`RULES_WRITEUP.md`）与 GitHub Project Board 的维护。

### 2.2 关键技术贡献（示例）

> 以下示例同样来自 commit 历史整理，只列出代表性提交。

- **认证与核心 CRUD 功能**  
  - `feat(#1): implement login and register pages with JWT auth flow`  
  - `feat(#11): implement skill profile CRUD with persistent storage`  
  - 建立从前端表单到后端 `/api/auth`、`/api/profile` 的完整链路，为后续所有自动化分析提供基础。

- **技能提取引擎与 match score 计算**  
  - `feat(#4): implement keyword skill extraction engine`  
  - `update/add extraction engine and tests`  
  - `feat(#5): implement match score calculation logic`（见 Issue 历史）  
  - 负责 `extraction/engine.py` 中 CURATED_SKILLS 与提取逻辑，实现了 JD 与用户技能之间的核心匹配算法。

- **前端用户体验与可视化**  
  - `feat(#12): implement animated match score ring visualization`  
  - `feat(#8): implement analysis history persistence and retrieval`（前端部分）  
  - 通过 Dashboard 页面整合 JD 输入、匹配结果展示、历史记录入口等，提高整体用户旅程连贯性。

- **规则与工程规范**  
  - 多次更新 `.antigravityrules` 与 `internal_working_planning_note/RULES_WRITEUP.md`，明确了类型、测试和 CI 的严格程度。  
  - 在 PR 流程中积极使用这些规则指导 AI 使用和代码评审。

### 2.3 对团队协作的影响

- Jing 在项目中类似「全栈 Feature Owner」的角色：  
  - 把握从用户视角出发的端到端体验。  
  - 把规则引擎与前端交互有机结合，为后续的 AI 路线与历史记录提供了稳固的「第一层价值」。  
  - 在项目初期快速搭建出可以 Demo 的 MVP，为后续 Sprint 2 的增强赢得时间。

---

## 3. 协同与交叉贡献

虽然两位成员在职责上有所侧重，但在很多关键任务上是高度协同的：

- **共同参与 Sprint 规划与文档撰写**  
  - 一起使用 Claude Web 制定 PRD、PROJECT2_MASTER_PLAN、Scrum 文档。  
  - 在 `docs/sprint-planning-*.md` 与 `docs/sprint-retro-*.md` 中共同反思过程。

- **共同维护质量与测试**  
  - Jing 在实现功能时就编写/调整前端与后端的测试。  
  - Melanie 在引入 CI 与 coverage 规则时，确保这些测试成为「必须通过」的门槛。

- **共同使用与反思 AI 工具**  
  - 两人都在 IDE 中大量使用 AI Agent，记录 Prompt 与重要对话（见 `internal_working_planning_note/ai chat history Liuyi/*`）。  
  - 在 `docs/ai-modalities-usage.md` 和 `docs/ai-reflection.md` 中，总结了团队整体对 AI 使用方式的经验与教训。

---

## 4. 关于 Commit 分布与证明材料

从 `internal_working_planning_note/GitHub commit history copy from github.md` 可以看出：

- 后期（尤其是 CI、AI 路线和文档收尾阶段）Melanie 的 commit 较为集中。  
- 早期（MVP 架构和核心功能阶段）Jing 在 auth、profile、extraction、前端主流程上的贡献占比较高。

考虑到：

- 项目中大量使用了 IDE AI Agent 和 Claude Web；  
- 某些较大的提交是「代码自动格式化」或 CI 配置更新；

我们不把「单纯的 commit 数量」作为衡量贡献的唯一指标，而是结合：

- **Issue 负责人与实现内容**（见 GitHub Project Board）。  
- **关键模块的 Ownership**（上文职责说明）。  
- **内部规划文档与 AI 对话记录**（证明谁在何时推动了哪些关键决策）。

综上，两位成员在本项目中都承担了不可替代的角色：  
Jing 更偏向产品功能与用户体验闭环；Melanie 更偏向系统稳定性、AI 深度集成与质量保障。  
从课程 rubric 的多个维度（Functionality / Technical Excellence / AI Mastery / CI/CD / Agile Process）来看，两人的贡献是互补且均衡的。

