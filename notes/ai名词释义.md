# AI 名词释义（补充完整版）

目标：把 AI 相关模块和专业名词做成一份可长期查阅的速查表。  
阅读建议：先看「模块地图」，再按需查「术语词典」。

---

## 1) AI 全景模块地图（从底到顶）

1. 数学与统计基础
- 线性代数、概率统计、微积分、最优化、信息论

2. 数据工程与数据治理
- 数据采集、清洗、标注、去重、特征工程、数据版本管理

3. 机器学习范式
- 监督学习、无监督学习、半监督学习、自监督学习、强化学习

4. 传统机器学习算法
- 线性回归、逻辑回归、SVM、决策树、随机森林、XGBoost、聚类、降维

5. 深度学习基础
- MLP、CNN、RNN、LSTM、GRU、Attention、Transformer

6. NLP 与文本理解
- 分词、词向量、语言模型、序列建模、文本分类、信息抽取

7. LLM 与生成式 AI
- 预训练、指令微调、对齐、推理解码、上下文管理、函数调用

8. 检索增强（RAG）与知识系统
- Embedding、向量库、检索、重排、引用、知识更新

9. Agent 与工具生态
- Tool/Skill、工作流编排、多 Agent、MCP、记忆系统

10. 多模态 AI
- 文本+图像+语音+视频联合建模，VLM、ASR、TTS、OCR

11. 模型评测与安全治理
- 质量评测、幻觉评估、红队测试、内容安全、合规治理

12. 工程化与部署（MLOps/LLMOps）
- 训练平台、模型服务、监控告警、A/B 测试、CI/CD、成本优化

---

## 2) 核心关系一图流

`模型能力(LLM)` + `外部知识(RAG)` + `工具调用(Tool/Skill)` + `执行编排(Agent)` + `标准协议(MCP)` = 可落地 AI 系统

---

## 3) 专业名词词典（按主题）

### A. 通用概念

- AI（Artificial Intelligence）：人工智能总称。
- ML（Machine Learning）：让模型从数据中学习规律。
- DL（Deep Learning）：基于深层神经网络的机器学习。
- GenAI（Generative AI）：生成文本/图像/音频等内容的 AI。
- AGI（Artificial General Intelligence）：通用人工智能概念。
- AIGC（AI Generated Content）：AI 生成内容。
- Foundation Model：基础模型，可迁移到多任务。
- Multimodal：多模态，处理多种数据类型。
- Inference：推理，模型上线时的前向计算过程。
- Training：训练，用数据更新模型参数。
- Finetuning：微调，在预训练模型上做任务适配。
- Transfer Learning：迁移学习，把已学能力迁移到新任务。
- Zero-shot：零样本，不提供任务示例直接完成任务。
- One-shot：单样本，给 1 个示例。
- Few-shot：小样本，给少量示例。

### B. 数学与优化

- Tensor：张量，深度学习中的基础数据结构。
- Vector：向量。
- Matrix：矩阵。
- Gradient：梯度，损失对参数的导数。
- Backpropagation：反向传播，计算梯度的方法。
- Loss Function：损失函数，衡量预测误差。
- Objective Function：目标函数，优化时要最小化/最大化的函数。
- Convex Optimization：凸优化。
- SGD：随机梯度下降。
- Momentum：动量优化。
- Adam：常用自适应优化器。
- AdamW：带权重衰减的 Adam。
- Learning Rate：学习率。
- LR Scheduler：学习率调度器。
- Warmup：学习率预热。
- Weight Decay：权重衰减，常用于正则化。
- Regularization：正则化，防止过拟合。
- Dropout：随机失活，提升泛化。
- BatchNorm：批标准化。
- LayerNorm：层标准化（Transformer 常用）。
- Overfitting：过拟合。
- Underfitting：欠拟合。
- Bias-Variance Tradeoff：偏差-方差权衡。
- Entropy：熵，不确定性度量。
- Cross Entropy：交叉熵损失。
- KL Divergence：KL 散度，分布差异度量。
- Perplexity（PPL）：困惑度，语言模型常用指标。

### C. 数据与特征工程

- Dataset：数据集。
- Train/Validation/Test Split：训练/验证/测试集划分。
- Data Augmentation：数据增强。
- Label：标签。
- Annotation：标注。
- Data Leakage：数据泄漏。
- Sampling：采样。
- Class Imbalance：类别不平衡。
- Feature：特征。
- Feature Engineering：特征工程。
- Transform：数据变换（标准化、归一化、编码、增强等处理步骤）。
- Feature Store：特征仓库。
- ETL/ELT：抽取转换加载流程。
- Data Pipeline：数据管道。
- Data Drift：数据漂移。
- Concept Drift：概念漂移。

### D. 传统机器学习

- Linear Regression：线性回归。
- Logistic Regression：逻辑回归。
- Naive Bayes：朴素贝叶斯。
- KNN：K 近邻。
- SVM：支持向量机。
- Decision Tree：决策树。
- Random Forest：随机森林。
- Gradient Boosting：梯度提升树。
- XGBoost：高性能梯度提升框架。
- LightGBM：高效 GBDT 框架。
- CatBoost：支持类别特征较强的 GBDT。
- K-means：K 均值聚类。
- DBSCAN：基于密度的聚类算法。
- Hierarchical Clustering：层次聚类。
- PCA：主成分分析降维。
- t-SNE：非线性可视化降维。
- UMAP：流形学习降维方法。
- ROC-AUC：二分类排序能力指标。
- Precision / Recall / F1：分类精确率/召回率/F1。

### E. 深度学习与网络结构

- Neuron：神经元。
- MLP：多层感知机。
- Activation Function：激活函数。
- ReLU / GELU / SiLU：常见激活函数。
- CNN：卷积神经网络。
- Convolution：卷积操作。
- Pooling：池化。
- RNN：循环神经网络。
- LSTM：长短期记忆网络。
- GRU：门控循环单元。
- Seq2Seq：序列到序列架构。
- Encoder-Decoder：编码器-解码器结构。
- Attention：注意力机制。
- Self-Attention：自注意力。
- Cross-Attention：交叉注意力。
- Multi-Head Attention：多头注意力。
- Transformer：基于注意力的主流架构。
- Positional Encoding：位置编码。
- Residual Connection：残差连接。
- Feed-Forward Network（FFN）：前馈子层。
- MoE（Mixture of Experts）：专家混合架构。
- Sparse Attention：稀疏注意力。
- Long Context：长上下文建模能力。

### F. NLP（自然语言处理）专项

- NLP（Natural Language Processing）：自然语言处理。
- NLU：自然语言理解。
- NLG：自然语言生成。
- Token：词元。
- Tokenization：分词/词元化。
- Subword：子词切分。
- BPE：字节对编码分词算法。
- WordPiece：子词分词算法。
- SentencePiece：无空格语言友好的分词方案。
- Vocabulary：词表。
- Embedding：向量表示。
- Word Embedding：词向量。
- Contextual Embedding：上下文化向量。
- Static Embedding：静态词向量（如 Word2Vec）。
- Word2Vec：经典词向量方法。
- GloVe：基于共现统计的词向量。
- FastText：支持子词信息的词向量。
- Language Modeling：语言建模。
- Causal LM：自回归语言模型。
- Masked LM：掩码语言模型。
- Next Token Prediction：下一词预测任务。
- POS Tagging：词性标注。
- NER：命名实体识别。
- RE（Relation Extraction）：关系抽取。
- IE（Information Extraction）：信息抽取。
- Sentiment Analysis：情感分析。
- Text Classification：文本分类。
- Text Summarization：文本摘要。
- Machine Translation：机器翻译。
- Dependency Parsing：依存句法分析。
- Coreference Resolution：指代消解。
- Prompt Template：提示模板。
- Prompt Engineering：提示词工程。
- System Prompt：系统提示词。
- Chain-of-Thought（CoT）：思维链提示。
- Self-Consistency：多路径采样一致性。
- Retrieval-Augmented Prompting：检索增强提示。

### G. LLM（大模型）与训练对齐

- LLM（Large Language Model）：大语言模型。
- VLM（Vision-Language Model）：视觉语言模型。
- Pretraining：预训练。
- Continued Pretraining：继续预训练。
- SFT（Supervised Fine-Tuning）：监督微调。
- Instruction Tuning：指令微调。
- RLHF：基于人类反馈强化学习。
- RLAIF：基于 AI 反馈强化学习。
- PPO：常见策略优化算法。
- DPO：直接偏好优化。
- ORPO/KTO：偏好优化变体方法。
- Alignment：对齐，控制模型行为与价值边界。
- Safety Tuning：安全对齐微调。
- Reward Model：奖励模型。
- Preference Data：偏好数据。
- Distillation：知识蒸馏。
- Parameter-Efficient Fine-Tuning（PEFT）：参数高效微调。
- LoRA：低秩适配微调。
- QLoRA：量化+LoRA 的微调方法。
- Adapters：插入式轻量模块。
- Full Fine-Tuning：全参数微调。
- Context Window：上下文窗口长度。
- KV Cache：推理阶段 key/value 缓存。
- Speculative Decoding：投机解码，加速生成。
- Decoding：解码策略总称。
- Greedy Search：贪心解码。
- Beam Search：束搜索。
- Top-k Sampling：按概率前 k 采样。
- Top-p Sampling：核采样。
- Temperature：温度参数，控制随机性。
- Stop Sequence：停止词序列。
- Hallucination：幻觉，生成不实内容。

### H. RAG（检索增强生成）与知识库

- RAG：检索增强生成。
- Knowledge Base：知识库。
- Document Loader：文档加载器。
- Chunking：文档切块。
- Sliding Window：滑动窗口切分。
- Metadata：元数据（来源、时间、权限等）。
- Embedding Model：嵌入模型。
- Vectorization：向量化。
- Vector Database：向量数据库。
- ANN（Approximate Nearest Neighbor）：近似最近邻检索。
- Similarity Search：相似度检索。
- Cosine Similarity：余弦相似度。
- Hybrid Retrieval：混合检索（向量+关键词）。
- BM25：经典关键词检索算法。
- Sparse Retrieval：稀疏检索。
- Dense Retrieval：稠密检索。
- Re-ranker：重排模型。
- Cross-Encoder：常见重排架构。
- Recall@K：检索召回指标。
- MRR / nDCG：排序质量指标。
- Context Compression：上下文压缩。
- Grounding：有证据支撑回答。
- Citation：引用来源。
- Query Rewriting：查询改写。
- Multi-hop Retrieval：多跳检索。
- Knowledge Refresh：知识更新。
- RAG Evaluation：RAG 系统评测。

### I. Agent、Tool、Workflow、MCP

- Agent：能规划并执行多步任务的智能体程序。
- Tool Calling：模型调用外部函数/接口。
- Function Calling：结构化函数调用机制。
- Tool Schema：工具参数规范（常用 JSON Schema）。
- Skill：成套能力包（工具+提示+配置）。
- Planner：任务规划器。
- Executor：任务执行器。
- Router：路由器，决定走哪个工具或子流程。
- Reflection：反思修正机制。
- Memory：记忆模块。
- Short-term Memory：短期会话记忆。
- Long-term Memory：长期用户记忆。
- Working Memory：当前任务工作记忆。
- ReAct：推理+行动的 Agent 方法。
- Multi-Agent：多智能体协作。
- Orchestration：编排。
- Workflow Engine：工作流引擎。
- Guardrail：护栏规则（格式/安全/策略约束）。
- Sandbox：隔离执行环境。
- MCP（Model Context Protocol）：模型连接工具和数据源的开放协议。
- MCP Server：按 MCP 提供工具能力的服务端。
- MCP Client：调用 MCP 服务的客户端。
- spec：规范/契约（接口、协议、行为要求）。

### J. 多模态与生成模型

- CV（Computer Vision）：计算机视觉。
- OCR：光学字符识别。
- Object Detection：目标检测。
- Segmentation：图像分割。
- ASR（Automatic Speech Recognition）：语音识别。
- TTS（Text To Speech）：语音合成。
- Speech-to-Text：语音转文本。
- Text-to-Speech：文本转语音。
- Text-to-Image：文生图。
- Image-to-Text：图像描述生成。
- Image Captioning：图像字幕生成。
- VQA（Visual Question Answering）：视觉问答。
- CLIP：图文对齐表征模型。
- Diffusion Model：扩散生成模型。
- Denoising：去噪过程。
- UNet：扩散模型常用骨干网络。
- Guidance Scale：生成引导强度参数。
- CFG（Classifier-Free Guidance）：无分类器引导。
- GAN：生成对抗网络。
- Generator / Discriminator：生成器/判别器。
- VAE：变分自编码器。
- Latent Space：潜空间。
- Autoencoder：自编码器。

### K. 训练系统与分布式计算

- Epoch：完整遍历一次训练集。
- Step / Iteration：一次参数更新。
- Batch Size：批大小。
- Gradient Accumulation：梯度累积。
- Mixed Precision：混合精度训练。
- FP32 / FP16 / BF16：常见浮点精度格式。
- Quantization：量化（INT8/INT4 等）。
- Pruning：剪枝，压缩模型。
- Checkpoint：训练断点保存。
- Distributed Training：分布式训练。
- Data Parallel（DP）：数据并行。
- Tensor Parallel（TP）：张量并行。
- Pipeline Parallel（PP）：流水并行。
- ZeRO：显存优化分片技术。
- FSDP：全分片数据并行。
- NCCL：GPU 通信库。
- CUDA：NVIDIA 并行计算平台。
- TPU / NPU：专用 AI 计算硬件。

### L. 评测、监控与安全合规

- Benchmark：基准测试集。
- MMLU：通识能力评测基准。
- GSM8K：数学推理评测集。
- Human Eval：代码生成评测集。
- Win Rate：对比胜率评估。
- LLM-as-a-Judge：用模型做评审。
- E2E Evaluation：端到端评测。
- Online Evaluation：线上评测。
- Offline Evaluation：离线评测。
- A/B Testing：A/B 实验。
- Observability：可观测性。
- Tracing：调用链追踪。
- Latency：延迟。
- Throughput：吞吐。
- Token Usage：Token 消耗统计。
- Cost per Request：单请求成本。
- Content Moderation：内容审核。
- Toxicity：有害性。
- Jailbreak：越狱攻击。
- Prompt Injection：提示注入攻击。
- Data Exfiltration：数据外泄风险。
- PII：个人敏感信息。
- Compliance：合规（如数据、行业监管）。
- Governance：模型治理。
- Red Teaming：红队对抗测试。

### M. 工程化、部署与生态工具

- API Gateway：API 网关。
- Model Serving：模型服务化。
- Serving Engine：推理引擎（如 vLLM/TGI 等）。
- Batch Inference：批处理推理。
- Real-time Inference：实时推理。
- Autoscaling：自动扩缩容。
- Caching：缓存（响应缓存/KV 缓存）。
- Load Balancing：负载均衡。
- Rate Limiting：限流。
- Canary Release：金丝雀发布。
- Blue-Green Deployment：蓝绿发布。
- Rollback：回滚。
- CI/CD：持续集成/持续交付。
- Model Registry：模型注册中心。
- Experiment Tracking：实验跟踪。
- Versioning：版本管理（数据/模型/提示）。
- LLMOps：大模型工程运维体系。
- MLOps：机器学习工程运维体系。
- LangChain / LlamaIndex：常见 LLM 应用编排框架。
- OpenAI API / Claude API / Gemini API：主流模型服务接口生态。

---

## 4) 你提到的几个词，放在统一框架里

- NLP：语言处理大方向（分词、语义理解、生成等都属于 NLP）。
- Transformer：现代 NLP/LLM 的核心网络架构（Attention 驱动）。
- LLM：建立在 Transformer 等架构上的大规模语言模型。
- RAG：给 LLM 动态补充外部知识，降低幻觉。
- Tool/Skill：让模型调用外部能力并执行任务。
- Agent：把模型、工具、记忆、流程组合成可自动执行的系统。
- LangChain：常用应用编排框架。
- MCP：把工具/数据源接入标准化的协议。
- spec：接口或行为规范文档（契约）。

---

## 5) 推荐学习顺序（精简版）

1. 基础概念：ML、DL、NLP、Transformer、LLM。
2. 应用核心：Prompt、Tool Calling、RAG。
3. 系统化：Agent、Workflow、MCP。
4. 工程化：评测、安全、部署、LLMOps。

如果你需要，我可以下一步再给你做一版「按岗位（算法/后端/产品）拆分」的术语学习清单。


