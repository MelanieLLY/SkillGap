# SkillGap 测试汇总报告 (Other Info)

## 1. 项目基本信息
- **项目名称**: SkillGap
- **核心目标**: 职位描述 (JD) 技能提取、缺口分析及 AI 学习路线生成。

## 2. 技术栈详情

### 前端 (Frontend)
- **框架**: React 18 (SPA)
- **构建工具**: Vite
- **语言**: TypeScript (Strict Mode)
- **状态管理**: Zustand
- **样式**: Tailwind CSS
- **动画**: Framer Motion
- **网络请求**: Axios
- **测试框架**: **Vitest** + React Testing Library + @vitest/coverage-v8

### 后端 (Backend)
- **框架**: FastAPI (Python 3.11/3.12)
- **ORM**: SQLAlchemy
- **数据库**: PostgreSQL (生产), SQLite (测试)
- **校验**: Pydantic v2
- **AI 接口**: Anthropic Claude API (`claude-sonnet-4-20250514`)
- **测试框架**: **Pytest** + pytest-cov

## 3. 测试覆盖率概览 (Coverage Overview)

### 前端 (Frontend)
- **Framework**: `Vitest` + `React Testing Library`
- **Total Tests**: 84
- **Status**: ✅ All Passing (100% Pass)
- **Coverage**: **87.17% (Lines)**
- **Report**: [frontend_test_report.txt](frontend_test_report.txt)

### 后端 (Backend)
- **Framework**: `pytest`
- **Total Tests**: 116
- **Status**: ✅ All Passing (100% Pass)
- **Coverage**: **92%**
- **Report**: [backend_test_report.txt](backend_test_report.txt)

## 4. AI Eval 测试
- **评测功能**: 学习路线 (Roadmap) 生成质量。
- **评测指标**: Relevance (相关性), Specificity (专业性), Completeness (完整性)。
- **给分标准**: 1-5 分制 (由 Claude 3.5 Sonnet 作为 Judge 模型评分)。
- **评测报告**: 请查看 [docs/eval_roadmaps/ai_eval_results.md](../eval_roadmaps/ai_eval_results.md)
