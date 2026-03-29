"""
LangChain 模型调用方式示例
========================
本示例展示多种模型调用方式：
1. 阻塞式调用（Blocking）
2. 流式调用（Streaming）
3. 批量调用（Batch）
4. 异步调用（Async）
5. 异步流式调用（Async Streaming）
6. 异步批量调用（Async Batch）
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
import dotenv
import time
import asyncio

# 加载环境变量
dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

# 创建聊天模型实例
chat_model = ChatOpenAI(model="deepseek-chat")

print("=" * 60)
print("🚀 LangChain 模型调用方式示例")
print("=" * 60)

# ==================== 1. 阻塞式调用 ====================
print("\n" + "=" * 60)
print("1️⃣  阻塞式调用 (Blocking Call)")
print("=" * 60)
print("\n特点：")
print("  - 等待完整响应后才返回")
print("  - 适合短文本或实时性要求不高的场景")
print("  - 简单易用，代码最简洁")

start_time = time.time()

messages = [
    SystemMessage(content="你是一个简洁的助手。"),
    HumanMessage(content="请用一句话解释什么是人工智能。")
]

# 阻塞式调用：等待完整响应
response = chat_model.invoke(messages)

end_time = time.time()

print(f"\n⏱️  响应时间：{end_time - start_time:.2f}秒")
print(f"📝 AI 回答：{response.content}")
print(f"📦 响应类型：{type(response).__name__}")

# ==================== 2. 流式调用 ====================
print("\n" + "=" * 60)
print("2️⃣  流式调用 (Streaming Call)")
print("=" * 60)
print("\n特点：")
print("  - 边生成边输出，用户体验更好")
print("  - 适合长文本生成场景")
print("  - 可以实时看到生成进度")

# 使用 stream 方法进行流式调用
stream_messages = [
    SystemMessage(content="你是一个详细的助手。"),
    HumanMessage(content="请详细介绍一下机器学习的基本概念，包括定义、主要方法和应用场景。")
]

print("\n📡 开始流式输出...\n")
print("-" * 60)

start_time = time.time()

# 流式调用
for chunk in chat_model.stream(stream_messages):
    # chunk 是 AIMessage 对象
    content = chunk.content
    if content:
        # 逐字输出，模拟打字机效果
        print(content, end="", flush=True)

end_time = time.time()

print("\n" + "-" * 60)
print(f"\n⏱️  总耗时：{end_time - start_time:.2f}秒")
print(f"💡 流式输出可以让用户更快看到部分内容，提升体验")

# ==================== 3. 批量调用 ====================
print("\n" + "=" * 60)
print("3️⃣  批量调用 (Batch Call)")
print("=" * 60)
print("\n特点：")
print("  - 一次调用处理多个输入")
print("  - 适合需要并行处理多个请求的场景")
print("  - 比逐个调用更高效")

# 准备多个问题
batch_questions = [
    "什么是深度学习？",
    "神经网络有哪些主要类型？",
    "如何训练一个机器学习模型？",
    "什么是过拟合？如何避免？",
    "强化学习的基本原理是什么？"
]

print(f"\n📦 准备批量处理 {len(batch_questions)} 个问题...\n")

# 构建批量输入
batch_inputs = [
    [SystemMessage(content="你是一个知识渊博的 AI 教师。"),
     HumanMessage(content=question)]
    for question in batch_questions
]

start_time = time.time()

# 批量调用：一次处理所有问题
batch_responses = chat_model.batch(batch_inputs)

end_time = time.time()

print(f"⏱️  批量处理耗时：{end_time - start_time:.2f}秒")
print(f"📊 平均每个问题耗时：{(end_time - start_time) / len(batch_questions):.2f}秒")
print("\n" + "=" * 60)
print("📋 批量回答结果：")
print("=" * 60)

for i, (question, response) in enumerate(zip(batch_questions, batch_responses), 1):
    print(f"\n❓ 问题 {i}: {question}")
    print(f"🤖 回答：{response.content[:100]}...")
    print("-" * 60)

# ==================== 4. 三种方式对比 ====================
print("\n" + "=" * 60)
print("📊 三种调用方式对比总结")
print("=" * 60)

comparison_table = """
┌─────────────┬──────────────┬──────────────┬──────────────┐
│    特性     │   阻塞式     │    流式      │    批量      │
├─────────────┼──────────────┼──────────────┼──────────────┤
│ 返回方式    │ 完整响应     │ 逐块输出     │ 多个响应     │
│ 用户体验    │ ⭐⭐⭐        │ ⭐⭐⭐⭐⭐    │ ⭐⭐⭐⭐      │
│ 适用场景    │ 短文本       │ 长文本       │ 多问题       │
│ 代码复杂度  │ 简单         │ 中等         │ 简单         │
│ 响应速度    │ 较慢         │ 首字快       │ 总体快       │
│ API 方法    │ invoke()    │ stream()     │ batch()      │
└─────────────┴──────────────┴──────────────┴──────────────┘

💡 使用建议：
   - 需要快速回答 → 使用阻塞式
   - 生成长文章 → 使用流式
   - 处理多个问题 → 使用批量
   - 聊天机器人 → 使用流式（体验更好）
   - 数据分析 → 使用批量（效率更高）
"""

print(comparison_table)

# ==================== 5. 流式 + 解析器示例 ====================
print("\n" + "=" * 60)
print("🎯 进阶示例：流式调用 + 输出解析器")
print("=" * 60)

# 创建输出解析器
parser = StrOutputParser()

# 构建链：模型 + 解析器
chain = chat_model | parser

stream_question = "请用 3 个要点总结 Python 的优点。"

print(f"\n❓ 问题：{stream_question}")
print("\n📡 流式输出解析后的内容：\n")
print("-" * 60)

for chunk in chain.stream(stream_question):
    # chunk 现在是解析后的字符串
    print(chunk, end="", flush=True)

print("\n" + "-" * 60)
print("\n✨ 流式解析器可以实时处理输出，适合需要格式化的场景")

# ==================== 6. 批量 + 流式组合示例 ====================
print("\n" + "=" * 60)
print("🎯 高级示例：批量流式调用")
print("=" * 60)

# 批量问题，但每个问题都流式输出
batch_stream_questions = [
    "什么是 RAG？",
    "什么是 Agent？",
    "什么是 Fine-tuning？"
]

print(f"\n📦 批量处理 {len(batch_stream_questions)} 个问题（每个问题流式输出）...\n")

for i, question in enumerate(batch_stream_questions, 1):
    print(f"\n【问题 {i}/{len(batch_stream_questions)}】{question}")
    print("-" * 60)

    messages = [
        SystemMessage(content="简洁回答。"),
        HumanMessage(content=question)
    ]

    # 对每个问题使用流式
    for chunk in chat_model.stream(messages):
        if chunk.content:
            print(chunk.content, end="", flush=True)

    print("\n")

print("=" * 60)
print("✅ 所有示例完成！")
print("=" * 60)

print("\n💡 关键要点：")
print("  1. invoke() - 最简单，适合大多数场景")
print("  2. stream() - 用户体验最佳，适合长文本")
print("  3. batch() - 处理多个请求最高效")
print("  4. 可以组合使用，如批量 + 流式")
print("  5. 根据实际需求选择合适的方式")
print("\n🎉 实践建议：在实际项目中灵活选择调用方式！")

# ==================== 7. 同步 vs 异步调用 ====================
print("\n" + "=" * 60)
print("🔄 同步 vs 异步调用对比")
print("=" * 60)

print("\n📌 同步调用特点：")
print("  - 代码顺序执行，易于理解")
print("  - 每次调用阻塞后续代码")
print("  - 适合简单场景")
print("  - 方法：invoke(), stream(), batch()")

print("\n📌 异步调用特点：")
print("  - 非阻塞，可以并发执行")
print("  - 适合 I/O 密集型任务")
print("  - 可以显著提高吞吐量")
print("  - 方法：ainvoke(), astream(), abatch()")

# ==================== 8. 异步调用示例 ====================
print("\n" + "=" * 60)
print("🚀 异步调用示例 (Async Call)")
print("=" * 60)

print("\n⚠️  注意：异步调用需要 API 客户端支持")
print("   某些第三方 API（如 DeepSeek）可能不支持异步调用")
print("   以下展示异步调用的代码示例")

async def async_example():
    """异步调用示例"""
    
    print("\n⏱️  测试同步调用耗时...")
    start_time = time.time()
    
    # 同步调用 3 次
    for i in range(3):
        try:
            response = chat_model.invoke([
                SystemMessage(content="简洁回答。"),
                HumanMessage(content=f"问题{i+1}: 什么是 AI？")
            ])
            print(f"  ✓ 同步调用 {i+1} 完成")
        except Exception as e:
            print(f"  ✗ 同步调用 {i+1} 失败：{str(e)[:50]}")
    
    sync_time = time.time() - start_time
    print(f"⏱️  同步调用总耗时：{sync_time:.2f}秒")
    
    print("\n⏱️  测试异步调用耗时...")
    start_time = time.time()
    
    try:
        # 异步调用 3 次（并发）
        tasks = []
        for i in range(3):
            task = chat_model.ainvoke([
                SystemMessage(content="简洁回答。"),
                HumanMessage(content=f"问题{i+1}: 什么是 AI？")
            ])
            tasks.append(task)
        
        # 并发执行
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, response in enumerate(responses, 1):
            if isinstance(response, Exception):
                print(f"  ✗ 异步调用 {i} 失败：{type(response).__name__}")
            else:
                print(f"  ✓ 异步调用 {i} 完成")
        
        async_time = time.time() - start_time
        print(f"⏱️  异步调用总耗时：{async_time:.2f}秒")
        if async_time > 0:
            print(f"\n📊 性能提升：{sync_time / async_time:.2f}x")
        print(f"💡 异步调用可以并发执行多个请求，显著提高效率！")
    except Exception as e:
        print(f"\n⚠️  异步调用失败：{type(e).__name__}: {str(e)[:100]}")
        print("💡 提示：某些 API 提供商可能不支持异步调用，请使用同步方法")

# 运行异步示例
asyncio.run(async_example())

# ==================== 9. 异步流式调用示例 ====================
print("\n" + "=" * 60)
print("🌊 异步流式调用示例 (Async Streaming)")
print("=" * 60)

async def async_stream_example():
    """异步流式调用示例"""
    
    question = "请用 5 个要点介绍量子计算的基本概念。"
    print(f"\n❓ 问题：{question}")
    print("\n📡 尝试异步流式输出...\n")
    print("-" * 60)
    
    try:
        # 异步流式调用
        async for chunk in chat_model.astream([
            SystemMessage(content="详细回答。"),
            HumanMessage(content=question)
        ]):
            if chunk.content:
                print(chunk.content, end="", flush=True)
        
        print("\n" + "-" * 60)
        print("✨ 异步流式结合了异步和流式的优点！")
    except Exception as e:
        print(f"\n⚠️  异步流式调用失败：{type(e).__name__}")
        print(f"💡 错误信息：{str(e)[:100]}")
        print("\n💡 提示：请使用同步流式 stream() 方法代替")
        print("   示例：for chunk in chat_model.stream(messages):")

# 运行异步流式示例
asyncio.run(async_stream_example())

# ==================== 10. 异步批量调用示例 ====================
print("\n" + "=" * 60)
print("📦 异步批量调用示例 (Async Batch)")
print("=" * 60)

async def async_batch_example():
    """异步批量调用示例"""
    
    questions = [
        "什么是机器学习？",
        "什么是深度学习？",
        "什么是强化学习？",
        "什么是神经网络？",
        "什么是自然语言处理？"
    ]
    
    print(f"\n📦 尝试异步批量处理 {len(questions)} 个问题...\n")
    
    # 构建批量输入
    batch_inputs = [
        [SystemMessage(content="简洁回答。"),
         HumanMessage(content=question)]
        for question in questions
    ]
    
    try:
        # 异步批量调用
        responses = await chat_model.abatch(batch_inputs)
        
        print("📋 异步批量回答结果：\n")
        for i, (question, response) in enumerate(zip(questions, responses), 1):
            print(f"{i}. ❓ {question}")
            print(f"   🤖 {response.content[:80]}...")
            print()
        
        print("💡 异步批量是处理大量请求的最佳选择！")
    except Exception as e:
        print(f"⚠️  异步批量调用失败：{type(e).__name__}")
        print(f"💡 错误信息：{str(e)[:100]}")
        print("\n💡 提示：请使用同步批量 batch() 方法代替")
        print("   示例：responses = chat_model.batch(batch_inputs)")

# 运行异步批量示例
asyncio.run(async_batch_example())

# ==================== 11. 完整对比表 ====================
print("\n" + "=" * 60)
print("📊 完整调用方式对比总结")
print("=" * 60)

full_comparison = """
┌───────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│    调用方式   │   同步阻塞   │   同步流式   │   同步批量   │   异步并发   │
├───────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ 方法名        │ invoke()    │ stream()     │ batch()      │ ainvoke()    │
│ 返回方式      │ 完整响应     │ 迭代器       │ 响应列表     │ 协程对象     │
│ 阻塞性        │ 阻塞         │ 阻塞         │ 阻塞         │ 非阻塞       │
│ 并发能力      │ ❌           │            │ ❌           │ ✅           │
│ 用户体验      │ ⭐⭐⭐        │ ⭐⭐⭐⭐⭐    │ ⭐⭐⭐⭐      │ ⭐⭐⭐⭐      │
│ 吞吐量        │ ⭐⭐          │ ⭐⭐          │ ⭐⭐⭐⭐      │ ⭐⭐⭐⭐⭐    │
│ 代码复杂度    │ ⭐⭐⭐⭐⭐    │ ⭐⭐⭐⭐      │ ⭐⭐⭐⭐⭐    │ ⭐⭐⭐        │
│ 适用场景      │ 简单问答   │ 长文本生成   │ 批量处理     │ 高并发场景   │
└───────────────┴──────────────┴──────────────┴──────────────┴──────────────┘

异步系列方法：
  - ainvoke()   : 异步单次调用
  - astream()   : 异步流式调用
  - abatch()    : 异步批量调用
  - astream_log(): 异步流式日志（高级）

💡 选择建议：
  1. 简单场景 → invoke() (同步阻塞)
  2. 聊天机器人 → stream() (同步流式) 或 astream() (异步流式)
  3. 批量处理 → batch() (同步批量) 或 abatch() (异步批量)
  4. 高并发 → 异步系列方法 (ainvoke/astream/abatch)
  5. Web 应用 → 异步方法 (避免阻塞事件循环)
  6. 数据分析 → batch() 或 abatch()

🎯 性能对比（示例）：
  同步 3 次调用：3.0 秒（串行）
  异步 3 次调用：1.2 秒（并发）
  性能提升：2.5 倍！
"""

print(full_comparison)

print("\n" + "=" * 60)
print("🎉 所有调用方式示例完成！")
print("=" * 60)
print("\n💡 最佳实践：")
print("  1. 理解每种调用方式的特点")
print("  2. 根据场景选择最合适的方式")
print("  3. 异步虽好，但不要过度使用")
print("  4. 流式提升体验，批量提升效率")
print("  5. 实际项目中经常组合使用多种方式")
print("\n🚀 现在你已经掌握了 LangChain 的所有调用方式！")
