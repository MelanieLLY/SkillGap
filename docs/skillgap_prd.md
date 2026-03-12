# Product Requirements Document (PRD): Tech Stack Skill Gap Analyzer

## 1. Document Overview
**Project Background & Vision**:
Job seekers (especially career changers and new graduates) often waste significant time applying to roles without a clear understanding of their actual skill fit. Reading a job description (JD) and self-assessing is subjective, slow, and often inaccurate. 
The "Tech Stack Skill Gap Analyzer" solves this by providing a focused, fast experience: users paste a JD and their skills, and within seconds, the app identifies the skill gap and provides an AI-generated personalized learning roadmap.

**Core Objectives**:
- Provide fast, accurate job skill match analysis based on a curated list of 60+ core tech skills.
- Generate specific, actionable AI learning roadmaps to help users close their skill gaps.
- Deliver a simple, intuitive user experience (animated match ring, three-column comparison view).

**Key Performance Indicators (KPIs)**:
- **AI Quality Metrics**:
  - Relevance: Do the recommended resources match the missing skill? (Scale 1-5)
  - Specificity: Does the roadmap give concrete next steps over vague advice?
  - Completeness: Are all missing skills addressed? (%)
- **Engineering Metrics**:
  - Backend test coverage of 80%+.
  - Fast response times for the extraction flow (excluding the fixed latency of the Claude API call).

## 2. Target Audience & Use Cases
**Target User Personas**:
1. **Graduate Students**: Actively preparing for technical interviews, needing to know what specific frameworks or tools they should study next.
2. **Career Changers**: Learning new skills and wanting a visual understanding of how close they are to job readiness.
3. **Active Job Seekers**: Wanting a quick, objective assessment of whether they meet a role's qualifications before applying.

**Typical Use Case**:
- A user finds an interesting job posting, copies the JD, and pastes it into the app. The app references the user's previously saved skill profile and instantly calculates a match score, categorizing skills into "Have", "Missing", and "Bonus", followed by an AI-generated learning plan with tutorial links.

## 3. Core User Stories (Product Perspective)
These represent the high-level goals of our end users. 

- **Story 1 (Profile Management)**: As a new user, I want to securely save my skill profile so I do not need to re-enter it each time.
- **Story 2 (Core Value)**: As a job seeker, I want to paste a job description and see an instant match score and a breakdown of my skill gap.
- **Story 3 (AI Guidance)**: As a job seeker, I want to receive an AI-generated learning roadmap for the missing skills I need to acquire.
- **Story 4 (Progress Tracking)**: As a returning user, I want my past analyses saved so I can track my progress and revisiting old roles.
- **Story 5 (Continuous Learning)**: As a learning user, I want to update my skill profile as I learn and re-analyze jobs to see my match score improve.

---

## 4. GitHub Issues Breakdown (Engineering Perspective)
*(Note: To satisfy Agile development processes and tracking, the core user stories above have been broken down into specific implementation issues spanning two sprints. These should be tracked on a GitHub Project Board.)*

### Sprint 1: Core Application (Feb 26 – Mar 14)
- **Issue 1: Implement User Registration & Login (Auth)**
  - *Context*: Implements Story 1.
  - **Acceptance Criteria**: Implement JWT-based signup/login/logout. Routes are protected.
- **Issue 2: Create Skill Profile Setup Flow**
  - *Context*: Implements Story 1.
  - **Acceptance Criteria**: Users can select/input skills; data is persisted to the DB per account.
- **Issue 3: Implement Skill Profile CRUD Operations**
  - *Context*: Implements Story 5.
  - **Acceptance Criteria**: Users can add, edit, or delete skills from their profile at any time.
- **Issue 4: Build Job Description Input Component**
  - *Context*: Implements Story 2.
  - **Acceptance Criteria**: A text area is available for pasting a JD; a submit button triggers the backend analysis pipeline.
- **Issue 5: Develop Keyword Skill Extraction Engine**
  - *Context*: Implements Story 2.
  - **Acceptance Criteria**: Keyword matching against a curated list of 60+ tech skills from both the JD and the user's profile.
- **Issue 6: Create Match Score Visualization (Animated Ring)**
  - *Context*: Implements Story 2.
  - **Acceptance Criteria**: An animated ring chart displays the % skill match, color-coded (green/yellow/red).
- **Issue 7: Build Three-Column Comparison View UI**
  - *Context*: Implements Story 2.
  - **Acceptance Criteria**: UI displays three distinct columns: Skills You Have, Skills You're Missing, Bonus Skills.

### Sprint 2: AI Features & Polish (Mar 15 – Apr 4)
- **Issue 8: Integrate Claude API for Learning Roadmap**
  - *Context*: Implements Story 3.
  - **Acceptance Criteria**: Backend calls Claude API with missing skills/JD; frontend renders returned JSON into an actionable roadmap.
- **Issue 9: Develop Analysis History View**
  - *Context*: Implements Story 4.
  - **Acceptance Criteria**: Users can access a history view of previously analyzed JDs and their scores.
- **Issue 10: Build AI Evaluation Suite**
  - *Context*: Engineering Quality Check.
  - **Acceptance Criteria**: Implement test cases measuring Relevance, Specificity, and Completeness for 10+ JD/profile pairs.
- **Issue 11: Implement UI Polish & Accessibility Standards**
  - *Context*: Frontend Quality Check.
  - **Acceptance Criteria**: Mobile-responsive design, Accessibility considerations, proper loading states, and error boundary handling.

---

## 5. Non-Functional Requirements
- **Performance**: Millisecond response times for core API routes. Graceful loading UI components (e.g. skeletons) while waiting for the AI API.
- **Security**: JWT token refresh mechanics. Passwords securely hashed in the database.
- **Testing**: 80%+ test coverage on the backend using Pytest. TDD approach for parsing logic.

## 6. Architecture & Tech Stack
- **Frontend**: React 18 + TypeScript, Vite, Tailwind CSS, Zustand (state). Axios for API calls, Recharts or Custom SVG for the match ring.
- **Backend**: FastAPI (Python 3.11, async endpoints), SQLAlchemy ORM + PostgreSQL. python-jose for JWT, Pydantic for validation, Alembic for migrations.
- **AI Integration**: Claude API (`claude-sonnet-4-20250514`).
- **CI/CD**: GitHub Actions (Lint -> Unit Tests -> Integration Tests -> Build -> Deploy). Docker Compose for local dev.

## 7. Design & UI Mockups Reference
- **Reference Images**: Please refer to `SkillGap wireframe hand draw-5.jpg` (hand-drawn sketch) and `SkillGap wireframe (ai generated based on handdraw).png` (AI generated wireframe design).
- **Dashboard Layout**: Top navigation bar containing Logo, My Profile, History, and Logout.
- **Main View**: Split layout (Left: JD Input Area | Right: Match Results).
- **Match Results Area**: Top displays the Animated Ring Score; below are the three skill columns; at the bottom, the structured AI Learning Roadmap (timeline or card format).

## 8. Sprint Plan & Release Constraints
- **Sprint 1 (Feb 26 – Mar 14)**: Deliver the core authenticated application without the AI call. TDD focus for the extraction engine. All Sprint 1 issues must be closed and PRs reviewed.
- **Sprint 2 (Mar 15 – Apr 4)**: Interface with the Claude API for the roadmap. Add history, build the evaluation suite, and polish the UI.
- **Stretch Goal**: Replace simple keyword matching with sentence-transformer embeddings for semantic skill matching.
