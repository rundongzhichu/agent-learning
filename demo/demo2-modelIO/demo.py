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

print("=" * 60)
print("📬 LangChain 消息类型示例")
print("=" * 60)

# ==================== 1. SystemMessage - 系统消息 ====================
print("\n1️⃣  SystemMessage - 系统消息")
print("-" * 60)
system_msg = SystemMessage(content="你是一个专业的数学助手，专门帮助学生解决数学问题。")
print(f"消息类型：{type(system_msg).__name__}")
print(f"消息内容：{system_msg.content}")
print(f"消息作用：设定 AI 的角色和行为准则")

# ==================== 2. HumanMessage - 用户消息 ====================
print("\n2️⃣  HumanMessage - 用户消息")
print("-" * 60)
human_msg = HumanMessage(content="你好，我想知道如何计算圆的面积。")
print(f"消息类型：{type(human_msg).__name__}")
print(f"消息内容：{human_msg.content}")
print(f"消息作用：代表用户的输入或问题")

# ==================== 3. AIMessage - AI 消息 ====================
print("\n3️⃣  AIMessage - AI 消息")
print("-" * 60)
ai_msg = AIMessage(content="圆的面积公式是：S = πr²，其中 r 是圆的半径。")
print(f"消息类型：{type(ai_msg).__name__}")
print(f"消息内容：{ai_msg.content}")
print(f"消息作用：代表 AI 助手的回复")

# ==================== 4. FunctionMessage - 函数消息 ====================
print("\n4️⃣  FunctionMessage - 函数消息")
print("-" * 60)
function_msg = FunctionMessage(
    name="calculate_circle_area",
    content="314.1592653589793"
)
print(f"消息类型：{type(function_msg).__name__}")
print(f"函数名称：{function_msg.name}")
print(f"消息内容：{function_msg.content}")
print(f"消息作用：记录函数调用的结果")

# ==================== 5. ToolMessage - 工具消息 ====================
print("\n5️⃣  ToolMessage - 工具消息")
print("-" * 60)
tool_msg = ToolMessage(
    content="半径为 10 的圆面积是 314.16",
    tool_call_id="call_abc123"
)
print(f"消息类型：{type(tool_msg).__name__}")
print(f"工具调用 ID: {tool_msg.tool_call_id}")
print(f"消息内容：{tool_msg.content}")
print(f"消息作用：记录工具调用的结果（FunctionMessage 的现代替代）")

# ==================== 6. ChatMessage - 聊天消息 ====================
print("\n6️⃣  ChatMessage - 聊天消息")
print("-" * 60)
chat_msg = ChatMessage(content="这是一个通用消息，可以扮演任何角色", role="assistant")
print(f"消息类型：{type(chat_msg).__name__}")
print(f"角色：{chat_msg.role}")
print(f"消息内容：{chat_msg.content}")
print(f"消息作用：通用消息类型，可以指定任意角色")

# ==================== 综合示例：多轮对话 ====================
print("\n" + "=" * 60)
print("💬 综合示例：多轮对话")
print("=" * 60)

# 构建对话历史
messages = [
    SystemMessage(content="你是一个友好的助手，名字叫小智。"),
    HumanMessage(content="你好，我叫小明。"),
    AIMessage(content="你好小明，很高兴认识你！有什么我可以帮助你的吗？"),
    HumanMessage(content="我想知道 2+2 等于几。"),
    AIMessage(content="2+2 等于 4。"),
    HumanMessage(content="谢谢！"),
]

print(f"\n构建的对话历史包含 {len(messages)} 条消息：")
for i, msg in enumerate(messages, 1):
    print(f"{i}. {type(msg).__name__:15} - {msg.content[:30]}...")

# 调用模型
print("\n🤖 调用模型继续对话...")
response = chat_model.invoke(messages)

print(f"\n✅ AI 的回复：{response.content}")
print(f"消息类型：{type(response).__name__}")

# ==================== 实际工具调用示例 ====================
print("\n" + "=" * 60)
print("🛠️  实际工具调用示例")
print("=" * 60)

# 定义一个简单的计算器工具
@tool
def add(a: int, b: int) -> int:
    """两个数相加。"""
    return a + b

tools = [add]

# 将工具绑定到模型
model_with_tools = chat_model.bind_tools(tools)

# 测试工具调用
tool_messages_example = [
    SystemMessage(content="你是一个数学助手，可以使用工具帮助学生计算。"),
    HumanMessage(content="请帮我计算 5+3"),
]

print("\n📝 问题：请帮我计算 5+3")
print("🔧 使用工具：add(5, 3)")

# 调用模型（可能会返回工具调用请求）
tool_response = model_with_tools.invoke(tool_messages_example)
print(f"\n模型响应类型：{type(tool_response).__name__}")
print(f"是否包含工具调用：{len(tool_response.tool_calls) > 0}")

if tool_response.tool_calls:
    tool_call = tool_response.tool_calls[0]
    print(f"工具名称：{tool_call['name']}")
    print(f"工具参数：{tool_call['args']}")
    
    # 创建 ToolMessage
    tool_msg = ToolMessage(
        content=str(add.invoke(tool_call['args'])),
        tool_call_id=tool_call['id']
    )
    print(f"\n工具执行结果：{tool_msg.content}")

print("\n" + "=" * 60)
print("✨ 示例完成！")
print("=" * 60)
