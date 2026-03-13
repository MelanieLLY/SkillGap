# CI/CD & Security Technical Specifications

## 1. CI/CD Architecture
Our pipeline (defined in `.github/workflows/ci.yml`) ensures that every update preserves the integrity and quality of the SkillGap platform.

| Stage | Tooling | Requirement |
|---|---|---|
| **Code Quality** | Ruff, ESLint, Prettier | 100% Pass (No warnings) |
| **Testing** | Pytest-cov, Vitest | **80%+ Coverage required** |
| **Integrity** | GitHub Actions | Build artifacts verification |

## 2. Automated Deployment
The application utilizes a **Multi-Cloud Hybrid Deployment** strategy:
- **Backend Infrastructure:** High-availability deployment on **Render** (Docker-based).
- **Frontend Infrastructure:** Global CDN delivery via **Netlify**.
- **Preview Mechanism:** **Netlify Deploy Previews** are automatically generated for PR reviews, providing a live URL for functional verification.

## 3. Security Scanning Workflow
Strategic security practices are integrated into our SDLC (Software Development Life Cycle):
- **Logical Security (SAST):** Automated **CodeQL** engine scanning for SQL Injection, XSS, and logical flaws.
- **Dependency Security (SCA):** **Dependabot** continuous monitoring for all Python and NPM packages.
- **Compliance:** **Secret Scanning** prevents sensitive API keys (e.g., Anthropic API keys) from being committed to the codebase.
