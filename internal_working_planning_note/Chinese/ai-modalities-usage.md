## AI Modalities 使用说明（Claude Web + IDE Agent + 其它）

本项目在开发过程中刻意区分了几类 AI 工具（modalities）的角色与使用场景，以满足课程对 **AI Mastery** 的要求，同时在工程实践中保持可追踪性和可复现性。

---

## 1. 使用的 AI Modalities 一览

- **Claude Web（浏览器端对话）**
  - 用途：前期需求澄清、架构设计、Mermaid 图、文档草稿（PRD、Blog outline、Eval Dashboard 草稿等）。
  - 特点：上下文窗口大、适合长文和多轮讨论。

- **IDE 内置 AI Agent（Antigravity / Cursor 类工具）**
  - 用途：具体代码实现与重构、测试生成、CI 配置、Bug 定位与修复。
  - 特点：直接读取/修改仓库文件，适合「看代码 → 改代码 → 跑测试」的闭环。

- **评估型 LLM（Judge 模式）**
  - 用途：在 `server/tests/ai_eval.py` 中，对 Claude 生成的学习路线做自动化质量评估。
  - 特点：以「评分员」身份出现，严格按照 rubric 输出 Relevance / Specificity / Completeness 等指标。

---

## 2. 在项目生命周期中的分工

### 2.1 规划与产品阶段（Planning / PRD / Roadmap）

- 使用 **Claude Web**：
  - 共同编写 `docs/skillgap_prd.md` 和 `internal_working_planning_note/PROJECT2_MASTER_PLAN.md`。  
  - 让模型根据课程 rubric 列出所有必需的 deliverables（API docs、Scrum docs、AI reflections、blog、video 等）。  
  - 生成初版的 Sprint 1/2 Issue 列表与时间预估。

- 人工 + Claude Web：
  - 对生成的计划进行人工审查与删改，只保留可执行、可验证的步骤。  
  - 将最终版本固化进 `PROJECT2_MASTER_PLAN.md`，作为 IDE 侧 Agent 的「工作说明书」。

### 2.2 开发与实现阶段（Coding / Refactor / Tests）

- 使用 **IDE Agent（Antigravity/Cursor）**：
  - 针对具体文件发起「局部任务」，例如：
    - 「在 `auth/router.py` 中为 `db.commit()` 增加事务与错误处理」。
    - 「为 `extraction/engine.py` 写 Pytest 单元测试，覆盖正负样例」。
    - 「补全 `LearningRoadmap.tsx` 的加载骨架屏和动画」。
  - 通过工具自动编辑代码、运行测试、修复 lint 错误。

- 人工把关：
  - 对每次大改动进行人工 code review（配合 Git diff 和测试结果）。  
  - 对安全相关逻辑（JWT、数据库操作）保持人工审核和最终决策。

### 2.3 AI Eval 与质量监控阶段

- 使用 **评估型 LLM（Judge 模式）**：
  - 在 `server/tests/ai_eval.py` 中，先调用 Claude 生成学习路线，再调用第二个模型打分。  
  - 将评分与点评写入 `docs/eval_roadmaps/ai_eval_results.md` 和 Eval Dashboard。

- 人工 spot check：
  - 对评分最高和最低的若干条路线进行人工阅读，对照 rubric 进行 sanity check。  
  - 若发现模型评分与人类直觉不符，会调整 Prompt 或评分说明。

---

## 3. 典型工作流示例

### 3.1 从需求到代码的完整闭环

1. **Claude Web – 需求澄清与拆解**
   - 让 Claude Web 阅读 `P2 requirement.md` 和课程 rubric，生成项目整体路线与分 Sprint 计划。
   - 输出整理到 `PROJECT2_MASTER_PLAN.md`，作为后续所有工作的「总蓝图」。

2. **IDE Agent – 具体实现与测试**
   - 以单个 Issue 为单位，在 IDE 里调用 Agent：
     - 例如：「根据 PRD 和 plan，为 `/api/roadmap/generate` 实现 Claude 集成，并编写对应测试」。
   - Agent 完成代码修改后，自动运行 `pytest` / Vitest，并修复报错。

3. **评估与迭代**
   - 用 AI Eval 脚本批量生成学习路线并打分。  
   - 若发现某些场景表现不佳，再回到 Claude Web 或 IDE Agent 调整 Prompt 或数据结构。

### 3.2 文档与 Demo 产出

- **Claude Web**：
  - 帮助草拟 Blog outline（`internal_working_planning_note/final_delivery/blog_post_outline.md`）。  
  - 协助写 Eval Dashboard 文本描述（后在 `docs/skillgap_eval_dashboard.html` 中落地）。

- **IDE Agent**：
  - 协助生成 README/CI 配置片段和部分文档骨架（如本文件、API docs、code-architecture 等）。  
  - 直接写入仓库，方便后续人工润色。

---

## 4. 使用原则与边界（Do / Don’t）

### 4.1 使用原则（Do）

- **始终保持「AI 为助手」而不是「黑箱决策者」**：
  - 所有安全相关与架构性决策都要有人工复核。  
  - 对每个重要改动，至少阅读一次关键代码和测试。

- **将 AI 输出转化为可审查的 artifact**：
  - PRD / Plan → `docs/skillgap_prd.md`、`PROJECT2_MASTER_PLAN.md`。  
  - 代码修改 → Git commits + Pull Requests。  
  - Eval 结果 → `docs/eval_roadmaps/ai_eval_results.md`、Eval Dashboard。

- **让不同 modality 扮演不同角色**：
  - Claude Web：大局规划、长文档、思维导图。  
  - IDE Agent：局部重构、单元测试、Bug 修复。  
  - Judge LLM：路线质量评估。

### 4.2 避免的用法（Don’t）

- 不把「AI 自动生成的大块代码」直接合并进 main，而不跑测试或人工 review。  
- 不把敏感信息（真实密码、生产密钥）直接贴入 Claude Web 或公共对话。  
- 不在不解释的前提下「盲从」评估类 LLM 的评分，而是用其作为信号之一。

---

## 5. 总结：如何在本项目中有效使用多种 AI 模态

在 SkillGap 项目中，我们采用了「**计划 → 实现 → 评估**」三环闭环：

- 用 **Claude Web** 和长对话来制定计划与文档，把课程要求翻译成可执行的工程路线。
- 用 **IDE 内的 AI Agent** 完成大量重复和机械的编码工作（重构、测试、CI 配置），并在本地持续运行测试。
- 用 **评估型 LLM** 为 Claude 输出的学习路线打分，再由人类进行 spot check 和汇总，形成 Eval Dashboard 与本项目的 AI Mastery 证据。

这种分工既充分利用了不同 AI 工具的优势，又把关键控制权和最终质量责任保留在人类工程师手中。

