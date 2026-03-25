# AI Lesson Workspace

这是一个面向「智能客服 / 知识库 / 坐席辅助」的 AI 学习与实战仓库。

当前状态：
- Week1 已完成（结构化输出 + Prompt + 基础评测）
- Week2 已完成（Tool Calling + 最小 Agent + 回归评测）
- Week3-Week6 计划已落地到文档并预建目录

## 1. 核心入口

- 学习总纲：[docs/notes/ai学习计划大纲.md](./docs/notes/ai学习计划大纲.md)
- 名词释义：[docs/notes/ai名词释义.md](./docs/notes/ai名词释义.md)
- Week1 记录：[docs/notes/week1](./docs/notes/week1)
- Week2 记录：[docs/notes/week2](./docs/notes/week2)

## 2. 目录结构（当前）

```text
ai_lesson/
  docs/
    notes/
      ai名词释义.md
      ai学习计划大纲.md
      week1/
      week2/
      week3/
      week4/
      week5/
      week6/
  eval/
    qa_samples.jsonl
    week1_cases.json
    week2_agent_cases.jsonl
  src/
    rag_core.py
    ingest.py
    ask.py
    evaluate.py
    week1_formatter.py
    week2_tools.py
    week2_agent.py
    week2_eval.py
  data/
    chroma/
  .env.example
  requirements.txt
```

## 3. 环境准备

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

然后在 `.env` 中填写 `GEMINI_API_KEY`。

## 4. RAG 主线命令

### 4.1 入库

```powershell
python src/ingest.py
```

### 4.2 单次问答

```powershell
python src/ask.py "你的问题"
python src/ask.py "你的问题" --vector_only
```

### 4.3 批量评测

```powershell
python src/evaluate.py --dataset eval/qa_samples.jsonl
```

## 5. Week1/Week2 可运行脚本

### 5.1 Week1：结构化格式化器

```powershell
python src/week1_formatter.py "订单 A123456 什么时候到" --pretty
```

### 5.2 Week2：工具层（mock）

```powershell
python src/week2_tools.py search_kb "退款多久到账" --domain refund --top_k 2
python src/week2_tools.py get_order_status A123456 --phone_tail 8899
python src/week2_tools.py create_ticket "用户投诉配送延迟" "订单 A123456 超过24小时未更新物流，请专员介入。" P1 u_9527 --category shipping --order_id A123456
```

### 5.3 Week2：最小 Agent

```powershell
python src/week2_agent.py "订单 A123456 什么时候到" --user_id u_1001 --trace_id tr_demo_001
```

### 5.4 Week2：回归评测

```powershell
python src/week2_eval.py --dataset eval/week2_agent_cases.jsonl --output_md docs/notes/week2/day6_regression.md
```

## 6. 当前进度快照

- Week1 产物：
  - `src/week1_formatter.py`
  - `eval/week1_cases.json`
- Week2 产物：
  - `docs/notes/week2/tool_schemas.md`
  - `src/week2_tools.py`
  - `src/week2_agent.py`
  - `src/week2_eval.py`
  - `eval/week2_agent_cases.jsonl`
  - `docs/notes/week2/day6_regression.md`
  - `docs/notes/week2/week2_review.md`

## 7. 下一步（Week3）

1. 完成切块策略文档：`docs/notes/week3/chunk_strategy.md`
2. 打通 RAG 1.0 链路（入库 -> 检索 -> 回答 -> 引用）
3. 将 Week2 的 `search_kb` mock 替换为真实检索实现

## 8. 常见问题

- `GEMINI_API_KEY missing`：检查仓库根目录 `.env` 是否存在并包含 `GEMINI_API_KEY`。
- `No .md/.txt documents found`：确认 `docs/` 下有可入库文档。
- 回答不稳定：优先调参 `chunk_size`、`chunk_overlap`、`top_k`、提示词约束。
