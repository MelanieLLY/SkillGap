# AI Chat History: Security and Quality Fixes

**Time**: 2026-03-11 11pm (23:24)
**Issue Reference**: #14 (Master Plan Step 4.3)

## 任务目标
执行 `ruff check` (代码质量), `bandit` (后端安全), `npm audit` (前端安全) 并修复发现的问题，满足 P2 Requirement 中的 Technical Excellence 要求。

## 修复过程与测试情况

### 1. 前端安全 (npm audit)
- **初始状态**: 发现 2 个 Moderate 风险漏洞（`esbuild` 漏洞影响 `vite`）。
- **执行动作**: 运行 `npm audit fix --force` 将 `vite` 升级至 `7.3.1`。
- **最终状态**: **Passed** (0 vulnerabilities). 
- **回归测试**: 运行 `npm run build` 确认升级未破坏构建流程，构建成功。

### 2. 后端安全 (bandit)
- **初始状态**: 
    - 1个 **Medium** 风险: [server/main.py](cci:7://file:///Users/melaniey/Github/SkillGap/server/main.py:0:0-0:0) 中硬编码 `host="0.0.0.0"`。
    - 249个 **Low** 风险: 主要是测试文件中的 `assert` 语句和模拟密码。
- **执行动作**:
    1. 修改 [server/core/config.py](cci:7://file:///Users/melaniey/Github/SkillGap/server/core/config.py:0:0-0:0) 和 [server/main.py](cci:7://file:///Users/melaniey/Github/SkillGap/server/main.py:0:0-0:0)，将 Host/Port 迁移至环境变量配置。
    2. 创建 [bandit.yaml](cci:7://file:///Users/melaniey/Github/SkillGap/bandit.yaml:0:0-0:0) 配置文件，排除 `server/tests/` 目录并忽略 `B101 (assert)` 警告。
    3. 在 `server/auth/router.py` 为 token type 添加 `# nosec` 标志。
- **最终状态**: **Passed** (0 issues Identified). 实现了从“存在中危风险”到“安全达标”的转变。

### 3. 代码质量 (ruff)
- **状态**: 始终保持 **Passed**。代码符合 PEP8 和项目定义的 Strict Typing 规范。

## 结论
所有安全和质量扫描工具目前均返回绿色（通过）状态，符合项目交付标准。
