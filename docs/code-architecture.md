## SkillGap Code Architecture Overview

This document provides an engineering-level overview of SkillGap's overall code structure, key modules, and data flow. Read alongside `docs/skillgap_prd.md` and `docs/user_story.txt` to understand how the implementation maps to the PRD's user stories.

---

## 1. High-Level Architecture

- **Frontend (`client/`)**: React 18 + TypeScript + Vite + Tailwind CSS, with Zustand for global state management and Vitest for frontend unit tests.
- **Backend (`server/`)**: FastAPI + SQLAlchemy + PostgreSQL, handling authentication, skill profile management, JD skill extraction, analysis history persistence, and Claude roadmap generation.
- **AI Layer**: Encapsulated in `server/roadmap/services.py`, calling the Anthropic Claude API to generate structured learning roadmaps.
- **Persistence Layer**: `server/database.py` creates the SQLAlchemy Engine/Session; ORM models are defined per module in `auth/models.py`, `history/models.py`, etc.
- **CI/CD & Quality**: `.github/workflows/ci.yml` configures a multi-stage pipeline (lint → test → coverage), with test results surfaced in `docs/test_results/*` and `docs/skillgap_eval_dashboard.html`.

The overall pattern is a classic **React SPA + FastAPI REST API + Postgres DB** stack — fully decoupled frontend and backend communicating over HTTPS JSON APIs.

---

## 2. Backend Structure & Module Responsibilities

Backend code lives in `server/`, with `main.py` as the entry point:

- Creates the FastAPI application (`app = FastAPI(title="SkillGap API", lifespan=lifespan)`).
- Configures CORS to allow access from local development and production frontend origins.
- Uses `lifespan` to handle database table creation and Postgres-specific `skills` array column migration on startup.
- Registers all business routers:
  - `/api/auth` → `auth/router.py`
  - `/api/profile` → `profile/router.py`
  - `/api` (skill extraction) → `extraction/router.py`
  - `/api/history` → `history/router.py`
  - `/api/roadmap` → `roadmap/router.py`

### 2.1 Auth Module (`auth/`)

- **`auth/models.py`**: Defines the `User` entity (fields: `email`, `hashed_password`, `is_active`, `skills`, `roadmap`, etc.).
- **`auth/schemas.py`**: Pydantic models for request/response contracts — `UserCreate`, `UserOut`, `Token`, etc.
- **`auth/utils.py`**:
  - Password hashing and verification (via `passlib` / `bcrypt`).
  - JWT creation (`create_access_token`) following the configured expiry policy.
- **`auth/deps.py`**:
  - `get_current_user` / `get_current_active_user` dependencies, used to inject the current user object into protected routes.

**Routes: `auth/router.py`**

- `POST /api/auth/register`: Creates a new user, hashes the password, and persists to the database.
- `POST /api/auth/login`: Validates email + password, returns a JWT access token.
- `GET /api/auth/me`: Returns the current user's info via `get_current_active_user`.

All protected business endpoints depend on `get_current_active_user`, which is applied consistently across Profile, History, and Roadmap modules — authentication logic is centralized and never duplicated.

### 2.2 Skill Profile Module (`profile/`)

- **`profile/schemas.py`**:
  - `SkillAddRequest`: Request body for adding a skill.
  - `ResumeExtractRequest`: Request body for resume-based skill extraction.
- **`profile/router.py`** provides CRUD operations around the user's skill array:
  - `GET /api/profile/skills`: Returns the current user's `skills` field (Postgres `VARCHAR[]`; a compatibility implementation is used in the SQLite test environment).
  - `POST /api/profile/skills`: Adds a single skill with empty-string rejection and case-insensitive deduplication.
  - `DELETE /api/profile/skills/{skill_name}`: Removes a skill by name.
  - `POST /api/profile/extract-resume`: Matches skills from long-form resume text against the `CURATED_SKILLS` list in `extraction/engine.py`, then merges results into the user's `skills` field.

This module abstracts away the array storage details, presenting the frontend with a simple string-list interface backed by `User.skills`.

### 2.3 JD Skill Extraction Module (`extraction/`)

- **`extraction/engine.py`**:
  - Defines `CURATED_SKILLS`: a curated list of 60+ technical skill keywords.
  - `extract_skills(job_description, user_skills)`: Matches skills from the JD and classifies them into `have` / `missing` / `bonus`.
  - `extract_company_and_position(job_description)`: Uses regex and heuristics to extract company name and job title from JD text.
- **`extraction/router.py`**:
  - Pydantic models `ExtractRequest` / `ExtractResponse`.
  - `POST /api/extract`: Exposes the extraction endpoint; pure functional call to the engine with no database dependency.

This module is the **core rule engine** of the application, producing the structured data that feeds both History persistence and Roadmap generation.

### 2.4 Analysis History Module (`history/`)

- **`history/models.py`**:
  - `AnalysisHistory` model: records each JD analysis result — job title, company, have/missing/bonus skills, match score, raw JD text, and timestamp.
- **`history/schemas.py`**:
  - `HistoryCreate` / `HistoryUpdate` / `HistoryResponse`: Pydantic schemas mapping the database model to REST API contracts.
- **`history/router.py`**:
  - `GET /api/history/`: Returns all history records for the current user, sorted by most recent first.
  - `POST /api/history/`: Creates a new history record; internally calls `extraction.engine.calculate_match_score` from `have_skills` and `missing_skills` to prevent client-side score manipulation.
  - `PUT /api/history/{history_id}`: Allows updating metadata (company name, job title) with ownership verification.

This module encapsulates a single analysis session as a persistent object, supporting the "history review" and "progress tracking" user stories in the PRD.

### 2.5 AI Learning Roadmap Module (`roadmap/`)

- **`roadmap/schemas.py`**:
  - `RoadmapGenerateRequest`: Contains `missing_skills` and optional `jd_text`.
  - `RoadmapGenerateResponse`: Wraps the structured roadmap returned by Claude (summary, phases, metrics, etc.).
- **`roadmap/services.py`**:
  - `generate_roadmap_with_claude(...)`: Communicates with the Anthropic Claude API using a constrained JSON template prompt to produce a structured roadmap.
  - Custom exceptions: `ClaudeTimeoutError` / `ClaudeAuthError` / `ClaudeAPIError` / `ClaudeParseError` — allow the router to differentiate failure modes cleanly.
- **`roadmap/router.py`**:
  - `POST /api/roadmap/generate`: Exposes the AI roadmap generation endpoint; saves the result to `current_user.roadmap` and returns it to the frontend.

This module implements the AI completion feature as a clean service layer + routing layer, making it straightforward to swap models or tune prompts without touching the frontend contract.

---

## 3. Frontend Structure & Page Routes

Frontend code lives in `client/`.

### 3.1 Application Entry & Base Config

- **`src/main.tsx`**: React app entry point, mounting the Router, global styles, and top-level state providers.
- **`src/index.css`** and `tailwind.config.js`: Global styles and Tailwind design system configuration.
- **`vite.config.ts`**: Vite build configuration.
- **`src/vite-env.d.ts`**: TypeScript declarations for Vite environment variables.

### 3.2 Page-Level Components (Pages)

Located in `client/src/pages/`:

- `Login.tsx`: Login page, calls `POST /api/auth/login`, stores the token in `authStore` on success.
- `Register.tsx`: Registration page, calls `POST /api/auth/register`; optionally auto-logs in or redirects to the login page.
- `Dashboard.tsx`: Main dashboard page, containing:
  - JD input area (`JDInput`).
  - Skill match results (`SkillMatchResults` + `AnimatedMatchRing`).
  - AI learning roadmap display (`LearningRoadmap`).
- `Profile.tsx`: Skill profile management page, calls `/api/profile/*` for add/remove/list skills and resume extraction.
- `History.tsx`: History page, calls `/api/history` to fetch and display past analysis records.

Route guarding is handled by `components/ProtectedRoute.tsx`, which redirects unauthenticated users to the login page based on whether `authStore` holds a valid token.

### 3.3 Shared Components

- `Navbar.tsx`: Global navigation bar with login status indicator and links to Dashboard / Profile / History.
- `JDInput.tsx`: Job description input component; collects JD text and triggers the `/api/extract` backend call.
- `SkillMatchResults.tsx`: Displays the have / missing / bonus skill columns in sync with `AnimatedMatchRing`.
- `AnimatedMatchRing.tsx`: SVG-based animated ring showing the match score — one of the primary UI wow-factors.
- `LearningRoadmap.tsx`: Renders `RoadmapGenerateResponse.roadmap` as a vertical timeline or card layout.
- `Skeleton.tsx`: Generic skeleton screen component providing smooth loading states while the AI roadmap is being generated.

Together, these components deliver the end-to-end "paste JD → see match → see roadmap" user journey defined in the PRD.

### 3.4 State Management (Stores)

Global state managed with Zustand:

- **`store/authStore.ts`**:
  - Holds `accessToken`, current user info, and login/logout logic.
  - Mirrors the backend Auth module; centralizes token persistence and restoration.
- **`store/profileStore.ts`**:
  - Holds the user's skill list, loading state, and error state.
  - Exposes high-level actions for interacting with `/api/profile/*`.

Page components only need to call store actions and consume store state — API calls and side effects are not scattered across UI components.

### 3.5 API Abstraction Layer

- **`lib/api.ts`**: Wraps an Axios instance or fetch utility with `VITE_API_BASE_URL` and `Authorization` header applied globally.
- **`api/auth.ts`**: Implements `login`, `register`, `fetchCurrentUser`, etc.
- **`api/roadmap.ts`**: Implements `generateRoadmap` calling `/api/roadmap/generate`.

Centralizing API calls in `api/*` makes it straightforward to swap the backend URL, add retry logic, or standardize error handling in one place.

---

## 4. Data Flow: From JD to AI Roadmap

The following traces the most critical user journey end-to-end:

1. **User logs in**:
   - `Login.tsx` calls `api/auth.login` → `POST /api/auth/login`.
   - `auth/router.py` validates credentials → generates JWT → returns `access_token`.
   - `authStore` saves the token and attaches it to all subsequent requests via the `Authorization` header.

2. **Maintaining the skill profile**:
   - `Profile.tsx` calls `/api/profile/skills` via `profileStore` to fetch and update skills.
   - Optionally calls `/api/profile/extract-resume` to auto-populate skills from resume text.
   - Backend persists skills to `User.skills`.

3. **JD skill analysis**:
   - User pastes a JD in `Dashboard.tsx` and submits; `JDInput` calls `POST /api/extract`.
   - `extraction/engine.py` analyzes the JD against `CURATED_SKILLS` and the user's skill list, returning `have` / `missing` / `bonus`.
   - Frontend updates `SkillMatchResults` and the `AnimatedMatchRing` animation.

4. **Persisting the history record**:
   - After analysis, the frontend posts a `HistoryCreate` request to `/api/history/`.
   - `history/router.py` calls `calculate_match_score`, inserts the full result into `AnalysisHistory`.
   - `History.tsx` fetches and displays past records via `GET /api/history/`.

5. **Generating the learning roadmap**:
   - User clicks "Generate Learning Roadmap"; `LearningRoadmap` (or the relevant action) calls `POST /api/roadmap/generate`.
   - `roadmap/services.py` invokes the Claude API with `missing_skills` and `jd_text` as context:
     - On success: returns structured JSON roadmap and writes it to `current_user.roadmap`.
     - On failure: raises the appropriate HTTP error (504 / 502 / 500).
   - Frontend transitions from skeleton → real roadmap cards.
   - The latest roadmap is available for reference in Dashboard / History on return visits.

---

## 5. Testing, Quality & CI/CD

- **Backend tests**: Located in `server/tests/`, covering Auth, Profile, History, Extraction, and Roadmap core logic with an 80%+ coverage threshold enforced in CI.
- **Frontend tests**: Located in `client/src/test/`, using Vitest + React Testing Library, covering pages and key components (Login, Dashboard, Profile, History, etc.).
- **Quality & evaluation**:
  - `docs/test_results/backend_test_report.txt` / `frontend_test_report.txt`: Test run summaries.
  - `docs/eval_roadmaps/ai_eval_results.md`: AI evaluation script output assessing Claude-generated roadmap quality.
  - `docs/skillgap_eval_dashboard.html`: Comprehensive Eval Dashboard presented against course requirements.
- **CI/CD Pipeline**:
  - `.github/workflows/ci.yml`: Multi-stage workflow — frontend/backend lint, then tests and coverage — protecting main branch quality.
  - Every PR also triggers **Netlify** Deploy Preview and site rule checks (Header rules, Pages changed, Redirect rules), making the full check status visible on the PR page (see README §8).

---

## 6. Mapping to PRD User Stories

- **Story 1 (Profile Management)**:
  - Backend: `/api/profile/*` + `User.skills` field.
  - Frontend: `Profile.tsx` + `profileStore`.
- **Story 2 (Core Value: JD Matching & Visualization)**:
  - Backend: `/api/extract` + `extraction/engine.py`.
  - Frontend: `JDInput`, `SkillMatchResults`, `AnimatedMatchRing`, `Dashboard.tsx`.
- **Story 3 (AI Guidance: Learning Roadmap)**:
  - Backend: `/api/roadmap/generate` + `roadmap/services.py`.
  - Frontend: `LearningRoadmap` and surrounding state management.
- **Story 4 (Progress Tracking: History)**:
  - Backend: `/api/history/*` + `history/models.py`.
  - Frontend: `History.tsx`.
- **Story 5 (Continuous Learning: Iterative Skill Profile)**:
  - Combines Profile + History + Roadmap layers; repeated JD analyses let users track score improvements over time.

Every core user story in the PRD maps directly to a frontend page + backend module + data model combination, making it straightforward to trace from requirements to the specific code responsible for delivering them.
