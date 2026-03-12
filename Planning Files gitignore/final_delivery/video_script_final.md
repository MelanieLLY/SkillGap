# SkillGap Final Video Script (10-Minute Collaborative Demo)

**Target Audience**: Global Public / Tech Community
**Total Duration**: ~10 Minutes
**Speakers**: Jing (Base Foundation & Core Logic) | Melanie (AI Integration & Engineering Quality)

---

## Part 0: Introduction (00:00 - 01:30)
**Speaker: Melanie**
*   **Visual**: Face cam + Product Landing Page.
*   **Speech**: "Hi everyone! I'm Melanie, and together with my teammate Jing, we built SkillGap. Searching for a job is tough—deciphering what skills you're actually missing is even tougher. Today, we'll show you how we used FastAPI, React, and Claude 3.5 to bridge that gap."
*   **Visual**: Quick 15-second "Wow-factor" demo. Paste JD -> Animated Ring -> Skeleton Loading -> Roadmap pops up.
*   **Speech**: "Our project is split into two halves: the robust data engine and the intelligent AI layer. Let's start with how we built the foundation with Jing."

---

## Part 1: Foundation & Core Logic (01:30 - 04:00)
**Speaker: Jing**
*   **Topic 1: Auth & Profile (01:30 - 02:30)**
    *   **Visual**: Screen recording of the Register/Login flow + User Profile skill selection.
    *   **Speech**: "Thanks, Melanie! I focused on the backbone of the app. I implemented the JWT authentication system to keep user profiles secure. Once logged in, users can manage their skill sets through our CRUD API, which persist their tech stack into a PostgreSQL database."
*   **Topic 2: Extraction Engine 1.0 (02:30 - 04:00)**
    *   **Visual**: Code snippet of the regex extraction algorithm + The Animated Match Ring spinning in the UI.
    *   **Speech**: "The heart of our first phase was the Keyword Extraction Engine. I built a parser that scans the Job Description against the user’s profile. This instantly calculates a match score and highlights what you have, what you're missing, and bonus skills. It provides the immediate feedback every job seeker needs."

---

## Part 2: AI Brain & Engineering Quality (04:00 - 08:00)
**Speaker: Melanie**
*   **Topic 1: Claude-Powered Roadmap (04:00 - 05:30)**
    *   **Visual**: `service.py` showing the System Prompt for Claude + The 12-week roadmap UI appearing with animations.
    *   **Speech**: "Building on Jing's engine, I integrated Claude 3.5 Sonnet to take us from analysis to action. We don't just tell you what's missing; we generate a custom 12-week roadmap. I designed a strict JSON-to-UI pipeline that translates AI insights into interactive milestones and course recommendations."
*   **Topic 2: TDD & Security (05:30 - 07:00)**
    *   **Visual**: Terminal running `pytest` showing 80%+ coverage + Code showing the backend match score validation.
    *   **Speech**: "To ensure project quality, I implemented a Test-Driven Development workflow. We maintained over 80% test coverage throughout development. I also hardened our security—for example, the match score is now calculated exclusively on the backend to prevent anyone from spoofing results through the API."
*   **Topic 3: CI/CD & UX Wow-Factor (07:00 - 08:00)**
    *   **Visual**: GitHub Actions pipeline interface + The shimmer effect of the Skeleton UI.
    *   **Speech**: "Finally, I set up a multi-stage CI/CD pipeline. Every PR is checked for linting, security, and coverage. And in the UI, I added framer-motion animations and skeleton loaders so users always feel a smooth, premium experience while waiting for the AI response."

---

## Part 3: Reflection & AI Mastery (08:00 - 10:00)
**Speaker: Melanie (08:00 - 09:00)**
*   **Visual**: AI Evaluation report (PDF or Markdown) showing scores for Relevance and Specificity.
*   **Speech**: "We didn't just trust the AI blindly. We built an 'AI-as-a-Judge' evaluation suite. We use another LLM to score our generated roadmaps based on teacher metrics. This automated feedback loop helped us refine our prompts to be more specific and actionable."

**Speaker: Both (09:00 - 10:00)**
*   **Visual**: Split screen with both faces.
*   **Jing**: "Reflecting on this journey, the biggest challenge was keeping the development decoupled while scaling the features."
*   **Melanie**: "And for me, it was managing the balance between AI innovation and strict engineering discipline. We hope SkillGap helps you land your next big role!"
*   **Both**: "Thanks for watching!"

---

## Recording Tips for Both:
1.  **Environment**: Use a clean background and decent lighting.
2.  **Audio**: Use a dedicated mic if possible; avoid echo.
3.  **B-Roll**: When talking about code, zoom in so it's readable. When talking about UI, show it in action.
4.  **Transitions**: Pause for 2 seconds at the end of each segment to make editing easier.
