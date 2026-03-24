# Week3 Day2 - Embedding Experiment（参数对照实验）

目标：比较两套入库参数在召回质量与成本上的差异，形成 Week3 默认配置。

---

## 1. 实验配置

### A 组（基线）
- `chunk_size=600`
- `chunk_overlap=120`
- `embedding_model=gemini-embedding-001`

### B 组（小块）
- `chunk_size=450`
- `chunk_overlap=80`
- `embedding_model=gemini-embedding-001`

---

## 2. 执行命令

```powershell
python src/week3_ingest_runner.py --profile baseline --collection kb_w3_a
python src/week3_ingest_runner.py --profile compact --collection kb_w3_b
```

---

## 3. 对比维度

- 入库耗时
- chunk 总数
- 检索召回质量（Recall@K）
- 回答有据率（citation 覆盖）
- 平均响应延迟

---

## 4. 结果记录表

| 维度 | A 组（600/120） | B 组（450/80） | 结论 |
|---|---:|---:|---|
| 入库耗时 |  |  |  |
| chunk 数量 |  |  |  |
| Recall@K |  |  |  |
| 有据率 |  |  |  |
| 延迟 |  |  |  |

---

## 5. 默认配置决策

- 当前建议默认：`A 组（600/120）`
- 原因：
  1. 与现有代码和索引结构一致，迁移成本最低。
  2. 语义完整度更稳，适合 SOP 场景。

> 若 B 组 Recall@K 显著更优，再切换到 B。
