以下内容是老师在课堂上对于project 2的要求进行的补充.如果有冲突的话,应该以 Planning Files gitignore/P2 requirement.md为准.

# 按问题主题汇总成最终版 checklist

下面是更像“交作业核对表”的版本，你可以直接拿去对照：

Project 2 口头要求总核对表

A. 总规则
	•	以 Canvas / rubric 已写明内容为准
	•	若老师口头与 written instructions 冲突，按 written instructions
	•	老师承认 AI 生成说明可能有模糊处，但同学提到的那些 deliverables 基本都算数

B. Documentation package
	•	README
	•	API docs
	•	technical / quality blog post
	•	video
	•	sprint planning 内容
	•	两个 sprint 的 retrospectives
	•	AI modalities 的使用说明
	•	AI reflections
	•	对整个代码的文档化

C. Blog post
	•	面向公众，不是内部反思
	•	user-facing
	•	product-oriented
	•	用来建立 social presence
	•	展示你们做了什么、会什么
	•	与 reflection 区分开
	•	长度按 rubric：1500 words

D. Eval dashboard / testing evidence
	•	本质是测试结果/测试报告
	•	最好提交 PDF
	•	Markdown / HTML 也可以
	•	截图不是最佳，但必要时可接受
	•	应展示 test suite 运行结果
	•	应展示通过的 tests / summary / coverage
	•	若有 Cypress / Playwright HTML 报告，也可以交

E. Video
	•	长度 10 分钟
	•	面向 general public
	•	不是只有 feature demo
	•	要讲应用 walkthrough
	•	要讲功能
	•	要讲怎么 build 的
	•	要讲 techniques / approaches
	•	要讲 development challenges
	•	要讲 AI 如何使用
	•	要讲团队如何协作
	•	要覆盖主要 deliverables
	•	开头最好有 short summary / intro
	•	两位组员都要出镜
	•	一个 shared video 即可
	•	视频可以剪辑
	•	视频应公开

F. 团队协作 / 个人贡献
	•	老师想看到每个人都参与了
	•	即使 GitHub 记录不理想，也要用其他证据补强
	•	要能说明每个人具体负责什么
	•	最好有文档/记录/分工痕迹，而不是口头声称
	•	反思里应谈 AI coding 下的 collaboration

# 课堂上的具体对话

## complete documentation package

最后可执行要求

	•	Documentation package 至少应理解为包含这些部分：
		•	README
		•	API docs
		•	technical / quality blog post
		•	video
		•	sprint planning 相关内容
		•	retrospectives（两个 sprint 的回顾）
		•	AI modalities 是怎么用的

	•	老师想看到你们对 Scrum 过程的反思。
		•	不要求特别冗长
		•	即使你们是“很快节奏的 Scrum”或者春假突击开发，也要写出反思

	•	老师想看到 AI reflections。
		•	也就是你们如何使用 AI、如何与 AI 协作、对这个过程有什么反思

	•	老师想看到“整个代码的文档”。
		•	他说在 AI coding 里，生成代码文档其实很容易，所以他希望你们把代码文档补起来

## blog post 和其他 documentation 是不是两回事？blog post 到底该写什么？

	•	老师说：blog post 是和其他内部文档不一样的东西。
	•	它不是写给老师/TA看的“内部说明”，而是：
		•	面向外部
		•	建立 social presence
		•	展示你有这些技能
		•	有点像在对外说：“看，我会做 AI-assisted coding 项目，快来 hire me”

	•	老师强调：
		•	它应该很 user-facing
		•	应该很 product-oriented
		•	应该展示你们构建了什么、有什么能力
		•	老师不想把 blog post 限定得过细，因为他想给学生保留一些自由度
		•	他说 blog post 不一定非得很长，哪怕短一点也行——但后来当发现 rubric 写了字数要求后，他又明确说：按 rubric 字数执行。

最后可执行要求

	•	Blog post 的定位：
		•	面向公众，不是只给老师看
		•	展示项目成果和个人/团队能力
		•	像作品展示文，而不是课程反思文

	•	Blog post 应该突出：
		•	你们做了什么应用
		•	这个应用对用户/产品层面是什么
		•	你们学到了/用到了哪些 AI coding skills

	•	Blog post 和 reflection 不一样：
		•	reflection = 对老师/助教汇报你做了什么
		•	blog post = 对外界展示你的能力与项目

	•	长度如果 rubric 写了，就按 rubric。
		•	录音里老师确认同学看到的是：1500-word technical blog post

	•	老师对质量的期待：
		•	product-oriented
		•	user-facing
		•	能建立你的“社会存在感/职业形象”
		•	不是纯 AI 套话

## 老师刚说 blog post 不用太长，但 rubric 写 1500 词，怎么办？

老师怎么回答

	•	老师直接说：那就按写在 rubric 里的要求做。
	•	他说如果 Claude 写了 1500 words，就按这个走。

	•	他的理由是：
		•	课堂口头说明不是所有同学都会听到
		•	很多人最后会只看 written instructions
		•	为了公平，应该以 written requirement 为准

	•	老师还补充：
		•	大家大概率会借助 AI 写这些内容
		•	但不要把它写成网上那种“AI blob”式空话套话
		•	要有质量，要区分自己，不要变成一坨 AI 味很重的内容

最后可执行要求

	•	遇到“老师口头 vs rubric文字”冲突时，以文字版为准。
	•	Blog post 按 1500 词准备。
	•	即便用 AI 辅助，也要人工提升质量，避免空洞、模板化、像 LinkedIn 那种 AI 味很重的长篇废话。

## eval dashboard 是什么？老师到底想要什么？

Eval Dashboard 的具体要求本质是测试结果文档：

	•	它应该是一个展示运行测试套件（如 npm run test）结果的文档，建议使用 PDF 或 Markdown (.md) 格式 。

	•	包含内容：
		•	测试通过情况：描述实现了哪些测试以及通过了多少项 。
		•	测试覆盖率 (Test Coverage)：需要展示具体的覆盖率百分比 。

	•	呈现形式：
		•	老师明确表示不喜欢只交一张截图，因为截图可能显示不全，且不方便助教评分 。
		•	如果非要用截图，必须确保它是非常详尽且易读的 。

	•	生成建议：
		•	你可以要求 Claude 针对你的测试结果生成一份简要报告 。
		•	如果你使用了 Cypress 或 Playwright 等工具，生成 HTML 报告 也是一个很好的选择 。

这部分老师前后说了两次，信息可以合并：

	•	一开始老师说，他从同学描述来看，自己期待看到的应该是测试运行结果。
	•	他举例说：
		•	像运行 npm run test
		•	输出通过了多少测试
		•	各个测试描述是什么

	•	他不太喜欢只有 screenshot，因为：
		•	不利于 TA 批改
		•	一张图往往放不下

	•	他更推荐：
		•	PDF
		•	文档
		•	或其他非图片形式的可读报告

	•	后面老师又专门总结了一次：
		•	eval dashboard 应提交一个 document
		•	最好是 PDF
		•	也许 Markdown 也可以
		•	内容是：展示你运行 test suite 的结果
		•	例如测试项、通过情况、coverage 等

	•	如果你用了更成熟的测试工具，比如：
		•	Cypress
		•	Playwright
		•	生成 HTML 报告
		•	那也很好，可以提交 HTML 报告

	•	如果最简单的方法真的是截图，只要足够完整，截图也不是完全不行，但老师明显更偏好可读文档/报告

最后可执行要求

	•	Eval dashboard 本质上是在交测试结果/测试报告，不是做一个复杂 UI dashboard。

	•	推荐提交格式：
		•	PDF 最佳
		•	Markdown / HTML 也可
		•	截图是次选

	•	应展示的内容：
		•	测试套件运行结果
		•	通过了多少 tests
		•	测试描述/summary
		•	coverage / testing coverage
		•	如果有自动生成的 web report / HTML report，可以交。

	•	目标是让老师/TA看得出你们确实做了测试并达到 coverage。

## documentation 里关于 code documentation 想看到什么？

老师怎么回答

	•	老师明确说：他想看到整个代码的文档化。
	•	原因是：
		•	在 AI coding 场景下，让 AI 生成代码文档并不难
		•	所以他希望你们把文档补齐

最后可执行要求

	•	要给代码做文档。
	•	至少应理解为：README、API docs，以及对代码结构/功能有足够说明。
	•	老师默认你们可以借助 AI 完成这部分，但最终结果要成型。

## Video要求

	•	视频长度：10 分钟。
	•	视频定位：面向公众，而不是只给 TA 的交作业 demo。

	•	视频应包含：
		•	项目简介 / short summary
		•	应用 walkthrough
		•	功能展示
		•	你们如何构建项目
		•	使用了哪些技术/方法
		•	遇到了什么挑战/问题
		•	AI 如何参与开发
		•	团队如何协作
		•	对项目 deliverables 的整体讲解

	•	视频不是“只有 features demo”。
	•	两位组员都要出镜。
	•	一个共同视频即可。
	•	视频可以剪辑。
	•	视频应公开。