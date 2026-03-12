# AI 对话历史记录: 全局数据库错误处理重构与 Git 问题排查

## 1. 初始需求
**目标**: 在 `auth`、`profile` 和 `history` 路由中，为数据库的 `db.commit()` 操作添加容错处理（`try...except SQLAlchemyError` 以及 `db.rollback()`），以修复缺少异常回滚保护的问题。

## 2. 方案讨论与选择
AI 提供了两种现代 FastAPI 架构下的最佳实践：
- **方案一：全局异常处理器 (Global Exception Handler)**。在 `server/main.py` 的 FastAPI 应用层级拦截所有的 `SQLAlchemyError`，好处是统一兜底、防止遗漏，并且保持路由业务代码极其干净。FastAPI 的依赖注入 (`finally: db.close()`) 会自动处理回滚。
- **方案二：局部上下文管理器 (Context Manager)**。封装一个 `transaction` 依赖，提供更细粒度的控制。

**决定**: User 选择了**方案一 (全局拦截)**，因为最简单且不易出错。

## 3. 代码实现过程
1.  **最初的尝试**: AI 在三个路由文件中分别添加了 `try...except` 代码块。
2.  **重构为全局**: 确认选择方案一后，AI 删除了三个路由文件中的局部错误处理代码，使其恢复清爽；并在 `server/main.py` 中加入了 `@app.exception_handler(SQLAlchemyError)`，统一返回 `{"detail": "A database error occurred while processing your request."}` (HTTP 500)。
3.  **增加 Debug Log**: 根据要求，在全局处理器中加入了一行 `print()` 语句，方便在后端终端直接查看红色的详细报错信息而不泄露给前端。

## 4. Git与GitHub Desktop问题排查
- **现象**: User 在 GitHub Desktop 和 `git status` 中看不到被修改的文件。
- **排查 1 (Xcode 协议)**: 发现 macOS 开发环境抛出了 `You have not agreed to the Xcode and Apple SDKs license` 错误，阻断了 Git 进程。建议执行 `sudo xcodebuild -license` 解决。
- **排查 2 (Diff 机制视觉差)**: 用户发现就算手动修改文件也会出现，但 AI 修改的三个路由器依然没出现。揭开真相：因为 AI 在切换到全局方案时，**原样撤销**了之前加在三个路由器里的局部保护代码。在 Git 的 Diff 机制看来，这三个文件和上一次 Commit 的内容**一模一样**，因此被认定为未修改，这是全局拦截方案优雅不污染代码的证明。

## 5. Scrum 规范与 GitHub 管理
AI 提供了一套完整的 Scrum 敏捷开发文案：
- **Issue 类别**: 推荐使用 `enhancement`（功能增强/优化）而不是 `bug`，因为这是对容错能力的架构升级，并非修复现有的崩溃。
- **Issue 详情**: 快速精准地描述了“Why, Solution, Benefits”。
- **分支命名**: `refactor/13-global-db-error-handler`
- **提交信息**: `feat(#13): implement global db error handler and debug logs` 
- **PR 模板**: 清晰列出了 What's Changed 和测试勾选框。

## 6. PR 冲突解决 (Merge Conflict)
- **现象**: PR 提示无法 Auto merge。
- **原因**: User 提交的分支包含了详尽的 `print()` 日志代码，而主干 `main` 分支在同一位置只是一句旧的草稿注释。
- **解决方案**: 在 GitHub 网页端的 "Resolve conflicts" 页面，删掉冲突标记（`<<<<<<<` 和 `>>>>>>>`）以及旧的草稿代码，完全保留最新的 `print()` 处理逻辑，点击 "Mark as resolved" 后完成合并。

## 7. Master Plan 更新
确认此次架构改进完全符合 Project 2 要求的 "Step 0.4 打通数据库异常回滚保护"，顺利打上 `[x]`。
