# AI 聊天记录：Match Score 安全漏洞修复

**时间:** 2026年3月11日，下午2点
**主题:** 修复 match_score 安全漏洞，将其改为由后端计算。

## 1. 用户需求
用户指出 `server/history/schemas.py` 里的 `HistoryCreate` schema 会接受客户端传来的 `match_score`，这存在安全漏洞。需求是更新 history 路由和相关 schema，使 `match_score` 改为由后端使用 Extraction Engine 进行计算和校验，而不是直接盲目信任请求体中的该值。

## 2. 实施过程：更新 Schemas & 路由
- **`server/history/schemas.py`**:
  - 从 `HistoryBase` (即 `HistoryCreate` 继承的类) 中移除了 `match_score`。
  - 将 `match_score` 移动到了 `HistoryResponse` 中。这确保了客户端无法在创建时提供该分数，但在返回给客户端的数据中依然会包含计算后的分数。
- **`server/history/router.py`**:
  - 从 `server.extraction.engine` 导入了 `calculate_match_score`。
  - 在 `create_history` (POST) 端点中，添加了后端计算逻辑：
    ```python
    match_score = calculate_match_score(history_in.have_skills, history_in.missing_skills)
    ```
  - 创建数据库模型时，将重新计算出的 `match_score` 传入并保存到数据库。

## 3. 部署后测试
- 在代码改动完成后，用户询问原有的测试是否还能跑通。
- 我运行了 `pytest server/tests`，发现 `server/tests/test_history.py::test_create_history` 测试失败了。
- **失败原因**: 测试用例中的假数据仍然在向 POST 接口发送包含 `match_score: 85.5` 的 payload，并预期返回的分数也是 85.5。由于后端现在忽略了传入的分数并改为自行计算，而假数据提供了 `have_skills: ["python"]` 和 `missing_skills: ["aws"]` （各包含一项技能），所以 Extraction Engine 计算出的正确分数是：`1 / 2 * 100 = 50.0`。
- **修复方法**: 更新了 `test_history.py`，移除了 Payload 中的 `match_score` 字段，并将断言校验的预期值更改为 `50.0`。
- **测试结果**: 重新运行测试后，后端所有的 26 个测试用例全部绿灯通过 (`26 passed`)。
