# AI Chat History - 02_0311_11am_EnvSetupAndPostgresMigration

**Date:** 2026-03-11
**Time:** 11:50 AM
**Focus:** Project Run, Environment Fix, and PostgreSQL Migration

---

## 摘要
本对话主要解决了 SkillGap 项目在本地运行环境的搭建问题。包括修复了 Python 命令兼容性（Mac 系统的 python3）、解决了 CSS 导入顺序导致的 Vite 报错，并将本地数据库从不一致的 SQLite 成功迁移到了 Render 托管的云端 PostgreSQL 数据库。此外，重构了自动化测试脚本以支持真实数据库连接，并创建了初始测试数据。

---

## 对话详情

### 1. 项目运行初探
**USER**: 请你阅读项目,告诉我要怎么run?这个项目是前后端写到一起的。
**AI**: 识别出项目为 FastAPI + React/Vite 架构。提供了 `npm run install:all` 和 `npm run dev` 指令，并解释了目录结构（`/client` 和 `/server`）。

### 2. 环境修复 (Python3 & CSS)
**USER**: `npm run install:all` 报错 `python: command not found`。
**AI**: 
- 发现 Mac 系统下应使用 `python3` 替代 `python`。
- 修改了 `package.json` 中的脚本命令。
- 修复了 `client/src/index.css` 中 `@tailwind` 和 `@import` 顺序冲突导致的 Vite 报错。

### 3. 数据库一致性问题与方案
**USER**: 注册真的链接了什么数据库吗？
**AI**: 分析代码发现项目代码使用了 PostgreSQL 特性（ARRAY 类型），但本地配置指向 localhost。
**USER**: 帮我跑一两个测试。
**AI**: 测试通过是因为原本的测试脚本使用了 SQLite 内存数据库。
**USER**: 为什么上一个版本可以，现在不行？
**AI**: 解释了“测试用 SQLite，运行用 Postgres”的不合理现状。之前的版本可能后端根本没起起来，或者环境配置不一致。

### 4. 迁移至 Render PostgreSQL
**USER**: 决定使用 Render 云端数据库。提供了连接字符串：`postgresql://skillgap_db_snas_user:***@***.render.com/skillgap_db_snas`。
**AI**: 
- 创建了 `server/.env.example` 模版。
- 完成了 `server/.env` 的配置。
- 修改了 `server/core/config.py`，支持基于 Pydantic 的环境变量加载。

### 5. 测试重构与数据初始化
**USER**: 要求修改测试文件以符合 PostgreSQL 环境。
**AI**: 
- 重构了 `server/tests/test_auth.py`，移除 SQLite 补丁，直接连接真实数据库。
- 引入了随机邮箱机制，确保测试可重复运行而不冲突。
- 运行脚本在云端数据库创建了测试账号：
    - `alice@example.com` / `password123`
    - `bob@example.com` / `password456`

---

## 待办事项 (TODOs)
- [ ] 按照 `PROJECT2_MASTER_PLAN.md` 中的 Step 0.4 修复数据库写入的容错处理 (Rollbacks)。
- [ ] 按照 Step 0.5 修复信任客户端传递 `match_score` 的安全漏洞。
- [ ] 按照 Step 0.7 彻底将同步 API 重构为异步 (AsyncSession)。
