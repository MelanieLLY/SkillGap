## AI Modalities Usage (Claude Web + IDE Agent + Others)

Throughout development, we deliberately separated the roles of different AI tools (modalities) to demonstrate **AI Mastery** as required by the course rubric, while maintaining traceability and reproducibility in our engineering workflow.

---

## 1. AI Modalities at a Glance

- **Claude Web (browser-based chat)**
  - Use cases: early-stage requirement clarification, architecture design, Mermaid diagrams, document drafting (PRD, blog outline, Eval Dashboard drafts, etc.).
  - Why: large context window, well-suited for long-form content and multi-turn discussions.

- **IDE AI Agent (Cursor)**
  - Use cases: concrete code implementation and refactoring, test generation, CI configuration, bug localization and fixes.
  - Why: reads and edits repository files directly, ideal for the "read code → change code → run tests" feedback loop.

- **Evaluator LLM (Judge mode)**
  - Use cases: automated quality evaluation of Claude-generated learning roadmaps in `server/tests/ai_eval.py`.
  - Why: acts as a structured scorer, outputting Relevance / Specificity / Completeness metrics against a fixed rubric.

---

## 2. Division of Responsibilities Across the Project Lifecycle

### 2.1 Planning & Product Phase (Planning / PRD / Roadmap)

- **Claude Web**:
  - Co-authored `docs/skillgap_prd.md` and `internal_working_planning_note/PROJECT2_MASTER_PLAN.md`.
  - Decomposed all course deliverables (API docs, Scrum docs, AI reflections, blog, video, etc.) from the rubric into actionable tasks.
  - Generated the initial Sprint 1/2 Issue list with time estimates.

- **Human + Claude Web**:
  - Manually reviewed and trimmed the generated plan, keeping only steps that were executable and verifiable.
  - Finalized the plan into `PROJECT2_MASTER_PLAN.md`, which served as the "work spec" for the IDE-side Agent.

### 2.2 Development & Implementation Phase (Coding / Refactor / Tests)

- **IDE Agent (Cursor)**:
  - Handled scoped, file-level tasks, for example:
    - "Add transaction handling and error recovery to `db.commit()` calls in `auth/router.py`."
    - "Write Pytest unit tests for `extraction/engine.py`, covering both positive and negative cases."
    - "Add loading skeleton and transition animations to `LearningRoadmap.tsx`."
  - Automatically edited code, ran tests, and fixed lint errors through tool calls.

- **Human review**:
  - Conducted manual code review for every significant change (using Git diff alongside test results).
  - Retained final authority over all security-related logic (JWT, database operations).

### 2.3 AI Eval & Quality Monitoring Phase

- **Evaluator LLM (Judge mode)**:
  - In `server/tests/ai_eval.py`: first invoked Claude to generate a learning roadmap, then used a second model to score it.
  - Scores and commentary were written to `docs/eval_roadmaps/ai_eval_results.md` and the Eval Dashboard.

- **Human spot-check**:
  - Manually read through the highest- and lowest-scoring roadmaps to perform a sanity check against the rubric.
  - When model scores diverged from human judgment, adjusted the prompt or scoring criteria accordingly.

---

## 3. Representative Workflow Examples

### 3.1 End-to-End: From Requirements to Code

1. **Claude Web – Requirement clarification and decomposition**
   - Had Claude Web read `P2 requirement.md` and the course rubric, then generate a project roadmap with Sprint-level breakdown.
   - Output consolidated into `PROJECT2_MASTER_PLAN.md` as the "master blueprint" for all subsequent work.

2. **IDE Agent – Concrete implementation and testing**
   - Worked one Issue at a time, invoking the Agent in the IDE:
     - Example: "Based on the PRD and plan, implement the Claude integration for `/api/roadmap/generate` and write the corresponding tests."
   - After the Agent completed code changes, it automatically ran `pytest` / Vitest and fixed any failures.

3. **Evaluate and iterate**
   - Used the AI Eval script to batch-generate and score roadmaps.
   - When certain scenarios underperformed, returned to Claude Web or the IDE Agent to refine the prompt or data structure.

### 3.2 Documentation & Demo Output

- **Claude Web**:
  - Drafted the blog outline (`internal_working_planning_note/final_delivery/blog_post_outline.md`).
  - Assisted with Eval Dashboard narrative text (later materialized in `docs/skillgap_eval_dashboard.html`).

- **IDE Agent**:
  - Generated README/CI config snippets and document scaffolding (e.g., this file, API docs, code-architecture).
  - Wrote directly into the repository, leaving content ready for human polish.

---

## 4. Usage Principles & Boundaries (Do / Don't)

### 4.1 Principles (Do)

- **Keep AI in the "assistant" role, not the "black-box decision-maker"**:
  - All security-related and architectural decisions require human review.
  - For every significant change, at least one engineer reads through the key code and tests.

- **Convert AI output into auditable artifacts**:
  - PRD / Plan → `docs/skillgap_prd.md`, `PROJECT2_MASTER_PLAN.md`.
  - Code changes → Git commits + Pull Requests.
  - Eval results → `docs/eval_roadmaps/ai_eval_results.md`, Eval Dashboard.

- **Assign distinct roles to different modalities**:
  - Claude Web: big-picture planning, long-form documents, mind maps.
  - IDE Agent: local refactoring, unit tests, bug fixes.
  - Judge LLM: roadmap quality evaluation.

### 4.2 Anti-patterns to Avoid (Don't)

- Never merge AI-generated code blocks directly into `main` without running tests or performing a human review.
- Never paste sensitive information (real passwords, production API keys) into Claude Web or any public conversation.
- Never blindly accept a scoring LLM's evaluation without explanation—treat it as one signal among many.

---

## 5. Summary: How We Used Multiple AI Modalities Effectively

In the SkillGap project, we followed a **Plan → Build → Evaluate** three-loop cycle:

- **Claude Web** and long-form conversations handled planning and documentation, translating course requirements into an executable engineering roadmap.
- **IDE AI Agent** handled the bulk of repetitive and mechanical coding work (refactoring, testing, CI configuration) with continuous local test runs.
- **Evaluator LLM** scored Claude-generated roadmaps, followed by human spot-checks and aggregation into the Eval Dashboard and AI Mastery evidence.

This division of labor fully leverages each AI tool's strengths while keeping critical control and final quality responsibility in the hands of the engineering team.
