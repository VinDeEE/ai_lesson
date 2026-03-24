# Week2 Day1 - Tool Schemas（工具契约文档）

目标：定义 `search_kb`、`get_order_status`、`create_ticket` 的统一调用契约，作为 Agent 的稳定接口层。

---

## 1. 全局约定

### 1.1 通用字段

- `trace_id`：请求链路 ID（用于日志追踪）。
- `request_id`：本次工具调用唯一 ID。
- `ts`：UTC 时间戳（ISO 8601）。
- `success`：调用是否成功。
- `error`：错误对象（失败时必填）。

### 1.2 通用错误结构

```json
{
  "code": "INVALID_PARAM",
  "message": "order_id is required",
  "retryable": false,
  "details": {
    "field": "order_id"
  }
}
```

### 1.3 错误码规范

- `INVALID_PARAM`：参数不合法或缺失。
- `NOT_FOUND`：资源不存在（如订单不存在）。
- `PERMISSION_DENIED`：无权限调用。
- `TIMEOUT`：调用超时。
- `RATE_LIMITED`：被限流。
- `UPSTREAM_UNAVAILABLE`：上游服务不可用。
- `INTERNAL_ERROR`：内部错误。

### 1.4 超时与重试策略（建议）

- 工具默认超时：`1500ms`。
- `retryable=true` 的错误允许最多重试 `2` 次。
- 仅对 `TIMEOUT`、`RATE_LIMITED`、`UPSTREAM_UNAVAILABLE` 自动重试。
- 指数退避：`200ms` -> `400ms`。

---

## 2. Tool: `search_kb`

用途：检索知识库并返回候选证据，用于后续回答生成。

### 2.1 入参 Schema

```json
{
  "type": "object",
  "required": ["query"],
  "properties": {
    "query": { "type": "string", "minLength": 2, "maxLength": 500 },
    "top_k": { "type": "integer", "minimum": 1, "maximum": 10, "default": 4 },
    "domain": { "type": "string", "enum": ["shipping", "refund", "complaint", "general"], "default": "general" },
    "trace_id": { "type": "string" }
  },
  "additionalProperties": false
}
```

### 2.2 出参 Schema

```json
{
  "type": "object",
  "required": ["success", "results", "request_id", "ts"],
  "properties": {
    "success": { "type": "boolean" },
    "request_id": { "type": "string" },
    "ts": { "type": "string" },
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source", "chunk_id", "score", "content"],
        "properties": {
          "source": { "type": "string" },
          "chunk_id": { "type": "string" },
          "score": { "type": "number" },
          "content": { "type": "string" }
        }
      }
    },
    "error": { "type": "object" }
  }
}
```

### 2.3 请求示例

```json
{
  "query": "退款多久到账",
  "top_k": 3,
  "domain": "refund",
  "trace_id": "tr_20260306_001"
}
```

### 2.4 成功响应示例

```json
{
  "success": true,
  "request_id": "req_kb_001",
  "ts": "2026-03-06T09:30:00Z",
  "results": [
    {
      "source": "refund_sop.md",
      "chunk_id": "refund_12",
      "score": 0.87,
      "content": "退款审核通过后，原路退回通常在 1-3 个工作日到账。"
    }
  ]
}
```

### 2.5 失败响应示例

```json
{
  "success": false,
  "request_id": "req_kb_002",
  "ts": "2026-03-06T09:31:00Z",
  "results": [],
  "error": {
    "code": "TIMEOUT",
    "message": "search_kb upstream timeout",
    "retryable": true,
    "details": {}
  }
}
```

---

## 3. Tool: `get_order_status`

用途：按订单号查询订单状态、物流阶段与最近更新时间。

### 3.1 入参 Schema

```json
{
  "type": "object",
  "required": ["order_id"],
  "properties": {
    "order_id": { "type": "string", "minLength": 6, "maxLength": 64 },
    "phone_tail": { "type": "string", "pattern": "^[0-9]{4}$" },
    "trace_id": { "type": "string" }
  },
  "additionalProperties": false
}
```

### 3.2 出参 Schema

```json
{
  "type": "object",
  "required": ["success", "request_id", "ts"],
  "properties": {
    "success": { "type": "boolean" },
    "request_id": { "type": "string" },
    "ts": { "type": "string" },
    "order": {
      "type": "object",
      "properties": {
        "order_id": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["CREATED", "PAID", "SHIPPED", "IN_TRANSIT", "DELIVERED", "CANCELLED", "REFUNDING", "REFUNDED"]
        },
        "carrier": { "type": "string" },
        "last_event": { "type": "string" },
        "updated_at": { "type": "string" }
      }
    },
    "error": { "type": "object" }
  }
}
```

### 3.3 请求示例

```json
{
  "order_id": "A123456",
  "phone_tail": "8899",
  "trace_id": "tr_20260306_002"
}
```

### 3.4 成功响应示例

```json
{
  "success": true,
  "request_id": "req_order_001",
  "ts": "2026-03-06T09:35:00Z",
  "order": {
    "order_id": "A123456",
    "status": "IN_TRANSIT",
    "carrier": "SF",
    "last_event": "已到达上海转运中心",
    "updated_at": "2026-03-06T08:50:00Z"
  }
}
```

### 3.5 失败响应示例

```json
{
  "success": false,
  "request_id": "req_order_002",
  "ts": "2026-03-06T09:36:00Z",
  "error": {
    "code": "NOT_FOUND",
    "message": "order not found",
    "retryable": false,
    "details": {
      "order_id": "X000000"
    }
  }
}
```

---

## 4. Tool: `create_ticket`

用途：在无法自动闭环时创建人工处理工单。

### 4.1 入参 Schema

```json
{
  "type": "object",
  "required": ["title", "content", "priority", "user_id"],
  "properties": {
    "title": { "type": "string", "minLength": 5, "maxLength": 120 },
    "content": { "type": "string", "minLength": 10, "maxLength": 3000 },
    "priority": { "type": "string", "enum": ["P0", "P1", "P2", "P3"] },
    "category": { "type": "string", "enum": ["shipping", "refund", "complaint", "other"], "default": "other" },
    "user_id": { "type": "string", "minLength": 1, "maxLength": 64 },
    "order_id": { "type": "string", "minLength": 6, "maxLength": 64 },
    "trace_id": { "type": "string" }
  },
  "additionalProperties": false
}
```

### 4.2 出参 Schema

```json
{
  "type": "object",
  "required": ["success", "request_id", "ts"],
  "properties": {
    "success": { "type": "boolean" },
    "request_id": { "type": "string" },
    "ts": { "type": "string" },
    "ticket": {
      "type": "object",
      "properties": {
        "ticket_id": { "type": "string" },
        "status": { "type": "string", "enum": ["OPEN", "PROCESSING", "RESOLVED", "CLOSED"] },
        "sla_hours": { "type": "integer" },
        "created_at": { "type": "string" }
      }
    },
    "error": { "type": "object" }
  }
}
```

### 4.3 请求示例

```json
{
  "title": "用户投诉配送延迟",
  "content": "订单 A123456 长时间未更新物流，用户要求加急处理。",
  "priority": "P1",
  "category": "shipping",
  "user_id": "u_9527",
  "order_id": "A123456",
  "trace_id": "tr_20260306_003"
}
```

### 4.4 成功响应示例

```json
{
  "success": true,
  "request_id": "req_ticket_001",
  "ts": "2026-03-06T09:40:00Z",
  "ticket": {
    "ticket_id": "T202603060001",
    "status": "OPEN",
    "sla_hours": 24,
    "created_at": "2026-03-06T09:40:00Z"
  }
}
```

### 4.5 失败响应示例

```json
{
  "success": false,
  "request_id": "req_ticket_002",
  "ts": "2026-03-06T09:41:00Z",
  "error": {
    "code": "INVALID_PARAM",
    "message": "priority must be one of P0/P1/P2/P3",
    "retryable": false,
    "details": {
      "field": "priority"
    }
  }
}
```

---

## 5. Agent 调用约束（Week2 统一规则）

1. 若用户意图为催单且有 `order_id`，优先调用 `get_order_status`。
2. 若用户问题为规则咨询，优先调用 `search_kb`。
3. 若低置信度、信息冲突或用户强投诉，调用 `create_ticket`。
4. 禁止跳过参数校验直接调用工具。
5. 工具失败后必须先给用户可解释反馈，再决定重试或转工单。

---

## 6. 待确认项（进入 Day2 前）

1. `priority` 映射规则是否按业务严重度自动计算。
2. `search_kb` 的 `domain` 是否由 Agent 自动识别，还是由上游传入。
3. `get_order_status` 是否要求强校验 `phone_tail`。
4. `create_ticket` 的 `sla_hours` 是否按 `priority` 固定映射。
