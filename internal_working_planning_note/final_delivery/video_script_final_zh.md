# SkillGap 最终视频脚本（10分钟均衡版）

**目标受众**：公众 / 未来雇主 / 教学团队  
**目标**：不仅展示 SkillGap 做了什么，也展示我们是如何构建它的、如何使用 AI、如何协作，以及它为什么满足 Project 2 的交付要求。  
**总时长**：10:00  
**讲者**：Jing 和 Melanie  
**时间分配**：Jing 约 5:00，Melanie 约 5:00

## 录制安排

**Plan A：分开录制 + 共享 Google Slides**
- 我们先建一个共享的 Google Slides，一起把各自部分中要展示的画面整理进去。
- 每个人用手机横屏录自己负责的出镜讲解部分。
- 每个人把自己板块对应的素材补齐（截图 + 关键短录屏/GIF）。
- 后期剪辑时按脚本时间线走，把 slides 当作画面切换主线。
- 为了确保两位成员都清楚出镜，结尾会加一个简短的双人同框镜头。

**Plan B：一起用 Zoom 录制**
- 我们也可以约一次 Zoom 联合录制。
- 全程开摄像头，边共享 slides / 产品演示，边按分段轮流讲解。
- 每一段仍然由对应成员主讲，并把总时长控制在 10 分钟左右。
- 结尾同样保留一个两人同时出镜的短收尾。
---

## 录制说明

- 用自然语速讲话：大约每分钟 115 到 130 个英文单词的节奏。
- 开场、过渡、协作反思和结尾建议保留人像镜头。
- 产品流程、代码、测试、CI 和文档证据部分使用录屏展示。
- 不要讲得太快。清晰自然比完美更重要。

---

## Part 0: 开场钩子与项目概述（00:00 - 00:40）
**Speaker: Jing**

**Visual**
- 前 5 秒使用人像镜头。
- 切到产品落地页。
- 快速蒙太奇：粘贴 job description，看到 match ring 动画，再展示 roadmap 正在生成。

**Script**
"大家好，我是 Jing，这个项目叫 SkillGap，是我和我的队友 Melanie 为 Project 2 一起完成的全栈应用。SkillGap 帮助求职者把自己现有的技能和岗位描述进行对比，找出缺口，并把这些缺口进一步转化为一个可执行的学习路线图。在这个视频里，我们会带大家看一遍产品流程，解释这个项目是怎么搭建起来的，展示 AI 在开发过程中扮演了什么角色，也会分享我们作为团队是如何协作完成它的。"

---

## Part 1: 问题背景、用户流程与产品作用（00:40 - 01:20）
**Speaker: Melanie**

**Visual**
- 角落保留人像镜头。
- 展示产品首页。
- 加一个简单的三步说明页或字幕：
  1. 建立技能档案
  2. 粘贴岗位描述
  3. 获取 gap analysis 和 roadmap

**Script**
"我是 Melanie。我们想解决的问题其实很直接：岗位描述通常很长、很杂，而且很难直接转换成一个真正可执行的学习计划。所以我们围绕一个非常清晰的用户流程来设计 SkillGap。第一步，用户创建账号并保存自己已有的技能。第二步，用户粘贴目标岗位的 job description。第三步，系统分析技能差距，并生成即时反馈和结构化的学习路线图。也就是说，这个产品不仅告诉用户问题在哪里，还进一步告诉用户下一步该怎么做。"

---

## Part 2: 核心产品体验 Walkthrough（01:20 - 02:40）
**Speaker: Jing**

**Visual**
- 注册或登录流程。
- 展示 profile 页面上的 skill CRUD 操作。
- 在 dashboard 中粘贴 JD。
- 展示 match score ring、提取出的技能、missing skills 和 history 列表。

**Script**
"接下来我来展示核心的产品流程。用户首先通过认证系统登录，这样每个人都拥有安全、独立的个人数据。登录之后，用户可以在个人技能档案中新增或删除技能。这些技能会被持久化存储到数据库中，作为之后分析的基础。在 dashboard 页面，用户粘贴一段岗位描述，我们的 extraction engine 会识别出哪些技能已经匹配，哪些技能缺失，以及哪些是额外加分项。我们还用一个动态的 match score ring 来可视化匹配结果，并且保存分析历史，这样用户之后可以回来看不同岗位目标之间的差异。这样一来，哪怕还没有进入 AI roadmap 阶段，用户也已经能立刻获得实际价值。"

---

## Part 3: AI 路线图与前端体验（02:40 - 04:00）
**Speaker: Melanie**

**Visual**
- 展示 dashboard 从分析结果切换到 roadmap 生成过程。
- 展示 skeleton loading 状态。
- 展示最终 roadmap UI，包括 milestones、week 分配和推荐内容。
- 简短放大 Claude service 或 prompt-to-JSON 流程代码。

**Script**
"当技能差距被识别出来之后，我负责的部分会把这个结果从诊断推进到行动。我集成了 Claude，根据分析阶段提取出的缺失技能，为用户生成一个个性化的学习路线图。我们并不是简单返回一大段自由文本，而是设计了一条结构化的数据流，让模型输出稳定一致的数据格式，再由前端把它渲染成 milestones、每周目标和学习建议。在用户体验方面，我也加入了 skeleton loading 和动画细节，因为 AI 响应需要时间，而我们希望整个界面在等待过程中依然显得流畅、专业，而不是卡住或者让用户困惑。"

---

## Part 4: 我们是如何搭建项目基础的（04:00 - 05:20）
**Speaker: Jing**

**Visual**
- 架构图：React frontend、FastAPI backend、PostgreSQL database、Claude integration。
- 简短展示 API 或后端代码片段。
- 展示数据库模型或 endpoint 列表。

**Script**
"在界面背后，这个项目是一个完整的全栈系统。我们使用 React 作为前端，FastAPI 作为后端，PostgreSQL 负责数据持久化。我主要负责应用的基础层，包括基于 JWT 的身份认证、skill profile 的 CRUD、analysis history，以及 extraction logic 的第一版实现。我们在设计时有一个很重要的目标，就是让系统模块化。规则驱动的分析层负责提供快速、确定性的反馈，而 AI 层是在这个结果之上继续生成更进一步的 roadmap，而不是直接取代前面的分析。这种分层让系统更容易理解、更容易调试，也更方便我们在团队中清晰分工。"

---

## Part 5: AI 技术、评估方式，以及为什么这不只是“调 prompt”（05:20 - 06:40）
**Speaker: Melanie**

**Visual**
- 展示 prompt 片段或 system prompt 的一部分。
- 展示 JSON 响应示例。
- 展示 AI evaluation report 或 eval dashboard。
- 可以短暂展示面向老师提交的 deliverables 文件夹。

**Script**
"我们学到的一件重要事情是，构建一个 AI-assisted application，绝对不只是调用一个模型 API 那么简单。真正困难的部分，是围绕可靠性去设计整个系统。我主要处理了 prompt 结构、响应格式、错误处理以及评估流程。我们还建立了一套 AI evaluation workflow，用来判断生成出来的 roadmap 是否足够相关、具体并且有用。这样我们在改进 prompt 的时候，不是凭感觉，而是基于证据来迭代。换句话说，我们把 LLM 当作一个工程系统中的组成部分来管理，而不是把它看成一个神奇但不可控的黑盒。"

---

## Part 6: 开发过程中的挑战，以及我们如何解决（06:40 - 07:40）
**Speaker: Jing**

**Visual**
- 用分屏展示“问题 -> 解决方案”。
- 展示 history feature、extraction 结果，或架构图。
- 可加简短字幕："challenge: consistency"、"challenge: separation"、"challenge: persistence"

**Script**
"我们在开发过程中遇到的最大挑战，是如何把快速的规则分析和更灵活的 AI 路线图连接起来，同时又不让系统变得脆弱。我们需要确保 extraction 的结果足够准确，这样下游的 AI 输出才有基础；我们也需要做好持久化，这样用户在多次使用时才会真正信任这个应用。另一个挑战是团队协作中的分工边界。我们的解决方法是尽量保持清晰的责任分层：我主要负责核心后端流程和数据基础，而 Melanie 在这些稳定输出之上继续扩展 roadmap generation、testing，以及交付质量相关的部分。"

---

## Part 7: 工程质量、安全性与 CI/CD（07:40 - 08:40）
**Speaker: Melanie**

**Visual**
- 终端里运行测试。
- 展示 coverage summary。
- 展示 GitHub Actions workflow。
- 展示后端校验或 match-score logic 的代码片段。

**Script**
"我们也希望这个项目不仅满足 demo 层面的要求，还能够体现 rubric 里强调的工程能力。所以我在测试、CI 和安全性改进上投入了很多精力。我们构建了自动化测试，跟踪 coverage，并准备了可以直接作为评估证据的测试结果，而不是只依赖截图。我们还把像 match score calculation 这样的重要逻辑移动到了后端，避免结果可以被前端轻易伪造。最后，我们配置了 CI checks，让每次改动都能持续得到验证。这帮助我们在保持开发速度的同时，也能对代码质量保持信心。"

---

## Part 8: 我们如何使用 AI，以及我们如何协作（08:40 - 09:30）
**Speaker: Jing, then Melanie**

**Visual**
- 先由 Jing 单独出镜。
- 然后切到 Melanie 单独出镜。
- 在各自讲话时叠加 commit history、branches、tests、docs 或 planning artifacts。

**Jing Script**
"在 AI 的使用上，我们并不是只把它用在一个单一场景里。我们会用 AI 来加快 planning、implementation support、debugging 和 documentation drafting，但我们始终会自己验证输出结果，并根据真实系统进行修改和落地。"

**Melanie Script**
"在协作方面，我们通过 commit history 和 feature boundary 让每个人的贡献都尽量清晰可见。Jing 主要负责 auth、profile CRUD、extraction 和 history 这些后端基础功能。我主要负责 roadmap generation、testing、CI/CD、frontend polish 以及系统加固。这种分工方式让我们既能并行推进，又能最终整合成一个一致、完整的产品。"

---

## Part 9: Deliverables、反思与结尾（09:30 - 10:00）
**Speaker: Melanie, then Jing**

**Visual**
- 最终产品页面。
- 快速蒙太奇展示 README、API docs、eval dashboard、blog/video 文件，以及 deployed app。
- 最后停在 Melanie 单人人像，再切到 Jing 单人人像，或者直接结束在项目 logo。

**Melanie Script**
"所以，除了应用本身之外，这个项目也覆盖了 Project 2 要求中的主要 deliverables，包括已部署的全栈产品、文档、测试证据，以及一套清晰的 AI-assisted development 记录。"

**Jing Script**
"更重要的是，SkillGap 展示了我们不仅能做出一个有产品价值的应用，也能用工程化的方法把一个 AI-assisted application 真正落地。谢谢大家观看。"

---

## 快速录制检查清单

1. 每一部分尽量控制在对应时间内，正式录之前先用计时器试讲一遍。
2. 展示代码时放大，只展示你正在讲的那一小段。
3. 展示 UI 时，鼠标移动尽量慢一点、稳一点。
4. 每一段之间留 1 到 2 秒停顿，方便后期剪辑。
5. 如果录制时觉得某句太书面，可以现场简化，真实自然比逐字照读更重要。
