## Team Contributions

**Project**: Tech Stack Skill Gap Analyzer (SkillGap)
**Team Members**: **Liuyi (MelanieLLY)**, **Jing**

> This document was automatically compiled by the AI assistant from the full GitHub commit history, GitHub Issues / Project Board metadata, and internal planning notes, then reviewed and supplemented by Liuyi. The focus is not on raw commit count, but on combining Issue ownership, module ownership, and timeline to reflect each member's genuine responsibilities and representative contributions across each Sprint.
> **Note**: The documentation package (API docs, Scrum documents, AI-related docs, code-architecture, etc.) was substantial and evolved continuously throughout the project, with both team members and multiple rounds of AI collaboration involved. Accordingly, this document does not itemize documentation work to the individual level — it can be understood as a "shared responsibility with reasonable division of labor." This document focuses primarily on engineering and code contributions.

---

## 1. Liuyi (MelanieLLY): Core Feature Implementation, Backend Architecture, CI/CD, AI Integration & Quality Assurance

### 1.1 Primary Responsibilities

- Owned the overall architecture and stability of the FastAPI backend service.
- Managed cloud PostgreSQL database configuration and migration strategy.
- Led and contributed to multiple **core business feature** implementations, including early skill extraction/matching optimizations, History and Roadmap backend logic, and more.
- Designed and built the multi-stage CI/CD pipeline to meet test and coverage requirements.
- Led the Claude AI learning roadmap integration and the AI Eval Suite implementation.
- Coordinated project-level documentation (API docs, code architecture guide, Eval Dashboard, etc.).

### 1.2 Key Technical Contributions (Examples)

> The examples below are drawn from `internal_working_planning_note/GitHub commit history copy from github.md` and represent a selection of representative commits.

- **CI/CD & Testing Infrastructure**
  - `feat(#14): implement backend test suite and multi-stage ci workflow`
  - `chore: streamline CI to focus on security and coverage requirements`
  - `test(#29): add unit tests for migrate_roadmap.py`
  - `docs: implement evaluation dashboard and generate test coverage reports` (Issue #9 Eval Dashboard)
  - `fix(ci): correct node cache path and package-lock location for workspaces`
  - These commits established the backend pytest foundation, coverage thresholds, and the joint frontend/backend CI pipeline. By surfacing test and coverage results in the Eval Dashboard, they ensured all subsequent PRs were held to a clear, observable quality bar.

- **AI Roadmap Integration & Roadmap Feature**
  - `feat(#21): setup Claude AI scaffolding with dummy service and integration tests`
  - `feat(#7): implement Claude-powered learning roadmap with TDD and frontend integration`
  - `feat(#7): implement roadmap and dashboard state persistence`
  - Owned `roadmap/services.py` and `/api/roadmap/generate`, as well as Dashboard state management and persistence integration with the frontend.

- **Security & Database Reliability**
  - `refactor(#15): implement global db error handler and debug logs`
  - `fix(#16): fix mac environment bugs and unify postgresql database`
  - Improved system stability and observability in real deployment environments by standardizing on cloud PostgreSQL and adding a global SQLAlchemy exception handler.

- **Deployment & Repository Structure (DevOps)**
  - `enhancement(#35): separate client and server structure for independent deployment`
  - `chore(deploy): (#37) configure FastAPI backend deployment on Render`
  - Completed the full frontend/backend separation structure and production deployment configuration for Render (backend) and Netlify (frontend), corresponding to Issues #35/#37/#38. Every PR triggers GitHub Actions (Lint / Test / Build) as well as Netlify Deploy Preview and site rule checks (Header rules, Pages changed, Redirect rules).

- **Frontend Testing & UI Polish**
  - `feat(#14): setup vitest testing environment and core unit tests`
  - `feat(#29): improve frontend line coverage to 87% and fix component accessibility`
  - `feat(#10): implement learning roadmap skeletons and framer-motion animations`
  - `fix(test): resolve CI lint errors and React scope in test setup`
  - Set up the Vitest testing framework for the frontend and pushed line coverage to 87%+; also delivered multiple rounds of animation, skeleton screen, and accessibility (a11y) improvements to make the Dashboard experience smoother and more inclusive.

- **Documentation & Project Management**
  - Led the final version of `PROJECT2_MASTER_PLAN.md`, translating the course rubric into an executable engineering roadmap.
  - Authored/completed core documents: `docs/api-docs.md`, `docs/code-architecture.md`, `docs/ai-modalities-usage.md`, `docs/ai-reflection.md`.

### 1.3 Impact on Team Collaboration

- Liuyi (MelanieLLY) effectively served as **Backend Tech Lead + DevOps Engineer** on the project:
  - Maintained the overall system architecture and quality boundaries.
  - Provided a stable CI and test foundation for Jing's frontend and rule engine work.
  - Delivered systematic support across the AI Mastery, CI/CD, and Documentation dimensions of the course rubric.

---

## 2. Jing: Core Feature Implementation, Frontend Experience & Extraction Engine

### 2.1 Primary Responsibilities

- Owned the core feature loop: authentication flow, skill profile management, JD skill extraction, and the frontend's primary user journey.
- Designed and implemented the animated match score ring and the three-column skill comparison UI — key UX differentiators.
- Led the `extraction` engine and its integration with the frontend Dashboard, ensuring rule engine results rendered accurately in the UI.
- Contributed to Sprint planning, rules files (`.antigravityrules`, `RULES_WRITEUP.md`), and GitHub Project Board maintenance.

### 2.2 Key Technical Contributions (Examples)

> The examples below are also drawn from the commit history review and represent a selection of representative commits.

- **Authentication & Core CRUD**
  - `feat(#1): implement login and register pages with JWT auth flow`
  - `feat(#11): implement skill profile CRUD with persistent storage`
  - Established the complete pipeline from frontend forms to backend `/api/auth` and `/api/profile`, providing the foundation for all subsequent automated analysis.

- **Skill Extraction Engine & Match Score Calculation**
  - `feat(#4): implement keyword skill extraction engine`
  - `update/add extraction engine and tests`
  - `feat(#5): implement match score calculation logic` (see Issue history)
  - Owned `CURATED_SKILLS` and the extraction logic in `extraction/engine.py`, implementing the core matching algorithm between JD requirements and the user's skill profile.

- **Frontend User Experience & Visualization**
  - `feat(#12): implement animated match score ring visualization`
  - `feat(#8): implement analysis history persistence and retrieval` (frontend portion)
  - Integrated JD input, match result display, and history record entry into the Dashboard page, delivering a cohesive user journey.

- **Engineering Standards**
  - Iteratively updated `.antigravityrules` and `internal_working_planning_note/RULES_WRITEUP.md` to enforce type safety, testing discipline, and CI rigor.
  - Actively applied these standards in the PR review process to guide AI usage and code reviews.

### 2.3 Impact on Team Collaboration

- Jing effectively served as **Full-Stack Feature Owner** on the project:
  - Maintained a user-centric, end-to-end perspective throughout development.
  - Bridged the rule engine and frontend interaction layer, delivering the "first layer of value" that Sprint 2's AI features and history tracking were built upon.
  - Quickly shipped a demo-ready MVP in the early Sprint, creating the time buffer that enabled Sprint 2 enhancements.

---

## 3. Collaboration & Cross-Contributions

While the two members had distinct areas of ownership, they collaborated closely on many critical tasks:

- **Joint Sprint Planning & Documentation**
  - Both used Claude Web together to draft the PRD, PROJECT2_MASTER_PLAN, and Scrum documents.
  - Jointly reflected on the process in `docs/sprint-planning-*.md` and `docs/sprint-retro-*.md`.

- **Shared Ownership of Quality & Testing**
  - Jing wrote and adjusted frontend and backend tests as features were implemented.
  - Melanie's CI and coverage rules turned those tests into mandatory gates that every PR had to pass.

- **Joint AI Tooling & Reflection**
  - Both used AI Agent extensively in the IDE and preserved key prompts and conversations in the internal notes (see `internal_working_planning_note/ai chat history Liuyi/*`).
  - `docs/ai-modalities-usage.md` and `docs/ai-reflection.md` summarize the team's collective experience and lessons learned around AI usage.

---

## 4. On Commit Distribution & Evidence

From `internal_working_planning_note/GitHub commit history copy from github.md`:

- Later in the project (especially during CI, AI integration, and documentation wrap-up), Melanie's commits are more concentrated.
- Earlier in the project (MVP architecture and core features), Jing had a higher share of contributions across auth, profile, extraction, and the frontend main flow.

Given that:

- The project made extensive use of IDE AI Agent and Claude Web.
- Some larger commits represent automated code formatting or CI configuration updates.

We do not treat raw commit count as the primary contribution metric. Instead, contributions are evaluated through:

- **Issue ownership and implementation scope** (see GitHub Project Board).
- **Key module ownership** (described in the role sections above).
- **Internal planning documents and AI conversation records** (showing who drove which key decisions and when).

In summary, both members played indispensable roles in this project:
Jing focused on product feature delivery and end-to-end user experience; Melanie focused on system reliability, deep AI integration, and quality assurance.
Across the course rubric dimensions (Functionality / Technical Excellence / AI Mastery / CI/CD / Agile Process), their contributions are complementary and balanced.
