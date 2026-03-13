## AI Reflections (Project-Level)

This document reflects on how we used multiple AI modalities throughout the project: where they added the most value, what limitations we encountered and how we resolved them, and what we would do differently next time.

---

## 1. The Human + AI Collaboration Model

In SkillGap, we intentionally positioned AI as a "senior assistant" rather than an autonomous decision-maker:

- During the **requirements and planning phase**, AI helped us quickly reverse-engineer the PRD, Sprint plans, and deliverables checklist from the course rubric.
- During the **coding and testing phase**, AI primarily handled high-intensity, repetitive work: generating boilerplate, filling out tests, running CI, and suggesting fixes.
- During the **evaluation and documentation phase**, we used LLMs as reviewers to analyze roadmap quality and organize written materials.

The overall experience: AI dramatically accelerated the production of initial drafts, but deciding *which approach to adopt and how to execute it* still required deliberate human judgment at every stage.

---

## 2. AI Performance Across Three Key Scenarios

### 2.1 Architecture Design & Planning (Claude Web)

**How we used it**:

- Had Claude Web read course requirements and initial ideas, producing `docs/skillgap_prd.md` and `internal_working_planning_note/PROJECT2_MASTER_PLAN.md`.
- Asked it to decompose all grading criteria (CI, AI Mastery, Scrum, Documentation) into actionable tasks organized by Sprint.

**Assessment**:

- **Strengths**:
  - Significantly reduced the time spent cross-referencing requirements and manually building checklists.
  - The generated plan was detailed enough (with time estimates, recommended tools, and suggested prompts) that execution could proceed almost directly from it.
- **Limitations**:
  - Occasionally produced overly ambitious plans that exceeded available time budgets (e.g., proposing complex CI/CD setups from day one).
  - The model had no awareness of the team's actual familiarity with certain tools, requiring manual pruning and reprioritization.

**Reflection**:

- We will continue using Claude Web for "first-draft planning," but will perform a deliberate scoping pass before finalizing:
  - Retain only items strongly tied to rubric scoring criteria.
  - Move "nice-to-have" items into a Stretch Goals section to protect the critical path.

### 2.2 Code Implementation & Refactoring (IDE Agent)

**How we used it**:

- Invoked the Agent directly in the IDE to make targeted changes to real project files:
  - Added type annotations and docstrings to FastAPI routes.
  - Wrapped database writes in `auth/profile/history` with transactions and exception handling.
  - Generated Pytest tests in `server/tests/`.
  - Configured repetitive YAML files like `.github/workflows/ci.yml`.

**Assessment**:

- **Strengths**:
  - Extremely efficient in the "read → change → test" micro-loop, well-suited for iterative refactoring.
  - Produced reasonably idiomatic implementations (PEP 8, type annotations, security recommendations) when given a project rules file.
- **Limitations & How We Addressed Them**:
  - Occasionally introduced minor regressions due to incomplete context (e.g., incorrect assumptions about test database configuration). These were caught immediately by the test suite and corrected in follow-up iterations.
  - For large cross-file refactors, requesting too much in a single session risked missing edge cases. We addressed this by breaking work into small, focused batches with explicit scope boundaries.

**Reflection**:

- The best approach is to scope each IDE Agent session to **one specific objective** — e.g., "only update the security logic in `history/router.py`" or "only write tests for the Roadmap module" — rather than asking for a half-project refactor at once.
- For changes touching critical paths (authentication, security, database), human code review combined with test coverage is non-negotiable and should not rely solely on the AI's self-verification.

### 2.3 AI Eval & Quality Assessment (Judge Model)

**How we used it**:

- In `server/tests/ai_eval.py`, a second LLM acted as a "reviewer" evaluating Claude-generated learning roadmaps across Relevance / Specificity / Completeness.
- Results were aggregated into `docs/eval_roadmaps/ai_eval_results.md` and the Eval Dashboard as AI Mastery evidence.

**Assessment**:

- **Strengths**:
  - Enabled systematic, rubric-based scoring of multiple roadmaps within limited time, without reading each one manually.
  - Surfaced pattern-level issues in prompt design (e.g., over-expanding bonus skills leading to bloated roadmaps).
- **Limitations**:
  - Fundamentally "AI evaluating AI" — poorly designed prompts could produce inflated scores.
  - Some high-scoring roadmaps, when read by a human, still felt slightly repetitive.

**Reflection**:

- AI Eval works best as a **first-pass filtering tool**, not a replacement for human judgment.
- In future projects, we would plan ahead for a small number of real users or peers to provide usability feedback, incorporating "human scoring" as an additional signal in the Eval Dashboard.

---

## 3. Overall Assessment of Multi-Modal Collaboration

Across all three modalities, the collaboration delivered measurable gains in two dimensions:

- **Speed and coverage**:
  - Delivering the same scope of PRD + documentation + tests + Eval entirely by hand would have been infeasible within the course timeline.
  - With AI, we completed both the functional requirements and comprehensive documentation and quality evidence within budget.

- **Quality and maintainability**:
  - AI contributed meaningfully to type annotations, docstrings, and test coverage, making the codebase more readable and extensible.
  - The Eval Suite gave us a quantitative signal on AI-generated content quality, replacing purely subjective "looks fine" assessments.

We also maintained a clear-eyed view of the boundaries:

- AI cannot automatically determine the optimal trade-off under a specific course grading rubric — that requires human judgment.
- When faced with incomplete context or ambiguous requirements, AI tends to produce solutions that are plausible but not fully tailored to the project. These cases were caught through human review and iterative correction.

---

## 4. What We Would Do Differently Next Time

1. **Document prompts and decision rationale earlier and more systematically**
   - Many high-quality conversations from this project were only partially preserved in notes and chat history.
   - Maintaining a dedicated `ai_prompt_logs.md` / `ai-decisions.md` from the start would significantly reduce the effort of writing AI reflections, blog posts, or presentations later.

2. **Explicitly budget time for human review of AI output during planning**
   - We would insert one or two time-boxed "human review of AI output" sessions into the project plan — for example, reading 5 roadmaps and performing a sanity check on the Eval Dashboard.

3. **Design the Mock strategy as a first-class architectural choice from day one**
   - This project adopted an iterative Mock strategy for the Claude API — introduced deliberately as our CI and offline testing pattern matured — rather than treating real API calls as the only path.
   - Going forward, we would define both "live API" and "mock" execution paths from the outset, defaulting to mock in CI to eliminate external API dependencies and make test runs fully deterministic.

---

## 5. Conclusion: AI's Role in This Project

In SkillGap, AI functioned as a **fast, senior Pair Programmer + documentation assistant + QA aide**:

- It produced initial implementations, tests, and documentation with remarkable speed.
- It helped interpret error logs and surface potential architectural issues.
- It enabled us to assess the quality of our own AI-generated features against a consistent rubric.

But it was **not**:

- The project owner — scope, trade-offs, and final quality were always human responsibilities.
- The single source of truth — every AI recommendation was validated against tests, documentation, and engineering experience before being adopted.

This reflection was itself completed with AI assistance, but the core judgments and trade-off decisions came from real experience accumulated across the full development cycle. We consider this a successful demonstration of how to use AI professionally in an engineering project.
