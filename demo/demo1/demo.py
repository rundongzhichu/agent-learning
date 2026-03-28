# 导入必要的库
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
import bs4
import dotenv

dotenv.load_dotenv()

print("=" * 60)
print("🤖 LangChain Agent 示例 - 政策咨询助手")
print("=" * 60)

# ==================== 1. 准备知识库 ====================
print("\n📚 步骤 1: 加载和准备知识库...")

# 使用 WebBaseLoader 加载网页内容
loader = WebBaseLoader(
    web_path="https://www.gov.cn/yaowen/liebiao/202603/content_7063789.htm",
    bs_kwargs=dict(parse_only=bs4.SoupStrainer(id="UCAP-CONTENT"))
)
docs = loader.load()
print(f"✓ 加载的文档数量：{len(docs)}")
if len(docs) > 0:
    print(f"✓ 第一个文档内容长度：{len(docs[0].page_content)}")

# 向量化——使用专业嵌入模型
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5"
)

# 使用分割器分割文档
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
documents = text_splitter.split_documents(docs)
print(f"✓ 分割后的文档片段数量：{len(documents)}")

if len(documents) == 0:
    raise ValueError("没有可用的文档片段，请检查网页是否可访问或 HTML 元素是否存在")

# 向量存储
vector = FAISS.from_documents(documents, embeddings)
print("✓ FAISS 向量库创建成功！")

# ==================== 2. 创建检索工具 ====================
print("\n🛠️  步骤 2: 创建 Agent 工具...")

# 创建检索器
retriever = vector.as_retriever(search_kwargs={"k": 3})


# 定义检索工具
@tool
def search_policy(query: str) -> str:
    """搜索相关政策信息。

    当你需要回答关于政策、法规、制度的问题时使用此工具。

    Args:
        query: 用户的问题或查询关键词
    """
    print(f"  🔍 Agent 正在搜索：{query}")
    results = retriever.invoke(query)
    return "\n\n".join(doc.page_content for doc in results)


# 创建工具列表
tools = [search_policy]

# ==================== 3. 创建大模型和 Agent ====================
print("\n 步骤 3: 创建 Agent...")

# 创建大模型实例
llm = ChatOpenAI(model="deepseek-chat")

# 定义系统提示词
system_prompt = """你是一个专业的政策咨询助手。你可以使用提供的工具来回答用户关于政策的问题。

请遵循以下原则：
1. 首先理解用户的问题
2. 如果需要查找信息，使用 search_policy 工具搜索相关政策
3. 根据搜索结果给出准确、完整的回答
4. 如果搜索结果为空或不足以回答问题，诚实地告诉用户
5. 回答要简洁明了，避免冗长

用户问题:
{input}

{agent_scratchpad}
"""

# 创建提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 创建工具调用 Agent
agent = create_openai_tools_agent(llm, tools, prompt)

# 创建 Agent 执行器
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,
)

print("✓ Agent 创建成功！")

# ==================== 4. 测试 Agent ====================
print("\n💬 步骤 4: 测试 Agent...")
print("-" * 60)

# 测试问题
test_questions = [
    "护理保险制度是什么？",
    "这个制度适用于哪些人群？",
]

for question in test_questions:
    print(f"\n❓ 问题：{question}")
    print("-" * 60)

    try:
        # 调用 Agent
        response = agent_executor.invoke({"input": question})

        print(f"\n✅ 回答：{response['output']}")
        print("-" * 60)
    except Exception as e:
        print(f"\n❌ 回答失败：{str(e)}")
        print("-" * 60)

# ==================== 5. 交互式对话 ====================
print("\n🎯 现在进入交互式对话模式（输入 'quit' 退出）")
print("=" * 60)

while True:
    try:
        user_input = input("\n👤 你：").strip()

        if user_input.lower() in ['quit', 'exit', '退出']:
            print("👋 再见！")
            break

        if not user_input:
            continue

        print("-" * 60)
        response = agent_executor.invoke({"input": user_input})
        print(f"\n🤖 Agent: {response['output']}")

    except KeyboardInterrupt:
        print("\n👋 再见！")
        break
    except Exception as e:
        print(f"\n❌ 发生错误：{str(e)}")
