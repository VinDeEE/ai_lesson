下面给你一套 **“能直接跑起来”的企业知识库 RAG 最小骨架**（Chroma 本地向量库 + LangChain + OpenAI）。你照着建目录、装依赖、跑两条命令就能问答，并且输出 **JSON（answer + citations + confidence + need_handoff）**。

> 依赖里会用到 `langchain-openai` 和 `langchain-chroma`（LangChain 官方把 OpenAI/Chroma 集成拆成了独立包）。([LangChain 文档](https://docs.langchain.org.cn/oss/python/integrations/text_embedding/openai?utm_source=chatgpt.com))

------

## 1) 先装依赖

在你的项目根目录（有 `main.py` 的那个目录）执行：

```bash
pip install -U langchain langchain-openai langchain-chroma langchain-community chromadb
```

（如果你要加载 PDF，再加：`pip install pypdf`）

------

## 2) 建议目录结构

```text
kb_bot/
  docs/                 # 放你的知识文件：md/txt（先用这两种最稳）
    faq.md
    sop.md
  data/
    chroma/             # 向量库持久化目录（自动生成）
  src/
    ingest.py           # 入库：加载→切分→写入向量库
    rag.py              # 查询：检索→生成→返回JSON
```

------

## 3) src/ingest.py（入库脚本）

把下面内容保存为 `src/ingest.py`：

```python
import argparse
import os
import shutil
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader


def load_documents(docs_dir: str):
    """
    最稳的方式：先只加载 md/txt，避免 unstructured 依赖导致的坑。
    """
    docs = []

    # .md
    md_loader = DirectoryLoader(
        docs_dir,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    docs.extend(md_loader.load())

    # .txt
    txt_loader = DirectoryLoader(
        docs_dir,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    docs.extend(txt_loader.load())

    return docs


def add_chunk_ids(chunks):
    """
    给每个 chunk 加一个稳定可引用的 chunk_id
    """
    counters = {}
    for d in chunks:
        src = d.metadata.get("source", "unknown")
        base = Path(src).name
        counters.setdefault(base, 0)
        counters[base] += 1
        d.metadata["chunk_id"] = f"{base}#{counters[base]}"
        d.metadata["source_file"] = base
    return chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs_dir", default="docs", help="知识库文件目录")
    parser.add_argument("--persist_dir", default="data/chroma", help="Chroma 持久化目录")
    parser.add_argument("--collection", default="kb", help="Chroma collection 名称")
    parser.add_argument("--rebuild", action="store_true", help="重建索引（会清空 persist_dir）")
    parser.add_argument("--chunk_size", type=int, default=800)
    parser.add_argument("--chunk_overlap", type=int, default=120)
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    if not docs_dir.exists():
        raise FileNotFoundError(f"docs_dir not found: {docs_dir.resolve()}")

    if args.rebuild and Path(args.persist_dir).exists():
        shutil.rmtree(args.persist_dir)

    # 1) load
    docs = load_documents(str(docs_dir))
    if not docs:
        raise RuntimeError(f"No documents found under {docs_dir.resolve()} (only .md/.txt are loaded).")

    # 2) split
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    chunks = add_chunk_ids(chunks)

    # 3) embed + store
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vs = Chroma(
        collection_name=args.collection,
        embedding_function=embeddings,
        persist_directory=args.persist_dir,
    )

    # 为了简单：每次 ingest 就 add（如果 rebuild 会先删目录）
    vs.add_documents(chunks)

    print(f"[OK] Loaded {len(docs)} docs, created {len(chunks)} chunks.")
    print(f"[OK] Persisted to: {Path(args.persist_dir).resolve()}  collection={args.collection}")


if __name__ == "__main__":
    # 可选：用 Python 临时输入 key（不建议写死在代码里）
    # import getpass
    # if not os.environ.get("OPENAI_API_KEY"):
    #     os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

    main()
```

------

## 4) src/rag.py（查询脚本）

把下面内容保存为 `src/rag.py`：

```python
import argparse
import json
import os
from typing import Any, Dict, List

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma


PROMPT = """你是企业知识库问答助手。你只能根据【证据】回答问题。
要求：
1) 如果证据不足以回答，必须返回 need_handoff=true，并说明原因；不要编造。
2) 回答要简洁、可执行。
3) citations 里要列出你用到的证据 chunk（source_file + chunk_id + quote）。
4) 输出必须是严格 JSON（不要 Markdown，不要多余文字）。

【问题】
{question}

【证据】
{context}

请输出 JSON，格式如下：
{{
  "answer": "...",
  "citations": [{{"source_file":"...","chunk_id":"...","quote":"..."}}],
  "confidence": "high|medium|low",
  "need_handoff": true|false,
  "handoff_reason": "..."
}}
"""


def build_context(docs) -> str:
    lines = []
    for d in docs:
        chunk_id = d.metadata.get("chunk_id", "")
        src = d.metadata.get("source_file", d.metadata.get("source", ""))
        text = d.page_content.strip().replace("\n", " ")
        quote = text[:220] + ("..." if len(text) > 220 else "")
        lines.append(f"- ({src} / {chunk_id}) {quote}")
    return "\n".join(lines)


def safe_json_loads(s: str) -> Dict[str, Any]:
    try:
        return json.loads(s)
    except Exception:
        # 兜底：返回一个尽量可用的结构，避免前端/调用方崩掉
        return {
            "answer": s.strip(),
            "citations": [],
            "confidence": "low",
            "need_handoff": True,
            "handoff_reason": "模型输出不是严格 JSON，已降级为原文返回。",
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question", help="要问的问题（用引号包起来）")
    parser.add_argument("--persist_dir", default="data/chroma")
    parser.add_argument("--collection", default="kb")
    parser.add_argument("--top_k", type=int, default=4)
    parser.add_argument("--model", default="gpt-4o-mini")
    args = parser.parse_args()

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vs = Chroma(
        collection_name=args.collection,
        embedding_function=embeddings,
        persist_directory=args.persist_dir,
    )

    retriever = vs.as_retriever(search_kwargs={"k": args.top_k})
    docs = retriever.get_relevant_documents(args.question)

    context = build_context(docs)

    llm = ChatOpenAI(model=args.model, temperature=0)
    msg = PROMPT.format(question=args.question, context=context)
    resp = llm.invoke(msg)

    data = safe_json_loads(resp.content)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    # 可选：用 Python 临时输入 key
    # import getpass
    # if not os.environ.get("OPENAI_API_KEY"):
    #     os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

    main()
```

> `gpt-4o-mini` 是 OpenAI 官方文档里稳定存在的模型名之一。([OpenAI开发者](https://developers.openai.com/api/docs/models/gpt-4o-mini?utm_source=chatgpt.com))

------

## 5) 运行方式（两步）

1）把你的知识文件放进 `docs/`（先用 md/txt）
2）入库（第一次建议重建）：

```bash
python src/ingest.py --docs_dir docs --persist_dir data/chroma --collection kb --rebuild
```

3）提问：

```bash
python src/rag.py "怎么申请退款？" --persist_dir data/chroma --collection kb
```

------

## 6) 你接下来最值得做的 3 个增强（按性价比排序）

1. **加评测集**：做 30 条 QA（10 命中、10 模糊、10 不存在），每天回归跑一遍
2. **拒答更稳**：根据检索相似度阈值/证据条数来强制 `need_handoff=true`
3. **Hybrid 检索**：向量 + 关键词（对 SOP/规则类文本提升很明显）

------

你现在把 `docs/` 里放上 2–3 个真实的 FAQ/SOP（可脱敏），然后告诉我你希望输出的引用格式（比如 `[sop.md#3]` 还是带原文 quote），我可以帮你把 **置信度规则 + 拒答策略** 调得更像线上客服知识库。