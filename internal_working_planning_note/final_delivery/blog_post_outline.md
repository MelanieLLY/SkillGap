# Blog Post Outline: SkillGap - Developing an AI-Powered Career Assistant

## 1. Introduction: The Vision of SkillGap
*   **The Problem**: Job descriptions are often generic or overwhelming. Self-assessment is subjective and prone to error.
*   **The Solution**: An automated pipeline that links your profile to market demands and generates a custom learning path.
*   **Collaborative Approach**: A two-tier development strategy: Building a robust core (Jing) and enhancing it with intelligent AI agents (Liu yi).
*   **AI Modalities at a Glance**:
    *   **Claude Web (planning + artifacts)**: Jing used Claude Web for early planning and idea refinement; Liuyi used Claude Web to generate a wireframe based on handwritten drafts; Liuyi later used Claude Web to generate the eval webpage from real test results.
    *   **Antigravity (IDE-centric coding)**: Used throughout implementation to accelerate coding, refactoring, and feature delivery in both frontend and backend.

## 2. Part I: The Foundation - Building the Core Engine
*   **User Identity & Persistence**: Implementation of the JWT authentication system and the Skill Profile CRUD operations.
*   **Data Modeling**: Designing a scalable SQLAlchemy schema for users, skill profiles, and analysis history.
*   **Extraction Engine 1.0**: The technical implementation of the keyword extraction algorithm to identify skill gaps immediately.
*   **Visualization**: The design of the "Animated Match Ring" to provide instant visual feedback on candidate-job fit.
*   **Claude Web in Early Product Definition**: How Jing used Claude Web to turn initial project ideas into a clearer execution plan and prioritized implementation path.

## 3. Part II: The Brain - AI Integration & Engineering Excellence 
*   **Claude 3.5 Sonnet Integration**: Moving beyond keywords to meaningful career guidance. Generating the 12-week structured roadmap (JSON-to-UI).
*   **The TDD Paradigm**: Ensuring reliability of AI features. Sharing insights on writing tests for non-deterministic AI outputs.
*   **Security & Architecture**: Refactoring the backend to validate match scores, preventing client-side spoofing, and implementing global error handlers for database stability.
*   **UI/UX Wow-Factor**: Using `framer-motion` for staggered animations and Skeleton UI to handle AI latency.
*   **Wireframe-to-Implementation Workflow**: How Liuyi used Claude Web to convert handwritten wireframe drafts into a clear UI direction, then implemented the production version with Antigravity support inside the IDE.

## 4. Part III: Quality Assurance & AI Mastery 
*   **Advanced CI/CD**: A multi-stage GitHub Actions pipeline that enforces linting, security scans, and 80%+ test coverage.
*   **AI-as-a-Judge**: How we used Gemini/Claude to evaluate the roadmap's relevance and specificity, creating an "Eval Dashboard" for the project.
*   **Evaluation Artifact Generation**: How Liuyi used Claude Web with actual test outputs to generate the eval webpage artifact for documentation and grading evidence.

## 5. Conclusion: Reflecting on AI-Assisted Development
*   **Efficiency Gains**: How an AI-first development workflow (using Antigravity and Claude) accelerated the build time by 3x.
*   **Division of AI Roles**: Claude Web for planning/document artifacts and Antigravity for day-to-day coding execution made our process both faster and more traceable.
*   **Future Roadmap**: Discussing potential upgrades like Semantic Embeddings (Sentence Transformers) for better skill matching.
*   **Final Thoughts**: A reflection on team collaboration and the power of modular development.
