## SkillGap API 文档（人类可读版本）

本项目后端基于 **FastAPI** 构建，部署地址为：

- **生产环境 Backend Base URL**：`https://skillgap-api-hrsc.onrender.com`
- **本地开发 Backend Base URL**：`http://127.0.0.1:8000`

前端通过 `VITE_API_BASE_URL` 访问后端，并自动拼接 `/api` 前缀。

### OpenAPI / Swagger

- **在线 OpenAPI JSON**：`https://skillgap-api-hrsc.onrender.com/openapi.json`
- **Swagger UI（交互式调试界面）**：`https://skillgap-api-hrsc.onrender.com/docs`

> 所有下文带有「需要认证」的接口，都使用 JWT Bearer Token（`Authorization: Bearer <access_token>`）进行鉴权，`access_token` 通过登录接口获取。

---

## 1. 核心基础接口

### 1.1 根路径

- **Method**: `GET`
- **Path**: `/`
- **Auth**: 不需要
- **说明**: 健康欢迎信息，用于快速确认服务存活。
- **Response 示例**:

```json
{
  "message": "Welcome to SkillGap API"
}
```

### 1.2 健康检查

- **Method**: `GET`
- **Path**: `/health`
- **Auth**: 不需要
- **说明**: 用于监控 / CI / 部署检查，返回应用健康状态。
- **Response 示例**:

```json
{
  "status": "healthy"
}
```

---

## 2. 认证与用户信息（Auth）

路由前缀：`/api/auth`

### 2.1 注册新用户

- **Method**: `POST`
- **Path**: `/api/auth/register`
- **Auth**: 不需要
- **说明**: 使用邮箱和密码注册新用户。
- **Request Body（JSON）**：

```json
{
  "email": "user@example.com",
  "password": "yourStrongPassword"
}
```

- **Response 201（`UserOut`）示例**：

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "skills": []
}
```

- **错误情况**：
  - `400 Bad Request`：邮箱已被注册（`"Email already registered"`）。

### 2.2 登录获取 Token

- **Method**: `POST`
- **Path**: `/api/auth/login`
- **Auth**: 不需要
- **说明**: 使用邮箱 + 密码登录，返回 JWT 访问令牌。
- **Request（`application/x-www-form-urlencoded`）**：
  - `username`: 邮箱（email）
  - `password`: 密码

示例：

```bash
curl -X POST https://skillgap-api-hrsc.onrender.com/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=yourStrongPassword"
```

- **Response 200（`Token`）示例**：

```json
{
  "access_token": "jwt-token-here",
  "token_type": "bearer"
}
```

- **错误情况**：
  - `401 Unauthorized`：邮箱或密码错误。

### 2.3 获取当前用户信息

- **Method**: `GET`
- **Path**: `/api/auth/me`
- **Auth**: 需要（Bearer Token）
- **说明**: 返回当前登录用户的基础信息。
- **Headers**：

```http
Authorization: Bearer <access_token>
```

- **Response 示例**：

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "skills": ["Python", "React"]
}
```

---

## 3. 个人技能档案（Profile）

路由前缀：`/api/profile`  
所有接口都需要登录（Bearer Token）。

### 3.1 获取当前用户技能列表

- **Method**: `GET`
- **Path**: `/api/profile/skills`
- **Auth**: 需要
- **说明**: 返回当前用户保存的技能数组，如未设置则为空列表。

- **Response 示例**：

```json
["Python", "FastAPI", "React"]
```

### 3.2 添加单个技能

- **Method**: `POST`
- **Path**: `/api/profile/skills`
- **Auth**: 需要
- **说明**: 为当前用户添加一个技能（忽略大小写去重）。
- **Request Body（JSON）**：

```json
{
  "skill": "FastAPI"
}
```

- **Response 示例**：

```json
["Python", "FastAPI", "React"]
```

- **错误情况**：
  - `400 Bad Request`：`skill` 为空字符串。

### 3.3 删除指定技能

- **Method**: `DELETE`
- **Path**: `/api/profile/skills/{skill_name}`
- **Auth**: 需要
- **说明**: 从当前用户技能列表中删除指定技能（大小写不敏感）。
- **Path 参数**：
  - `skill_name`: 要删除的技能名。

- **Response 示例**：

```json
["Python", "React"]
```

- **错误情况**：
  - `404 Not Found`：技能不存在于当前用户的技能列表中。

### 3.4 从简历文本自动提取技能

- **Method**: `POST`
- **Path**: `/api/profile/extract-resume`
- **Auth**: 需要
- **说明**: 从一段简历文本中，基于内置的 `CURATED_SKILLS` 表扫描关键词，提取技能并合并到当前用户技能列表。

- **Request Body（JSON）**：

```json
{
  "resume_text": "I have experience with Python, Django, React, and PostgreSQL..."
}
```

- **Response 示例**：

```json
["Python", "Django", "React", "PostgreSQL"]
```

> 若未找到新的技能，返回的仍然是当前技能列表。

---

## 4. JD 技能提取（Extraction）

路由前缀：`/api`  
核心接口用于对「职位描述 + 用户技能」进行技能分类。

### 4.1 提取并分类技能

- **Method**: `POST`
- **Path**: `/api/extract`
- **Auth**: 不需要（前端通常在登录后使用，但后端本身未强制要求）
- **说明**: 传入职位描述和当前用户技能，返回「已有技能 / 缺失技能 / 加分项」，并尝试从 JD 中提取公司名、职位名称。

- **Request Body（JSON，`ExtractRequest`）**：

```json
{
  "job_description": "We are hiring a Senior Full-Stack Engineer with React, TypeScript, FastAPI, and PostgreSQL...",
  "user_skills": ["React", "JavaScript", "Git"]
}
```

- **Response Body（`ExtractResponse`）示例**：

```json
{
  "have": ["React"],
  "missing": ["TypeScript", "FastAPI", "PostgreSQL"],
  "bonus": ["Git"],
  "company_name": "ExampleCorp",
  "position_name": "Senior Full-Stack Engineer"
}
```

字段含义：

- `have`: 用户技能中，在 JD 中也出现的技能。
- `missing`: JD 要求中出现，但用户技能列表中缺失的技能。
- `bonus`: 属于用户技能但 JD 中未提及的「额外加分项」。
- `company_name` / `position_name`: 基于 JD 文本的简单规则提取结果（可能为 `null`）。

---

## 5. 分析历史记录（History）

路由前缀（在 `main.py` 中注册）：`/api/history`  
所有接口都需要登录。

### 5.1 获取当前用户的全部历史记录

- **Method**: `GET`
- **Path**: `/api/history/`
- **Auth**: 需要
- **说明**: 按时间倒序返回当前用户的所有分析历史记录。

- **Response 示例（`HistoryResponse[]`）**：

```json
[
  {
    "id": 1,
    "user_id": 1,
    "job_title": "Senior Backend Engineer",
    "company_name": "ExampleCorp",
    "match_score": 78,
    "have_skills": ["Python", "FastAPI"],
    "missing_skills": ["PostgreSQL", "Docker"],
    "bonus_skills": ["Go"],
    "created_at": "2026-03-11T10:00:00Z",
    "date_analyzed": "2026-03-11T10:00:00Z"
  }
]
```

> 具体字段请以 `/openapi.json` 为准，这里给出典型示例。

### 5.2 创建一条新的历史记录

- **Method**: `POST`
- **Path**: `/api/history/`
- **Auth**: 需要
- **说明**: 为当前用户创建新的分析记录；后端会基于 `have_skills` 和 `missing_skills` 自动计算 `match_score`，不会信任客户端传入的分数。

- **Request Body（`HistoryCreate`，示例）**：

```json
{
  "job_title": "Senior Backend Engineer",
  "company_name": "ExampleCorp",
  "have_skills": ["Python", "FastAPI"],
  "missing_skills": ["PostgreSQL", "Docker"],
  "bonus_skills": ["Go"],
  "jd_text": "Full job description text..."
}
```

- **Response 200（`HistoryResponse`）示例**：

```json
{
  "id": 1,
  "user_id": 1,
  "job_title": "Senior Backend Engineer",
  "company_name": "ExampleCorp",
  "match_score": 78,
  "have_skills": ["Python", "FastAPI"],
  "missing_skills": ["PostgreSQL", "Docker"],
  "bonus_skills": ["Go"],
  "jd_text": "Full job description text...",
  "date_analyzed": "2026-03-11T10:00:00Z"
}
```

### 5.3 更新已有历史记录（例如修改职位名称）

- **Method**: `PUT`
- **Path**: `/api/history/{history_id}`
- **Auth**: 需要
- **说明**: 局部更新一条历史记录（如修改 `job_title`、`company_name` 等）。后端会检查该记录是否属于当前用户。

- **Path 参数**：
  - `history_id`: 要更新的历史记录主键 ID。

- **Request Body（`HistoryUpdate`，仅需提供要修改的字段）**：

```json
{
  "job_title": "Senior Backend Engineer (Platform Team)"
}
```

- **Response 200**：返回更新后的完整历史记录对象。

- **错误情况**：
  - `404 Not Found`：记录不存在。
  - `403 Forbidden`：尝试修改不属于当前用户的记录。

---

## 6. AI 学习路线（Roadmap）

路由前缀：`/api/roadmap`  
所有接口都需要登录。

### 6.1 生成学习路线

- **Method**: `POST`
- **Path**: `/api/roadmap/generate`
- **Auth**: 需要
- **说明**: 调用 Anthropic Claude API，根据缺失技能（以及可选 JD 文本）生成个性化学习路线，并将最新路线持久化到当前用户的 `roadmap` 字段。

- **Request Body（`RoadmapGenerateRequest`）**：

```json
{
  "missing_skills": ["FastAPI", "PostgreSQL"],
  "jd_text": "Full job description text here (optional but recommended)"
}
```

- **Response Body（`RoadmapGenerateResponse`，结构化 JSON）**：

```json
{
  "roadmap": {
    "summary": "12-week roadmap to learn FastAPI and PostgreSQL",
    "phases": [
      {
        "name": "Phase 1: Fundamentals",
        "weeks": 4,
        "skills": ["FastAPI basics", "SQL fundamentals"],
        "resources": [
          {
            "title": "FastAPI Official Tutorial",
            "url": "https://fastapi.tiangolo.com/"
          }
        ],
        "projects": [
          {
            "title": "Build a simple CRUD API with FastAPI + SQLite",
            "description": "Practice basic routing, models, and DB operations."
          }
        ]
      }
    ],
    "metrics": {
      "estimated_hours_per_week": 8,
      "total_duration_weeks": 12
    }
  }
}
```

> 实际字段以 `roadmap/schemas.py` 和 OpenAPI 为准，这里给的是典型结构示例，前端使用这些字段渲染学习路线时间线。

- **错误情况（HTTPException）**：
  - `504 Gateway Timeout`：Claude API 调用超时。
  - `502 Bad Gateway`：Claude API 返回错误或无法解析的响应。
  - `500 Internal Server Error`：API Key 认证失败或配置缺失。

---

## 7. 全局数据库错误处理

应用层面定义了一个全局的 SQLAlchemy 异常处理器：

- 任何路由内发生的 `SQLAlchemyError`，都会被捕获，并返回：

```json
{
  "detail": "A database error occurred while processing your request."
}
```

- 同时在服务器日志中打印具体错误，便于调试。

这保证了在数据库暂时不可用或出现异常时，API 仍然能以一致的 JSON 形式失败，而不会直接崩溃。

---

## 8. 快速测试清单（给助教 / 自己验证）

1. 打开 `https://skillgap-api-hrsc.onrender.com/health`，确认返回 `{"status": "healthy"}`。
2. 打开 `https://skillgap-api-hrsc.onrender.com/docs`，浏览自动生成的 Swagger UI 与 OpenAPI schema。
3. 在 Swagger UI 中按顺序调用：
   - `POST /api/auth/register` → 创建测试账号。
   - `POST /api/auth/login` → 复制 `access_token`。
   - 带上 `Authorization: Bearer <token>` 访问 Profile/History/Roadmap 系列接口。
4. 在前端应用中，从「粘贴 JD → 查看匹配结果 → 生成学习路线 → 在 History 页查看记录」完整跑一遍，验证前后端接口链路是否打通。

