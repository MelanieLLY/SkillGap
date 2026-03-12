# Blog Post Outline: SkillGap - Developing an AI-Powered Career Assistant

## 1. Introduction: The Vision of SkillGap
*   **The Problem**: Job descriptions are often generic or overwhelming. Self-assessment is subjective and prone to error.
*   **The Solution**: An automated pipeline that links your profile to market demands and generates a custom learning path.
*   **Collaborative Approach**: A two-tier development strategy: Building a robust core (Jing) and enhancing it with intelligent AI agents (Melanie).

## 2. Part I: The Foundation - Building the Core Engine (Jing's Contribution)
*   **User Identity & Persistence**: Implementation of the JWT authentication system and the Skill Profile CRUD operations.
*   **Data Modeling**: Designing a scalable SQLAlchemy schema for users, skill profiles, and analysis history.
*   **Extraction Engine 1.0**: The technical implementation of the keyword extraction algorithm to identify skill gaps immediately.
*   **Visualization**: The design of the "Animated Match Ring" to provide instant visual feedback on candidate-job fit.

## 3. Part II: The Brain - AI Integration & Engineering Excellence (Melanie's Contribution)
*   **Claude 3.5 Sonnet Integration**: Moving beyond keywords to meaningful career guidance. Generating the 12-week structured roadmap (JSON-to-UI).
*   **The TDD Paradigm**: Ensuring reliability of AI features. Sharing insights on writing tests for non-deterministic AI outputs.
*   **Security & Architecture**: Refactoring the backend to validate match scores, preventing client-side spoofing, and implementing global error handlers for database stability.
*   **UI/UX Wow-Factor**: Using `framer-motion` for staggered animations and Skeleton UI to handle AI latency.

## 4. Part III: Quality Assurance & AI Mastery (Melanie's Contribution)
*   **Advanced CI/CD**: A multi-stage GitHub Actions pipeline that enforces linting, security scans, and 80%+ test coverage.
*   **AI-as-a-Judge**: How we used Gemini/Claude to evaluate the roadmap's relevance and specificity, creating an "Eval Dashboard" for the project.

## 5. Conclusion: Reflecting on AI-Assisted Development
*   **Efficiency Gains**: How an AI-first development workflow (using Antigravity and Claude) accelerated the build time by 3x.
*   **Future Roadmap**: Discussing potential upgrades like Semantic Embeddings (Sentence Transformers) for better skill matching.
*   **Final Thoughts**: A reflection on team collaboration and the power of modular development.
