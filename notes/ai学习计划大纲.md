# AI 学习计划大纲（结合名词释义版）

适用目标：智能客服 / 企业知识库 / 坐席辅助

---

## 1. 学习目标

1. 建立完整 AI 技术地图：从 NLP、Transformer、LLM 到 RAG、Agent、MCP、LLMOps。
2. 能独立搭建一个可演示、可评测、可迭代的 AI 项目（优先：坐席辅助 Copilot）。
3. 具备工程化思维：指标、监控、安全、成本、发布。

---

## 2. 学习范围（对齐《AI 名词释义》）

1. 基础层：数学与优化、数据与特征工程、传统机器学习、深度学习结构。
2. 模型层：NLP、Transformer、LLM、对齐训练、解码策略。
3. 应用层：Prompt、Tool Calling、RAG、Agent、Workflow、MCP。
4. 工程层：评测体系、安全合规、可观测性、部署与 LLMOps。

---

## 3. 6 周主线计划（项目驱动）

### 第 1 周：LLM 与 NLP 基础 + Prompt 规范化

学习重点：
- NLP 基础：Token、Tokenization、Embedding、Language Modeling。
- Transformer 核心：Self-Attention、Positional Encoding、Decoder 思路。
- LLM 使用边界：Context Window、Hallucination、Temperature、Top-p。
- Prompt 规范：System Prompt、Prompt Template、结构化输出 spec。

必会术语：
- NLP、Transformer、Token、Embedding、Causal LM、Prompt Engineering、Decoding、Hallucination、spec。

本周产出：
- 一个结构化问答 Demo（固定 JSON 输出）。
- 一个 Prompt 模板库（问答、分类、抽取 3 套模板）。

验收标准：
- JSON 输出成功率 >= 95%。
- 能解释 Temperature/Top-p 对输出稳定性的影响。

---

### 第 2 周：Tool Calling + 最小 Agent

学习重点：
- Function Calling / Tool Calling 机制。
- Tool Schema（参数约束、必填项、枚举值、错误码）。
- 最小 Agent 循环：意图识别 -> 工具选择 -> 调用 -> 回复。

必会术语：
- Tool Calling、Function Calling、Tool Schema、Router、Executor、Guardrail。

本周产出：
- 3 个工具：`search_kb`、`get_order_status`、`create_ticket`（可先 mock）。
- 1 个最小 Agent：可自动选择工具并返回结果。

验收标准：
- 工具调用成功率 >= 90%。
- 对缺失参数能追问，不直接胡答。

---

### 第 3 周：RAG 1.0（最小可用）

学习重点：
- RAG 基本链路：Loader -> Chunking -> Embedding -> Vector DB -> Retrieval -> Generation。
- 检索基础：TopK、Cosine Similarity、Recall@K。
- 引用与溯源：Citation、Grounding。

必会术语：
- RAG、Chunking、Vectorization、Vector Database、ANN、Recall@K、Citation。

本周产出：
- 文档问答机器人（支持来源引用）。
- 首版知识库（FAQ + SOP 文档入库流程）。

验收标准：
- 20 条测试问题中，带引用回答覆盖率 >= 90%。
- 明显“无依据”问题可拒答或降级处理。

---

### 第 4 周：RAG 2.0（精度与稳定性优化）

学习重点：
- Hybrid Retrieval（向量检索 + BM25）。
- Re-ranker / Cross-Encoder 重排。
- Query Rewriting、多跳检索、上下文压缩。
- Prompt Injection 防护与知识可信度分级。

必会术语：
- Hybrid Retrieval、BM25、Re-ranker、MRR、nDCG、Context Compression、Prompt Injection。

本周产出：
- RAG 优化版：检索融合 + 重排 + 安全护栏。
- 30-50 条评测集（问题、标准答案、证据来源）。

验收标准：
- 相比第 3 周，正确率或有据率显著提升（建议 >= 10%）。
- 高风险注入场景下不执行恶意指令。

---

### 第 5 周：Agent 工作流（客服场景）

学习重点：
- 工作流编排：Planner、Router、Executor、Reflection。
- 状态管理：Short-term Memory、Working Memory。
- 多步任务闭环：收集信息 -> 查知识 -> 决策 -> 执行 -> 回填。

必会术语：
- Agent、Workflow Engine、Memory、ReAct、Orchestration、Reflection。

本周产出：
- 坐席辅助 Copilot 流程：
  - 自动抽取用户关键信息。
  - 查知识库给建议话术。
  - 低置信度自动创建工单。
  - 输出“用户回复 + 工单摘要 + 下一步动作”。

验收标准：
- 多步流程连续成功率 >= 85%。
- 关键状态可追踪、可回放。

---

### 第 6 周：MCP + LLMOps（上线前能力）

学习重点：
- MCP 接入：MCP Client / MCP Server。
- 可观测性：Tracing、Latency、Token Usage、Cost。
- 发布策略：限流、缓存、灰度、回滚。
- 线上评测：Offline + Online + A/B。

必会术语：
- MCP、Tracing、Observability、Rate Limiting、Canary Release、LLMOps、A/B Testing。

本周产出：
- 至少 1 个 MCP 工具接入（文件系统或内部服务）。
- 项目评测与监控看板（基础版本）。
- 最终演示版：可运行的客服 Copilot MVP。

验收标准：
- 能展示完整调用链（检索、工具、回复、耗时、成本）。
- 出现异常可定位到具体环节（检索、模型、工具或规则）。

---

## 4. 每周固定执行节奏

1. 学习输入（20 分钟）：只看一个主题，避免发散。
2. 代码实现（40-60 分钟）：必须有可运行结果。
3. 复盘沉淀（10 分钟）：记录失败样例、原因、改进动作。

---

## 5. 项目建议与优先级

1. 优先做：坐席辅助 Copilot（覆盖 RAG + Agent + Tool + 评测 + 工程化）。
2. 次选 A：企业知识库机器人（RAG 核心能力优先）。
3. 次选 B：智能质检系统（分类与规则融合场景）。

---

## 6. 里程碑验收清单

1. 基础能力：能清晰解释 NLP、Transformer、LLM、RAG、Agent、MCP 关系。
2. 系统能力：能从 0 到 1 搭出可运行 Demo。
3. 质量能力：有评测集、关键指标和优化记录。
4. 工程能力：有日志追踪、错误处理、发布与回滚策略。
5. 业务能力：能将方案映射到真实客服流程并说明 ROI。

---

## 7. 附：术语学习优先顺序（建议）

1. 第一层：NLP、Transformer、LLM、Prompt、Decoding。
2. 第二层：Embedding、RAG、Vector DB、Re-ranker、Citation。
3. 第三层：Tool Calling、Agent、Workflow、Memory、MCP。
4. 第四层：Evaluation、Guardrail、Tracing、LLMOps、Compliance。

这四层按周推进，和上面的 6 周主线一一对应。

---

## 8. 第 1 周每日任务清单（7 天版）

每日投入建议：60-90 分钟（20 分钟学习 + 40-60 分钟实现 + 10 分钟复盘）

### Day 1：搭建认知地图与开发环境

任务：
- 通读 [ai名词释义.md](D:/python_space/ai_lesson/docs/notes/ai名词释义.md) 的模块地图与 A/F/G/I 四个术语分区。
- 梳理一页笔记：NLP -> Transformer -> LLM -> Prompt -> RAG -> Agent -> MCP。
- 准备开发环境与项目目录（`src/`、`docs/notes/week1/prompts/`、`eval/`、`logs/`）。

当日产出：
- 一张个人术语关系图（可用 Markdown 列表表示）。
- 可运行的最小调用脚本（Hello LLM）。

验收：
- 能口头解释 “Transformer 与 LLM 的关系”。

### Day 2：NLP 与 Token 机制入门

任务：
- 学习：`Token`、`Tokenization`、`Embedding`、`Causal LM`。
- 实验同一段文本在不同提示写法下的 token 消耗。
- 记录上下文窗口（Context Window）对输入长度的限制表现。

当日产出：
- `docs/notes/week1/day2_token.md`（包含 3 组 token 对比实验）。

验收：
- 能解释“为什么精简提示词可降低成本与延迟”。

### Day 3：Prompt 模板与结构化输出

任务：
- 写 3 类模板：问答、分类、信息抽取。
- 统一输出 JSON 格式：`intent`、`entities`、`required_info`、`reply`。
- 增加 JSON 解析失败重试（至少 1 次）。

当日产出：
- `docs/notes/week1/prompts/` 下 3 个模板文件。
- 一个可运行的结构化输出脚本。

验收：
- 10 次测试中 JSON 可解析率 >= 90%。

### Day 4：解码策略实验（稳定性）

任务：
- 对比 `temperature`、`top_p`、`top_k`（若接口支持）对输出稳定性的影响。
- 同一输入跑 10 次，记录“格式一致性”和“内容漂移”。
- 为客服场景确定默认参数（偏稳定）。

当日产出：
- `docs/notes/week1/day4_decoding_eval.md`（表格记录参数与结果）。

验收：
- 给出一组推荐参数，并说明理由（稳定性/创造性权衡）。

### Day 5：客服问答格式化器 V1

任务：
- 实现“用户问题 -> 结构化 JSON -> 用户回复文本”的最小链路。
- 设计 15 条客服样例（催单、退款、改地址、投诉等）。
- 增加兜底策略：信息缺失时触发追问。

当日产出：
- `src/week1_formatter.py`（或同等脚本）。
- `eval/week1_cases.json`（15 条样例）。

验收：
- 15 条样例中，意图识别与字段抽取可用率 >= 80%。

### Day 6：质量提升与失败样例修复

任务：
- 复盘 Day 5 失败样例，按类别归因：提示不清晰、字段歧义、模型幻觉。
- 优化 prompt 与字段定义（`spec`）。
- 增加简单 Guardrail：禁止编造订单号、禁止承诺无依据补偿。

当日产出：
- `docs/notes/week1/day6_failure_analysis.md`。
- 优化后的 Prompt V2。

验收：
- 与 Day 5 对比，整体正确率提升 >= 10%。

### Day 7：周验收与下周准备

任务：
- 做一次周验收：20 条测试集完整跑通并记录结果。
- 输出一页周报：已掌握术语、已完成能力、问题清单、下周目标。
- 为第 2 周准备工具清单：`search_kb`、`get_order_status`、`create_ticket` 的参数草案。

当日产出：
- `docs/notes/week1/week1_review.md`。
- 第 2 周工具 `schema` 草稿。

验收：
- 满足第 1 周里程碑：可稳定输出结构化 JSON，能解释关键术语并展示 Demo。

---

## 9. 第 1 周完成定义（Definition of Done）

1. 已完成一个可运行的“客服问答格式化器”脚本。
2. 已沉淀 3 套 Prompt 模板和 20 条测试样例。
3. 已形成失败样例复盘文档和参数选择依据。
4. 已准备第 2 周 Tool Calling 的工具 schema 草案。



---

## 10. 第 2 周每日任务清单（Tool Calling + 最小 Agent）

每日投入建议：60-90 分钟（20 分钟学习 + 40-60 分钟实现 + 10 分钟复盘）

### Day 1：工具边界与 schema 设计

任务：
- 明确 3 个工具输入输出：`search_kb`、`get_order_status`、`create_ticket`。
- 统一字段命名、必填项、错误码、超时策略。
- 写工具契约文档。

当日产出：
- `docs/notes/week2/tool_schemas.md`。

验收：
- 每个工具都有请求/响应示例与失败场景定义。

### Day 2：实现 mock 工具层

任务：
- 编写本地 mock 工具（不依赖真实后端）。
- 为每个工具加参数校验与错误返回。
- 给工具加最小日志输出。

当日产出：
- `src/week2_tools.py`。

验收：
- 三个工具都可独立调用，错误输入不崩溃。

### Day 3：最小 Agent 分发器

任务：
- 实现“意图 -> 工具”的路由分发逻辑。
- 输入一条用户消息，自动选择对应工具。
- 返回“工具结果 + 用户可读回复”。

当日产出：
- `src/week2_agent.py`。

验收：
- 10 条样例中，工具选择正确率 >= 80%。

### Day 4：异常处理与追问机制

任务：
- 对缺关键参数的场景统一追问。
- 工具超时、返回空值、参数错误时给出可解释回复。
- 增加 Guardrail（禁止凭空承诺/编造结果）。

当日产出：
- `docs/notes/week2/exception_strategy.md`。

验收：
- 失败场景可稳定返回，不出现未处理异常。

### Day 5：构建 Week2 评测集

任务：
- 设计 30 条测试样例（意图分类、参数缺失、异常输入）。
- 标注期望工具和期望输出核心字段。
- 形成可回归的数据集。

当日产出：
- `eval/week2_agent_cases.jsonl`。

验收：
- 样例覆盖 3 工具全部主路径和异常路径。

### Day 6：批量回归与修正

任务：
- 跑完整评测集并统计：路由正确率、参数完整率、失败可解释率。
- 修复 Top5 失败模式。
- 更新 schema 与提示模板。

当日产出：
- `docs/notes/week2/day6_regression.md`。

验收：
- 路由正确率 >= 90%。

### Day 7：周验收与交接 Week3

任务：
- 输出周复盘（问题、修复、下周风险）。
- 记录 RAG 接入的接口预留位（`search_kb` 的真实实现替换点）。
- 评估当前 Agent 的可扩展性。

当日产出：
- `docs/notes/week2/week2_review.md`。

验收：
- 形成可接 RAG 的最小 Agent 骨架。

---

## 11. 第 2 周完成定义（Definition of Done）

1. 已有 `src/week2_tools.py` 与 `src/week2_agent.py` 可运行版本。
2. 已完成 30 条评测集并可回归。
3. 已形成工具 schema 和异常处理规范文档。

---

## 12. 第 3 周每日任务清单（RAG 1.0）

每日投入建议：60-90 分钟

### Day 1：知识库与切块策略

任务：
- 盘点文档来源（FAQ、SOP、政策规则）。
- 定义 chunk 策略（按标题优先，兼顾段落长度）。
- 记录 metadata 字段（来源、版本、更新时间）。

当日产出：
- `docs/notes/week3/chunk_strategy.md`。

验收：
- 可明确解释 chunk_size/chunk_overlap 选择依据。

### Day 2：Embedding 与索引实验

任务：
- 对同一批文档测试 2 套 embedding 参数组合。
- 比较召回质量与构建耗时。
- 记录 embedding 版本与索引版本关系。

当日产出：
- `docs/notes/week3/embedding_experiment.md`。

验收：
- 给出一套默认 embedding 参数。

### Day 3：入库流程固化

任务：
- 固化文档入库流程（清洗 -> 切块 -> 向量化 -> 持久化）。
- 增加重复入库和空文档保护。
- 输出入库统计（文档数、chunk 数、失败数）。

当日产出：
- `src/week3_ingest_runner.py`。

验收：
- 可稳定完成一次全量入库。

### Day 4：检索链路打通

任务：
- 以用户问题执行 TopK 检索。
- 输出检索结果分数和来源。
- 增加最低分阈值逻辑。

当日产出：
- `src/week3_retrieve.py`。

验收：
- 检索结果可解释，包含来源和分值。

### Day 5：带引用回答

任务：
- 组装上下文并生成回答。
- 回答必须附带 citation。
- 低置信度走拒答或转人工。

当日产出：
- `src/week3_rag_answer.py`。

验收：
- 20 条样例中引用覆盖率 >= 90%。

### Day 6：构建 RAG 评测集

任务：
- 设计 40 条 RAG 问题（命中、模糊、无答案）。
- 标注标准答案与证据片段。
- 添加拒答预期。

当日产出：
- `eval/week3_rag_cases.jsonl`。

验收：
- 评测集可用于后续 Week4 对比。

### Day 7：周复盘与风险梳理

任务：
- 分析错答与幻觉来源。
- 明确 Week4 优化优先级（检索、重排、压缩）。
- 形成周总结。

当日产出：
- `docs/notes/week3/week3_review.md`。

验收：
- 形成“RAG 1.0 -> RAG 2.0”优化路线图。

---

## 13. 第 3 周完成定义（Definition of Done）

1. 已完成可用的 RAG 1.0 链路（入库、检索、回答、引用）。
2. 已具备 40 条可回归评测样例。
3. 已形成下一周优化项优先级。

---

## 14. 第 4 周每日任务清单（RAG 2.0 优化）

每日投入建议：60-90 分钟

### Day 1：Hybrid Retrieval 设计

任务：
- 设计向量检索 + BM25 融合策略。
- 定义融合权重与候选召回规模。
- 明确不同问题类型路由策略。

当日产出：
- `docs/notes/week4/hybrid_design.md`。

验收：
- 给出融合算法与参数初值。

### Day 2：BM25 与向量融合实现

任务：
- 实现 BM25 检索基线。
- 与向量检索做结果融合。
- 输出融合前后命中差异。

当日产出：
- `src/week4_hybrid_retrieval.py`。

验收：
- 融合后 Recall@K 相比 Week3 有提升。

### Day 3：重排与查询改写

任务：
- 接入简单重排策略（规则或模型均可）。
- 对长问题做 query rewrite。
- 记录重排收益与开销。

当日产出：
- `src/week4_rerank.py`。

验收：
- Top1 命中率有可观察提升。

### Day 4：上下文压缩与提示防护

任务：
- 实现上下文压缩，控制 token 成本。
- 增加 Prompt Injection 基础防护。
- 明确“数据内容”和“系统指令”边界。

当日产出：
- `docs/notes/week4/context_and_security.md`。

验收：
- 注入样例不再触发越权回答。

### Day 5：安全评测集

任务：
- 新增攻击样例（注入、越权、敏感信息诱导）。
- 标注期望拒答策略。
- 建立安全回归脚本。

当日产出：
- `eval/week4_security_cases.jsonl`。

验收：
- 高风险样例拒答率达到预期（建议 >= 90%）。

### Day 6：指标看板与优化闭环

任务：
- 汇总 Week3 与 Week4 指标对比（有据率、正确率、耗时、成本）。
- 确定默认线上参数。
- 固化优化闭环流程。

当日产出：
- `docs/notes/week4/metrics_compare.md`。

验收：
- 指标对比完整，参数选择有依据。

### Day 7：周验收与交接 Week5

任务：
- 输出周复盘。
- 梳理 Agent 编排所需输入输出约束。
- 明确状态机草图。

当日产出：
- `docs/notes/week4/week4_review.md`。

验收：
- 已准备好进入多步 Agent 阶段。

---

## 15. 第 4 周完成定义（Definition of Done）

1. 已完成 Hybrid + 重排 + 安全防护基础能力。
2. 已具备安全评测集和对比指标。
3. RAG 质量、稳定性、可解释性均较 Week3 提升。

---

## 16. 第 5 周每日任务清单（Agent 工作流）

每日投入建议：60-90 分钟

### Day 1：工作流状态机设计

任务：
- 定义状态：`collect_info -> retrieve -> decide -> act -> respond`。
- 明确状态迁移条件与失败回滚路径。
- 输出工作流 spec。

当日产出：
- `docs/notes/week5/workflow_spec.md`。

验收：
- 可用状态机图解释端到端流程。

### Day 2：Planner 与 Router

任务：
- 实现 Planner（拆分任务步骤）。
- 实现 Router（选择 RAG 或工具）。
- 记录决策日志。

当日产出：
- `src/week5_planner_router.py`。

验收：
- 多场景下路由行为可解释。

### Day 3：记忆机制接入

任务：
- 增加短期会话记忆。
- 增加工作记忆（当前任务关键字段）。
- 定义记忆清理策略。

当日产出：
- `src/week5_memory.py`。

验收：
- 连续对话中上下文不丢失关键字段。

### Day 4：串联 RAG + Tool + Agent

任务：
- 把 Week2 工具层与 Week4 RAG 优化版接入 Agent。
- 跑完整“查知识 -> 决策 -> 工单”的闭环。
- 增加失败兜底路径。

当日产出：
- `src/week5_copilot_flow.py`。

验收：
- 端到端主流程可稳定跑通。

### Day 5：E2E 场景评测

任务：
- 设计 30 条端到端场景。
- 标注预期动作（回复/追问/工单）。
- 跑批量评测并记录成功率。

当日产出：
- `eval/week5_e2e_cases.jsonl`。

验收：
- E2E 成功率 >= 85%。

### Day 6：反思机制与稳定性增强

任务：
- 增加 Reflection 机制（失败后重试策略）。
- 增加动作前校验（字段完整性、权限、风险）。
- 修复高频失败路径。

当日产出：
- `docs/notes/week5/day6_reflection.md`。

验收：
- 重试后成功率有可量化提升。

### Day 7：周复盘与上线前准备

任务：
- 输出周总结与遗留风险。
- 梳理 Week6 需要接入的 MCP/监控项。
- 准备最终演示脚本。

当日产出：
- `docs/notes/week5/week5_review.md`。

验收：
- Agent 流程具备上线前基础形态。

---

## 17. 第 5 周完成定义（Definition of Done）

1. 已实现 RAG + Tool + Agent 的多步闭环。
2. 已完成 E2E 评测并达到目标成功率。
3. 已具备反思重试和稳定性策略。

---

## 18. 第 6 周每日任务清单（MCP + LLMOps）

每日投入建议：60-90 分钟

### Day 1：MCP 接入方案与边界

任务：
- 选定 1-2 个 MCP 能力接入点。
- 定义客户端调用边界与权限范围。
- 输出接入设计文档。

当日产出：
- `docs/notes/week6/mcp_design.md`。

验收：
- 能清晰说明为何需要 MCP，而非直接耦合工具。

### Day 2：MCP 适配层实现

任务：
- 实现 MCP 调用封装。
- 打通 Agent 到 MCP 工具的调用链。
- 增加调用失败兜底。

当日产出：
- `src/week6_mcp_adapter.py`。

验收：
- 至少 1 个 MCP 工具可稳定调用。

### Day 3：可观测性接入

任务：
- 增加关键日志：query、retrieval、tool_call、response。
- 增加 tracing id，支持一次请求全链路追踪。
- 记录 token、延迟、错误类型。

当日产出：
- `src/week6_observability.py`。

验收：
- 单次请求可完整回放。

### Day 4：成本与性能基线

任务：
- 统计平均延迟、P95 延迟、单请求 token 成本。
- 定义限流、缓存、降级策略。
- 固化默认配置。

当日产出：
- `docs/notes/week6/cost_latency_baseline.md`。

验收：
- 有明确可执行的性能与成本阈值。

### Day 5：线上评测与 A/B 准备

任务：
- 统一 Offline 与 Online 指标定义。
- 准备 A/B 对照方案（旧流程 vs 新流程）。
- 输出评测执行清单。

当日产出：
- `eval/week6_online_eval_plan.md`。

验收：
- 指标定义一致，能够按天回归。

### Day 6：发布与回滚演练

任务：
- 设计发布流程（灰度、监控、回滚条件）。
- 演练异常回滚路径。
- 补充应急手册。

当日产出：
- `docs/notes/week6/release_rollback.md`。

验收：
- 出现异常可在预定时间内回滚。

### Day 7：最终验收与总结

任务：
- 完成最终 Demo 演示。
- 汇总 6 周成果（代码、指标、文档、风险）。
- 输出下一阶段路线图。

当日产出：
- `docs/notes/week6/final_report.md`。

验收：
- 满足“可演示、可评测、可迭代”的项目目标。

---

## 19. 第 6 周完成定义（Definition of Done）

1. 已完成 MCP 接入与全链路可观测性。
2. 已形成上线策略（限流、灰度、回滚、评测）。
3. 已交付完整 6 周总结报告和下一阶段计划。
