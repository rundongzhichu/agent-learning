# 导入 dotenv 库的 load_dotenv 函数，用于加载环境变量配置文件 (.env) 中的配置
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
import bs4
import dotenv

dotenv.load_dotenv()

# 使用 WebBaseLoader 加载网页内容
loader = WebBaseLoader(
    web_path="https://www.gov.cn/yaowen/liebiao/202603/content_7063789.htm",
    bs_kwargs=dict(parse_only=bs4.SoupStrainer(id="UCAP-CONTENT"))
)
docs = loader.load()
print(f"加载的文档数量：{len(docs)}")
if len(docs) > 0:
    print(f"第一个文档内容长度：{len(docs[0].page_content)}")

# 对于嵌入模型，这里通过 API 调用
# 3. 向量化——使用专业嵌入模型
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5"
)


# 使用分割器分割文档
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
documents = text_splitter.split_documents(docs)
print(f"分割后的文档片段数量：{len(documents)}")

if len(documents) == 0:
    raise ValueError("没有可用的文档片段，请检查网页是否可访问或 HTML 元素是否存在")

# 向量存储 embeddings 会将 documents 中的每个文本片段转换为向量，并将这些向量存储在 FAISS 向量数据库中
vector = FAISS.from_documents(documents, embeddings)


from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# 4. 检索器设置
retriever = vector.as_retriever()
retriever.search_kwargs = {"k": 3}
docs = retriever.invoke("护理保险制度是什么？")

# 打印检索结果
for i, doc in enumerate(docs):
    print(f"⭐ 第{i+1}条规定：")
    print(doc)

# 5. 定义提示词模板

prompt_template = """
你是一个回答机器人。
你的任务是根据下述给定的已知信息回答用户问题。
确保你的回复完全依据下述已知信息，不要编造答案。
如果下述已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。

已知信息：
{info}

用户问：
{question}
"""

prompt = PromptTemplate.from_template(prompt_template)

# 6. 创建 RAG 链

# 创建格式化函数，将检索结果转换为字符串
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 创建大模型实例
llm = ChatOpenAI(model="deepseek-chat")  # 默认使用 gpt-3.5-turbo

# 构建 RAG 链
rag_chain = (
    {"info": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 7. 测试 RAG 检索增强生成
response = rag_chain.invoke("护理保险制度是什么？")
print("\n🤖 RAG 回答：")
print(response)