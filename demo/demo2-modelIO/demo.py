from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
import dotenv
from openai.types import EmbeddingModel

# 加载环境变量
dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

# ########核心代码############
# 创建聊天模型实例
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")

# 输出结果
res1 = embedding_model.embed_query("你好")
print(res1)
