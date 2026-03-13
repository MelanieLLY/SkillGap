# PROJECT2_MASTER_PLAN (Ultimate Guide)

这是一份由Liuyi和AI助手共同写的,极其详细的操作指南，包含了时间预估、使用的 AI 模型推荐、具体的 Prompt 模版、测试驱动开发（TDD）流程、CI/CD 与自动化部署的详细步骤。请**一步一步**打勾执行。

---

## 📅 第 0 阶段：环境准备与 Review 队友代码
**预估时间：1.5 - 2 小时** | **推荐工具：Antigravity IDE AI (使用 Claude Sonnet 模型代替人工通读)**

> **📌 [提前规划] Blog & Video 素材与 AI 记录收集策略**
> 为了避免最后一天手忙脚乱找不到好看的截图和连贯的录屏，**必须从现在开始**，把收集素材作为写每一行代码的“顺手动作”：
>
> ⚠️ **强烈建议：所有的重要 AI 交互（包括 Antigravity IDE 和 Claude Web 里的对话），每得到一个满意的代码结果，顺手就把满意的 Prompt 拷到一个 `ai_prompt_logs.md` 文件里，甚至直接完整截长图。这最后做 AI Reflection (AI Mastery 分数) 会极大地减轻工作量。**
>
> 📝 **Blog 核心素材清单 (1500 字，面向真实产品读者)：**
> - [] **Pain Point 截图：** 之前找工作时繁琐对比 JD 的痛点（可以去网上截图真实 JD）。
> - [] **UI Wow-factor 截图：** 你队友做好的“匹配度环形动画”在深色模式下的高清截图。
> - [] **架构/思维导图：** 用 Claude Web 随时让他画一张 Mermaid 架构图并保存。
> - [] **AI 协作高光时刻：** 遇到神级 Bug 被 Antigravity 一秒修好的时候，**立刻截图你们的对话**。
> - [] **真实用户的 Roadmap 截图：** 第三阶段生成出来的最完美的那个学习路径，截长图。
>
> 🎥 **Video 核心素材清单 (10 分钟，需有起承转合，非流水账)：**
> - [] **开发过程的短录屏：** 比如你在敲一段关键算法时，或者跑 `pytest` 看到 coverage 瞬间变绿的那 5 秒，马上用 Cmd+Shift+5 录下来备用。
> - [] **遇到 Bug 的崩溃瞬间：** 录制一段真实的报错红屏，后面 Video 讲“Challenges”特别好用。
> - [] **丝滑体验连招录屏：** JD 导入 -> 环形动画出分 -> 加载骨架屏 -> 真实 Roadmap 出现的**完整体验流程（没有任何卡顿的版本）**。

---

在开始你的开发之前，**必须先 Review 队友的代码**，因为她已经提交了核心的基础逻辑。如果基础逻辑有漏洞，你后面的 AI 调用和测试会不断报错。

- [x] **Step 0.1 梳理队友成果**
  - **Prompt (发给 Antigravity)**: *"Please review the recent commits and the current state of `main.py` and the frontend components related to Issue #1 to #12. Summarize what my teammate has implemented, the data structures used for the User and Profile models, and point out any obvious bugs, missing error handling, or deviations from the `.antigravityrules` strict type/PEP8 rules."*
  - **Action**: 阅读 AI 的总结，本地跑一下前端 (`npm run dev`) 和后端 (`fastapi dev` 或类似)，确保你能在本地注册、登录、粘贴 JD，并且能看到她做好的环形动画。
- [x] **Step 0.2 建立前后端部署仓库的认知**
  - **部署策略**：根据 `antigravityrules`，前后端必须完全解耦 (SPA 架构)。
  - **前端**：部署在 Vercel 或 Netlify。
  - **后端 & 数据库**：部署在 Render 或 Railway (提供免费/便宜的 PostgreSQL 数据库托管)。
  - *注：我们会在 Step 3 讲如何部署，现在只需知道它们需要分开打包。*

### 🕵️‍♂️ 调查结果与待办修复工作 (Investigation Results & TODOs)
在完成代码 Review 后，我们发现了以下四个严重问题，必须在进入 CI/CD 和测试流程之前立刻修复（请按照顺序打勾完成）：

- [x] **Step 0.3 统一测试与开发的数据库至云端 PostgreSQL**
  - **问题描述**: 队友在测试代码中使用了本地 SQLite，而不符合项目规范中要求必须使用 PostgreSQL 连接云端数据库的要求，这会导致本地测试环境与云端开发/生产环境不一致的严重隐患。
  - **Prompt (发给 Antigravity)**: *"The project currently uses SQLite for testing. According to the project requirements, we must use a cloud PostgreSQL database. Please refactor the database configurations and `pytest` setups to exclusively connect to the Postgres database provided by the `DATABASE_URL` environment variable instead of SQLite."*
  - **Action**: 确保已经在 `.env` 文件中配置了正确的云端 PostgreSQL 的地址，并且 `pytest` 和 FastAPI 能够成功连接并跑通。

- [x] **Step 0.4 修复数据库写入的容错处理 (Missing Rollbacks)**
  - **问题描述**: 在 `auth`、`profile` 和 `history` 的路由中，数据库的增删改操作（`db.commit()`）缺少 `try...except SQLAlchemyError` 以及 `db.rollback()` 保护，容错性极差。
  - **Prompt (发给 Antigravity)**: *"I noticed that the database commit operations in `auth`, `profile`, and `history` routers lack error handling. Please refactor all `db.commit()` calls to include `try...except SQLAlchemyError` blocks with `db.rollback()` and appropriate `HTTPException` raises."*
  - **Action**: 应用 AI 提供的修改，确保所有写库操作都有异常回滚保护。

- [x] **Step 0.5 修复信任客户端传递 `match_score` 的安全漏洞**
  - **问题描述**: 前端目前可以直接提交 `match_score` 到 `/api/history`，这是一个严重的业务逻辑漏洞。分数必须要由后端引擎验证并计算保存。
  - **Prompt (发给 Antigravity)**: *"Currently, our `HistoryCreate` schema in `server/history/schemas.py` accepts `match_score` from the client, which is a security flaw. Please update the `history` router and schemas so that `match_score` is calculated and verified on the backend using our Extraction Engine instead of being blindly trusted from the request body."*
  - **Action**: 跑通本地测试，确保任何人无法伪造分数。

- [x] **Step 0.6 搭建 Claude AI 接入的基础脚手架 (仅限依赖与配置)**
  - **问题描述**: 队友目前只用正则完成了初步的关键词匹配，完全没有接入 Claude AI 生成 subsequent learning plan。为了避免一次性修改过多代码，我们在这一步只做最基础的“脚手架”搭建（比如安装依赖、配置环境变量、写个空函数），不实现完整的业务逻辑和 LLM 对话代码。
  - **Prompt (发给 Antigravity)**: *"We need to prepare for integrating Claude AI later to generate a learning plan. For now, DO NOT write the actual implementation or LLM API calls. I only want you to set up the scaffolding: 1. Ensure `anthropic` is in our dependencies. 2. Add `ANTHROPIC_API_KEY` to `.env.example` and `core/config.py`. 3. Create an empty async placeholder function `generate_roadmap_with_claude` in an appropriate services file that simply returns dummy JSON data. Keep your response and code changes strictly limited to this setup."*
  - **Action**: 确认 `anthropic` 依赖安装无误，配置文件更新完毕，并且占位服务函数已创建好，为将来编写核心 Prompt 逻辑打下基础。

- [x] **Step 0.7 完善代码质量与规范 (类型标注、Docstring、PEP8)**
  - **问题描述**: 部分 FastAPI 处理函数缺少返回值类型提示 (`-> Type`)，底层代码也缺少标准的 Docstrings 以及 PEP8 细节检查。
  - **Prompt (发给 Antigravity)**: *"According to our `.antigravityrules`, we need to adhere to PEP8 with strict typing and high-quality Docstrings. Please review all routers (`auth`, `profile`, `history`, `extraction`) and core services, add complete return Type Hints to every function, and write professional docstrings for all core logic. Keep the current synchronous database session (Session) usage unchanged."*
  - **Action**: 逐一审查后端代码，确认类型提示和文档注释完整且符合 PEP8。

---

## 🧪 第 1 阶段：CI/CD Pipeline 与 TDD 后端测试 
**预估时间：3 - 4 小时** | **推荐工具：Antigravity (切换至 Claude Sonnet 进行强代码逻辑) + Claude Web (写文档/脚本)**

> **🎯 为什么要做 Advanced CI/CD？会很难吗？**
> 老师在项目要求 (Line 26: *Advanced CI/CD: multi-stage pipeline, deploy previews, coverage reporting*) 给了整整 30 分.

按照项目要求的 80%+ Test Coverage，你必须现在就开始写测试。TDD (测试驱动开发) 要求你先让 AI 帮你写好 Test Case，然后再写/跑代码。

- [x] **Step 1.1 设定 Multi-Stage CI/CD Pipeline 与 Coverage Reporting**
  - **Prompt (发给 Claude Web)**: *"I need an advanced GitHub Actions workflow `.yml` file for my full-stack project (React/Vite frontend, FastAPI/Python backend). The pipeline needs to be MULTI-STAGE: Job 1: Linting (ESLint, Prettier). Job 2: Testing (Frontend UI tests if any, and Backend `pytest` with coverage). Job 3: Build & Coverage Reporting (Output coverage to summary). Fail the PR if coverage is below 80%. Please write the detailed `.github/workflows/ci.yml`."*
  - **Action**: 放入 `.github/workflows/ci.yml`。
- [x] **Step 1.2 Setup Pytest & 覆盖率 (Issue #14)**
  - **Prompt (发给 Antigravity)**: *"We need to achieve >80% backend test coverage using `pytest`. Based on the current FastAPI routes and SQLAlchemy models, please create `conftest.py` with database fixtures (using SQLite in-memory for testing) and write unit tests for the Authorization and Keyword Extraction endpoints. We are using TDD, so generate the comprehensive test suite first."*
  - **Action**: 确认 Coverage 达到 80%+。

---

## 🤖 第 2 阶段：核心 AI 接入 (Implementation Phase)
**预估时间：3 - 4 小时** | **推荐工具：Antigravity (Claude Sonnet)**

- [x] **Step 2.1 接入 Claude API 生成 Roadmap (Issue #7)**
  - **Prompt (发给 Claude Web 原型设计)**: *"Design a structured learning roadmap JSON for a developer missing [Skill A, Skill B]. Include timeline, courses, and projects."*
- [x] **Step 2.2 接入后端 Claude API (Issue #7)**
  - **Prompt (发给 Antigravity)**: *"I have designed the JSON schema for our learning roadmap (refer to Step 2.1). Now, please implement the `generate_roadmap_with_claude` function in the backend service. **System Prompt for Claude**: 'You are an expert career coach and technical architect. Your job is to take a list of [MISSING SKILLS] and current [JOB DESCRIPTION] to generate a hyper-realistic 12-week learning roadmap. You MUST ONLY respond in the following JSON format: [粘贴你在 2.1 得到的 JSON 样本]。Do not include any talk or explanation before or after the JSON.' **Requirements**: 1. Use the `anthropic` Python client with `claude-3-5-sonnet-20241022`. 2. Implement a new FastAPI route `/api/roadmap/generate` that uses the missing skills from the user profile. 3. Ensure the function is `async` and includes a 15-second timeout protection."*
  - **Action**: 测试 API，确保后端能稳定返回符合结构的 JSON 数据。
- [x] **Step 2.3 前端呈现 Roadmap 核心数据**
  - **Prompt (发给 Antigravity)**: *"Now that the backend API is ready, please update the Dashboard or Result page. 1. Add a 'Generate Learning Roadmap' button. 2. When clicked, it calls `/api/roadmap/generate`. 3. 复用现有React 组件 RoadmapCard.tsx，接收该 JSON 数据，并使用 Tailwind CSS 将其展示为一个纵向时间线或卡片列表。 We will polish the aesthetics in the next phase."*
  - **Action**: 点击按钮，确认前端能正确接收并初步循环渲染出 Roadmap 的内容。

---

## 🎨 第 3 阶段：UI/UX 打磨与前端 Polish
**预估时间：3 - 4 小时** | **推荐工具：Antigravity (Claude Sonnet)**

- [x] **Step 3.1 前端 UI 骨架屏与 Accessibility (Issue #10)**
  - **Prompt (推荐)**: 针对 `client/src/components/LearningRoadmap.tsx` 实现一个平滑扫光效果 (Shimmer) 的骨架屏状态。要求：1. 结构与真实 Roadmap 一致；2. 数据加载完成后平滑淡入 (Fade-in)；3. 增加 `aria-busy` 等 A11y 细节；4. 组件需可复用且符合accessibility规范。
- [x] **Step 3.2 流程优化与 Wow-factor**
  - **Prompt (推荐)**: 为 Dashboard 增加 Wow-factor 动画：1. 优化 `MatchRing` 使分数增长带弹簧跳动感；2. 实现 Have/Missing/Bonus 三列技能的交错入场 (Staggered Entrance)；3. 给卡片增加 Hover elevation 微交互；4. 如果需要，可引入 `framer-motion`。
  - **Action**: 优化动画过场，录制 90 秒黄金 Demo 素材。

---

## 📊 第 4 阶段：综合评估、质量保证与 Eval Dashboard (核心得分项)
**预估时间：2 - 3 小时** | **推荐工具：Antigravity (切换至 Gemini Pro 处理报告)**

在提交前，我们需要汇总所有的质量证据。

- [x] **Step 4.1 分析并总结现有测试成果 (Part A)**
  - **Prompt (发给 Antigravity)**: *"Please analyze all existing test files in the `tests/` directory. Summarize what features are currently covered by unit and integration tests. Run the full test suite and categorize the results (e.g., Auth tests: 10 passed, Extraction tests: 5 passed). This summary will be Part A of our Eval Dashboard."*
- [x] **Step 4.2 运行 AI 对 AI 质量评估 (Part B - AI Mastery 分数)**
  - **Prompt (发给 Antigravity)**: *"Write an automated AI Assessment script `ai_eval.py`. It should take 5 sample Job Descriptions, run them through our Claude roadmap generator, and then use another LLM call as a 'Judge' to score the generated roadmap based on: 1. Relevance, 2. Specificity, and 3. Completeness (1-5 scale). Output results to `docs/ai_eval_results.md`."*
- [x] **Step 4.3 代码质量与安全扫描 (Part C)**
  - **Action**: 运行 `ruff check .` (代码质量), `bandit -r server/` (安全), `npm audit` (前端安全)。记录结果。
- [x] **Step 4.4 整合并生成最终 Eval Dashboard PDF**
  - **Action**: 将以上数据（Pytest 总结、AI 质量评分、安全报告）汇总成一份 PDF。这才是老师要的 **Eval Dashboard**。---我写成了html:skillgap-eval-dashboard.html

---

## 🚀 第 5 阶段：自动化部署与 Deploy Previews
**预估时间：2 小时**

- [ ] **Step 5.1 前端部署 (Vercel) 与 Deploy Previews**
  - **Action**: 链接 GitHub 仓库，配置 PR Previews。
- [ ] **Step 5.2 后端部署 (Render/Railway)**
  - **Action**: 部署 FastAPI 和云端 PostgreSQL。

---

## 📝 第 6 阶段：Documentation Package 与 Final 整理
**预估时间：4 - 6 小时**

- [ ] **Step 6.1 整理 README, API Docs & Blog Post**
- [ ] **Step 6.2 整理 Scrum (Sprint Retrospectives) 与 AI Reflection**
- [ ] **Step 6.3 视频制作与提交**

---

## 💡 总指导原则 (Cheat Sheet)
1. **是否要边做边 check coverage？**  
   **绝对是的。** 每次修改重要逻辑（特别是提取算法或 AI 提示词路由），必须跑一次 `pytest` 看看是否掉了 80%。掉下去立刻让 Antigravity 补充相应的单元测试。**TDD 原则：先让 AI 写测试 -> 报错 -> 让 AI 写实现代码 -> 通过。**
2. **前后端必须分开吗？**  
   **必须的。** 根据你们的 `.antigravityrules`，你们是 React SPA + FastAPI，完全分离。你需要分别部署在专门托管前端（Vercel）和后端（Render/Railway）的平台上。
3. **不同 AI 模型怎么分工？（只使用我们定好的工具）**  
   - **Antigravity (IDE 侧的 AI Agent)**: 你可以根据需要在 Antigravity 中**灵活切换模型**：
     - **使用 Claude 3.5/3.7 Sonnet**: 强代码逻辑，负责改 Bug、写 `pytest` 测试、处理架构、写代码组件。
     - **使用 Gemini 1.5/3.1 Pro**: 大上下文窗口，当你需要扔进海量 Evaluation 测试数据/日志分析时使用。
   - **Claude Web**: 前期用来发散探索架构思路、生成思维导图/流程图 (Mermaid)、生成最初的 Demo JSON 结构、写偏向叙事性质的长篇英文 Blog 等。

---

## ✅ Final 要交的文件与材料清单

- [x] **GitHub 仓库链接** (预计: 0.5 小时 / Est: 0.5h): https://github.com/MelanieLLY/SkillGap 
- [x] **已部署前端应用 URL**(生产环境, 如 Vercel) (预计: 3–4 小时 / Est: 3–4h)  
  - `https://skillgapweb.netlify.app`
- [x] **已部署后端 API 基础 URL**(如 Render/Railway) (预计: 4–6 小时 / Est: 4–6h)  
  - `https://skillgap-api-hrsc.onrender.com`

- [x] **Eval Dashboard 文档本体** (预计: 已完成, 如需补充 PDF 再花 0.5–1 小时 / Est: done; extra 0.5–1h for PDF)  
  - [x] 一份面向老师/TA 的测试结果文档(目前为 HTML `docs/skillgap_eval_dashboard.html`, 推荐后续再导出/补充 PDF 版本), 内容包括:
    - [x] 测试套件运行结果说明(哪些测试、通过多少、分类情况)
    - [x] 覆盖率数据与截图/报告摘录
    - [ ] 如有 Cypress/Playwright 等 HTML 报告, 在文档中附链接或截图说明

- [△] **项目根目录主 `README` 文件** (预计: 2–3 小时 / Est: 2–3h)  
  - [△] 项目简介与主要功能说明(当前 `README.md` 只有安装/运行说明, 需要补全简介和功能)
  - [△] Tech stack 说明(前端/后端/数据库/部署)
  - [x] 本地运行与部署步骤(安装 & 本地运行命令已存在, 但还可更详细)
  - [ ] 测试运行方式(`pytest`、前端测试命令等)
  - [ ] CI/CD 简要说明(使用了什么 workflow、覆盖率门槛等)
  - [ ] 指向其他文档的链接(博客、视频、API docs、Eval dashboard 等)

- [ ] **API 文档** (预计: 2–3 小时 / Est: 2–3h)  
  - [ ] 人类可读的 API 文档文件(例如 `docs/api-docs.md` 或 `api-documentation.pdf`)  
  - [ ] 如有 OpenAPI/Swagger:
    - [ ] 在线 Swagger UI 链接, 或
    - [ ] 导出的 OpenAPI JSON/YAML 文件路径

- [△] **Documentation Package 相关文档** (预计: 4–6 小时 / Est: 4–6h)  
  - [ ] Sprint planning 文档(例如 `docs/sprint-planning-sprint1.md`, `...sprint2.md` 或合并在一个文件中清晰分段)  
  - [ ] 两个 sprint 的 retrospectives 文档(可以与 planning 区分小节或分文件)  
  - [ ] AI modalities 使用说明文档(例如 `docs/ai-modalities-usage.md`, 说明 Claude Web / IDE 等如何在项目中使用、什么时候用、用来做什么)  
  - [△] AI reflections 文档(已有内部规划类文档和 AI 对话记录, 但尚未整理成正式 `docs/ai-reflection.md`)  
  - [△] 整个代码的文档化文件(已有较完整的 PRD `docs/skillgap_prd.md` 和 `docs/user_story.txt`, 但仍需一份专门面向代码结构/模块的数据流的总结文档, 如 `docs/code-architecture.md`)

- [△] **1500 字 technical / quality blog post** (预计: 4–6 小时(含 AI 辅助与人工润色) / Est: 4–6h incl. AI + editing)  
  - [△] Blog 正文本身(目前有 internal outline `internal_working_planning_note/final_delivery/blog_post_outline.md`, 但尚未整理成对外成稿)  
  - [ ] 内容面向公众、product-oriented、user-facing, 展示产品和团队能力(区别于课程反思)

- [△] **10 分钟公开视频** (预计: 4–6 小时(准备脚本+录制+剪辑) / Est: 4–6h for script + recording + editing)  
  - [ ] 公共可访问的视频 URL(YouTube 等)  
  - [ ] 视频中包含:
    - [ ] 项目简介 / short summary / intro  
    - [ ] 应用 walkthrough 与功能展示  
    - [ ] 技术/架构/开发方法讲解  
    - [ ] 开发过程中遇到的挑战与解决方式  
    - [ ] AI 如何参与开发  
    - [ ] 团队分工与协作方式  
    - [ ] 主要 deliverables 的总体讲解  
    - [ ] 两位组员都出镜  

- [△] **Agile / 团队协作相关证据** (预计: 2–3 小时 / Est: 2–3h)  
  - [△] 描述每个成员具体贡献与分工的文档(目前有 `internal_working_planning_note/GitHub project board.md` 等内部记录, 但尚未提炼成对老师的正式 summary, 如 `docs/team-contributions.md`)  
  - [△] 若 GitHub commit 记录不均衡, 提供额外佐证(你已有大量 AI chat history 和 planning note, 但需要挑出代表性片段整理到正式文档中)

- [x] **测试与质量相关原始/辅助文件** (预计: 已完成, 如需统一整理摘要再花 1–2 小时 / Est: done; 1–2h for consolidated summary)  
  - [x] 后端测试代码目录(如 `server/tests/`)  
  - [x] 用于 AI 质量评估的脚本及结果(已根据 `docs/eval_roadmaps/ai_eval_results.md` 和 Eval Dashboard 生成评估结果)  
  - [x] 覆盖率报告原始文件/输出(已有 `docs/test_results/backend_test_report.txt` 与 `docs/test_results/frontend_test_report.txt`, 以及 `docs/test_results/test_summary.md`)  
  - [ ] 代码质量/安全扫描结果摘要(如 `docs/quality-and-security-report.md`, 目前仅有运行记录, 尚未写成统一总结文档)

- [ ] **CI/CD 相关文件与说明** (预计: 2–3 小时 / Est: 2–3h)  
  - [ ] GitHub Actions workflow 文件(如 `.github/workflows/ci.yml`)  
  - [x] 若有部署 pipeline / preview 配置, 在 README 或 `docs/ci-cd.md` 中简单说明其行为：已在 **README §8 Deployment** 中说明 GitHub Actions（Lint / Test / Build）、Netlify Deploy Preview 及 Netlify 规则检查（Header / Pages changed / Redirect），并附 PR 检查截图链接。  

- [ ] **提交到 Canvas 用的总索引说明文档** (预计: 1–2 小时 / Est: 1–2h)  
  - [ ] 在 GitHub 仓库中创建一份汇总所有关键链接和仓库内路径的短文档(例如仓库根目录或 `docs/` 下的 `submission-index.md`)  
  - [ ] 文档内容至少包括:
    - [ ] GitHub 仓库链接  
    - [ ] 前端生产环境 URL  
    - [ ] (可选) 后端 API base URL  
    - [ ] Eval Dashboard 文档链接或在仓库中的路径  
    - [ ] Blog post 链接  
    - [ ] 视频链接  
    - [ ] Documentation package 中 README / API docs / Scrum / AI reflections / code docs 等关键文档的相对路径列表  
  - [ ] 提交 Canvas 时, 选择其一:
    - [ ] 方式 A: 将 `submission-index.md` 的内容复制到 Canvas 的文本框中  
    - [ ] 方式 B: 将 `submission-index.md` 导出为 PDF 或下载后上传到 Canvas  


---

## 📝 Appendix: Final Deliverables Checklist (English Mirror)

> This section is a **1:1 English mirror** of the Chinese checklist above.  
> The structure, items, and check/triangle states are intentionally kept **identical** for team alignment.

### ✅ Final Deliverables & Artifacts

- [x] **GitHub Repository Link** (Estimated: 0.5h): https://github.com/MelanieLLY/SkillGap 
- [x] **Deployed Frontend App URL** (production, e.g. Vercel) (Estimated: 3–4h)  
  - `https://skillgapweb.netlify.app`
- [x] **Deployed Backend API Base URL** (e.g. Render/Railway) (Estimated: 4–6h)  
  - `https://skillgap-api-hrsc.onrender.com`

- [x] **Eval Dashboard Document** (Estimated: done; if exporting/adding PDF, extra 0.5–1h)  
  - [x] A test-results document for instructor/TA (currently HTML `docs/skillgap_eval_dashboard.html`; recommended to later export/add a PDF version) including:
    - [x] Explanation of full test suite runs (which tests, how many, by category)
    - [x] Coverage numbers with screenshots / report excerpts
    - [ ] If Cypress/Playwright HTML reports exist, add links or screenshots in this doc

- [△] **Root-Level Project `README`** (Estimated: 2–3h)  
  - [△] Project overview & main feature description (current `README.md` only has install/run instructions; needs a fuller intro and feature list)
  - [△] Tech stack overview (frontend / backend / DB / deployment)
  - [x] Local run & setup steps (install & dev commands already exist, could still be expanded)
  - [ ] Test commands (`pytest`, frontend test commands, etc.)
  - [ ] CI/CD summary (which workflows, coverage gate, etc.)
  - [ ] Links to other docs (blog, video, API docs, eval dashboard, etc.)

- [ ] **API Documentation** (Estimated: 2–3h)  
  - [ ] Human-readable API docs file (e.g. `docs/api-docs.md` or `api-documentation.pdf`)  
  - [ ] If using OpenAPI/Swagger:
    - [ ] Online Swagger UI link, or
    - [ ] Exported OpenAPI JSON/YAML file path

- [△] **Documentation Package Artifacts** (Estimated: 4–6h)  
  - [ ] Sprint planning docs (e.g. `docs/sprint-planning-sprint1.md`, `...sprint2.md`, or a single file with clearly separated sections)  
  - [ ] Two sprint retrospective docs (may be separate files or sections distinct from planning)  
  - [ ] AI modalities usage document (e.g. `docs/ai-modalities-usage.md`, explaining how Claude Web / IDE, etc. are used, when, and for what)  
  - [△] AI reflections document (you already have rich internal planning notes and AI chat logs, but they have not been curated into a formal `docs/ai-reflection.md`)  
  - [△] Full-code documentation file (you have a solid PRD `docs/skillgap_prd.md` and `docs/user_story.txt`, but still need a code-structure/data-flow–focused summary such as `docs/code-architecture.md`)

- [△] **1500-word Technical / Quality Blog Post** (Estimated: 4–6h incl. AI assistance + human editing)  
  - [△] Blog body itself (currently you have an internal outline `internal_working_planning_note/final_delivery/blog_post_outline.md`, but not a polished external-facing article)  
  - [ ] Content must be public-facing, product-oriented, and user-oriented, showcasing product and team capabilities (distinct from course reflection)

- [△] **10-Minute Public Video** (Estimated: 4–6h for script + recording + editing)  
  - [ ] Publicly accessible video URL (YouTube, etc.)  
  - [ ] Video should include:
    - [ ] Project intro / short summary  
    - [ ] Application walkthrough and feature demo  
    - [ ] Explanation of key techniques / architecture / approaches  
    - [ ] Development challenges and how you solved them  
    - [ ] How AI participated in development  
    - [ ] Team roles and collaboration  
    - [ ] High-level overview of major deliverables  
    - [ ] Both teammates appearing on camera  

- [△] **Agile / Team Collaboration Evidence** (Estimated: 2–3h)  
  - [△] Document describing each member’s concrete contributions and responsibilities (you currently have internal records like `internal_working_planning_note/GitHub project board.md`, but not yet a polished summary doc like `docs/team-contributions.md`)  
  - [△] If GitHub commit history is imbalanced, provide supporting evidence (you already have extensive AI chat history and planning notes, but need to extract representative snippets into a formal document)

- [x] **Testing & Quality-Related Raw/Supporting Files** (Estimated: done; 1–2h if writing a consolidated summary doc)  
  - [x] Backend test directory (e.g. `server/tests/`)  
  - [x] AI evaluation scripts and results (based on `docs/eval_roadmaps/ai_eval_results.md` and the Eval Dashboard)  
  - [x] Raw coverage outputs (e.g. `docs/test_results/backend_test_report.txt`, `docs/test_results/frontend_test_report.txt`, and `docs/test_results/test_summary.md`)  
  - [ ] Consolidated code-quality / security summary doc (e.g. `docs/quality-and-security-report.md`; currently you have run results but not a unified written summary)

- [ ] **CI/CD Files & Explanations** (Estimated: 2–3h)  
  - [ ] GitHub Actions workflow files (e.g. `.github/workflows/ci.yml`)  
  - [ ] If you have deploy pipelines / preview configs, briefly describe them in `README` or `docs/ci-cd.md`  

- [ ] **Canvas Submission Index Document** (Estimated: 1–2h)  
  - [ ] Create a short index document in the GitHub repo that aggregates all key links and repo paths (e.g. `submission-index.md` at repo root or under `docs/`)  
  - [ ] The document should at least contain:
    - [ ] GitHub repository link  
    - [ ] Frontend production URL  
    - [ ] (Optional) Backend API base URL  
    - [ ] Eval Dashboard document link or repo path  
    - [ ] Blog post link  
    - [ ] Video link  
    - [ ] Relative paths for key Documentation Package artifacts (README / API docs / Scrum docs / AI reflections / code docs, etc.)  
  - [ ] When submitting on Canvas, choose one:
    - [ ] Option A: Copy the content of `submission-index.md` into the Canvas text entry box  
    - [ ] Option B: Export `submission-index.md` as PDF or download it and upload to Canvas  


---

## 📝 附录：Blog & Video 详细骨架草案
*(内容同前，已根据新阶段调整)*
