# AI Study Starter

这是一个从零开始的 AI 学习项目骨架，目标是让你按照「概念 -> 代码 -> 可评测」的方式稳定推进。

当前版本先落地 A 方向：企业知识库机器人（RAG）。
完整 6 周学习节奏见 [LEARNING_PLAN.md](./LEARNING_PLAN.md)。
说明：`docs/` 里有你之前的学习笔记，部分内容提到 OpenAI/LangChain，那是历史资料；当前可运行代码已切换为 Gemini。

## 1. 项目结构

```text
ai_lesson/
  docs/                  # 你的知识库文档（md/txt）
    notes/               # 学习笔记归档
  eval/                  # 评测集（jsonl）
  data/                  # 本地向量索引目录（json）
  src/
    rag_core.py          # 共用核心逻辑（检索 + 生成 + 解析）
    ingest.py            # 文档入库
    ask.py               # 单次提问
    evaluate.py          # 批量评测
  .env.example
  requirements.txt
```

## 2. 从零到跑通（20 分钟）

1. 创建虚拟环境并安装依赖

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. 配置环境变量

```powershell
Copy-Item .env.example .env
```

然后编辑 `.env`，填入你的 `GEMINI_API_KEY`。

3. 准备知识文档

项目内已经放了 3 份示例文档，并已复制你原项目的 4 份学习文档到 `docs/`，可以直接入库。

激活环境（以下命令默认使用 PowerShell）：

```powershell
.venv\Scripts\Activate.ps1
```

4. 入库

```powershell
python src/ingest.py --docs_dir docs --persist_dir data/chroma --collection kb --chunk_size 600 --chunk_overlap 120 --embedding_model gemini-embedding-001 --batch_size 64
```

5. 提问

```powershell
python src/ask.py "你的问题" --persist_dir data/chroma --collection kb --top_k 4
```

你会得到结构化 JSON：

- `answer`
- `citations`
- `confidence`
- `need_handoff`
- `handoff_reason`

6. 跑评测

```powershell
python src/evaluate.py --dataset eval/qa_samples.jsonl
```

## 3. 学习节奏（建议）

### 第 1 周：结构化输出

- 目标：让模型稳定返回 JSON
- 产出：定义 `answer/citations/confidence/need_handoff` 结构并跑通

### 第 2 周：工具化与异常处理

- 目标：引入 `create_ticket/get_order_status` 等工具（mock 先行）
- 产出：低置信度时自动走工单策略

### 第 3 周：RAG 1.0

- 目标：文档入库 -> 检索 -> 回答可引用
- 产出：能回答 FAQ 且能列证据来源

### 第 4 周：RAG 2.0 + 评测迭代

- 目标：提升稳定性与准确率
- 产出：固定评测集 + 每日回归结果

## 4. 常见问题

1. `GEMINI_API_KEY missing`
   - 说明 `.env` 没填或没加载，检查仓库根目录 `.env`。

2. `No .md/.txt documents found`
   - 确认 `docs/` 里有 UTF-8 编码的 `.md` 或 `.txt` 文件。

3. 回答不稳定
   - 先调 `chunk_size/chunk_overlap/top_k`，再考虑换模型。

4. `Gemini API error HTTP 404 ... embedContent`
   - 把 `.env` 的 `EMBEDDING_MODEL` 改成 `gemini-embedding-001`。

5. `Gemini API error HTTP 404 ... generateContent`
   - 把 `.env` 的 `GEMINI_MODEL` 改成你账号可用模型（例如 `gemini-2.0-flash`）。
   - 或配置 `GEMINI_MODEL_FALLBACKS`，代码会自动尝试备用模型。

## 5. 下一步建议

1. 将 `docs/` 里的示例文档逐步替换成你的真实业务 FAQ/SOP（先 10-20 条即可）。
2. 补充 `eval/qa_samples.jsonl` 到 30-50 条，覆盖命中/模糊/拒答场景。
3. 再加工具层，把 `need_handoff=true` 的问题自动创建工单。
