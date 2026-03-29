"""
LangChain Chain 类型实用案例
============================================
本示例展示 LangChain 中各种 Chain 类型的使用场景
"""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os
import dotenv

# 加载环境变量
dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

# 创建聊天模型实例
llm = ChatOpenAI(model="deepseek-chat")

print("=" * 60)
print("🔗 LangChain Chain 类型实用案例")
print("=" * 60)

# ==================== 1. Sequential Chain - 顺序链 ====================
print("\n" + "=" * 60)
print("案例 1：Sequential Chain - 顺序链")
print("=" * 60)

print("\n📌 特点：顺序执行多个组件，每个组件的输出作为下一个组件的输入")

# 定义多个处理步骤
summarize_prompt = PromptTemplate.from_template("""
请总结以下内容，列出 3 个要点：

{text}

要点：
""")

translate_prompt = PromptTemplate.from_template("""
请将以下总结翻译成英文：

{summary}

英文翻译：
""")

# 使用 LCEL 构建顺序链
sequential_chain = (
    summarize_prompt
    | llm
    | StrOutputParser()
    | (lambda x: {"summary": x})
    | translate_prompt
    | llm
    | StrOutputParser()
)

# 测试文本
text = """
机器学习是人工智能的一个分支，它使用统计技术让计算机系统能够从数据中学习，
而无需明确编程。机器学习算法通过训练数据建立模型，然后使用该模型进行预测
或决策。主要类型包括监督学习、无监督学习和强化学习。
"""

print(f"\n📄 原始文本：{text[:50]}...")
print("\n🔗 执行顺序：总结 → 翻译")

result = sequential_chain.invoke({"text": text})
print(f"\n📝 最终结果：{result}")

# ==================== 2. Conditional Chain - 条件链 ====================
print("\n" + "=" * 60)
print("案例 2：Conditional Chain - 条件链")
print("=" * 60)

print("\n📌 特点：根据条件执行不同的组件")

# 定义条件判断函数
def route_by_task(task_type: str) -> str:
    """根据任务类型路由到不同的处理链"""
    routes = {
        "summarize": "summarize_chain",
        "translate": "translate_chain",
        "explain": "explain_chain"
    }
    return routes.get(task_type, "explain_chain")

# 定义不同的处理链
summarize_chain = (
    PromptTemplate.from_template("请总结：{text}")
    | llm
    | StrOutputParser()
)

translate_chain = (
    PromptTemplate.from_template("请翻译成英文：{text}")
    | llm
    | StrOutputParser()
)

explain_chain = (
    PromptTemplate.from_template("请解释：{text}")
    | llm
    | StrOutputParser()
)

# 使用 RunnableBranch 实现条件链
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: x["task_type"] == "summarize", summarize_chain),
    (lambda x: x["task_type"] == "translate", translate_chain),
    explain_chain  # 默认
)

# 测试
test_cases = [
    {"task_type": "summarize", "text": "Python 是一种高级编程语言，具有简洁的语法。"},
    {"task_type": "translate", "text": "你好，世界"},
    {"task_type": "explain", "text": "什么是 API？"}
]

print("\n🎯 条件分支测试：")
for case in test_cases:
    result = branch.invoke(case)
    print(f"\n任务：{case['task_type']}")
    print(f"输入：{case['text']}")
    print(f"输出：{result[:50]}...")

# ==================== 3. Tool Chain - 工具链 ====================
print("\n" + "=" * 60)
print("案例 3：Tool Chain - 工具链")
print("=" * 60)

print("\n📌 特点：将工具与 LLM 组合，实现基于工具进行任务的处理")

# 定义工具
@tool
def calculate(expression: str) -> float:
    """计算数学表达式"""
    try:
        return eval(expression)
    except:
        return 0.0

@tool
def get_current_time(city: str = "北京") -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def search_knowledge(query: str) -> str:
    """搜索知识库"""
    knowledge_base = {
        "Python": "Python 是一种高级编程语言",
        "AI": "人工智能是模拟人类智能的技术",
        "ML": "机器学习是 AI 的分支，让计算机从数据中学习"
    }
    return knowledge_base.get(query, "未找到相关信息")

tools = [calculate, get_current_time, search_knowledge]

# 将工具绑定到 LLM
llm_with_tools = llm.bind_tools(tools)

# 测试工具调用
test_questions = [
    "请计算 25 * 4 + 100",
    "现在几点了？",
    "什么是 Python？"
]

print("\n🛠️ 工具调用测试：")
for question in test_questions:
    print(f"\n❓ 问题：{question}")
    
    response = llm_with_tools.invoke(question)
    
    if hasattr(response, 'tool_calls') and response.tool_calls:
        for tool_call in response.tool_calls:
            print(f"  🔧 调用工具：{tool_call['name']}")
            print(f"  📝 参数：{tool_call['args']}")
            
            # 执行工具
            for t in tools:
                if t.name == tool_call['name']:
                    result = t.invoke(tool_call['args'])
                    print(f"  ✅ 结果：{result}")
    else:
        print(f"  💬 回答：{response.content[:50]}...")

# ==================== 4. Custom Chain - 自定义链 ====================
print("\n" + "=" * 60)
print("案例 4：Custom Chain - 自定义链")
print("=" * 60)

print("\n📌 特点：自定义链，实现自定义的链式结构")

from langchain_core.runnables import RunnableLambda, RunnablePassthrough

# 定义自定义处理步骤
def add_context(text: str) -> dict:
    """添加上下文信息"""
    return {
        "original": text,
        "word_count": len(text),
        "timestamp": "2024"
    }

def format_with_context(data: dict) -> str:
    """格式化输出"""
    return f"""
【分析对象】
{data['original']}

【元数据】
- 字数：{data['word_count']}
- 年份：{data['timestamp']}

【分析结果】
"""

# 构建自定义链
custom_chain = (
    RunnableLambda(add_context)
    | format_with_context
    | (lambda x: x + "这是一个自定义的处理流程。")
    | (lambda x: {"text": x})
    | PromptTemplate.from_template("{text}请总结这个流程的特点。")
    | llm
    | StrOutputParser()
)

print("\n🔧 自定义链：添加上下文 → 格式化 → 处理")
result = custom_chain.invoke("Python 编程语言")
print(f"\n📝 结果：{result[:100]}...")

# ==================== 5. Multi-Task Chain - 多任务链 ====================
print("\n" + "=" * 60)
print("案例 5：Multi-Task Chain - 多任务链")
print("=" * 60)

print("\n📌 特点：同时处理多个任务")

# 定义多个任务
tasks = {
    "summarize": PromptTemplate.from_template("请总结：{text}"),
    "translate": PromptTemplate.from_template("请翻译成英文：{text}"),
    "keywords": PromptTemplate.from_template("请提取 3 个关键词：{text}"),
    "sentiment": PromptTemplate.from_template("请分析情感倾向：{text}")
}

# 构建多任务处理链
def process_multi_tasks(text: str):
    """并行处理多个任务"""
    from concurrent.futures import ThreadPoolExecutor
    
    results = {}
    
    def process_task(task_name, prompt):
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"text": text})
    
    with ThreadPoolExecutor() as executor:
        futures = {
            task_name: executor.submit(process_task, task_name, prompt)
            for task_name, prompt in tasks.items()
        }
        
        for task_name, future in futures.items():
            results[task_name] = future.result()
    
    return results

test_text = "人工智能技术正在快速发展，深度学习在图像识别和自然语言处理领域取得了重大突破。"

print(f"\n📄 文本：{test_text[:30]}...")
print("\n🔄 并行处理 4 个任务：总结、翻译、关键词、情感分析")

results = process_multi_tasks(test_text)

for task_name, result in results.items():
    print(f"\n{task_name.upper()}: {result[:50]}...")

# ==================== 6. Hybrid Chain - 混合链 ====================
print("\n" + "=" * 60)
print("案例 6：Hybrid Chain - 混合链")
print("=" * 60)

print("\n📌 特点：将多个链组合在一起，实现更复杂的任务处理")

# 第一层：信息提取
extraction_chain = (
    PromptTemplate.from_template("""
    从以下文本中提取关键信息：
    {text}
    
    请以 JSON 格式返回，包含：topic, key_points, sentiment
    """)
    | llm
    | JsonOutputParser()
)

# 第二层：基于提取结果生成报告
report_chain = (
    PromptTemplate.from_template("""
    基于以下提取的信息，生成一份简短报告：
    
    主题：{topic}
    要点：{key_points}
    情感：{sentiment}
    
    报告：
    """)
    | llm
    | StrOutputParser()
)

# 组合成混合链
def hybrid_process(text: str) -> str:
    """混合链处理"""
    # 第一步：提取信息
    extracted = extraction_chain.invoke({"text": text})
    
    # 第二步：生成报告
    report = report_chain.invoke({
        "topic": extracted.get("topic", "未知"),
        "key_points": extracted.get("key_points", []),
        "sentiment": extracted.get("sentiment", "中性")
    })
    
    return report

test_news = """
2024 年 3 月，OpenAI 发布了 GPT-5 模型，性能大幅提升。
该模型在语言理解、代码生成和多模态处理方面都有重大突破。
业界专家认为这将推动 AI 应用的快速发展。
"""

print(f"\n📰 新闻：{test_news[:30]}...")
print("\n🔗 混合链：信息提取 → 报告生成")

result = hybrid_process(test_news)
print(f"\n📝 生成的报告：{result[:100]}...")

# ==================== 7. Loop Chain - 循环链 ====================
print("\n" + "=" * 60)
print("案例 7：Loop Chain - 循环链")
print("=" * 60)

print("\n📌 特点：循环执行多个组件，直到满足条件")

# 定义迭代优化链
def iterative_refinement(initial_text: str, max_iterations: int = 3) -> str:
    """迭代优化文本"""
    current_text = initial_text
    
    for i in range(max_iterations):
        print(f"\n🔄 第 {i+1} 次迭代...")
        
        # 优化提示
        refine_prompt = PromptTemplate.from_template("""
        请优化以下文本，使其更简洁清晰：
        
        {text}
        
        优化后：
        """)
        
        chain = refine_prompt | llm | StrOutputParser()
        refined_text = chain.invoke({"text": current_text})
        
        print(f"优化前：{current_text[:50]}...")
        print(f"优化后：{refined_text[:50]}...")
        
        # 检查是否满足条件（长度小于 50）
        if len(refined_text) < 50:
            print("✅ 满足条件，停止迭代")
            return refined_text
        
        current_text = refined_text
    
    return current_text

initial_text = """
这是一个非常长的句子，包含了很多不必要的修饰词和重复的表达，
需要进行简化和优化，使其更加简洁明了。
"""

print(f"\n📝 初始文本：{initial_text[:30]}...")
print("\n🔄 循环优化直到长度<50")

result = iterative_refinement(initial_text)
print(f"\n✅ 最终结果：{result}")

print("\n" + "=" * 60)
print("✅ 所有 Chain 类型案例完成！")
print("=" * 60)

print("\n💡 关键要点：")
print("  1. Sequential Chain - 线性流程，简单直接")
print("  2. Conditional Chain - 条件分支，灵活路由")
print("  3. Tool Chain - 工具集成，扩展能力")
print("  4. Custom Chain - 自定义逻辑，满足特殊需求")
print("  5. Multi-Task Chain - 并行处理，提升效率")
print("  6. Hybrid Chain - 多层组合，处理复杂场景")
print("  7. Loop Chain - 迭代优化，逐步改进")
print("\n🎉 根据实际需求选择合适的 Chain 类型！")
