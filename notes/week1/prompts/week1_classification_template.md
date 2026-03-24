# Week1 Classification Prompt Template

## Task
将用户输入分类到以下意图之一：
- 催单
- 退款
- 改地址
- 投诉
- 咨询
- 未知

## Input
{{user_query}}

## Output
{
  "intent": "...",
  "reason": "一句话解释分类依据"
}

## Constraints
- 只能返回 JSON。
- 不要虚构不存在的事实。
