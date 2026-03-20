# LangChain 开发文档

## 目录
1. [LangChain 概述](#langchain-概述)
2. [核心概念](#核心概念)
3. [安装与配置](#安装与配置)
4. [主要模块](#主要模块)
5. [开发实践](#开发实践)
6. [最佳实践](#最佳实践)

---

## LangChain 概述

### 什么是 LangChain？

LangChain 是一个用于开发由语言模型驱动的应用程序的框架。它提供了模块化的抽象，使开发者能够轻松构建复杂的 LLM 应用，如聊天机器人、问答系统、数据分析工具等。

### 核心优势

- **模块化**: 提供可组合的组件，支持灵活的应用架构
- **链式调用**: 将多个操作串联成完整的工作流
- **代理能力**: 支持 LLM 与外部工具和数据源交互
- **记忆管理**: 维护对话历史和上下文信息
- **评估测试**: 提供调试和评估工具

### 适用场景

- 智能客服系统
- 文档问答与分析
- 代码生成与辅助编程
- 数据分析与可视化
- 多步骤任务自动化

---

## 核心概念

### 1. Models（模型）

#### LLMs（大语言模型）
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    max_tokens=1000
)
```

#### Chat Models（对话模型）
```python
from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="你是一个有帮助的助手"),
    HumanMessage(content="你好！")
]

response = llm.invoke(messages)
```

### 2. Prompts（提示）

#### Prompt Templates
```python
from langchain_core.prompts import ChatPromptTemplate

template = """
你是一个{role}。请回答以下问题：
问题：{question}
"""

prompt = ChatPromptTemplate.from_template(template)
formatted = prompt.format(role="数学老师", question="什么是微积分？")
```

#### Few-Shot Prompts
```python
from langchain_core.prompts import FewShotPromptTemplate

examples = [
    {"input": "高兴", "output": "悲伤"},
    {"input": "大", "output": "小"}
]

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="输入：{input}\n输出：{output}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="给出反义词:",
    suffix="输入：{input}\n输出：",
    input_variables=["input"]
)
```

### 3. Chains（链）

#### 基础链
```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

chain = (
    {"question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke("什么是人工智能？")
```

#### 顺序链
```python
from langchain.chains import SequentialChain

chain1 = prompt1 | llm1 | output_parser1
chain2 = prompt2 | llm2 | output_parser2

sequential_chain = chain1 | chain2
```

### 4. Memory（记忆）

#### Conversation Buffer Memory
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

memory.save_context({"input": "你好"}, {"output": "你好！有什么可以帮助你的？"})
memory.load_memory_variables({})
```

#### Conversation Summary Memory
```python
from langchain.memory import ConversationSummaryMemory

summary_memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="summary"
)
```

### 5. Retrieval（检索）

#### Document Loaders
```python
from langchain_community.document_loaders import TextLoader, PyPDFLoader

# 加载文本文档
loader = TextLoader("document.txt")
documents = loader.load()

# 加载 PDF
pdf_loader = PyPDFLoader("document.pdf")
pdf_docs = pdf_loader.load()
```

#### Vector Stores
```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

# 从文档创建向量库
vectorstore = FAISS.from_documents(documents, embeddings)

# 保存和加载
vectorstore.save_local("faiss_index")
loaded_vectorstore = FAISS.load_local("faiss_index", embeddings)
```

#### Retrievers
```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

relevant_docs = retriever.invoke("查询内容")
```

### 6. Agents（代理）

#### 基础代理
```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    \"\"\"搜索互联网获取信息\"\"\"
    # 实现搜索逻辑
    return "搜索结果"

tools = [search]

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

#### Tool Calling
```python
from langchain_core.tools import tool

@tool
def calculate(expression: str) -> float:
    \"\"\"计算数学表达式\"\"\"
    return eval(expression)

@tool
def get_weather(city: str) -> str:
    \"\"\"获取城市天气\"\"\"
    return f"{city}的天气是晴朗"
```

---

## 安装与配置

### 基础安装

```bash
# 安装核心包
pip install langchain

# 安装 OpenAI 集成
pip install langchain-openai

# 安装社区包
pip install langchain-community

# 安装向量数据库
pip install faiss-cpu  # CPU 版本
pip install faiss-gpu  # GPU 版本

# 安装文档处理工具
pip install pypdf docx python-docx
```

### 环境配置

```bash
# .env 文件
OPENAI_API_KEY=your_api_key_here
LANGCHAIN_API_KEY=your_langchain_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=my_project
```

### Python 代码配置

```python
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_API_KEY"] = "your-langchain-key"
```

---

## 主要模块

### 1. LangChain Core

提供基础抽象和接口：
- `langchain_core.language_models`: 模型接口
- `langchain_core.prompts`: 提示模板
- `langchain_core.chains`: 链的基础类
- `langchain_core.agents`: 代理定义

### 2. LangChain Community

第三方集成：
- 向量数据库（FAISS, Pinecone, Weaviate）
- 文档加载器（PDF, Word, HTML）
- 工具集成（搜索 API, 数据库连接）

### 3. LangChain OpenAI

OpenAI 专用集成：
- ChatOpenAI 模型
- OpenAI Embeddings
- Azure OpenAI 支持

### 4. LangChain Experimental

实验性功能：
- 自反思代理
- 多代理协作
- 高级推理模式

---

## 开发实践

### 示例 1: RAG 问答系统

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 1. 文档处理
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

# 2. 创建向量库
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# 3. 设置检索器
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 4. 构建 RAG 链
prompt = ChatPromptTemplate.from_template("""
基于以下上下文回答问题:
{context}

问题：{question}
回答:""")

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4")
    | StrOutputParser()
)

# 5. 使用
answer = rag_chain.invoke("你的问题")
```

### 示例 2: 对话机器人

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

# 初始化内存
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 创建对话链
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-4"),
    retriever=vectorstore.as_retriever(),
    memory=memory,
    return_source_documents=True
)

# 对话
result = conversation_chain({"question": "你好，介绍一下你自己"})
print(result["answer"])
```

### 示例 3: 数据分析代理

```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_core.prompts import ChatPromptTemplate

# 工具
tools = [PythonREPLTool()]

# 代理提示
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个数据分析专家，使用 Python 分析数据"),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# 创建代理
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# 执行
response = agent_executor.invoke({
    "input": "生成 100 个随机数并计算平均值"
})
```

### 示例 4: 多文档分析

```python
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# 创建文档链
stuff_chain = create_stuff_documents_chain(llm, prompt)

# 创建检索链
retrieval_chain = create_retrieval_chain(retriever, stuff_chain)

# 批量分析
response = retrieval_chain.invoke({"input": "总结所有文档的关键点"})
```

---

## 最佳实践

### 1. Prompt 工程

✅ **推荐做法**:
```python
# 具体明确的指令
prompt = """
请按照以下步骤分析这个问题:
1. 识别问题类型
2. 列出相关概念
3. 提供详细解答
4. 给出实际示例

问题：{question}
"""
```

❌ **避免**:
```python
# 模糊不清的指令
prompt = "回答这个问题：{question}"
```

### 2. 分块策略

```python
# 根据文档类型选择合适的分块大小
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # 较小块提高检索精度
    chunk_overlap=200,    # 保持上下文连贯性
    length_function=len,
    separators=["\n\n", "\n", "。", " ", ""]
)
```

### 3. 检索优化

```python
# 混合检索策略
retriever = vectorstore.as_retriever(
    search_type="mmr",  # 最大边际相关性
    search_kwargs={
        "k": 5,         # 返回文档数
        "fetch_k": 10   # 初始检索数
    }
)
```

### 4. 错误处理

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def call_llm(prompt):
    return llm.invoke(prompt)
```

### 5. 性能优化

```python
# 使用缓存减少 API 调用
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache

set_llm_cache(InMemoryCache())

# 批量处理
from langchain.batch import batch

results = batch(chain, inputs, batch_size=10)
```

### 6. 监控与调试

```python
import langchain
langchain.debug = True

# 使用 LangSmith 追踪
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "my-project"
```

### 7. 安全考虑

```python
# 限制输出长度
llm = ChatOpenAI(max_tokens=500)

# 过滤不当内容
from langchain.output_parsers import PydanticOutputParser

class SafeResponse(BaseModel):
    content: str = Field(description="安全的回复内容")
    is_appropriate: bool = Field(description="内容是否合适")
```

---

## 常见问题

### Q1: 如何处理长文档？
**A**: 使用分块 + 检索的策略，结合 Map-Reduce 或 Refine 模式进行摘要。

### Q2: 如何提高回答准确性？
**A**: 
- 优化检索策略（增加 k 值、使用 MMR）
- 改进 Prompt 设计
- 添加 Few-Shot 示例
- 使用更强大的模型

### Q3: 如何降低成本？
**A**:
- 使用缓存机制
- 选择适当的模型大小
- 优化 token 使用
- 实施请求限流

### Q4: 如何部署生产？
**A**:
- 使用 FastAPI 封装服务
- 实施速率限制
- 添加监控日志
- 配置自动扩展

---

## 参考资源

- **官方文档**: https://python.langchain.com/
- **GitHub**: https://github.com/langchain-ai/langchain
- **Discord 社区**: https://discord.gg/langchain
- **教程**: https://github.com/langchain-ai/langchain-academy

---

*最后更新：2026 年 3 月*
