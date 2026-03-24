# Week2 周复盘（Tool Calling + 最小 Agent）

周期：Week2
日期：2026-03-06

## 1. 本周目标完成情况

- 目标 1：完成 3 个工具 schema 设计。已完成。
- 目标 2：完成 mock 工具实现并可单独调用。已完成。
- 目标 3：打通最小 Agent 路由闭环。已完成。
- 目标 4：建立回归集并完成批量评测。已完成。

## 2. 交付物清单

- `docs/notes/week2/tool_schemas.md`
- `src/week2_tools.py`
- `src/week2_agent.py`
- `eval/week2_agent_cases.jsonl`（30 条）
- `src/week2_eval.py`
- `docs/notes/week2/day6_regression.md`
- `docs/notes/week2/exception_strategy.md`

## 3. 指标结果（Day6）

- 通过率：100.00%
- 意图准确率：100.00%
- 动作准确率：100.00%
- 工具准确率：100.00%

## 4. 关键改进点

1. 修复了中文语境下 `order_id` 正则匹配不稳定问题。
2. 增加了意图判定优先级，避免“退款 + 单号”误路由到催单。
3. 固化了工具错误码结构，统一异常处理策略。

## 5. 已知限制

1. 当前工具层仍为 mock，实现了接口稳定性但未接真实业务系统。
2. 退款/投诉等场景仍以“先追问再执行”为主，尚未做多轮会话状态记忆。
3. 评测集为当前规则定制，Week3 接入 RAG 后需扩展题型。

## 6. Week3 交接计划

1. 先完成文档切块策略与 metadata 设计。
2. 打通入库与检索脚本，形成 RAG 1.0 链路。
3. 基于 Week2 Agent 预留接口，替换 `search_kb` 为真实检索。
