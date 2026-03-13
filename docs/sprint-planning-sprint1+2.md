> This document was assembled by the AI assistant after reviewing `docs/skillgap_prd.md`, `internal_working_planning_note/PROJECT2_MASTER_PLAN.md`, GitHub Issues (with Sprint labels), and the Project Board. Liuyi then made minor corrections based on actual execution. The Issue numbers, time ranges, and goals presented here are a structured summary of the real GitHub history and course requirements — not a retrospective reconstruction from memory.

## Sprint 1 Planning (Core Application)

- **Time range**: 2026-02-26 – 2026-03-14
- **Theme**: Deliver a fully usable core application without AI-generated roadmaps — covering authentication, skill profile management, JD skill matching, and basic visualization.

### 1. Sprint Goal

Based on `docs/skillgap_prd.md` §4 and the GitHub Project Board, this Sprint aimed to deliver:

- User registration and login with secure data persistence.
- A skill profile that users can create and maintain.
- A JD input entry point with automated matching against the user's skill profile.
- Visual display of the match score and the have / missing / bonus skill breakdown.
- The data and architectural groundwork for Sprint 2's AI roadmap and history features.

### 2. User Story Scope (from PRD)

This Sprint primarily covers the following user stories from the PRD:

- **Story 1 – Profile Management**
  As a new user, I want to save my skill profile so I don't have to re-enter it every time.
- **Story 2 – Core Value (JD Skill Match)**
  As a job seeker, I want to paste a JD and see a match score along with a skill gap analysis.
- **Story 5 – Continuous Learning (partial)**
  As a learner, I want to update my skill profile and re-analyze to track changes in my match score.

### 3. Issues Selected for Sprint 1

(Based on `docs/skillgap_prd.md` §4 and `internal_working_planning_note/GitHub project board.md`)

- **Issue #1: Implement User Registration & Login (JWT Auth)**
  - Build the `/api/auth` backend routes and JWT flow.
  - Implement login/register pages in the frontend, connected to the real API.
  - Acceptance criteria: can register a new user, log in, and persist the token in the frontend.

- **Issue #2: Implement Skill Profile CRUD**
  - Backend: implement the `/api/profile/skills` endpoints and `User.skills` field.
  - Frontend: support add, remove, and display of skills on the Profile page.
  - Acceptance criteria: skills persist across page refreshes; duplicate additions are deduplicated.

- **Issue #3: Build Job Description Input Component**
  - Frontend: JD text input area and submit button on the Dashboard.
  - Acceptance criteria: users can paste a full JD and trigger a backend call by clicking Analyze.

- **Issue #4: Develop Keyword Skill Extraction Engine**
  - Backend: implement the `CURATED_SKILLS`-based keyword matching algorithm in `extraction/engine.py`.
  - Expose the `/api/extract` endpoint returning have / missing / bonus classifications.
  - Acceptance criteria: correctly classifies all three skill categories for a typical JD.

- **Issue #5: Implement Match Score Calculation Logic**
  - Backend: implement `calculate_match_score` in `history` or the extraction engine.
  - Acceptance criteria: score is consistent with the have/missing ratio; cannot be spoofed by the client.

- **Issue #6: Build Three-Column Comparison UI**
  - Frontend: have / missing / bonus three-column component on the Dashboard.
  - Acceptance criteria: columns are clearly arranged, responsive layout works well, long lists are scrollable.

- **Issue #12: Create Match Score Visualization (Animated Ring)**
  - Frontend: `AnimatedMatchRing` component for visualizing the match score.
  - Acceptance criteria: smooth animation on score change, with distinct color transitions for high / medium / low scores.

> Note: Although the PRD places Issue #12 under Sprint 1 Core Application, some UI polish work extended into Sprint 2.

### 4. Out of Scope (explicitly excluded from Sprint 1)

- AI learning roadmap generation (Claude API call and `/api/roadmap/generate`) — deferred to Sprint 2.
- Analysis History view and persistence — core logic to be completed in Sprint 2.
- Eval Dashboard, AI evaluation scripts, and complex CI configuration — addressed in later phases.

### 5. Definition of Done

For Issues selected in Sprint 1, the team agreed on the following criteria:

- Passes the GitHub Actions CI pipeline (at minimum: basic lint + pytest).
- All core backend routes have corresponding unit tests or integration tests.
- Key frontend pages (Login / Dashboard / Profile) complete the full flow successfully in a local environment.
- New code complies with the type and PEP 8 standards in `.antigravityrules`.
- Code merged via Pull Request; direct pushes to `main` are prohibited.

### 6. Anticipated Risks & Mitigation

- **Risk 1: Auth/database configuration issues**
  - Mitigation: complete basic Auth + DB connectivity testing early in Sprint 1 and document the migration strategy in `PROJECT2_MASTER_PLAN.md`.

- **Risk 2: Frequent frontend/backend contract changes**
  - Mitigation: treat the API contract in `docs/skillgap_prd.md` as the source of truth; surface any changes through small PRs with quick sync.

- **Risk 3: Insufficient test coverage affecting later CI rules**
  - Mitigation: write Pytest tests alongside each set of routes during Sprint 1, so Sprint 2 can raise coverage rather than retroactively writing tests.


## Sprint 2 Planning (AI Features & Polish)

- **Time range**: 2026-03-15 – 2026-04-04
- **Theme**: Build on Sprint 1's core application by adding Claude AI learning roadmaps, history view, testing, and UI polish to deliver a complete end-to-end experience.

### 1. Sprint Goal

Based on the "Sprint 2: AI Features & Polish" section in `docs/skillgap_prd.md`, this Sprint aimed to:

- Integrate the Claude API to generate structured learning roadmaps for missing skills.
- Persist every JD analysis record and allow users to review them later.
- Build the AI quality evaluation suite and Eval Dashboard.
- Polish the UI/UX (skeleton screens, animations, accessibility) to reach a demo-ready experience.

### 2. User Story Scope (from PRD)

This Sprint primarily covers the following user stories from the PRD:

- **Story 3 – AI Guidance**
  As a job seeker, I want an AI-generated learning roadmap for my skill gaps so I know what to study next.
- **Story 4 – Progress Tracking**
  As a returning user, I want to see my history of analyses and how my match score has changed over time.
- **Story 5 – Continuous Learning (completed)**
  As skills are updated and roadmaps are followed, I can re-analyze JDs and compare results before and after.

### 3. Issues Selected for Sprint 2

(Based on `docs/skillgap_prd.md` and Phase 2/3 of `PROJECT2_MASTER_PLAN.md`)

- **Issue #7: Integrate Claude API for learning roadmap generation**
  - Backend: implement `generate_roadmap_with_claude` in `roadmap/services.py` using the Anthropic SDK.
  - Route: `POST /api/roadmap/generate` with `RoadmapGenerateRequest/Response`.
  - Frontend: add "Generate Learning Roadmap" button and rendering component in the Dashboard.
  - Acceptance criteria: structured roadmap is visible in the frontend; error states (timeout, auth failure) are handled gracefully.

- **Issue #8: Develop Analysis History View**
  - Backend: complete `history/models.py` and `history/router.py`, ensuring `match_score` is computed server-side.
  - Frontend: implement the `History.tsx` page, calling `/api/history/` to display all user analysis records.
  - Acceptance criteria: user can view time-sorted history records with fields consistent with the Dashboard.

- **Issue #9: Build AI Evaluation Suite (roadmap metrics)**
  - Implement and document AI roadmap quality evaluation in `server/tests/ai_eval.py` and `docs/eval_roadmaps/*`.
  - Use a second LLM as a "Judge" to score Relevance / Specificity / Completeness.
  - Acceptance criteria: can batch-evaluate multiple JD/skill combinations and produce `docs/ai_eval_results.md`.

- **Issue #10: Improve UI polish and accessibility**
  - Add detail animations and skeleton screens to `AnimatedMatchRing`, `LearningRoadmap`, `Skeleton`, and related components.
  - Add `aria-*` attributes, button state management, and light/dark mode support.
  - Acceptance criteria: no noticeable "blank flash" or unindicated loading in the core user flow; meets baseline accessibility practices.

- **Issue #14: Set up pytest and backend test coverage**
  - Fill out tests for Auth / Extraction / History / Roadmap in `server/tests/`.
  - Configure a coverage threshold (80%+) enforced in CI.
  - Acceptance criteria: `pytest` passes fully locally and in CI; coverage report meets the threshold.

### 4. Technical & DevOps Tasks

These tasks support Sprint 2 but do not map directly to a single user story (corresponding to Issues #31, #35, #37, #38, etc.):

- **CI Pipeline & Quality Report Improvements**
  - Add multi-stage jobs to `.github/workflows/ci.yml`: lint → test → build/coverage.
  - Run lint/test independently for frontend and backend; output reports to `docs/test_results/` and display them in `docs/skillgap_eval_dashboard.html` (see Issues #9, #29, #31).

- **Database & Error Handling Hardening**
  - Wrap all `db.commit()` calls in `auth/profile/history` with `try/except SQLAlchemyError` and rollback logic.
  - Add a global SQLAlchemy exception handler in `main.py` to prevent raw 500 crashes in production (see Issues #15, #16).

- **Repository Structure & Deployment Preparation (DevOps)**
  - Clearly separate the repository into `client/` and `server/` subdirectories for independent deployment and CI caching (Issue #35: repo restructure).
  - Prepare deployment configuration for backend on Render and frontend on Netlify (Issue #37: Render backend, Issue #38: Netlify frontend).
  - Every PR runs GitHub Actions (Lint / Test / Build) and triggers Netlify Deploy Preview plus site rule checks (Header rules, Pages changed, Redirect rules), allowing frontend preview validation before merging.

### 5. Definition of Done

For Stories/Issues introduced in Sprint 2, the team agreed:

- Claude-related logic has a **minimum reproducible prompt** documented in internal notes (for AI reflections).
- The AI-generated roadmap JSON schema is **stable**; frontend components render using strict type definitions.
- `docs/ai_eval_results.md` and `docs/skillgap_eval_dashboard.html` cover at least 5 real JD scenarios.
- CI pipeline runs by default on every Pull Request, blocking merges when tests fail or coverage falls short.

### 6. Out of Scope (explicitly excluded from Sprint 2)

- External blog post and public video (belong to the Documentation / Presentation phase of the course).
- Advanced features unrelated to course requirements — e.g., vector search, semantic search, complex permission systems.
- Full UI design system rewrite: Sprint 2 focuses on polish, not large-scale redesign.
