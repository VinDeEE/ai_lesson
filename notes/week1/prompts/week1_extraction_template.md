# Week1 Extraction Prompt Template

## Task
从用户文本中抽取结构化字段。

## Input
{{user_query}}

## Target Fields
- order_id
- phone_tail
- refund_reason
- new_address
- issue_detail

## Output
{
  "entities": {
    "order_id": "",
    "phone_tail": "",
    "refund_reason": "",
    "new_address": "",
    "issue_detail": ""
  }
}

## Constraints
- 未提及字段返回空字符串。
- 仅输出 JSON。
