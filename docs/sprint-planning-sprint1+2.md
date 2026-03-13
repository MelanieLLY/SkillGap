> 本文件由 AI 助手在阅读 `docs/skillgap_prd.md`、`internal_working_planning_note/PROJECT2_MASTER_PLAN.md`、GitHub Issues（含 Sprint 标签）以及 Project Board 之后，自动汇总整理两个 Sprint 的规划内容，并由 Liuyi 根据实际执行情况做了少量文字校正。  
> 因此，这里的 Issue 编号、时间范围与目标是对「真实 GitHub 历史 + 课程要求」的一个结构化总结，而不是事后凭记忆回填。

## Sprint 1 规划文档（Core Application）

- **时间范围**：2026-02-26 – 2026-03-14  
- **目标主题**：交付一个「不带 AI 学习路线」的可用核心应用，覆盖认证、技能档案、JD 技能匹配和基础可视化。

### 1. Sprint 目标

结合 `docs/skillgap_prd.md` 第 4 节和 GitHub Project Board，本次 Sprint 旨在完成：

- 支持用户注册 / 登录，并安全地持久化用户数据。
- 允许用户创建和维护自己的技能档案。
- 提供粘贴 JD 的入口，将 JD 与技能档案进行自动匹配。
- 以可视化方式展示匹配度（match score）和 have / missing / bonus 三列技能。
- 为第二个 Sprint 的 AI 路线和历史记录打好数据与架构基础。

### 2. 用户故事范围（来自 PRD）

本 Sprint 主要覆盖 PRD 中的以下用户故事：

- **Story 1 – Profile Management**  
  作为新用户，我希望能够保存我的技能档案，这样我不需要每次重新输入。
- **Story 2 – Core Value（JD Skill Match）**  
  作为求职者，我希望可以粘贴 JD，看到匹配分数和 skill gap 分析。
- **Story 5 – Continuous Learning（部分）**  
  作为学习用户，我希望可以更新自己的技能档案并重新分析，以看到匹配度变化。

### 3. 选入 Sprint 1 的 Issue 列表

（根据 `docs/skillgap_prd.md` 第 4 节和 `internal_working_planning_note/GitHub project board.md`）

- **Issue #1: Implement User Registration & Login (JWT Auth)**  
  - 建立后端 `/api/auth` 路由与 JWT 流程。  
  - 前端实现登录 / 注册页面，连接真实 API。  
  - 接受标准：能够注册新用户、登录并在前端持久化 token。

- **Issue #2: Implement Skill Profile CRUD**  
  - 后端：实现 `/api/profile/skills` 系列接口与 `User.skills` 字段。  
  - 前端：在 Profile 页面支持技能添加、删除和展示。  
  - 接受标准：技能在刷新之后仍然存在，重复添加会去重。

- **Issue #3: Build Job Description Input Component**  
  - 前端：Dashboard 上的 JD 文本输入区和提交按钮。  
  - 接受标准：用户可以粘贴长 JD，点击分析按钮触发后端调用。

- **Issue #4: Develop Keyword Skill Extraction Engine**  
  - 后端：`extraction/engine.py` 中实现基于 `CURATED_SKILLS` 的关键词匹配算法。  
  - 提供 `/api/extract` 端点，返回 have/missing/bonus。  
  - 接受标准：对于典型 JD，能够正确区分三类技能。

- **Issue #5: Implement Match Score Calculation Logic**  
  - 后端：在 `history` 或提取引擎内实现 `calculate_match_score`。  
  - 接受标准：score 与 have/missing 的比例一致，不允许由前端伪造。

- **Issue #6: Build Three-Column Comparison UI**  
  - 前端：Dashboard 中的 have / missing / bonus 三列组件。  
  - 接受标准：三列排列明确、响应式布局良好，支持滚动查看长列表。

- **Issue #12: Create Match Score Visualization (Animated Ring)**  
  - 前端：`AnimatedMatchRing` 组件，用于可视化显示 match_score。  
  - 接受标准：环形动画在分数变化时具有流畅过渡和明显的高/中/低颜色差异。

> 注：虽然 PRD 中将 Issue #12 标记在 Sprint 1 Core Application 下，但实际实现中有部分 UI polish 可能延伸到 Sprint 2。

### 4. 范围外（明确不在 Sprint 1 内）

- AI 学习路线生成（Claude 调用与 `/api/roadmap/generate`）——推迟到 Sprint 2。
- Analysis History 视图和持久化 —— 核心逻辑在 Sprint 2 完成。
- Eval Dashboard、AI 评估脚本和 CI 复杂配置 —— 在后续阶段处理。

### 5. 完成定义（Definition of Done）

对 Sprint 1 选入的 Issue，团队在规划时约定：

- 通过 GitHub Actions CI 流水线（至少基本 lint + pytest）。
- 后端核心路由都有对应的单元测试或集成测试。
- 前端关键页面（Login/Dashboard/Profile）在本地可跑通完整流程。
- 新增代码遵守 `.antigravityrules` 中的类型与 PEP8 要求。
- 代码通过 Pull Request 审查，禁止直接推 main。

### 6. 预期风险与缓解策略

- **风险 1：认证/数据库配置踩坑**  
  - 缓解：在 Sprint 1 早期即完成基础 Auth + DB 连通性测试，并在 `PROJECT2_MASTER_PLAN.md` 中记录迁移策略。

- **风险 2：前后端契约频繁变更**  
  - 缓解：以 `docs/skillgap_prd.md` 中的 API 契约为主，接口变更通过小 PR 和快速同步解决。

- **风险 3：测试覆盖率不足影响后续 CI 规则**  
  - 缓解：在实现每组路由时同时写 Pytest，用于后续 Sprint 2 直接提升覆盖率而不是「最后补测试」。  


## Sprint 2 规划文档（AI Features & Polish）

- **时间范围**：2026-03-15 – 2026-04-04  
- **目标主题**：在 Sprint 1 核心应用基础上，引入 Claude AI 学习路线、历史记录视图、测试与 UI Polish，完成端到端体验。

### 1. Sprint 目标

基于 `docs/skillgap_prd.md` 中「Sprint 2: AI Features & Polish」章节，本次 Sprint 目标是：

- 接入 Claude API，为缺失技能生成结构化学习路线。
- 持久化每一次 JD 分析记录，支持用户事后回顾。
- 搭建 AI 质量评估脚本和 Eval Dashboard。
- 打磨 UI/UX（骨架屏、动画、可访问性）以达到 Demo 级体验。

### 2. 用户故事范围（来自 PRD）

本 Sprint 主要覆盖 PRD 中的以下用户故事：

- **Story 3 – AI Guidance**  
  作为求职者，我希望获得针对缺失技能的 AI 学习路线，以便知道接下来该学什么。
- **Story 4 – Progress Tracking**  
  作为回访用户，我希望可以看到历史分析记录和分数变化。
- **Story 5 – Continuous Learning（完成）**  
  随着路线执行和技能更新，我可以多次分析 JD 并比较前后差异。

### 3. 选入 Sprint 2 的 Issue 列表

（根据 `docs/skillgap_prd.md` 以及 `PROJECT2_MASTER_PLAN.md` 中 Phase 2/3）

- **Issue #7: Integrate Claude API for learning roadmap generation**  
  - 后端：在 `roadmap/services.py` 中实现 `generate_roadmap_with_claude`，对接 Anthropic SDK。  
  - 路由：`POST /api/roadmap/generate`，使用 `RoadmapGenerateRequest/Response`。  
  - 前端：在 Dashboard 中新增「Generate Learning Roadmap」按钮和渲染组件。  
  - 接受标准：在前端可见结构化路线，错误状态（超时、认证失败）有合适提示。

- **Issue #8: Develop Analysis History View**  
  - 后端：完善 `history/models.py`、`history/router.py`，保证 `match_score` 在后端安全计算。  
  - 前端：实现 `History.tsx` 页面，调用 `/api/history/` 获取用户所有分析记录。  
  - 接受标准：用户可以查看按时间排序的历史记录，且记录字段与 Dashboard 一致。

- **Issue #9: Build AI Evaluation Suite（roadmap metrics）**  
  - 在 `server/tests/ai_eval.py` 和 `docs/eval_roadmaps/*` 中实现和记录 AI 路线质量评估。  
  - 使用第二个 LLM 作为「Judge」给出 Relevance / Specificity / Completeness 评分。  
  - 接受标准：可以对多份 JD/技能组合批量评估，并生成 `docs/ai_eval_results.md`。

- **Issue #10: Improve UI polish and accessibility**  
  - 在 `AnimatedMatchRing`、`LearningRoadmap`、Skeleton 组件等处补充细节动画和骨架屏。  
  - 增加 A11y 属性（`aria-*`）、按钮状态管理、深浅色模式等。  
  - 接受标准：核心用户流程中不存在明显的「空白闪烁」或无提示加载，符合基本可访问性实践。

- **Issue #14: Setup pytest and backend test coverage**  
  - 在 `server/tests/` 中补齐针对 Auth/Extraction/History/Roadmap 的测试。  
  - 配置覆盖率门槛（80%+）并在 CI 中强制执行。  
  - 接受标准：本地与 CI 上运行 `pytest` 全绿，覆盖率报告达标。

### 4. 技术性工作与 DevOps 任务

这些任务服务于 Sprint 2 但不直接对应单一用户故事（对应 Issue #31、#35、#37、#38 等）：

- **CI 流水线与质量报告升级**  
  - `.github/workflows/ci.yml` 中增加多阶段 Job：lint → test → build/coverage。  
  - 对前后端分别执行 lint/test，统一输出报告到 `docs/test_results/`，并在 `docs/skillgap_eval_dashboard.html` 中集中展示（见 Issue #9、#29、#31）。

- **数据库与错误处理强化**  
  - 对 `auth/profile/history` 的所有 `db.commit()` 添加 `try/except SQLAlchemyError` 和回滚逻辑。  
  - 在 `main.py` 中增加全局 SQLAlchemy 异常处理器，避免生产环境直接 500 崩溃（见 Issue #15、#16）。

- **仓库结构与部署准备（DevOps）**  
  - 将仓库明确拆分为 `client/` 与 `server/` 两个子目录，方便独立部署和 CI 缓存（Issue #35: repo 结构重构）。  
  - 为后端 Render 部署和前端 Netlify 部署准备配置（Issue #37: Render backend，Issue #38: Netlify frontend）。  
  - 每个 PR 运行 GitHub Actions（Lint / Test / Build）并触发 Netlify Deploy Preview 及 Netlify 规则检查（Header rules、Pages changed、Redirect rules），合并前即可验证前端预览与站点配置。

### 5. 完成定义（Definition of Done）

对于 Sprint 2 引入的故事/Issue，规划时约定：

- Claude 相关逻辑有**最小可复现 Prompt**，并在内部文档中记录（用于后续 AI reflections）。
- AI 生成路线的 JSON 结构**稳定**，前端组件使用严格的类型定义渲染。
- `docs/ai_eval_results.md` 和 `docs/skillgap_eval_dashboard.html` 至少覆盖 5+ 真实 JD 场景。  
- CI 流水线默认运行在 Pull Request 上，阻止未通过测试 / 覆盖率不足的代码进入主分支。

### 6. 范围外（明确不在 Sprint 2 内）

- 外部 Blog Post 与公开 Video（属于课程要求的 Documentation/Presentation 阶段）。  
- 与课程无关的高级特性，例如：向量检索、语义搜索、复杂权限系统等。  
- 重写整个 UI 设计系统：Sprint 2 只做「打磨」，不做大规模重构。

