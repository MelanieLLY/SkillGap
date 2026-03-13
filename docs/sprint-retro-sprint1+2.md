> 本文件中的 Sprint 1 / Sprint 2 回顾段落，由 AI 助手在梳理 GitHub commit 历史、Issues 完成情况（含 Sprint 标签）、CI 记录以及内部 planning note 之后，先生成初稿，再由 Liuyi 结合真实开发体验进行修改与确认。  
> 因此，这里的「做得好的地方」「可以改进的地方」和行动项，都是以实际历史数据为基础的总结，而不是纯主观印象。

## Sprint 1 回顾（Retrospective）—— Core Application

### 1. 目标回顾

**原定目标**（见 `docs/sprint-planning-sprint1.md` 与 PRD）：

- 交付可用的认证与技能档案管理。
- 支持用户粘贴 JD 并看到匹配结果（have/missing/bonus + match score）。
- 实现基础的匹配度可视化和三列技能对比 UI。

**实际完成情况**：

- `auth`、`profile`、`extraction` 模块全部上线，并通过 pytest 覆盖核心路径。
- 前端 Login/Register/Profile/Dashboard 页面在本地与部署环境中均可跑通完整流程。
- Animated Match Ring 完成了第一版实现，为后续 UI polish 打好了基础。

总体来说，本 Sprint 完成了「无 AI 学习路线版本」的完整闭环，为 Sprint 2 的 Claude 接入和历史记录打下了扎实基础。

### 2. 做得好的地方（What went well）

1. **PRD 与 GitHub Project Board 对齐彻底**  
   - 在 Sprint 1 启动前，团队已经有了详细的 `docs/skillgap_prd.md` 和 `PROJECT2_MASTER_PLAN.md`。  
   - 每个 Issue 都能映射回具体用户故事，规划和实现之间的沟通成本很低。

2. **前后端契约相对稳定**  
   - 在实现 `/api/extract` 和 `/api/profile/*` 时，先由后端定义 Pydantic schema，再由前端根据 OpenAPI/Swagger 做集成。  
   - 出现接口字段变更时，通过小范围 PR 调整，避免了「大爆炸式重构」。

3. **测试和 CI 有提前意识**  
   - 虽然完整的 coverage 门槛在 Sprint 2 才严格执行，但在 Sprint 1 就开始写后端测试。  
   - 这为后续增加 AI & History 功能时的重构提供了安全网。

4. **Animated Match Ring 作为 UI 核心卖点**  
   - 在 Sprint 1 中尽早完成了第一版动画，为后续 Wow-factor 动画留足时间。  
   - 因为动画组件结构清晰，后面升级为 framer-motion 只需要局部修改。

### 3. 可以改进的地方（What could be improved）

1. **数据库与环境配置踩坑较多**  
   - 早期本地开发与测试使用的是 SQLite，与课程要求的 PostgreSQL 不一致。  
   - 后期在迁移到云端 Postgres 时付出了一定的时间来修配置和迁移脚本。

2. **错误处理和回滚逻辑初期不够严谨**  
   - 一开始部分路由直接 `db.commit()`，缺少 `try/except` 和 `rollback`，在异常场景下容易留下一半成功的写入。  
   - 这部分在 Sprint 1 后期和 Sprint 2 初期通过重构补齐。

3. **前端测试覆盖率偏低**  
   - Sprint 1 更关注「跑通功能」，对组件级测试和错误状态测试覆盖不足。  
   - 这导致后续引入更复杂动画/骨架屏时，缺少回归测试的保障。

### 4. 行动项（Action Items）

1. **统一数据库策略并文档化**  
   - 行动：将「所有测试使用同一个云端 Postgres 实例」写入 `PROJECT2_MASTER_PLAN.md` 与 `.antigravityrules`，并在 `server/tests/conftest.py` 中统一配置。  
   - 负责人：Liuyi。

2. **为所有写库操作补充事务与异常处理**  
   - 行动：系统性梳理 `auth/profile/history` 中的增删改操作，统一加入 `try/except SQLAlchemyError` 和 `rollback`，并在 `main.py` 中增加全局异常处理器。  
   - 负责人：Melanie；状态：已在 Sprint 2 起始阶段完成。

3. **在 Sprint 2 中提升前端测试覆盖率**  
   - 行动：把关键页面（Dashboard/Profile/History）的渲染、加载状态、错误态加入 Vitest 测试计划，并在 CI 中强制执行。  
   - 负责人：全队共同负责，在 Issue #10 和 #14 中落实。

## Sprint 2 回顾（Retrospective）—— AI & Polish

### 1. 目标回顾

**原定目标**（见 `docs/sprint-planning-sprint2.md`）：

- 集成 Claude AI，产出结构化学习路线。
- 实现分析历史记录视图与后端持久化。
- 搭建 AI Eval Suite 与 Eval Dashboard。
- 打磨 UI/UX（骨架屏、动画、可访问性）并完善测试与 CI。

**实际完成情况**：

- 已实现 `POST /api/roadmap/generate`，成功对接 Anthropic Claude API，前端可视化学习路线（Issue #7）。  
- 已上线 History 页面，用户可以查看每次分析记录和 match score（Issue #8）。  
- 已实现 AI 质量评估脚本（`server/tests/ai_eval.py`）以及结果文档 `docs/eval_roadmaps/ai_eval_results.md` 和 `docs/skillgap_eval_dashboard.html`（Issue #9）。  
- 引入了 Skeleton 组件、framer-motion 动画，Dashboard 体验流畅，UI wow-factor 达标（Issue #10）。  
- 后端 pytest 和前端 Vitest 流水线在 CI 中运行，通过率和覆盖率满足课程要求（Issue #14、#29、#31）。  
- 完成了仓库结构重构与生产部署准备：清晰分离 `client/` 与 `server/`，并配置 Render 后端与 Netlify 前端部署（Issue #35、#37、#38）。

整体来看，Sprint 2 成功完成了从「规则引擎 MVP」到「AI 驱动、带历史记录与评估的完整产品」的升级。

### 2. 做得好的地方（What went well）

1. **Claude 集成分阶段推进，风险可控**  
   - 先在 `PROJECT2_MASTER_PLAN.md` 中规划了「空实现 scaffolding」阶段，再逐步增加真实 Prompt 和错误处理。  
   - 通过 `ClaudeTimeoutError`/`ClaudeAuthError` 等自定义异常，把 API 故障与业务逻辑解耦。

2. **AI Eval Suite 有清晰的指标与样本集**  
   - 使用第二个 LLM 作为「Judge」，对 Relevance / Specificity / Completeness 进行打分。  
   - 把结果汇总到 `docs/ai_eval_results.md` 和 Eval Dashboard 中，既满足课程的 AI Mastery 要求，也让我们对路线质量有量化认知。

3. **CI 流水线多阶段化显著提升了开发信心**  
   - `.github/workflows/ci.yml` 中分离 lint/test/build，出现问题时能迅速定位。  
   - 覆盖率门槛和严格的 lint 一度阻挡了不合格 PR，迫使我们在提交前修复问题。  
   - 每个 PR 除 GitHub Actions 外还会触发 Netlify 的 Deploy Preview 及站点规则检查（Header rules、Pages changed、Redirect rules），便于在合并前验证前端预览。

4. **UI Polish 与 Skeleton 设计提升了整体观感**  
   - Loading 态通过 Skeleton 组件与渐变动画过渡，避免了「空白屏」体验。  
   - AnimatedMatchRing、三列技能和 Roadmap 组合出的视觉效果，有足够的 demo 价值与截图素材。

### 3. 可以改进的地方（What could be improved）

1. **AI Prompt 与错误处理复盘不足**  
   - 虽然在实现过程中迭代过数版 Prompt，但只有部分总结被保存在规划文档和 Eval Dashboard 里。  
   - 某些边缘 case（如 JD 极短、技能列表为空）在 Prompt 设计初期没有被单独考虑。

2. **AI Eval 与真实用户反馈之间仍有空白**  
   - Eval Suite 使用的是「AI 评 AI」的方式，缺少真实用户的主观评价。  
   - 一些路线在分数上表现良好，但在实际阅读体验上仍稍显冗长。

3. **前后端调试偶尔受限于外部 API 状态**  
   - Claude API 的偶发性超时/限流，导致本地和 CI 测试有时需要打桩或跳过。  
   - 这些行为虽在代码中有保护，但在文档和测试策略中可以更明确区分「带真 API」与「离线 mock」模式。

### 4. 行动项（Action Items）

1. **系统化记录 Prompt 设计与演进**  
   - 行动：将当前 Claude Prompt、几版关键修改对比和对应的 Eval 分数整理到 `docs/ai-reflection.md`，作为课程反思的一部分。  
   - 预期效果：未来如果更换模型或升级 Prompt，有清晰的基线可参考。

2. **为 AI Eval 增加「人工 spot check」流程**  
   - 行动：选取 3–5 条 Eval 中评分最高和最低的路线，由团队成员人工阅读并写简短点评，合并进 `docs/ai-modalities-usage.md` 或 Eval Dashboard。  
   - 预期效果：避免完全依赖 LLM 自评，补充人类视角。

3. **增加离线 mock 测试模式**  
   - 行动：在 `roadmap/services.py` 中保留可切换的 mock 模式（通过环境变量），CI 默认启用 mock，以减少对真实 Claude API 的依赖。  
   - 预期效果：CI 更稳定，开发环境在无外网或 API 限流时仍可完整验证前后端逻辑。

