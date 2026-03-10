# Week2 学习记录

请按 `docs/notes/ai学习计划大纲.md` 对应 Week2 的 Day1-Day7 逐日补充记录。

## Day 1 已完成
- 工具契约文档：`docs/notes/week2/tool_schemas.md`

## Day 2 已完成
- Mock 工具实现：`src/week2_tools.py`
- 已验证 3 个工具成功路径可运行：
  - `search_kb`
  - `get_order_status`
  - `create_ticket`

## Day 3 已完成
- 最小 Agent 分发器：`src/week2_agent.py`
- 已打通流程：意图识别 -> 路由 -> 工具调用 -> 用户回复
- 现阶段策略：缺关键参数优先追问，再执行工具

## Day 4 已完成
- 异常与追问规范：`docs/notes/week2/exception_strategy.md`
- 覆盖缺参追问、工具失败分层、重试与转人工策略

## Day 5 已完成
- 回归数据集：`eval/week2_agent_cases.jsonl`（30 条）
- 覆盖意图分类、追问分支、工具调用分支、错误码校验

## Day 6 已完成
- 批量评测脚本：`src/week2_eval.py`
- 回归报告：`docs/notes/week2/day6_regression.md`
- 当前指标：通过率/意图准确率/动作准确率/工具准确率均为 100%

## Day 7 已完成
- 周总结：`docs/notes/week2/week2_review.md`
- Week3 交接项已明确（切块、入库、检索、RAG 1.0）
