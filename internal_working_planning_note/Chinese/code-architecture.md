## SkillGap 代码架构总览

本文件从**工程视角**概括 SkillGap 的整体代码结构、关键模块与数据流，配合 `docs/skillgap_prd.md` 和 `docs/user_story.txt` 使用，可以帮助读者快速理解实现如何支撑 PRD 中的用户故事。

---

## 1. 总体架构

- **前端（client）**：React 18 + TypeScript + Vite + Tailwind CSS，使用 Zustand 做全局状态管理，Vitest 做前端单元测试。
- **后端（server）**：FastAPI + SQLAlchemy + PostgreSQL，负责认证、技能档案管理、JD 技能提取、分析历史持久化、Claude 路线生成。
- **AI 层**：封装在 `server/roadmap/services.py` 中，通过 Anthropic Claude API 生成结构化学习路线。
- **持久化层**：`server/database.py` 负责创建 SQLAlchemy Engine/Session；各模块在 `auth/models.py`、`history/models.py` 等中定义 ORM 模型。
- **CI/CD 与质量控制**：`.github/workflows/ci.yml` 配置多阶段流水线（lint → test → coverage），并配合 `docs/test_results/*`、`docs/skillgap_eval_dashboard.html` 做质量展示。

整体模式是典型的 **React SPA + FastAPI REST API + Postgres DB**，前后端完全分离，通过 HTTPS JSON API 交互。

---

## 2. 后端结构与模块职责

后端代码位于 `server/` 目录，核心入口为 `main.py`：

- 创建 FastAPI 应用（`app = FastAPI(title="SkillGap API", lifespan=lifespan)`）。
- 配置 CORS，允许本地开发和生产前端域名访问。
- 在 `lifespan` 中完成数据库表创建和 Postgres 专用的 `skills` 数组列迁移。
- 注册各业务路由：
  - `/api/auth` → `auth/router.py`
  - `/api/profile` → `profile/router.py`
  - `/api`（技能提取） → `extraction/router.py`
  - `/api/history` → `history/router.py`
  - `/api/roadmap` → `roadmap/router.py`

### 2.1 认证模块 `auth/`

- **`auth/models.py`**：定义 `User` 实体（包含 `email`、`hashed_password`、`is_active`、`skills`、`roadmap` 等字段）。
- **`auth/schemas.py`**：Pydantic 模型，用于请求/响应：
  - `UserCreate` / `UserOut` / `Token` 等。
- **`auth/utils.py`**：
  - 密码哈希与校验（通常基于 `passlib` 或 `bcrypt`）。
  - JWT 创建工具（`create_access_token`），遵守配置中的过期时间。
- **`auth/deps.py`**：
  - `get_current_user` / `get_current_active_user` 等依赖，用于在路由中注入当前用户对象。

**路由：`auth/router.py`**

- `POST /api/auth/register`：创建新用户、加密密码并持久化到数据库。
- `POST /api/auth/login`：验证邮箱 + 密码，返回 JWT access token。
- `GET /api/auth/me`：通过 `get_current_active_user` 返回当前用户信息。

所有受保护的业务接口都依赖 `get_current_active_user`，这一点在 Profile/History/Roadmap 模块中统一使用，确保业务逻辑不重复实现认证流程。

### 2.2 技能档案模块 `profile/`

- **`profile/schemas.py`**：
  - `SkillAddRequest`：添加技能时的请求体。
  - `ResumeExtractRequest`：简历文本技能提取请求体。
- **`profile/router.py`** 提供围绕用户技能数组的 CRUD 逻辑：
  - `GET /api/profile/skills`：返回当前用户 `skills` 字段（Postgres VARCHAR[]，在 SQLite 测试环境下则为兼容实现）。
  - `POST /api/profile/skills`：添加单个技能，做去空 & 去重（大小写不敏感）。
  - `DELETE /api/profile/skills/{skill_name}`：按名称删除技能。
  - `POST /api/profile/extract-resume`：利用 `extraction/engine.py` 中 `CURATED_SKILLS` 列表，从长文本简历中匹配技能，并合并到用户 `skills`。

该模块本质上是对 `User.skills` 列的封装，隐藏了数组存储细节，为前端提供简单的字符串列表接口。

### 2.3 JD 技能提取模块 `extraction/`

- **`extraction/engine.py`**：
  - 定义 `CURATED_SKILLS`：经过人工挑选的 60+ 技术技能关键字。
  - `extract_skills(job_description, user_skills)`：从 JD 中匹配技能并划分为 `have` / `missing` / `bonus`。
  - `extract_company_and_position(job_description)`：通过正则/启发式方法从 JD 文本中提取公司名和职位名。
- **`extraction/router.py`**：
  - Pydantic 模型 `ExtractRequest` / `ExtractResponse`。
  - `POST /api/extract`：对外暴露提取接口，纯函数式调用 `engine`，无数据库依赖。

此模块是整个应用的「规则引擎核心」，为后续 History 与 Roadmap 提供结构化的基础数据。

### 2.4 分析历史模块 `history/`

- **`history/models.py`**：
  - `AnalysisHistory` 模型：记录每一次 JD 分析结果，包括 job title、company、have/missing/bonus、match_score、原始 JD 文本、分析时间等。
- **`history/schemas.py`**：
  - `HistoryCreate` / `HistoryUpdate` / `HistoryResponse`：将数据库模型结构化为 REST API 接口契约。
- **`history/router.py`**：
  - `GET /api/history/`：返回当前用户的所有历史记录，按时间倒序。
  - `POST /api/history/`：创建新历史记录，内部调用 `extraction.engine.calculate_match_score` 从 `have_skills` 与 `missing_skills` 计算 `match_score`，避免客户端伪造分数。
  - `PUT /api/history/{history_id}`：允许用户更新公司名 / 职位名等元数据，并进行「记录归属校验」。

该模块将「一次分析」封装为持久化对象，支撑 PRD 中的「历史回顾」和「进度跟踪」用户故事。

### 2.5 AI 学习路线模块 `roadmap/`

- **`roadmap/schemas.py`**：
  - `RoadmapGenerateRequest`：包含 `missing_skills` 与可选 `jd_text`。
  - `RoadmapGenerateResponse`：封装从 Claude 返回的结构化路线（summary、phases、metrics 等）。
- **`roadmap/services.py`**：
  - `generate_roadmap_with_claude(...)`：与 Anthropic Claude API 通信，使用约束 JSON 模版 prompt 生成路线。
  - 自定义异常：`ClaudeTimeoutError` / `ClaudeAuthError` / `ClaudeAPIError` / `ClaudeParseError`，便于上层路由区分错误类型。
- **`roadmap/router.py`**：
  - `POST /api/roadmap/generate`：对外暴露 AI 路线生成接口，将结果保存在 `current_user.roadmap` 字段，同时返回给前端。

该模块将「AI 补全」实现为一个干净的服务层 + 路由层，便于未来替换模型或调参，而不影响前端契约。

---

## 3. 前端结构与页面路由

前端代码位于 `client/` 目录。

### 3.1 应用入口与基础配置

- **`src/main.tsx`**：React 应用入口，挂载 Router、全局样式和顶层状态提供者。
- **`src/index.css`** 与 `tailwind.config.js`：全局样式与 Tailwind 设计系统配置。
- **`vite.config.ts`**：Vite 构建配置。
- **`src/vite-env.d.ts`**：TypeScript 对 Vite 环境变量的声明。

### 3.2 页面级组件（Pages）

位于 `client/src/pages/`：

- `Login.tsx`：登录页面，调用 `POST /api/auth/login`，成功后将 token 存入 `authStore`。
- `Register.tsx`：注册页面，调用 `POST /api/auth/register`，可选自动登录或引导用户去登录。
- `Dashboard.tsx`：主面板页面，包含：
  - JD 输入区域（`JDInput`）。
  - 技能匹配结果展示（`SkillMatchResults` + `AnimatedMatchRing`）。
  - AI 学习路线展示（`LearningRoadmap`）。
- `Profile.tsx`：技能档案管理页面，调用 `/api/profile/*`，用于增删改查技能、触发简历提取。
- `History.tsx`：历史记录页面，调用 `/api/history` 获取并渲染以往分析结果。

路由守卫由 `components/ProtectedRoute.tsx` 实现，根据 `authStore` 中是否存在有效 token 决定是否重定向至登录页。

### 3.3 复用组件（Components）

- `Navbar.tsx`：全局导航栏，包含登录状态、跳转到 Dashboard / Profile / History 等入口。
- `JDInput.tsx`：职位描述输入组件，负责采集 JD 文本并调用 `/api/extract`。
- `SkillMatchResults.tsx`：展示 have/missing/bonus 三列技能列表，与 `AnimatedMatchRing` 联动展示匹配度。
- `AnimatedMatchRing.tsx`：使用 SVG 或第三方动效库构建环形匹配度动画，是 UI 的「Wow-factor」之一。
- `LearningRoadmap.tsx`：根据 `RoadmapGenerateResponse.roadmap` 渲染纵向时间线或卡片。
- `Skeleton.tsx`：通用骨架屏组件，在 AI 路线加载期间提供平滑的加载状态。

这些组件共同实现 PRD 中「粘贴 JD → 看匹配 → 看路线」的一整套交互流程。

### 3.4 状态管理（Stores）

使用 Zustand 管理全局状态：

- **`store/authStore.ts`**：
  - 保存 `accessToken`、当前用户信息以及登录 / 登出逻辑。
  - 对应后端 Auth 模块，统一封装 token 持久化与恢复。
- **`store/profileStore.ts`**：
  - 保存用户技能列表、加载状态、错误信息等。
  - 提供与 `/api/profile/*` 交互的高层 action。

这样，页面组件只关心「调用 store 的 action」和「消费 store 状态」，避免在 UI 层散落大量 API 调用和副作用逻辑。

### 3.5 API 封装层

- **`lib/api.ts`**：封装 Axios 实例或 fetch 包装，统一挂上 `VITE_API_BASE_URL` 和 Authorization 头。
- **`api/auth.ts`**：实现 `login` / `register` / `fetchCurrentUser` 等函数。
- **`api/roadmap.ts`**：实现 `generateRoadmap` 调用 `/api/roadmap/generate`。

通过将 API 调用集中在 `api/*` 模块中，方便未来替换后端 URL、增加重试逻辑、统一错误处理等。

---

## 4. 数据流示例：从 JD 到 AI 路线

下面以最核心的用户场景为例，串起前后端数据流：

1. **用户登录**：
   - 前端 `Login.tsx` 调用 `api/auth.login` → `POST /api/auth/login`。
   - 后端 `auth/router.py` 验证凭据 → 生成 JWT → 返回 `access_token`。
   - 前端 `authStore` 保存 token，并在后续请求中附加到 `Authorization` 头。

2. **维护技能档案**：
   - 前端 `Profile.tsx` 通过 `profileStore` 调用 `/api/profile/skills` 获取 & 更新技能。
   - 可选调用 `/api/profile/extract-resume`，从简历文本自动补全技能。
   - 后端将技能保存到 `User.skills` 数组字段。

3. **JD 技能分析**：
   - 在 `Dashboard.tsx` 中，用户粘贴 JD 并提交，触发 `JDInput` 调用 `POST /api/extract`。
   - 后端 `extraction/engine.py` 根据 `CURATED_SKILLS` 分析 JD，与 `user_skills` 一起计算 `have`/`missing`/`bonus`。
   - 前端接收结果，更新 `SkillMatchResults` 组件和 `AnimatedMatchRing` 动画。

4. **持久化历史记录**：
   - 前端在分析完成后，通过 `/api/history/` 提交一个 `HistoryCreate` 请求。
   - 后端 `history/router.py` 调用 `calculate_match_score`，将完整结果插入 `AnalysisHistory` 表。
   - `History.tsx` 页面通过 `GET /api/history/` 展示以往记录。

5. **生成学习路线**：
   - 用户点击「生成学习路线」按钮，前端 `LearningRoadmap` 或相关 action 调用 `POST /api/roadmap/generate`。
   - 后端 `roadmap/services.py` 调用 Claude API，将 `missing_skills` 与 `jd_text` 作为上下文：
     - 若成功，返回结构化 JSON 路线，并写入 `current_user.roadmap`。
     - 若失败，抛出对应 HTTP 错误（504/502/500）。
   - 前端收到数据后：
     - 展示骨架屏 → 渐变为真实路线卡片。
     - 支持用户回访时在 Dashboard/History 中复用最新路线。

---

## 5. 测试、质量与 CI/CD

- **后端测试**：位于 `server/tests/`，覆盖 Auth、Profile、History、Extraction、Roadmap 等核心逻辑，并在 CI 中强制 80%+ 覆盖率。
- **前端测试**：位于 `client/src/test/`，使用 Vitest + React Testing Library，覆盖页面与关键组件（Login/Dashboard/Profile/History 等）。
- **质量与评估**：
  - `docs/test_results/backend_test_report.txt` / `frontend_test_report.txt`：测试运行摘要。
  - `docs/eval_roadmaps/ai_eval_results.md`：AI 评测脚本输出，评估 Claude 生成路线的质量。
  - `docs/skillgap_eval_dashboard.html`：面向课程要求的综合 Eval Dashboard。
- **CI/CD Pipeline**：
  - `.github/workflows/ci.yml`：多阶段工作流，先前端/后端 lint，再跑测试与覆盖率，保障主分支质量。
  - 每个 PR 还会触发 **Netlify** 的 Deploy Preview 及站点规则检查（Header rules、Pages changed、Redirect rules），PR 页可看到完整检查状态（见 README §8 与截图 `internal_working_planning_note/screenshot during dev/每次PR的自动化检测CI和部署平台.png`）。

---

## 6. 与 PRD 的对应关系（简要映射）

- **Story 1（Profile Management）**：
  - 后端：`/api/profile/*` + `User.skills` 字段。
  - 前端：`Profile.tsx` + `profileStore`。
- **Story 2（Core Value：JD 匹配与可视化）**：
  - 后端：`/api/extract` + `extraction/engine.py`。
  - 前端：`JDInput`、`SkillMatchResults`、`AnimatedMatchRing`、`Dashboard.tsx`。
- **Story 3（AI Guidance：学习路线）**：
  - 后端：`/api/roadmap/generate` + `roadmap/services.py`。
  - 前端：`LearningRoadmap` 及其周边状态管理。
- **Story 4（Progress Tracking：历史记录）**：
  - 后端：`/api/history/*` + `history/models.py`。
  - 前端：`History.tsx`。
- **Story 5（Continuous Learning：迭代技能档案）**：
  - 复用 Profile + History + Roadmap 三个层面，通过多次分析看到分数随时间变化。

通过以上映射，可以清晰看到：**每个 PRD 中的核心用户故事，都有一个清晰的前端页面 + 后端模块 + 数据模型组合实现**，便于助教/读者从需求反向追踪到具体代码位置。

