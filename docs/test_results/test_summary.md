# SkillGap Test Summary Report

## 1. Project Overview
- **Project Name**: SkillGap
- **Core Objective**: Job description (JD) skill extraction, skill gap analysis, and AI-powered learning roadmap generation.

## 2. Tech Stack Details

### Frontend
- **Framework**: React 18 (SPA)
- **Build Tool**: Vite
- **Language**: TypeScript (Strict Mode)
- **State Management**: Zustand
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **HTTP Client**: Axios
- **Test Framework**: **Vitest** + React Testing Library + @vitest/coverage-v8

### Backend
- **Framework**: FastAPI (Python 3.11/3.12)
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL (production), SQLite (testing)
- **Validation**: Pydantic v2
- **AI Interface**: Anthropic Claude API (`claude-sonnet-4-20250514`)
- **Test Framework**: **Pytest** + pytest-cov

## 3. Test Coverage Overview

### Frontend
- **Framework**: `Vitest` + `React Testing Library`
- **Total Tests**: 84
- **Status**: ✅ All Passing (100% Pass)
- **Coverage**: **87.17% (Lines)**
- **Report**: [frontend_test_report.txt](frontend_test_report.txt)

### Backend
- **Framework**: `pytest`
- **Total Tests**: 116
- **Status**: ✅ All Passing (100% Pass)
- **Coverage**: **97%**
- **Report**: [backend_test_report.txt](backend_test_report.txt)

## 4. AI Eval Tests
- **Evaluated Feature**: Learning roadmap generation quality.
- **Evaluation Metrics**: Relevance, Specificity, Completeness.
- **Scoring Scale**: 1–5 (scored by Claude 3.5 Sonnet acting as the Judge model).
- **Evaluation Report**: See [docs/eval_roadmaps/ai_eval_results.md](../eval_roadmaps/ai_eval_results.md)
