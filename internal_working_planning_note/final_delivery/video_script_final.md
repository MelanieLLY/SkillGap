# SkillGap Final Video Script (Balanced 10-Minute Version)

**Target Audience**: General public / future employers / teaching team  
**Goal**: Show not only what SkillGap does, but how we built it, how we used AI, how we collaborated, and why it meets the Project 2 deliverables.  
**Total Duration**: 10:00  
**Speakers**: Jing and Liuyi  
**Time Balance**: Jing ~5:00, Liuyi ~5:00

## Recording Plan

**Plan A: Record separately + use shared Google Slides**
- We’ll first create a shared Google Slides deck and organize the visuals each of us needs for our own sections.- Each of us records our own on-camera parts on phone (landscape is easiest for editing).
- Each person adds visuals for their own section (screenshots + short screen recordings/GIFs).
- In editing, we follow the script timeline and move through slides as the visual guide.
- To make sure both members clearly appear on camera, we add a short joint ending shot.

**Plan B: Record together on Zoom**
- We can also do one Zoom recording session together.
- We keep cameras on, screen-share slides/product walkthrough, and take turns by section.
- We keep the speaking ownership clear for each section and stay close to the 10-minute target.
- We still include a short ending moment with both teammates on camera.


---

## Delivery Notes

- Speak at a natural pace: about 115 to 130 words per minute.
- Keep face cam on for intros, transitions, collaboration, and closing.
- Use screen recording for product flow, code, tests, CI, and documentation evidence.
- Do not read too fast. It is better to sound clear than perfect.

---

## Part 0: Hook and Summary (00:00 - 00:40)
**Speaker: Jing**

**Visual**
- Face cam for 5 seconds.
- Cut to landing page.
- Quick montage: paste a job description, see the match ring animate, then show the roadmap loading.

**Script**
"Hi everyone, I'm Jing, and this is SkillGap, the full-stack app my teammate Liuyi and I built for Project 2. SkillGap helps job seekers compare their current skills against a job description, understand what they are missing, and turn that gap into a realistic learning roadmap. In this video, we'll walk through the product, explain how we built it, show how AI supported our development process, and reflect on how we worked together as a team."

---

## Part 1: Problem, User Flow, and What the App Does (00:40 - 01:20)
**Speaker: Liuyi**

**Visual**
- Face cam in corner.
- Product home page.
- Simple slide or overlay with three steps:
  1. Build profile
  2. Paste job description
  3. Get gap analysis and roadmap

**Script**
"I'm Liuyi. The problem we wanted to solve is simple: job descriptions are long, inconsistent, and difficult to translate into an actual study plan. So we designed SkillGap around a clear user journey. First, users create an account and save their existing skills. Second, they paste a target job description. Third, the system analyzes the gap and generates both instant feedback and a structured roadmap. That means the product is not just informative, but actionable."

---

## Part 2: Walkthrough of the Core Product Experience (01:20 - 02:40)
**Speaker: Jing**

**Visual**
- Register or login flow.
- Profile page with skill CRUD interactions.
- Paste JD into dashboard.
- Match score ring, extracted skills, missing skills, history list.

**Script**
"Let me show the core walkthrough. Users start with authentication, so each person has a secure account and their own saved data. After logging in, they manage their technical profile by adding or removing skills. That profile is stored persistently in our database and becomes the baseline for analysis. On the dashboard, the user pastes a job description, and our extraction engine identifies matched skills, missing skills, and bonus skills. We also visualize the result with an animated match score ring, and we save analysis history so users can come back and compare multiple job targets over time. This gives users immediate product value before the AI roadmap even begins."

---

## Part 3: AI Roadmap and Frontend Experience (02:40 - 04:00)
**Speaker: Liuyi**

**Visual**
- Dashboard transitions from analysis result to roadmap generation.
- Skeleton loading state.
- Final roadmap UI with milestones, weeks, and recommendations.
- Brief code zoom on Claude service or prompt-to-JSON flow.

**Script**
"Once the gap is identified, my part of the system takes the user from diagnosis to action. I integrated Claude to generate a personalized learning roadmap based on the missing skills from the analysis stage. Instead of returning a loose paragraph of AI text, we designed a structured pipeline so the model returns consistent data that the frontend can render into milestones, weekly goals, and learning recommendations. On the user experience side, I also added skeleton loading states and animation polish, because AI responses take time and we wanted the interface to feel smooth, responsive, and professional rather than frozen or confusing."

---

## Part 4: How We Built the Foundation (04:00 - 05:20)
**Speaker: Jing**

**Visual**
- Architecture slide: React frontend, FastAPI backend, PostgreSQL database, Claude integration.
- Brief API or backend code snippets.
- Database model or endpoint list.

**Script**
"Behind the interface, the project is a full-stack system. We used React on the frontend, FastAPI on the backend, and PostgreSQL for persistence. I focused heavily on the application foundation: JWT-based authentication, skill profile CRUD, analysis history, and the first version of the extraction logic. A key design goal was to keep the product modular. The rule-based analysis layer gives fast, deterministic feedback, while the AI layer builds on top of that result instead of replacing it. That separation made the product easier to reason about, easier to debug, and easier for us to divide between teammates."

---

## Part 5: AI Techniques, Evaluation, and Why It Was More Than Prompting (05:20 - 06:40)
**Speaker: Liuyi**

**Visual**
- Prompt snippet or system prompt section.
- JSON response example.
- AI evaluation report or eval dashboard.
- Maybe show teacher-facing deliverables folder briefly.

**Script**
"One important thing we learned is that building an AI-assisted application is not just about calling a model API. The hard part is designing the system around reliability. I worked on prompt structure, response formatting, error handling, and evaluation. We also built an AI evaluation workflow to judge whether the generated roadmap was relevant, specific, and useful. That helped us iterate on prompts with evidence instead of intuition. In other words, we treated the LLM like one component in an engineered system, not like a magic black box."

---

## Part 6: Development Challenges and How We Solved Them (06:40 - 07:40)
**Speaker: Jing**

**Visual**
- Split screen of issue -> fix.
- Show history feature, extraction results, or architecture diagram.
- Optional short text overlay: "challenge: consistency", "challenge: separation", "challenge: persistence"

**Script**
"Our biggest development challenge was connecting fast rule-based analysis with a more flexible AI-generated roadmap without making the system fragile. We needed the extraction results to be accurate enough to support downstream AI output, and we needed persistence so users could trust the app over repeated sessions. Another challenge was dividing work cleanly as a team. We solved that by keeping clear boundaries: I concentrated on the core backend flows and data foundation, while Liuyi extended those stable outputs into roadmap generation, testing, and delivery quality."

---

## Part 7: Engineering Quality, Security, and CI/CD (07:40 - 08:40)
**Speaker: Liuyi**

**Visual**
- Terminal with tests running.
- Coverage summary.
- GitHub Actions workflow.
- Code snippet showing backend validation or match-score logic.

**Script**
"We also wanted this project to meet the professional engineering side of the rubric, not just the demo side. So I invested heavily in testing, CI, and security-related improvements. We built automated tests, tracked coverage, and prepared evaluation evidence rather than relying on screenshots alone. We also moved sensitive logic like match score calculation to the backend so results could not simply be spoofed from the client. Finally, we set up CI checks so changes were validated continuously. That helped us keep shipping quickly without losing confidence in the codebase."

---

## Part 8: How We Used AI and How We Collaborated (08:40 - 09:30)
**Speaker: Jing, then Liuyi**

**Visual**
- Jing speaks on camera first.
- Then cut to Liuyi on camera.
- Overlay commit history, branches, tests, docs, or planning artifacts while each person speaks.

**Jing Script**
"In terms of AI usage, we did not use it in a single way. We used AI to speed up planning, implementation support, debugging, and documentation drafting, but we still validated the outputs ourselves and adapted them to the actual system."

**Liuyi Script**
"For collaboration, we used our commit history and feature boundaries to make responsibilities visible. Jing led major backend foundations like auth, profile CRUD, extraction, and history. I focused on roadmap generation, testing, CI/CD, frontend polish, and system hardening. That division let us move quickly while still integrating into one coherent product."

---

## Part 9: Deliverables, Reflection, and Closing (09:30 - 10:00)
**Speaker: Liuyi, then Jing**

**Visual**
- Final product page.
- Brief montage of README, API docs, eval dashboard, blog/video folder, and deployed app.
- End on Liuyi's face cam, then cut to Jing's face cam, or end on the project logo.

**Liuyi Script**
"So beyond the app itself, this project also includes the major deliverables required for Project 2: a deployed full-stack product, documentation, testing evidence, and a clear record of AI-assisted development."

**Jing Script**
"More importantly, SkillGap shows that we can build an AI-assisted application with both product value and engineering discipline. Thanks for watching."

---

## Quick Recording Checklist

1. Keep each section close to its assigned time. Do one dry run with a timer.
2. When showing code, zoom in and only show the part you are actively talking about.
3. When showing UI, keep the mouse movement slow and deliberate.
4. Leave a 1 to 2 second pause between sections to make editing easier.
5. If a line sounds too formal while recording, simplify it live. Natural delivery is better than perfect wording.
