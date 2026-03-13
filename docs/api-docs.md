## SkillGap API Reference

The backend is built on **FastAPI** and deployed at:

- **Production Backend Base URL**: `https://skillgap-api-hrsc.onrender.com`
- **Local Development Backend Base URL**: `http://127.0.0.1:8000`

The frontend accesses the backend via `VITE_API_BASE_URL` and automatically prepends the `/api` prefix to all API calls.

### OpenAPI / Swagger

- **Live OpenAPI JSON**: `https://skillgap-api-hrsc.onrender.com/openapi.json`
- **Swagger UI (interactive)**: `https://skillgap-api-hrsc.onrender.com/docs`

> All endpoints marked as "requires authentication" use JWT Bearer Token (`Authorization: Bearer <access_token>`). The `access_token` is obtained via the login endpoint.

---

## 1. Core Endpoints

### 1.1 Root

- **Method**: `GET`
- **Path**: `/`
- **Auth**: None
- **Description**: Health welcome message; used to quickly confirm the service is running.
- **Response example**:

```json
{
  "message": "Welcome to SkillGap API"
}
```

### 1.2 Health Check

- **Method**: `GET`
- **Path**: `/health`
- **Auth**: None
- **Description**: Used for monitoring / CI / deployment checks; returns application health status.
- **Response example**:

```json
{
  "status": "healthy"
}
```

---

## 2. Authentication & User Info (Auth)

Route prefix: `/api/auth`

### 2.1 Register a New User

- **Method**: `POST`
- **Path**: `/api/auth/register`
- **Auth**: None
- **Description**: Registers a new user with email and password.
- **Request Body (JSON)**:

```json
{
  "email": "user@example.com",
  "password": "yourStrongPassword"
}
```

- **Response 201 (`UserOut`) example**:

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "skills": []
}
```

- **Error cases**:
  - `400 Bad Request`: Email already registered (`"Email already registered"`).

### 2.2 Login and Obtain Token

- **Method**: `POST`
- **Path**: `/api/auth/login`
- **Auth**: None
- **Description**: Authenticates with email and password; returns a JWT access token.
- **Request (`application/x-www-form-urlencoded`)**:
  - `username`: email address
  - `password`: password

Example:

```bash
curl -X POST https://skillgap-api-hrsc.onrender.com/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=yourStrongPassword"
```

- **Response 200 (`Token`) example**:

```json
{
  "access_token": "jwt-token-here",
  "token_type": "bearer"
}
```

- **Error cases**:
  - `401 Unauthorized`: Incorrect email or password.

### 2.3 Get Current User Info

- **Method**: `GET`
- **Path**: `/api/auth/me`
- **Auth**: Required (Bearer Token)
- **Description**: Returns the currently authenticated user's basic profile.
- **Headers**:

```http
Authorization: Bearer <access_token>
```

- **Response example**:

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "skills": ["Python", "React"]
}
```

---

## 3. Skill Profile (Profile)

Route prefix: `/api/profile`
All endpoints require authentication (Bearer Token).

### 3.1 Get Current User's Skills

- **Method**: `GET`
- **Path**: `/api/profile/skills`
- **Auth**: Required
- **Description**: Returns the current user's saved skill list; returns an empty array if none are set.

- **Response example**:

```json
["Python", "FastAPI", "React"]
```

### 3.2 Add a Skill

- **Method**: `POST`
- **Path**: `/api/profile/skills`
- **Auth**: Required
- **Description**: Adds a single skill to the current user's profile (case-insensitive deduplication applied).
- **Request Body (JSON)**:

```json
{
  "skill": "FastAPI"
}
```

- **Response example**:

```json
["Python", "FastAPI", "React"]
```

- **Error cases**:
  - `400 Bad Request`: `skill` is an empty string.

### 3.3 Remove a Skill

- **Method**: `DELETE`
- **Path**: `/api/profile/skills/{skill_name}`
- **Auth**: Required
- **Description**: Removes the specified skill from the current user's profile (case-insensitive match).
- **Path parameter**:
  - `skill_name`: Name of the skill to remove.

- **Response example**:

```json
["Python", "React"]
```

- **Error cases**:
  - `404 Not Found`: Skill does not exist in the current user's skill list.

### 3.4 Extract Skills from Resume Text

- **Method**: `POST`
- **Path**: `/api/profile/extract-resume`
- **Auth**: Required
- **Description**: Scans a block of resume text for keywords against the built-in `CURATED_SKILLS` list, then merges any matched skills into the current user's profile.

- **Request Body (JSON)**:

```json
{
  "resume_text": "I have experience with Python, Django, React, and PostgreSQL..."
}
```

- **Response example**:

```json
["Python", "Django", "React", "PostgreSQL"]
```

> If no new skills are found, the response returns the existing skill list unchanged.

---

## 4. JD Skill Extraction (Extraction)

Route prefix: `/api`
Core endpoint for classifying skills against a job description.

### 4.1 Extract and Classify Skills

- **Method**: `POST`
- **Path**: `/api/extract`
- **Auth**: Not required (frontend typically calls this while authenticated, but the backend does not enforce it)
- **Description**: Accepts a job description and the current user's skill list; returns skills classified as "have / missing / bonus" and attempts to extract company name and job title from the JD text.

- **Request Body (JSON, `ExtractRequest`)**:

```json
{
  "job_description": "We are hiring a Senior Full-Stack Engineer with React, TypeScript, FastAPI, and PostgreSQL...",
  "user_skills": ["React", "JavaScript", "Git"]
}
```

- **Response Body (`ExtractResponse`) example**:

```json
{
  "have": ["React"],
  "missing": ["TypeScript", "FastAPI", "PostgreSQL"],
  "bonus": ["Git"],
  "company_name": "ExampleCorp",
  "position_name": "Senior Full-Stack Engineer"
}
```

Field descriptions:

- `have`: Skills from the user's profile that appear in the JD.
- `missing`: Skills required by the JD that are absent from the user's profile.
- `bonus`: Skills the user has that are not explicitly mentioned in the JD.
- `company_name` / `position_name`: Extracted from the JD text via heuristics (may be `null`).

---

## 5. Analysis History (History)

Route prefix (registered in `main.py`): `/api/history`
All endpoints require authentication.

### 5.1 Get All History Records

- **Method**: `GET`
- **Path**: `/api/history/`
- **Auth**: Required
- **Description**: Returns all analysis history records for the current user, sorted by most recent first.

- **Response example (`HistoryResponse[]`)**:

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

> Refer to `/openapi.json` for the full schema; the above shows a representative example.

### 5.2 Create a History Record

- **Method**: `POST`
- **Path**: `/api/history/`
- **Auth**: Required
- **Description**: Creates a new analysis record for the current user. The backend calculates `match_score` from `have_skills` and `missing_skills` server-side — client-supplied scores are not trusted.

- **Request Body (`HistoryCreate`, example)**:

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

- **Response 200 (`HistoryResponse`) example**:

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

### 5.3 Update an Existing History Record

- **Method**: `PUT`
- **Path**: `/api/history/{history_id}`
- **Auth**: Required
- **Description**: Partially updates an existing history record (e.g., correcting `job_title` or `company_name`). The backend verifies record ownership before applying changes.

- **Path parameter**:
  - `history_id`: Primary key of the history record to update.

- **Request Body (`HistoryUpdate`, only include fields to change)**:

```json
{
  "job_title": "Senior Backend Engineer (Platform Team)"
}
```

- **Response 200**: Returns the fully updated history record object.

- **Error cases**:
  - `404 Not Found`: Record does not exist.
  - `403 Forbidden`: Attempting to modify a record belonging to another user.

---

## 6. AI Learning Roadmap (Roadmap)

Route prefix: `/api/roadmap`
All endpoints require authentication.

### 6.1 Generate a Learning Roadmap

- **Method**: `POST`
- **Path**: `/api/roadmap/generate`
- **Auth**: Required
- **Description**: Calls the Anthropic Claude API to generate a personalized learning roadmap based on the user's missing skills (and optionally the JD text), then persists the latest roadmap to the current user's `roadmap` field.

- **Request Body (`RoadmapGenerateRequest`)**:

```json
{
  "missing_skills": ["FastAPI", "PostgreSQL"],
  "jd_text": "Full job description text here (optional but recommended)"
}
```

- **Response Body (`RoadmapGenerateResponse`, structured JSON)**:

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

> Refer to `roadmap/schemas.py` and the OpenAPI spec for the authoritative field definitions; the above is a representative structural example used by the frontend to render the roadmap timeline.

- **Error cases (HTTPException)**:
  - `504 Gateway Timeout`: Claude API call timed out.
  - `502 Bad Gateway`: Claude API returned an error or an unparseable response.
  - `500 Internal Server Error`: API key authentication failed or configuration is missing.

---

## 7. Global Database Error Handling

The application defines a global SQLAlchemy exception handler at the app level:

- Any `SQLAlchemyError` raised within a route is caught and returns:

```json
{
  "detail": "A database error occurred while processing your request."
}
```

- The specific error is also logged to the server console for debugging.

This ensures that when the database is temporarily unavailable or encounters an unexpected condition, the API fails consistently with a well-formed JSON response rather than crashing with an unhandled 500.

---

## 8. Quick Validation Checklist (for TAs / self-verification)

1. Open `https://skillgap-api-hrsc.onrender.com/health` and confirm the response is `{"status": "healthy"}`.
2. Open `https://skillgap-api-hrsc.onrender.com/docs` to browse the auto-generated Swagger UI and OpenAPI schema.
3. In Swagger UI, call the following endpoints in order:
   - `POST /api/auth/register` → create a test account.
   - `POST /api/auth/login` → copy the `access_token`.
   - Use `Authorization: Bearer <token>` to access the Profile / History / Roadmap endpoints.
4. In the frontend application, run through the full user journey: paste a JD → view skill match results → generate a learning roadmap → verify the record appears in the History page. This confirms the entire frontend-to-backend call chain is working end-to-end.
