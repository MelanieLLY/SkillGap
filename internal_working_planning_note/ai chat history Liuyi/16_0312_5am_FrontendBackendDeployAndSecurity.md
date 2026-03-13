## 2026-03-12 Frontend & Backend Deploy, Env, CORS, Sample Accounts

> 本文是与 AI 助手在 2026-03-12 的一次完整对话整理，主要围绕：后端 Render 部署确认、前端 Netlify 部署与环境变量配置、前后端 URL 替换、CORS 安全设置、示例账号与密码管理，以及少量测试（health check / OpenAPI）记录。

---

### 1. 后端部署健康检查（Render）

- 后端 URL: `https://skillgap-api-hrsc.onrender.com`
- AI 在本机 terminal 中运行：

```bash
curl -sS -w "\nHTTP_STATUS:%{http_code}\n" https://skillgap-api-hrsc.onrender.com/health
```

- 结果：
  - 返回 `{"status":"healthy"}`，HTTP 状态码 `200`。
  - 说明 Render 上的 FastAPI 后端已经成功部署，并且 `/health` endpoint 正常工作。
- 另外还抓取了 `/openapi.json` 的前几行，确认：
  - 项目公开了完整的 OpenAPI schema。
  - 主要路由包括：
    - `POST /api/extract`
    - `POST /api/auth/register`
    - `POST /api/auth/login`
    - `GET /api/auth/me`
    - `GET/POST /api/profile/skills`
    - `POST /api/profile/extract-resume`
    - `GET/POST/PUT /api/history/...`
    - `POST /api/roadmap/generate`
    - `/health` 等。

测试结论：**后端 Render 服务健康、路由齐全，可以直接作为生产 API Base 使用。**

---

### 2. 前端如何绑定后端：环境变量与代码结构

#### 2.1 前端 API Base URL 设计

查看 `client/src/lib/api.ts`：

```12:9:/Users/melaniey/Github/SkillGap/client/src/lib/api.ts
const configuredApiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim();

const normalizedApiBaseUrl = (
  configuredApiBaseUrl && configuredApiBaseUrl.length > 0
    ? configuredApiBaseUrl
    : "http://127.0.0.1:8000"
).replace(/\/+$/, "");

export const API_BASE_URL = `${normalizedApiBaseUrl}/api`;
```

要点：
- 前端统一通过 `import.meta.env.VITE_API_BASE_URL` 读取后端 base URL；
- 若未配置，则 fallback 到本地 `http://127.0.0.1:8000`；
- 末尾会自动追加 `/api`，并去掉多余的尾部 `/`。

结论：
- 生产环境只需要把 `VITE_API_BASE_URL` 配成 `https://skillgap-api-hrsc.onrender.com`，**不要加 `/api`**；
- 部署平台（Netlify）只要注入这个 env 即可。

#### 2.2 `.env.example` 与 README 更新

- `client/.env.example` 中保留本地示例，并补充生产示例：

```1:6:/Users/melaniey/Github/SkillGap/client/.env.example
VITE_API_BASE_URL=http://127.0.0.1:8000

# For production deployment (e.g. Vercel), set this to your deployed backend base URL
# Example (Render):
# VITE_API_BASE_URL=https://skillgap-api-hrsc.onrender.com
```

- 根目录 `README.md` 中增加了环境配置说明：

```33:47:/Users/melaniey/Github/SkillGap/README.md
## 🌐 Environment configuration

- **Local development backend**: `http://127.0.0.1:8000` (started by `npm run dev`)
- **Deployed backend API base URL** (Render): `https://skillgap-api-hrsc.onrender.com`
- **Deployed frontend app URL** (Netlify): `https://skillgapweb.netlify.app`

### Frontend (Vite) API base URL

The frontend reads the backend base URL from `VITE_API_BASE_URL` and automatically appends `/api`:

- **Env variable**: `VITE_API_BASE_URL`
  - **Local dev example**: `VITE_API_BASE_URL=http://127.0.0.1:8000`
  - **Production example (Render)**: `VITE_API_BASE_URL=https://skillgap-api-hrsc.onrender.com`

When deploying the frontend (e.g. to Vercel), configure `VITE_API_BASE_URL` in the project settings using the deployed backend URL above.
```

结论：**API Base URL 已统一通过 `VITE_API_BASE_URL` 管理，代码内只有本地 fallback，不再需要硬编码生产地址。**

---

### 3. 8000 端口相关引用的全局检查

AI 使用全局搜索 `8000`，检查所有引用是否需要变更：

- `client/src/lib/api.ts`：fallback `http://127.0.0.1:8000` → 保留，用于本地开发兜底。
- `client/.env.example`：本地示例 → 保留。
- `client/vite.config.ts`：

```8:15:/Users/melaniey/Github/SkillGap/client/vite.config.ts
server: {
    port: 5173,
    proxy: {
        '/api': {
            target: 'http://localhost:8000',
            changeOrigin: true,
            rewrite: (path) => path.replace(/^\/api/, '')
        }
    }
}
```

  - 仅用于本地 dev proxy，将 `/api` 转发到 `http://localhost:8000`，不影响生产构建 → 保留。

- `server/core/config.py`：

```8:15:/Users/melaniey/Github/SkillGap/server/core/config.py
class Settings(BaseSettings):
    database_url: str = "postgresql://localhost/skillgap_db"
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    anthropic_api_key: str = ""
    host: str = "127.0.0.1"
    port: int = 8000
```

  - 本地默认端口设置 → 可以保留。

- `server/.env.example`：`PORT=8000` → 本地示例，不改。
- `package.json`：`dev:server` 使用 `--port 8000` → 仅本地。
- `README.md` 中本地后端地址 → 已记录为本地开发说明。
- `.github/workflows/ci.yml`：

```222:223:/Users/melaniey/Github/SkillGap/.github/workflows/ci.yml
VITE_API_BASE_URL: ${{ secrets.VITE_API_BASE_URL || 'http://localhost:8000' }}
```

  - 对 CI 构建而言，推荐在 GitHub Secrets 里配置 `VITE_API_BASE_URL=https://skillgap-api-hrsc.onrender.com`，默认 `http://localhost:8000` 仅作为兜底。

结论：**所有 `8000` 引用目前都仅用于本地或 CI 兜底，不会影响生产环境使用 Render URL。无需额外替换。**

---

### 4. CORS 策略与安全考虑

#### 4.1 初始状态

原本后端 `server/main.py` 中的 CORS 配置是：

```59:66:/Users/melaniey/Github/SkillGap/server/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- 优点：开发期任何来源都能访问，不会有 CORS 问题。
- 缺点：生产环境安全性略差（虽然 API 自身还有认证保护）。

#### 4.2 部署后收紧 CORS 白名单

在前端成功部署到 Netlify（见第 5 节）后，AI 直接帮忙修改为白名单：

```59:66:/Users/melaniey/Github/SkillGap/server/main.py
# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://skillgapweb.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- 保留本地开发前端：`http://localhost:5173`
- 新增生产前端：`https://skillgapweb.netlify.app`

关于是否要把 origin 放到 env 变量：
- Origin 本身并不是秘密（浏览器轻松可见）。
- 对本项目这种「单一 prod 前端 + 一个本地 dev」的简单场景，**代码里硬编码白名单更直观，也足够工程化**。
- 若未来有 dev/staging/prod 多环境，才更有理由用 `CORS_ORIGINS` 这类 env 进行配置。

#### 4.3 关于 Claude Credit 安全性的讨论

- 真正触发 Anthropic / Claude 消耗 credit 的 endpoint 是：

```33:38:/Users/melaniey/Github/SkillGap/server/roadmap/router.py
@router.post("/generate", response_model=RoadmapGenerateResponse)
async def generate_roadmap(
    request: RoadmapGenerateRequest,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> RoadmapGenerateResponse:
```

- 这里依赖 `get_current_active_user`，即：
  - 必须先调用 `/api/auth/login` 获得 token；
  - 再携带 `Authorization: Bearer <token>` 调用 `/api/roadmap/generate`。
- 未登录或没有有效 token 的用户无法触发 Claude 调用，自然也无法滥刷 credit。
- `ANTHROPIC_API_KEY` 只存在于后端 `.env` / Render 环境变量中，前端无法读取。

结论：**匿名访问者只能访问公开 endpoint（如 `/health`），不会消耗 Claude 配额。只有登录用户才可调用生成 Roadmap 的 API。**

---

### 5. 前端部署到 Netlify 的完整配置

前端生产 URL: `https://skillgapweb.netlify.app/`

#### 5.1 Netlify 基本表单配置

在 Netlify 中导入 GitHub 仓库 `SkillGap`，使用 `client/` 子目录作为前端根目录。

- Team: `Husky Luck`（默认）
- Project name: 可以使用 `skillgap-frontend` 或默认随机名字，影响的是默认域名。

**Build settings:**
- **Branch to deploy**: `main`
- **Base directory**: `client`
- **Build command**: `npm run build`
- **Publish directory**: `dist`
- **Functions directory**: 留空（不使用 Netlify Functions）

#### 5.2 Netlify 环境变量 `VITE_API_BASE_URL`

在 Netlify 项目设置中添加 env：

- Key: `VITE_API_BASE_URL`
- Value: `https://skillgap-api-hrsc.onrender.com`

一开始勾选了「Secret」，结果触发了 Netlify 的 secrets scanning：

```text
Secret env var "VITE_API_BASE_URL"'s value detected:
  found value at line 13 in dist/assets/index-BHXVX8JD.js

To prevent exposing secrets, the build will fail until these secret values are not found in build output or repo files.
```

分析：
- 对前端来说，API Base URL 必须是公开的（浏览器要看到），并不是真正意义上的 secret。
- Netlify 误把它当作敏感值扫描并阻止构建。

解决：
- 在 Netlify 环境变量设置中 **取消勾选 "Contains secret"**，保持：
  - Scopes: `Builds`（足够）
  - Deploy contexts: `Production` + `Deploy Previews`（可选）
- 再次触发部署，构建顺利完成，站点可访问。

结论：**生产前端已经成功部署到 Netlify，并正确指向 Render 后端。**

#### 5.3 Netlify 在 PR 上的自动化检查

每个 Pull Request 除 GitHub Actions（Lint / Test / Build）外，还会触发 Netlify 的自动化检查：

- **Deploy Preview**：Netlify bot 在 PR 下评论「Deploy Preview for skillgapweb ready!」，并给出预览链接（如 `https://deploy-preview-39--skillgapweb.netlify.app`）、最新部署日志链接等。
- **Netlify 规则检查**（通常显示为 neutral/completed）：
  - **Header rules - skillgapweb**：头部规则处理情况。
  - **Pages changed - skillgapweb**：页面变更与上传状态（如 "All files already uploaded"）。
  - **Redirect rules - skillgapweb**：重定向规则处理情况。

这样在合并前即可在 PR 页看到 CI 与 Netlify 的完整检查状态。截图见：`internal_working_planning_note/screenshot during dev/每次PR的自动化检测CI和部署平台.png`。

---

### 6. 项目计划文档中更新前后端 URL

对 `internal_working_planning_note/PROJECT2_MASTER_PLAN.md` 做了中英双语同步更新：

#### 中文 Checklist 部分

```160:166:/Users/melaniey/Github/SkillGap/internal_working_planning_note/PROJECT2_MASTER_PLAN.md
## ✅ Final 要交的文件与材料清单

- [x] **GitHub 仓库链接** (预计: 0.5 小时 / Est: 0.5h): https://github.com/MelanieLLY/SkillGap 
- [x] **已部署前端应用 URL**(生产环境, 如 Vercel) (预计: 3–4 小时 / Est: 3–4h)  
  - `https://skillgapweb.netlify.app`
- [x] **已部署后端 API 基础 URL**(如 Render/Railway) (预计: 4–6 小时 / Est: 4–6h)  
  - `https://skillgap-api-hrsc.onrender.com`
```

#### 英文 Mirror 部分

```247:253:/Users/melaniey/Github/SkillGap/internal_working_planning_note/PROJECT2_MASTER_PLAN.md
### ✅ Final Deliverables & Artifacts

- [x] **GitHub Repository Link** (Estimated: 0.5h): https://github.com/MelanieLLY/SkillGap 
- [x] **Deployed Frontend App URL** (production, e.g. Vercel) (Estimated: 3–4h)  
  - `https://skillgapweb.netlify.app`
- [x] **Deployed Backend API Base URL** (e.g. Render/Railway) (Estimated: 4–6h)  
  - `https://skillgap-api-hrsc.onrender.com`
```

结论：**项目总计划中的部署相关条目已经全部勾选并填入实际 URL。**

---

### 7. Sample 测试账号与 1Password 管理

你希望为 TA / 老师 / Reviewer 提供两组现成的测试账号，但不希望在仓库中明文保存密码，而是通过 1Password 共享链接。

#### 7.1 创建与更新示例账号密码

两个示例账号：

- `alice@example.com` → 新密码：`Fm8!!9oMg`
- `bob@example.com` → 新密码：`XTr3UpJk.`

AI 使用与后端相同的密码哈希逻辑（`passlib[bcrypt]`）和数据库会话，直接对云端 Postgres 进行更新：

```bash
cd server && python - << 'PY'
from core.config import settings
from database import SessionLocal
from auth.models import User
from auth.utils import get_password_hash

updates = {
    "alice@example.com": "xxxxxxxFg",
    "bob@example.com": "xxxxxxxJk.",
}

print("Using DATABASE_URL:", settings.database_url)

with SessionLocal() as db:
    for email, new_pw in updates.items():
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"[WARN] User not found: {email}")
            continue
        user.hashed_password = get_password_hash(new_pw)
        db.add(user)
        print(f"[OK] Updated password hash for {email}")
    db.commit()
    print("Changes committed.")
PY
```

输出（在申请 full network 权限后成功）：

```text
Using DATABASE_URL: postgresql://skillgap_db_snas_user:...@dpg-d6xxxxp5g-a.oregon-postgres.render.com/skillgap_db_snas
[OK] Updated password hash for alice@example.com
[OK] Updated password hash for bob@example.com
Changes committed.
```

测试结论：
- 这一步相当于「一次性脚本修改生产数据库中的密码哈希」，无新增测试代码。
- 之后你在前端登录页面已验证新密码可以成功登录。

#### 7.2 README 中记录 Sample Accounts 信息

在 `README.md` 中增加了「Sample test accounts」章节：

```51:58:/Users/melaniey/Github/SkillGap/README.md
## 🧪 Sample test accounts

For instructors, TAs, or reviewers who want to quickly explore the app without creating their own accounts, two sample users are provisioned:

- `alice@example.com`
- `bob@example.com`

The **passwords are not stored in this repository**. They are managed in a 1Password shared item for security and can be retrieved via the shared link provided separately (link valid until **2026-04-11**; after that date, please contact the author for a refreshed link at `liuyyang07@gmail.com`):

- 1Password shared item: `https://share.1password.com/s#5oJnJ6o2ybcwW8CjIq8FZ_nts3c_aVVlP1JxmMJPHjo`
```

要点：
- 明确列出两个 sample 邮箱；
- 说明密码不在仓库中保存，而是在 1Password 共享项中；
- 链接有效期到 **2026-04-11**，之后可通过 `liuyyang07@gmail.com` 联系作者获取新的分享链接。

结论：**sample 账号可方便 TA 测试，又兼顾了密码的安全管理。**

---

### 8. 本次对话中的测试情况总结

本次会话没有新增自动化测试文件，但有以下「运行层面的测试 / 验证」：

1. **后端健康检查与 OpenAPI 验证**
   - 手动通过 `curl` 调用 `/health`：
     - 返回 `{"status":"healthy"}`，HTTP 200 → ✅。
   - 通过 `curl` 抓取 `/openapi.json`，确认：
     - 所有关键路由（auth、profile、history、roadmap、extract 等）均已正确暴露；
     - OpenAPI 中的安全设置（OAuth2PasswordBearer）等配置正确。

2. **数据库密码更新的运行验证**
   - 通过一次性 Python 脚本对 `alice@example.com`、`bob@example.com` 的密码进行更新；
   - 输出中显示 `Updated password hash for alice@example.com / bob@example.com` 且 `Changes committed.`；
   - 随后你在部署前端页面上使用新密码登录，确认登录成功（从弱密码变为强密码、功能仍正常）。

3. **前端与后端联通性（间接测试）**
   - 通过成功登录 / 访问已部署前端 `https://skillgapweb.netlify.app/` 并与 Render 后端交互，间接验证：
     - `VITE_API_BASE_URL` 在 Netlify 上配置生效；
     - CORS 白名单没有阻止来自 Netlify 的请求；
     - JWT 认证流程在生产环境能正常跑通。

没有出现「自动化测试从失败到成功」的变化记录，本次工作重心是**部署配置 + 安全设置 + 文档补全 + 手动验证**。如需后续，可以在 README 或专门的 `docs/api-docs.md` 中进一步补充「如何使用 sample account 进行端到端测试」的步骤说明。 
