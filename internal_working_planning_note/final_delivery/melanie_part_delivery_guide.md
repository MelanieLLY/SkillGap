# Liuyi Part 视频交付指南

本文档仅针对 **Liuyi** 的台词与画面，帮助你在录制时：  
1. 使用优化后的台词（准确、长度合适、用词简单，并已根据 commit/Issue 记录更新）  
2. 在正确停顿处切换画面，素材均使用可点击的超链接  
3. 展示素材已精简，确保每句话 1-2 个画面，跳转节奏适中。

**时间参考**：自然语速约 115–130 词/分钟；每段录前用计时器试讲一遍。  
**画面原则**：展示代码时只放大你正在讲的那一小段；展示 UI 时鼠标移动慢而稳。

**关于链接**：  
- 所有素材链接已替换为相对路径 `../screenshot_during_dev/`，修复了路径层级和空格导致的跳转问题。  
- [已部署前端](https://skillgapweb.netlify.app)：由于路由保护，请先访问首页并登录，再根据提示操作。  
- [skillgap_eval_dashboard.html](../../docs/skillgap_eval_dashboard.html)：在浏览器中看排版效果，请右键该文件 → Reveal in Finder，再用浏览器打开。

---

## 全片大纲（含队友 Part，便于你对齐节奏）

| 时间段 | Part | Speaker | 标题 |
|--------|------|---------|------|
| 00:00–00:40 | Part 0 | **Jing** | 开场钩子与项目概述 |
| 00:40–01:20 | Part 1 | **Liuyi** | 问题背景、用户流程与产品作用 |
| 01:20–02:40 | Part 2 | **Jing** | 核心产品体验 Walkthrough |
| 02:40–04:00 | Part 3 | **Liuyi** | AI 路线图与前端体验 |
| 04:00–05:20 | Part 4 | **Jing** | 我们是如何搭建项目基础的 |
| 05:20–06:40 | Part 5 | **Liuyi** | AI 技术、评估方式，以及为什么这不只是「调 prompt」 |
| 06:40–07:40 | Part 6 | **Jing** | 开发过程中的挑战，以及我们如何解决 |
| 07:40–08:40 | Part 7 | **Liuyi** | 工程质量、安全性与 CI/CD |
| 08:40–09:30 | Part 8 | **Jing → Liuyi** | 我们如何使用 AI，以及我们如何协作 |
| 09:30–10:00 | Part 9 | **Liuyi → Jing** | Deliverables、反思与结尾 |

---

## Part 0：Jing Part - 跳过
(00:00 - 00:40) 开场钩子与项目概述

---

## Part 1：问题背景、用户流程与产品作用（00:40 - 01:20）  
**时长约 40 秒**

### 优化后的台词（中文）
「我是 Liuyi。我们想解决的问题很简单：岗位描述通常很长、信息杂，而且很难直接变成一份真正能执行的学习计划。所以我们把 SkillGap 设计成一条清晰的用户流程。第一步，用户注册账号并保存自己已有的技能。第二步，用户粘贴目标岗位的 job description。第三步，系统分析技能差距，并给出即时反馈和一份结构化的学习路线图。也就是说，产品不仅告诉用户缺什么，还告诉用户下一步该怎么做。」

### 画面与停顿

| 顺序 | Pause at this line (English) | 画面切换方案 | 素材链接 |
|------|-------------------------------|--------------|----------|
| 1 | I'm Liuyi. | **Screen 1**: 人像镜头 | 摄像头 |
| 2 | The problem we wanted to solve is simple: job descriptions are long, inconsistent, and difficult to translate into an actual study plan. | **Screen 1**: 产品首页 | [不share截图：User Journey Slide](../screenshot_during_dev/SkillGap_User_Journey.png) |
| 3 | So we designed SkillGap around a clear user journey. | **Screen 1**: User Journey 核心流程图 | [截图：User Journey Slide](../screenshot_during_dev/SkillGap_User_Journey.png) |
| 4 | First, users create an account and save their existing skills. | **Screen 1**: Profile 技能列表 (Live 展示) | [截图：User Journey Slide](../screenshot_during_dev/SkillGap_User_Journey.png) |
| 5 | Second, they paste a target job description. | **Screen 1**: Dashboard 粘贴 JD (Live 展示) | [截图：User Journey Slide](../screenshot_during_dev/SkillGap_User_Journey.png) |
| 6 | Third, the system analyzes the gap and generates feedback and a structured roadmap. That means the product is not just informative, but actionable. | **Screen 1**: 技能匹配结果与路线图入口 (Live 展示) | [截图：User Journey Slide](../screenshot_during_dev/SkillGap_User_Journey.png) |

---

## Part 2：Jing Part - 跳过
(01:20 - 02:40) 核心产品体验 Walkthrough

---

## Part 3：AI 路线图与前端体验（02:40 - 04:00）  
**时长约 1 分 20 秒**

### 优化后的台词（中文）
「当技能差距被分析出来之后，我负责的部分会把结果从「诊断」推进到「行动」。我接入了 Claude，根据分析阶段得到的缺失技能，为用户生成一份个性化的学习路线图。我们不是简单返回一大段 AI 文字，而是设计了一条结构化的数据流：让模型输出固定格式的数据，再由前端把它渲染成阶段、每周目标和学习建议。在体验上，我还加了 skeleton 加载和动效，因为 AI 需要时间响应，我们希望等待时界面依然流畅、专业，而不是卡住或让用户困惑。」
 
### 画面与停顿
## 不用切换屏幕
| 顺序 | Pause at this line (English) | 画面切换方案 | 素材链接 |
|------|-------------------------------|--------------|----------|
| 1 | Once the gap is identified,the system takes the user from diagnosis to action. | **Screen 1**: 技能匹配三栏结果 (复习诊断)<br>**Screen 2**: 点击「生成路线图」按钮 | [截图：技能匹配_现有_缺失_bonus](../screenshot_during_dev/SkillGap_仪表盘_技能匹配12_现有_缺失_bonus三栏目.png) <br> [已部署 App](https://skillgapweb.netlify.app) |
| 2 | I integrated Claude to generate a personalized learning roadmap based on the missing skills from the analysis stage. | **Screen 1**: Skeleton 加载态 |[RoadmapSkeleton 组件](../../client/src/components/RoadmapSkeleton.tsx) |
| 3 | Instead of returning a loose paragraph of AI text, we designed a structured pipeline so the model returns consistent data that the frontend can render into milestones, weekly goals, and learning recommendations. | **Screen 1**: 路线图完整 UI 展示 <br> **Screen 2**: 仪表盘+职位描述+路线图全景 | [截图：仪表盘_路线图](../screenshot_during_dev/SkillGap_仪表盘_技能职位描述_学习路线图_2026-03-11_16.34.57.png) <br> [截图：仪表盘_职位描述_路线图](../screenshot_during_dev/SkillGap_仪表盘_技能职位描述_学习路线图_2026-03-11_16.34.57.png) |
| 4 | On the user experience side, I also added skeleton loading states and animation polish, because AI responses take time and we wanted the interface to feel smooth and responsive rather than frozen. |生成路线的按钮点一下 |[已部署 App](https://skillgapweb.netlify.app) |

---

## Part 4：Jing Part - 跳过
(04:00 - 05:20) 项目基础搭建

---

## Part 5：AI 技术、评估方式，以及为什么这不只是「调 prompt」（05:20 - 06:40）  
**时长约 1 分 20 秒**

### 优化后的台词（中文）
「我们学到很重要的一点是：做一个 AI 应用，远不止「调一个模型 API」那么简单。难的是围绕「可靠性」来设计整个系统。我主要负责 prompt 结构、返回格式、错误处理，以及评估流程。我们还做了一套 AI 评估流程（对应 Issue #9），用同一套模型对多份真实 JD 生成的路线图打分，判断是否足够相关、具体、有用。这样我们改 prompt 的时候，是有依据地迭代，而不是凭感觉。换句话说，我们把大模型当作工程系统里的一个组件来管理，而不是一个不可控的黑盒。」

### 画面与停顿

| 顺序 | Pause at this line (English) | 画面切换方案 | 素材链接 |
|------|-------------------------------|--------------|----------|
| 1 | One important thing we learned is that building an AI-assisted application is not just about calling a model API. The hard part is designing the system around reliability. | **Screen 1**: Prompt 模板片段 | [roadmap/services.py](../../server/roadmap/services.py) |
| 2 | I worked on prompt structure, response formatting, error handling, and evaluation. | **Screen 1**: JSON 响应架构 | [截图：JSON架构示例](../screenshot_during_dev/AI_学习路线图_JSON架构示例_2026-03-11_15.41.29.png) |
| 3 | We also built an AI evaluation workflow to judge whether the generated roadmap was relevant, specific, and useful. | **Screen 1**: Eval Dashboard | [浏览器里打开skillgap_eval_dashboard.html](../../docs/skillgap_eval_dashboard.html) |
| 4 | That helped us iterate on prompts with evidence instead of intuition. In other words, we treated the LLM like one component in an engineered system, not like a magic black box. | **Screen 1**: 评估报告 | [ai_eval_results.pdf](../../docs/eval_roadmaps/ai_eval_results.pdf) |

---

## Part 6：Jing Part - 跳过
(06:40 - 07:40) 开发挑战与解决

---

## Part 7：工程质量、安全性与 CI/CD（07:40 - 08:40）  
**时长约 1 分钟**

### 优化后的台词（中文）
「除了功能演示，我们还希望这个项目不仅满足业务需求，还能体现专业的工程标准。因此，我在测试、CI 和安全性上投入了大量精力。我们利用 Vitest 和 Pytest 建立了自动化测试，覆盖率分别达到了前端 87% 和后端 97%。更重要的是，我们将安全性扫描集成到了开发生命周期中，使用 CodeQL 进行 SAST 扫描，以及 Dependabot 和密钥扫描。最后，通过 GitHub Actions 配合 Netlify 和 Render 实现了完整的 CI/CD 闭环。这保证了我们在快速迭代时，代码质量和安全性始终处于受控状态。」

### 画面与停顿

| 顺序 | Pause at this line (English) | 画面切换方案 | 素材链接 |
|------|-------------------------------|--------------|----------|
| 1 | Beyond a functional demo, we also wanted this project to meet professional engineering standards. So I invested heavily in testing, CI, and security-related improvements. | **Screen 1**: 测试报错 (全红 GIF) | [GIF：测试全红](../screenshot_during_dev/测试一开始很多报错__全红.gif) |
| 2 | We built automated tests and tracked coverage, achieving high coverage on both frontend and backend. | **Screen 1**: 测试通过 (全绿 GIF) <br> **Screen 2**: 后端 97% 覆盖率图 | [GIF：AI辅助修复测试](../screenshot_during_dev/ai根据报错帮助修复_最后全部通过测试.gif) <br> [截图：后端97覆盖率](../screenshot_during_dev/ai帮助提升测试覆盖率后达到了后端百分之97.png) |
| 3 | We integrated security scanning into our workflow, using CodeQL for static analysis and Dependabot for dependency monitoring. | **Screen 1**: Security 设置 <br> **Screen 2**: CodeQL 日志 | [截图：Security设置](../screenshot_during_dev/github_repo_security_setting.png) <br> [不用打开GitHub Actions 日志](https://github.com/MelanieLLY/SkillGap/actions) |
| 4 | Finally, we set up CI/CD so every commit is validated and automatically deployed to Netlify and Render. | **Screen 1**: CI 通过界面 | [截图：CI与部署平台](../screenshot_during_dev/每次PR的自动化检测CI和部署平台.png) |

---

## Part 8：协作与 AI 使用 — Liuyi 段（08:40 - 09:30）  
**时长约 30 秒**

### 优化后的台词（中文）
「在协作上，我们通过 commit 历史和 Issue、PR 边界让每一个人的贡献都看得见。Jing 主要负责认证、技能档案 CRUD、技能提取和分析历史这些后端基础（比如 Issue #1 #11 #4 #8）。我主要负责路线图生成、测试、CI/CD、前端打磨和系统加固（比如 Issue #7 #14 #29 #9 #31），以及后来的客户端与服务器分离和部署配置。这种分工让我们既能并行开发，又能整合成一个完整的、一致的产品。」

### 画面与停顿

| 顺序 | Pause at this line (English) | 画面切换方案 | 素材链接 |
|------|-------------------------------|--------------|----------|
| 1 | For collaboration, we used our commit history and feature boundaries to make responsibilities visible. | **Screen 1**: AI 辅助修复过程 GIF | [GIF：AI辅助修复过程](../screenshot_during_dev/ai根据报错帮助修复_最后全部通过测试.gif)<br/>[github_issues.png](../screenshot_during_dev/github_issues.png)|
| 2 | Jing led major backend foundations like auth, profile CRUD, extraction, and history. I focused on roadmap generation, testing, CI/CD, frontend polish, and system hardening. | **Screen 1**: 分工台账 (文档) | [team-contributions.md](../../docs/team-contributions.md) |
| 3 | That division let us move quickly while still integrating into one coherent product. | **Screen 1**: 项目 GitHub 主页 | [README.md](../../README.md) |

---

## Part 9：Deliverables 与结尾 — Liu yi 段（09:30 - 10:00）  
**时长约 20 秒**

### 优化后的台词（中文）
「所以除了应用本身之外，这个项目也覆盖了 Project 2 要求的主要交付物：全栈已部署，前端在 Netlify、后端 API 在 Render，且都配置了 GitHub 更新即自动部署；文档、测试证据和 Eval Dashboard 都已就绪，还有一套清晰的 AI 辅助开发记录。」

### 画面与停顿

| 顺序 | Pause at this line (English) | 画面切换方案 | 素材链接 |
|------|-------------------------------|--------------|----------|
| 1 | So beyond the app itself, this project also includes the major deliverables required for Project 2. | **Screen 1**: 最终路线图全貌 | [已部署 App (展示 Dashboard)](https://skillgapweb.netlify.app) |
| 2 | A deployed full-stack product, documentation, testing evidence, and a clear record of AI-assisted development. | **Screen 1**: 文档蒙太奇 | [api-docs.md](../../docs/api-docs.md) · [ai_eval_results.md](../../docs/eval_roadmaps/ai_eval_results.md) |
| 3 | (End) | **Screen 1**: 人像收尾 | 摄像头 |

---

## 快速链接检查表 (全部使用相对路径修复)

1. [仪表盘技能匹配三栏](../screenshot_during_dev/SkillGap_仪表盘_技能匹配12_现有_缺失_bonus三栏目.png)
2. [路线图界面](../screenshot_during_dev/SkillGap_仪表盘_技能职位描述_学习路线图_2026-03-11_16.34.57.png)
3. [JSON架构示例](../screenshot_during_dev/AI_学习路线图_JSON架构示例_2026-03-11_15.41.29.png)
4. [GIF：测试报错全红](../screenshot_during_dev/测试一开始很多报错__全红.gif)
5. [GIF：AI辅助修复测试](../screenshot_during_dev/ai根据报错帮助修复_最后全部通过测试.gif)
6. [后端97%覆盖率](../screenshot_during_dev/ai帮助提升测试覆盖率后达到了后端百分之97.png)
7. [Security设置截图](../screenshot_during_dev/github_repo_security_setting.png)
