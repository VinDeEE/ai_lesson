# Week3 Day1 - Chunk Strategy（切块与 Metadata 设计）

目标：在当前 `src/ingest.py` 的实现基础上，确定一套可解释、可回归的切块策略，支撑 RAG 1.0 的召回稳定性。

---

## 1. 文档分层与优先级

- P0（高频规则）：退款、物流、投诉处理 SOP。
- P1（通用说明）：FAQ、规则说明。
- P2（背景材料）：学习笔记与扩展资料。

建议：RAG 主检索默认只入 P0 + P1，避免噪声过大。

---

## 2. 切块策略（当前默认）

当前代码参数（`src/ingest.py`）：
- `chunk_size=600`
- `chunk_overlap=120`
- 分隔符优先级：`\n\n` -> `\n` -> 中文标点 -> 英文标点 -> 空格

### 2.1 参数建议

- 业务 SOP（结构化强）：`chunk_size=500~700`, `overlap=80~120`
- FAQ（短问短答）：`chunk_size=300~500`, `overlap=50~80`
- 长段说明文：`chunk_size=700~900`, `overlap=120~180`

### 2.2 设计原则

1. 优先语义完整，不在句中硬切。
2. overlap 只用于承接上下文，不宜过大（会引入重复噪声）。
3. 一个 chunk 只承载一个核心事实，避免多主题混杂。

---

## 3. Metadata 设计

建议每个 chunk 至少包含：
- `source`：原始文件绝对路径
- `source_file`：文件名
- `chunk_id`：文件内序号（例如 `refund_sop#12`）
- `domain`：`refund/shipping/complaint/general`
- `doc_version`：文档版本号（可选）
- `updated_at`：切块时间戳

> 当前 `ingest.py` 已含 `source/source_file/chunk_id/text`，Week3 可在此基础上扩展 `domain/doc_version`。

---

## 4. 质量检查清单（切块后）

1. 空 chunk 比例 = 0
2. 超短 chunk（<50 字）比例 < 10%
3. 重复 chunk 比例 < 5%
4. 关键 SOP 条目是否完整落入 chunk（人工抽样 20 条）

---

## 5. Week3 执行建议

1. 先固定一套基线参数（600/120）构建索引。
2. 再做 1 组对照参数（450/80 或 800/160）。
3. 用同一评测集比较 Recall@K、有据率、回答稳定性。

---

## 6. 结论（Day1）

- 本周采用基线参数：`chunk_size=600`, `chunk_overlap=120`。
- 先保证可用链路，再在 Week4 做检索层优化（Hybrid/Rerank）。
