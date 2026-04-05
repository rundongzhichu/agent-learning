"""
自定义实现大模型记忆功能 Demo

本示例展示了如何不依赖 LangChain 的 Memory 模块，
手动实现大模型的记忆功能，包括：
1. 基于列表的简单对话历史记忆
2. 基于摘要的压缩记忆
3. 基于向量检索的智能记忆
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

# 导入必要的库
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# 加载环境变量
load_dotenv()


# ============================================================================
# 方案一：基于列表的简单对话历史记忆（最常用）
# ============================================================================

class SimpleConversationMemory:
    """
    简单的对话记忆管理器
    使用列表存储所有历史消息
    """
    
    def __init__(self, max_history_length: int = 10):
        """
        初始化记忆管理器
        
        Args:
            max_history_length: 最大保留的历史消息数量（对数）
        """
        self.messages: List[Dict[str, str]] = []
        self.max_history_length = max_history_length
    
    def add_message(self, role: str, content: str):
        """添加一条消息到历史记录"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # 如果超过最大长度，移除最早的记录
        if len(self.messages) > self.max_history_length:
            self.messages.pop(0)
    
    def get_history_messages(self) -> List[Dict[str, str]]:
        """获取所有历史消息"""
        return self.messages
    
    def clear(self):
        """清空历史记录"""
        self.messages = []
    
    def save_to_file(self, filepath: str):
        """保存记忆到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filepath: str):
        """从文件加载记忆"""
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                self.messages = json.load(f)


# ============================================================================
# 方案二：基于摘要的压缩记忆（节省 Token）
# ============================================================================

class SummaryMemory:
    """
    基于摘要的记忆管理器
    定期使用 LLM 总结对话历史，避免上下文过长
    """
    
    def __init__(self, llm: ChatOpenAI, summary_interval: int = 5):
        """
        初始化摘要记忆管理器
        
        Args:
            llm: 用于生成摘要的 LLM 实例
            summary_interval: 每多少轮对话进行一次摘要
        """
        self.llm = llm
        self.summary_interval = summary_interval
        self.current_summary: str = ""
        self.recent_messages: List[Dict[str, str]] = []
        self.message_count: int = 0
    
    def add_message(self, role: str, content: str):
        """添加消息并检查是否需要摘要"""
        self.recent_messages.append({
            "role": role,
            "content": content
        })
        self.message_count += 1
        
        # 达到摘要间隔时，生成新的摘要
        if self.message_count % self.summary_interval == 0:
            self._update_summary()
    
    def _update_summary(self):
        """使用 LLM 更新对话摘要"""
        if not self.recent_messages:
            return
        
        # 构建摘要提示
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in self.recent_messages[-self.summary_interval:]
        ])
        
        prompt = f"""请总结以下对话的核心内容，提取关键信息点（100 字以内）：

{conversation_text}

总结："""
        
        try:
            response = self.llm.invoke(prompt)
            # 合并新旧摘要
            if self.current_summary:
                self.current_summary = f"{self.current_summary}\n最新进展：{response.content}"
            else:
                self.current_summary = response.content
            
            # 清空最近的详细消息
            self.recent_messages = []
        except Exception as e:
            print(f"生成摘要失败：{e}")
    
    def get_context(self) -> str:
        """获取当前上下文（摘要 + 最近消息）"""
        context_parts = []
        
        if self.current_summary:
            context_parts.append(f"[历史对话摘要]\n{self.current_summary}")
        
        if self.recent_messages:
            recent_text = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in self.recent_messages[-3:]  # 只包含最近 3 条
            ])
            context_parts.append(f"[最近对话]\n{recent_text}")
        
        return "\n\n".join(context_parts)
    
    def clear(self):
        """清空记忆"""
        self.current_summary = ""
        self.recent_messages = []
        self.message_count = 0


# ============================================================================
# 方案三：基于向量检索的智能记忆（高级用法）
# ============================================================================

class VectorRetrievalMemory:
    """
    基于向量检索的记忆管理器
    将对话历史向量化存储，通过相似性检索相关记忆
    """
    
    def __init__(self, embedding_model: str = "BAAI/bge-small-zh-v1.5"):
        """
        初始化向量检索记忆
        
        Args:
            embedding_model: 嵌入模型名称
        """
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=20
        )
        self.vector_store = None
        self.conversation_chunks: List[Dict[str, Any]] = []
    
    def add_conversation(self, user_input: str, ai_response: str):
        """添加一对对话到向量库"""
        # 创建对话片段
        conversation_text = f"用户：{user_input}\nAI: {ai_response}"
        
        # 分割文本
        chunks = self.text_splitter.split_text(conversation_text)
        
        for chunk in chunks:
            self.conversation_chunks.append({
                "content": chunk,
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "ai_response": ai_response
            })
        
        # 重建向量库
        if self.conversation_chunks:
            texts = [chunk["content"] for chunk in self.conversation_chunks]
            self.vector_store = FAISS.from_texts(texts, self.embeddings)
    
    def retrieve_relevant(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """检索与查询最相关的历史对话"""
        if not self.vector_store:
            return []
        
        # 向量检索
        docs = self.vector_store.similarity_search(query, k=top_k)
        
        # 找到对应的完整对话
        relevant_conversations = []
        for doc in docs:
            for chunk in self.conversation_chunks:
                if chunk["content"] == doc.page_content:
                    relevant_conversations.append(chunk)
                    break
        
        return relevant_conversations
    
    def get_memory_context(self, current_query: str) -> str:
        """获取基于当前查询的相关记忆上下文"""
        relevant = self.retrieve_relevant(current_query)
        
        if not relevant:
            return ""
        
        context_parts = []
        for i, conv in enumerate(relevant, 1):
            context_parts.append(
                f"[相关记忆{i}]\n用户：{conv['user_input']}\nAI: {conv['ai_response']}"
            )
        
        return "[历史相关记忆]\n" + "\n\n".join(context_parts)
    
    def clear(self):
        """清空向量记忆"""
        self.conversation_chunks = []
        self.vector_store = None


# ============================================================================
# 主程序：演示三种记忆方式的使用
# ============================================================================

def demo_simple_memory():
    """演示简单列表记忆"""
    print("\n" + "="*60)
    print("📝 方案一：基于列表的简单对话历史记忆")
    print("="*60)
    
    # 创建 LLM 实例
    llm = ChatOpenAI(model="deepseek-chat", temperature=0.7)
    
    # 创建记忆管理器
    memory = SimpleConversationMemory(max_history_length=10)
    
    # 模拟多轮对话
    conversations = [
        ("你好，我叫小明", "你好小明！很高兴认识你。"),
        ("我喜欢打篮球", "篮球是一项很好的运动，可以锻炼身体和团队合作精神。"),
        ("你最喜欢什么运动？", "作为 AI，我没有个人喜好，但我了解很多运动项目。"),
    ]
    
    # 添加历史对话
    for user_msg, ai_msg in conversations:
        memory.add_message("用户", user_msg)
        memory.add_message("AI", ai_msg)
    
    # 进行新对话
    user_input = "你还记得我喜歡什么吗？"
    print(f"\n👤 用户：{user_input}")
    
    # 构建包含历史上下文的提示
    system_prompt = "你是一个友好的助手，能够记住之前的对话内容。"
    
    messages = [SystemMessage(content=system_prompt)]
    
    # 添加历史消息
    for msg in memory.get_history_messages():
        if msg["role"] == "用户":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    
    # 添加当前问题
    messages.append(HumanMessage(content=user_input))
    
    # 调用 LLM
    response = llm.invoke(messages)
    print(f"🤖 AI: {response.content}")
    
    # 保存记忆
    memory.save_to_file("demo_memory.json")
    print("\n✓ 记忆已保存到 demo_memory.json")


def demo_summary_memory():
    """演示摘要记忆"""
    print("\n" + "="*60)
    print("📝 方案二：基于摘要的压缩记忆")
    print("="*60)
    
    # 创建 LLM 实例
    llm = ChatOpenAI(model="deepseek-chat", temperature=0.7)
    
    # 创建摘要记忆管理器
    summary_memory = SummaryMemory(llm, summary_interval=3)
    
    # 模拟多轮对话
    conversations = [
        ("今天天气怎么样？", "今天天气晴朗，温度适宜。"),
        ("我打算去公园散步", "很好的主意，散步有益身心健康。"),
        ("公园里有什么好玩的？", "公园里有湖泊、花园和健身器材。"),
        ("你喜欢大自然吗？", "大自然很美，能让人放松心情。"),
        ("周末我还想去爬山", "爬山是很好的有氧运动，可以欣赏美景。"),
    ]
    
    # 添加对话
    for user_msg, ai_msg in conversations:
        summary_memory.add_message("用户", user_msg)
        summary_memory.add_message("AI", ai_msg)
        
        print(f"\n👤 用户：{user_msg}")
        print(f"🤖 AI: {ai_msg}")
    
    # 显示当前摘要
    print("\n" + "-"*60)
    print("📋 当前记忆摘要:")
    print(summary_memory.get_context())
    
    # 进行新对话
    user_input = "我之前说想去做什么运动？"
    print(f"\n{'-'*60}")
    print(f"👤 用户：{user_input}")
    
    # 构建提示
    context = summary_memory.get_context()
    prompt = f"""基于以下对话历史和摘要，回答问题：

{context}

问题：{user_input}
回答："""
    
    response = llm.invoke(prompt)
    print(f"🤖 AI: {response.content}")


def demo_vector_memory():
    """演示向量检索记忆"""
    print("\n" + "="*60)
    print("📝 方案三：基于向量检索的智能记忆")
    print("="*60)
    
    # 创建向量检索记忆
    vector_memory = VectorRetrievalMemory()
    
    # 添加一些对话记录
    conversations = [
        ("Python 怎么安装？", "你可以从 python.org 下载安装包，按照指引安装即可。"),
        ("推荐一些 Python 学习资源", "推荐《Python 编程：从入门到实践》和菜鸟教程网站。"),
        ("如何学习机器学习？", "建议先学习 Python 基础，然后学习 numpy、pandas 等库。"),
        ("有什么好的 AI 框架？", "TensorFlow、PyTorch 和 scikit-learn 都是不错的选择。"),
        ("深度学习难学吗？", "需要一定的数学基础，但循序渐进学习并不难。"),
    ]
    
    print("\n正在添加对话记忆...")
    for user_msg, ai_msg in conversations:
        vector_memory.add_conversation(user_msg, ai_msg)
        print(f"  ✓ 已添加：{user_msg[:20]}...")
    
    # 测试检索
    test_queries = [
        "怎么学习 Python？",
        "AI 框架有哪些？",
    ]
    
    for query in test_queries:
        print(f"\n{'-'*60}")
        print(f"🔍 查询：{query}")
        
        # 获取相关记忆
        context = vector_memory.get_memory_context(query)
        
        if context:
            print("\n📚 检索到的相关记忆:")
            print(context)
        else:
            print("\n⚠️ 未找到相关记忆")
    
    # 进行实际问答
    print(f"\n{'-'*60}")
    user_input = "我应该先学什么编程语言？"
    print(f"👤 用户：{user_input}")
    
    llm = ChatOpenAI(model="deepseek-chat")
    context = vector_memory.get_memory_context(user_input)
    
    if context:
        prompt = f"""基于以下相关历史对话，回答问题：

{context}

问题：{user_input}
回答："""
    else:
        prompt = user_input
    
    response = llm.invoke(prompt)
    print(f"🤖 AI: {response.content}")


if __name__ == "__main__":
    print("="*60)
    print("🧠 自定义大模型记忆功能 Demo")
    print("="*60)
    
    # 运行三个演示
    demo_simple_memory()
    demo_summary_memory()
    demo_vector_memory()
    
    print("\n" + "="*60)
    print("✅ 所有演示完成！")
    print("="*60)
    print("""
💡 三种方案的对比：

方案一（列表记忆）:
  ✅ 优点：实现简单，保留完整信息
  ❌ 缺点：Token 消耗大，不适合长对话
  
方案二（摘要记忆）:
  ✅ 优点：节省 Token，保留核心信息
  ❌ 缺点：可能丢失细节，需要额外 LLM 调用
  
方案三（向量记忆）:
  ✅ 优点：智能检索，适合大量历史数据
  ❌ 缺点：实现复杂，需要嵌入模型和向量库
""")
