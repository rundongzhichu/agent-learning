from langchain_core.messages import (
    SystemMessage,      # 系统消息
    HumanMessage,       # 用户消息
    AIMessage,          # AI 消息
    FunctionMessage,    # 函数消息
    ToolMessage,        # 工具消息
    ChatMessage,        # 聊天消息
)
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os
import dotenv

# 加载环境变量
dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

# 创建聊天模型实例
chat_model = ChatOpenAI(model="deepseek-chat")

# ==================== 多轮对话上下文示例 ====================
print("\n" + "=" * 60)
print("💬 多轮对话上下文示例 - 旅游咨询场景")
print("=" * 60)

# 创建一个新的对话会话
conversation_history = []

# 第一轮对话
print("\n📍 第一轮对话")
print("-" * 60)
user_input_1 = "我想去日本旅游，有什么建议吗？"
print(f"👤 用户：{user_input_1}")

# 添加到对话历史
conversation_history.append(HumanMessage(content=user_input_1))

# 调用模型
response_1 = chat_model.invoke(conversation_history)
print(f"🤖 AI: {response_1.content}")

# 将 AI 回复也添加到历史中
conversation_history.append(AIMessage(content=response_1.content))

# 第二轮对话（依赖上下文）
print("\n📍 第二轮对话 - AI 需要理解上文提到的'日本'")
print("-" * 60)
user_input_2 = "那最佳旅游季节是什么时候？"
print(f"👤 用户：{user_input_2}")

conversation_history.append(HumanMessage(content=user_input_2))
response_2 = chat_model.invoke(conversation_history)
print(f"🤖 AI: {response_2.content}")

conversation_history.append(AIMessage(content=response_2.content))

# 第三轮对话（继续深入）
print("\n📍 第三轮对话 - AI 需要记住之前提到的地点和季节")
print("-" * 60)
user_input_3 = "我只有 1 万元预算，够吗？"
print(f"👤 用户：{user_input_3}")

conversation_history.append(HumanMessage(content=user_input_3))
response_3 = chat_model.invoke(conversation_history)
print(f"🤖 AI: {response_3.content}")

conversation_history.append(AIMessage(content=response_3.content))

# 第四轮对话（测试长期记忆）
print("\n📍 第四轮对话 - AI 需要综合所有历史信息")
print("-" * 60)
user_input_4 = "对了，你刚才推荐的京都和东京，哪个更适合樱花季节去？"
print(f"👤 用户：{user_input_4}")

conversation_history.append(HumanMessage(content=user_input_4))
response_4 = chat_model.invoke(conversation_history)
print(f"🤖 AI: {response_4.content}")

conversation_history.append(AIMessage(content=response_4.content))

# 显示完整的对话历史
print("\n" + "=" * 60)
print("📋 完整对话历史记录")
print("=" * 60)
print(f"\n对话共包含 {len(conversation_history)} 条消息：\n")

for i, msg in enumerate(conversation_history, 1):
    msg_type = type(msg).__name__
    # 根据消息类型选择图标
    if msg_type == "HumanMessage":
        icon = "👤"
    elif msg_type == "AIMessage":
        icon = "🤖"
    else:
        icon = "📝"
    
    # 截断过长的内容
    content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
    print(f"{i}. {icon} {msg_type:15} - {content_preview}")

# 上下文管理技巧
print("\n" + "=" * 60)
print("💡 上下文管理技巧")
print("=" * 60)

print("\n1️⃣  保持上下文连贯性")
print("   - 每次对话都要将完整的历史记录传给模型")
print("   - 模型会自动理解上下文中的指代关系（如'那'、'哪个'）")

print("\n2️⃣  控制上下文长度")
print("   - 对话轮数过多时，可以：")
print("     * 只保留最近 N 轮对话")
print("     * 总结早期对话为摘要")
print("     * 删除不重要的消息")

# 示例：只保留最近 2 轮对话
print("\n3️⃣  示例：保留最近 2 轮对话")
recent_messages = conversation_history[-4:]  # 保留最后 4 条（2 轮）
print(f"   原始对话数：{len(conversation_history)}")
print(f"   保留后对话数：{len(recent_messages)}")

print("\n4️⃣  添加系统指令来强化角色")
print("   - 在对话开始时设置 SystemMessage")
print("   - 或在关键节点插入指导性消息")

# 交互式对话示例
print("\n" + "=" * 60)
print("🎮 交互式对话体验（输入'quit'退出）")
print("=" * 60)

# 创建新的对话历史
interactive_history = [
    SystemMessage(content="你是一个友好的旅游顾问，名字叫小游。你擅长根据用户的预算、时间和兴趣推荐旅游目的地和行程。")
]

print("\n👋 你好！我是你的旅游顾问小游。请问你想去哪里旅游？\n")

while True:
    try:
        user_input = input("👤 你：").strip()
        
        if user_input.lower() in ['quit', 'exit', '退出']:
            print("\n👋 感谢使用，祝你旅途愉快！再见！")
            break
            
        if not user_input:
            continue
        
        # 添加用户消息到历史
        interactive_history.append(HumanMessage(content=user_input))
        
        # 调用模型
        response = chat_model.invoke(interactive_history)
        
        # 显示 AI 回复
        print(f"\n🤖 小游：{response.content}\n")
        
        # 添加 AI 回复到历史
        interactive_history.append(AIMessage(content=response.content))
        
        # 可选：显示当前对话长度
        if len(interactive_history) % 4 == 0:  # 每 2 轮显示一次
            print(f"   [当前对话轮数：{(len(interactive_history)-1)//2}]\n")
        
    except KeyboardInterrupt:
        print("\n\n👋 再见！")
        break
    except Exception as e:
        print(f"\n❌ 发生错误：{str(e)}\n")
        break
