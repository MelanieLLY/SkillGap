# PROJECT2_MASTER_PLAN (Ultimate Guide)

这是一份极其详细的操作指南，包含了时间预估、使用的 AI 模型推荐、具体的 Prompt 模版、测试驱动开发（TDD）流程、CI/CD 与自动化部署的详细步骤。请**一步一步**打勾执行。

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
> 老师在项目要求 (Line 26: *Advanced CI/CD: multi-stage pipeline, deploy previews, coverage reporting*) 给了整整 30 分。听起来吓人，但**在使用 AI 辅助编程时，写一个包含全部高级玩法的 CI/CD YAML 文件只需要 10 秒钟**。所以这其实是白送分，你只要按下面的 Prompt 生成文件并推送到 GitHub 即可，完全不需要去手敲那些配置。

按照项目要求的 80%+ Test Coverage，你必须现在就开始写测试。TDD (测试驱动开发) 要求你先让 AI 帮你写好 Test Case，然后再写/跑代码。

- [x] **Step 1.1 设定 Multi-Stage CI/CD Pipeline 与 Coverage Reporting**
  - **Prompt (发给 Claude Web)**: *"I need an advanced GitHub Actions workflow `.yml` file for my full-stack project (React/Vite frontend, FastAPI/Python backend). The pipeline needs to be MULTI-STAGE: Job 1: Linting (ESLint, Prettier). Job 2: Testing (Frontend UI tests if any, and Backend `pytest` with coverage). Job 3: Build & Coverage Reporting (Output coverage to summary). Fail the PR if coverage is below 80%. Please write the detailed `.github/workflows/ci.yml`."*
  - **Action**: 将生成的 `ci.yml` 放入仓库底下的 `.github/workflows/ci.yml`（没有文件夹就新建）。然后在 GitHub Actions 页面查看它分阶段打绿勾的过程。这时候挂掉完全没关系，继续往下走去写测试。
  *(注：这里的截图等 Step 1.2 你的覆盖率真的合格后，或者第二阶段所有功能写完后，最后回来截一次最新跑绿的 CI。不用第一天强行去截。)*
- [x] **Step 1.2 Setup Pytest & 覆盖率 (Issue #14)**
  - **Prompt (发给 Antigravity)**: *"We need to achieve >80% backend test coverage using `pytest`. Based on the current FastAPI routes and SQLAlchemy models, please create `conftest.py` with database fixtures (using SQLite in-memory for testing) and write unit tests for the Authorization and Keyword Extraction endpoints. We are using TDD, so generate the comprehensive test suite first."*
  - **Action**: 运行 `pytest --cov=app --cov-report=term-missing` (或类似命令)。**每次做完一个新功能，立刻跑这个命令看 coverage 是否掉下 80%。**
  - 📸 **视频素材收集 (Video Artifact):** 用屏幕录制软件 (Cmd+Shift+5) 录制一次你敲下 `pytest --cov` 并看到整排变绿、Coverage 超过 80% 的动画过程 (3-5秒素材，为 10 分钟 Demo Video 的 DevOps 环节积攒震撼力)。
  - 📸 **文档素材收集 (Eval Dashboard Artifact):** 截图/保存 Terminal 中 Test Coverage 达到 80%+ 的输出画面，转存为 PDF。

---

## 🤖 第 2 阶段：核心 AI 接入与评估系统 (Evaluation Suite)
**预估时间：4 - 5 小时** | **推荐工具：Antigravity (切换至 Claude Sonnet 写后端, 切换至 Gemini 1.5/3.1 Pro 处理巨量评估报告)**

这部分对应老师的 *AI Mastery* (30 pts)。结合你的批注，我们要同时使用：Antigravity 用于代码与大规模数据处理，Claude Web 用于原型与设计。

- [ ] **Step 2.1 接入 Claude API 生成 Roadmap (Issue #7)**
  - **Prompt (发给 Claude Web 原型设计)**: *"I am building a feature that takes a list of 'Missing Skills' from a user's profile and generates a structured learning roadmap. Can you act as the Anthropic API and give me a sample JSON response that includes a timeline, course recommendations, and project ideas? Keep it highly structured."*
  - **Prompt (发给 Antigravity 生成代码)**: *"Now, using the Anthropic Python SDK, write an asynchronous FastAPI endpoint `/api/roadmap/generate`. It must take the missing skills, call the `claude-3-5-sonnet-20241022` model (token strictly in `.env`), and parse the response into Pydantic models matching this JSON structure: [粘贴上一步的 JSON]。Ensure proper error handling if the API times out."*
  - **Action**: 测试 API，确保后端能稳定返回 roadmap。
  - 📸 **博客素材收集 (Blog Artifact):** 截图你和 Claude Web 设计原始 JSON 的讨论过程（展示你对 Prompt Engineering 和原型设计的思考）。
- [ ] **Step 2.2 构建 AI Evaluation Suite (Issue #9)**
  - 老师要求评价 AI 质量。
  - **Prompt (发给 Antigravity)**: *"I need an automated AI Evaluation Suite in Python. Write a batch script `eval_suite.py` that takes 5 dummy Job Descriptions, runs them through our keyword extractor and Claude roadmap generator, and then uses another LLM call (as a judge) to score the generated roadmap based on 1. Relevance, 2. Specificity, and 3. Completeness (1-5 scale). Output the results to a Markdown report."*
  - **Action**: 运行该脚本。
  - 📸 **Artifact Collection**: 保存生成的 `eval_results.md`。这就是你们的 **Eval Dashboard / Testing Report** 交付物！

---

## 🎨 第 3 阶段：UI/UX 打磨与自动化部署
**预估时间：3 - 4 小时** | **推荐工具：Antigravity (切换至 Claude Sonnet 专精前端 Tailwind)**

- [ ] **Step 3.1 前端 UI 骨架屏与 Accessibility (Issue #10)**
  - 等待 Claude API 返回需要十几秒，必须有 Loading 动画。
  - **Prompt (发给 Antigravity)**: *"Our users wait around 10-15 seconds for the Claude API to generate a roadmap. Please create a highly polished, responsive skeleton loading state component using Tailwind CSS. It should mimic the timeline card layout. Also, ensure all new buttons and inputs have `aria-label` and full keyboard accessibility."*
  - **Action**: 体验应用，确保从注册 -> JD输入 -> 匹配度环形动画 -> 生成 Roadmap 的整个流程“丝滑且看起来非常高级 (Wow factor)”。
  - 📸 **博客素材收集 (Blog Artifact):** 截取最高清的深色模式（或你们设计的风格）UI 图，特别是那张绝美的环形动画成果图，作为博客的 Hero Image。
  - 📸 **视频素材收集 (Video Artifact):** 终于完成整个闭环了！现在立刻录制一段**最完美的一镜到底 Demo (黄金 90 秒)**，这将会是你们组最终 Demo Video 里的核心画面。
- [ ] **Step 3.2 部署 (Deployment) 与 Deploy Previews**
  - 老师要求的 **Deploy Previews**（自动化预览）最简单的拿分方式是用 **Vercel 免费版**。你不需要自己去拉服务器配域名，这完全是白给的分数。
  - **前端部署 (Vercel)**：将你的 GitHub 仓库根目录下的 `client/` 文件夹链接到 Vercel。每次你提 Pull Request 开发新功能时，Vercel 都会自动给你生成一个针对这个 PR 的独立预览链接（**这就是老师要求的 Deploy Preview**）。
  - **后端/数据库部署**：在 Render, Railway 或 Fly.io (都提供免费层) 链接你的仓库里的 `server/`，设置 Start Command (`uvicorn main:app --host 0.0.0.0`)。去申请一个 PostgreSQL 数据库，把 `DATABASE_URL` 塞进后端环境变量。
  - 📸 **文档素材收集 (Deploy Previews Artifact):** 提一个包含新功能的 PR 到 `main` 分支。在 GitHub PR 页面截图 Vercel 机器人的自动回复（"Vercel Deploy Preview Ready!"和对应的独占 URL 链接）。把这张图放到最终报告里。
  - **Prompt (发给 Antigravity 若部署遇报错)**: *"I am trying to deploy the frontend to Vercel and the backend to Render. Here is my folder structure and the error log from Render: [粘贴报错]. How do I fix the build command or docker deployment?"*

---

## 📝 第 4 阶段：Documentation Package 与 Final 整理
**预估时间：4 - 6 小时** | **推荐工具：Antigravity (切换至 Gemini 模型) / Claude Web (擅长长文本和博客排版)**

这是你拿满 *Documentation* (15 pts) 和展示 *Agile Process* (20 pts) 的关键。

- [ ] **Step 4.0 最终代码规范清扫 (Type Hints & Docstrings)**
  - **问题描述**: 在前面的一路狂奔式开发中，AI 和你难免会漏掉一些类型提示 (`Type Hints`)，也没有在所有地方补齐完全符合 PEP8 规范的专业 Docstrings。现在功能已经写完了，是时候做一次大规模的规范清理了，这样不仅不会引发业务 Bug，还能拿满代码质量分。
  - **Prompt (发给 Antigravity)**: *"Our codebase features are fully implemented, but we need to ensure strictly typed and fully documented code according to `.antigravityrules`. Please sweep through all files in `server/`, add complete Python Type Hints (`-> Type`) to every function, and write high-quality PEP8 compliant Docstrings explaining the arguments, return values, and behavior of all classes and core algorithms. Do not alter any business logic or the current synchronous session usage."*
  - **Action**: 快速通过 IDE 查看是不是每个函数都有了绿色的文档注释和类型提示。

- [ ] **Step 4.1 准备 README & API Docs**
  - **Prompt (发给 Claude Web)**: *"Here is my FastAPI `openapi.json` and my `docker-compose.yml`. Generate a comprehensive `README.md` for a full-stack project and a separate `API_DOCS.md`. Include a polished project description, setup instructions, sequence diagrams (in Mermaid JS), and the tech stack."*
- [ ] **Step 4.2 攥写 1500 字 Technical Blog Post**
  - **Prompt (发给 Antigravity 或 Claude Web)**: *"I need to write a 1500-word product-oriented, user-facing technical blog post for my project 'SkillGap'. The project matches resumes to JD keywords and uses Claude AI to generate a learning roadmap. Structure the blog to talk about the product value, the technical architecture (React + FastAPI), the challenges of CI/CD and AI integration, and a showcase of the final UI. Write it in a professional, engaging tone suitable for Medium or LinkedIn. DO NOT sound like a generic AI blob. Use real architectural insights."*
  - **Action**: 人工润色，插入 2-3 张最精美的真实页面截图。
- [ ] **Step 4.3 整理 Scrum 与 AI Reflection**
  - **Prompt (发给 Claude Web)**: *"Write a Sprint Retrospective for Sprint 2. Also write an 'AI Reflection' document detailing how my teammate and I used IDE-centric AI (Antigravity with Claude Sonnet) for coding React components/pytest, and Web-based AI (Claude Web) for documentation, initial API prototyping, and brainstorming. Discuss our strategy of doing continuous test coverage and how AI accelerated the CI/CD pipeline setup."*
- [ ] **Step 4.4 录制 10-Minute Video**
  - 📸 **内容大纲**：
    - 0-2min: 自我介绍与产品解决的痛点 (User Story)。
    - 2-5min: 丝滑的 UI Walkthrough（演示核心环形动画、获取 Roadmap 的全环节）。
    - 5-7min: 代码架构、CI/CD Pipeline 展示（展示 GitHub Actions 跑通的绿勾）。
    - 7-9min: AI 评估系统展示与覆盖率报告展示。
    - 9-10min: 团队敏捷协作反思与 AI 协作心得总结。
- [ ] **Step 4.5 最终提交**
  - 将 README, API Docs, Blog Post, Eval/Coverage PDF, AI Reflections, Scrum Retrospectives 全部放进 `docs/` 文件夹。
  - 在 Canvas 提交：GitHub 链接，部署的 App URL，YouTube 视频链接，以及 Blog 链接/PDF。

---

## 📝 附录：Blog & Video 详细骨架草案

### 📖 Blog Post 草稿大纲 (1500 字，主打印刷品一样的观感)
*   **引言 (150 字)**: 谁需要 SkillGap？讲述个人曾经面临 JD 与自身简历不符合的繁琐找工作经历。
*   **产品展示/Product Showcase (300 字)**: 放入最完美的深色模式截图。介绍产品的三个核心功能：JWT 保护的个人档案管理 -> 自动抓取分析岗位关键字引擎 -> Anthropic 动态大模型加持的学习路径 (Roadmap) 生成器。
*   **技术架构 (400 字)**: 展现这门课的灵魂——你的后端如何使用 FastAPI 与 Pydantic 并发解构来自客户端的高强度请求，以及你的 Postgres 数据库如何在 Render 上优雅托管。**插入用 Claude Web 生成的 Mermaid 架构图。**
*   **Advanced CI/CD 之路 (250 字)**: 分享一开始自动化测试是红色的，你们怎么通过编写 80%+ 覆盖率的 Pytest 和 Vercel Deploy Preview 一步手搓出现代化工业流水线。**插入那一阶梯绿色的 GitHub Actions 跑通图。**
*   **AI 狂欢与团队协作 (250 字)**: 你与队友如何运用双 AI (IDE AI vs Web AI) 模型极速写出前后端分离项目。**放入你们那张修神级 Bug 瞬间最得意的长截图。**
*   **总结 (150 字)**: 项目展望，号召别人使用。附上你的 LinkedIn 和 Repo 地址。

### 🎥 10 分钟 Demo Video 脚本提纲 (精确到分钟，坚决拒绝流水账念稿)
在这 10 分钟的视频里，你俩作为开发者一定要在镜头中连线露面（画中画）。
*   **[0:00 - 1:30] The Hook (吸引力法则):**
    *   开头抛出问题："Have you ever spent hours reading a JD, only to realize you have no idea what skills you’re missing?"
    *   介绍产品名称解决什么问题，并直接贴出**最丝滑的那个“环形动态计分板”过场动画（前期收集的 90 秒黄金 Demo 录屏剪辑 10 秒进来作为前戏）**。
*   **[1:30 - 4:00] Product Walkthrough (真实操作秀):**
    *   队友或你演示：注册登录 -> 右边贴上 JD -> 秒出三列式比较表 -> 接着点击“生成学习规划”，等待 Skeleton 动几下，出来完整的 Roadmap 卡片。
    *   *强调 UX 的丝滑度与骨架加载等产品细节。*
*   **[4:00 - 6:00] Under the Hood: Technical Architecture & DevOps (高级开发分摊板):**
    *   展示你们解耦（Decoupled）的 Vercel + Render 部署情况。
    *   **重点展示：** 打开 GitHub Actions 页面指着绿框说 "This is our multi-stage pipeline..." 以及 "We set up automated Deploy Previews with Vercel." 这是全方位的得分点。
*   **[6:00 - 7:30] Test Coverage & AI Eval Suite (品质保证与测试):**
    *   秀出你们跑出来的后端 80% Coverage HTML（或者之前的终端截图录屏）。
    *   秀出那个针对 5 个 Dummy JDs 的 Evaluation Score 结果，告诉老师你们怎么通过 AI Judge 控制大模型回答的准确性。
*   **[7:30 - 9:30] AI Modalities & Challenges (AI 的双重维度使用与困难解决):**
    *   轮流讲：我们在本地用 Anthropic 构建逻辑，在网页上用 Gemini 批量处理大量测试日志，互相补足。
    *   分享你们曾经修过的前后端分离跨域或者 ORM 持久化存数据的巨大挑战，然后是如何用 AI 解决的。
    *   拿出那张**满头大汗报错红屏 -> 修复绿屏的精美对比截图**。
*   **[9:30 - 10:00] Agile Retrospective (敏捷回顾):**
    *   总结两周 Sprint 的心路历程，挥手收尾，提供部署链接。

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
