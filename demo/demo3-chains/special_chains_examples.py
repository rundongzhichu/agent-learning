"""
LangChain 特殊 Chain 类型示例
============================================
本示例展示数学链、路由链和文档链的使用场景
"""
from langchain_classic.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_classic.chains.llm_math.base import LLMMathChain
from langchain_classic.chains.router import LLMRouterChain
from langchain_classic.chains.sequential import SequentialChain, SimpleSequentialChain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.runnables import RunnableLambda, RunnableBranch
import os
import dotenv
import re

# 加载环境变量
dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

# 创建聊天模型实例
llm = ChatOpenAI(model="deepseek-chat")

print("=" * 60)
print("🔢 LangChain 特殊 Chain 类型示例")
print("=" * 60)

# ==================== 1. 数学链 (Math Chain) ====================
print("\n" + "=" * 60)
print("案例 1：数学链 (Math Chain)")
print("=" * 60)

print("\n📌 特点：专门用于处理数学计算问题，结合 LLM 理解和精确计算")

# 方法 1：使用工具增强数学能力
@tool
def add(a: float, b: float) -> float:
    """两个数相加"""
    return a + b

@tool
def multiply(a: float, b: float) -> float:
    """两个数相乘"""
    return a * b

@tool
def calculate_percentage(value: float, percent: float) -> float:
    """计算百分比"""
    return value * (percent / 100)

@tool
def solve_equation(equation: str) -> float:
    """解简单数学方程"""
    try:
        # 安全的表达式计算
        return eval(equation.replace('^', '**'))
    except:
        return 0.0

math_tools = [add, multiply, calculate_percentage, solve_equation]
llm_with_math = llm.bind_tools(math_tools)

# 测试数学问题
math_questions = [
    "25 乘以 4 等于多少？",
    "如果一件商品原价 200 元，打 8 折后的价格是多少？",
    "计算：(15 + 25) * 3 - 20",
    "100 的 15% 是多少？"
]

print("\n🧮 数学计算测试：")
for question in math_questions:
    print(f"\n❓ 问题：{question}")
    
    response = llm_with_math.invoke(question)
    
    if hasattr(response, 'tool_calls') and response.tool_calls:
        for tool_call in response.tool_calls:
            print(f"  🔧 使用工具：{tool_call['name']}")
            print(f"  📝 参数：{tool_call['args']}")
            
            # 执行工具
            for t in math_tools:
                if t.name == tool_call['name']:
                    result = t.invoke(tool_call['args'])
                    print(f"  ✅ 结果：{result}")
    else:
        print(f"  💬 回答：{response.content[:80]}...")

# 方法 2：使用提示词模板处理应用题
print("\n" + "-" * 60)
print("方法 2：数学应用题求解")

math_word_problem_prompt = PromptTemplate.from_template("""
请逐步解决以下数学应用题：

题目：{problem}

要求：
1. 分析题目中的已知条件
2. 列出解题步骤
3. 给出最终答案
4. 验证答案的合理性

解答：
""")

word_problems = [
    "小明去超市买了 3 个苹果，每个苹果 2.5 元，又买了 2 瓶牛奶，每瓶 5 元。他给了收银员 50 元，应该找回多少钱？",
    "一个长方形花坛的长是 8 米，宽是 5 米。如果要在花坛周围围一圈栅栏，需要多少米的栅栏？如果每平方米种 4 朵花，这个花坛可以种多少朵花？"
]

math_chain = math_word_problem_prompt | llm | StrOutputParser()

for problem in word_problems:
    print(f"\n📝 题目：{problem[:50]}...")
    result = math_chain.invoke({"problem": problem})
    print(f"✅ 解答：{result[:150]}...\n")

# ==================== 2. 路由链 (Routing Chain) ====================
print("\n" + "=" * 60)
print("案例 2：路由链 (Routing Chain)")
print("=" * 60)

print("\n📌 特点：根据输入内容自动路由到合适的处理链")

# 定义路由函数
def route_query(query: str) -> str:
    """根据问题类型路由到不同的处理链"""
    query_lower = query.lower()
    
    # 关键词匹配路由
    if any(word in query_lower for word in ['计算', '多少', '数学', '价格', '数量']):
        return "math_chain"
    elif any(word in query_lower for word in ['翻译', 'translate', '英文', '中文']):
        return "translation_chain"
    elif any(word in query_lower for word in ['总结', '概括', '要点', '摘要']):
        return "summary_chain"
    elif any(word in query_lower for word in ['解释', '什么是', '为什么', '如何']):
        return "explanation_chain"
    else:
        return "general_chain"

# 定义不同的处理链
math_chain = (
    PromptTemplate.from_template("""
    请计算以下数学问题：
    {query}
    
    计算步骤和答案：
    """)
    | llm
    | StrOutputParser()
)

translation_chain = (
    PromptTemplate.from_template("""
    请将以下内容翻译成英文：
    {query}
    
    英文翻译：
    """)
    | llm
    | StrOutputParser()
)

summary_chain = (
    PromptTemplate.from_template("""
    请总结以下内容的要点：
    {query}
    
    要点总结：
    """)
    | llm
    | StrOutputParser()
)

explanation_chain = (
    PromptTemplate.from_template("""
    请详细解释以下问题：
    {query}
    
    解释：
    """)
    | llm
    | StrOutputParser()
)

general_chain = (
    PromptTemplate.from_template("""
    请回答以下问题：
    {query}
    
    回答：
    """)
    | llm
    | StrOutputParser()
)

# 使用 RunnableBranch 实现路由
router = RunnableBranch(
    (lambda x: route_query(x["query"]) == "math_chain", math_chain),
    (lambda x: route_query(x["query"]) == "translation_chain", translation_chain),
    (lambda x: route_query(x["query"]) == "summary_chain", summary_chain),
    (lambda x: route_query(x["query"]) == "explanation_chain", explanation_chain),
    general_chain  # 默认
)

# 测试路由链
test_queries = [
    "25 乘以 38 等于多少？",
    "请把'你好，世界'翻译成英文",
    "总结一下机器学习的主要特点",
    "什么是深度学习？",
    "今天天气怎么样？"
]

print("\n🔀 路由链测试：")
for query in test_queries:
    print(f"\n❓ 问题：{query}")
    route_type = route_query(query)
    print(f"  🎯 路由到：{route_type}")
    
    result = router.invoke({"query": query})
    print(f"  💬 回答：{result[:80]}...")

# 智能路由：使用 LLM 判断意图
print("\n" + "-" * 60)
print("方法 2：基于 LLM 的智能路由")

intent_classifier_prompt = PromptTemplate.from_template("""
请分析以下问题的意图，并分类到以下类别之一：
- MATH: 数学计算问题
- TRANSLATION: 翻译问题
- SUMMARY: 总结概括问题
- EXPLANATION: 解释说明问题
- GENERAL: 一般问题

问题：{query}

类别（只返回类别名称）：
""")

intent_chain = intent_classifier_prompt | llm | StrOutputParser()

def smart_router(input_data: dict) -> str:
    """智能路由"""
    query = input_data["query"]
    
    # 使用 LLM 判断意图
    intent = intent_chain.invoke({"query": query}).strip()
    print(f"  🧠 LLM 判断意图：{intent}")
    
    # 根据意图路由
    if "MATH" in intent.upper():
        return math_chain.invoke({"query": query})
    elif "TRANSLATION" in intent.upper():
        return translation_chain.invoke({"query": query})
    elif "SUMMARY" in intent.upper():
        return summary_chain.invoke({"query": query})
    elif "EXPLANATION" in intent.upper():
        return explanation_chain.invoke({"query": query})
    else:
        return general_chain.invoke({"query": query})

print("\n🧠 智能路由测试：")
smart_queries = [
    "计算 123 + 456",
    "苹果用英语怎么说？",
    "用一句话概括这篇文章",
    "黑洞是怎么形成的？"
]

for query in smart_queries:
    print(f"\n❓ 问题：{query}")
    result = smart_router({"query": query})
    print(f"  💬 回答：{result[:80]}...")

# ==================== 3. 文档链 (Document Chain) ====================
print("\n" + "=" * 60)
print("案例 3：文档链 (Document Chain)")
print("=" * 60)

print("\n📌 特点：专门用于处理文档相关的任务，如总结、问答、分析等")

# 模拟文档内容
sample_documents = [
    {
        "title": "人工智能发展报告",
        "content": """
        2024 年，人工智能技术取得了重大突破。在语言模型方面，GPT-5 和 Gemini 2.0 
        等新一代大模型的发布，显著提升了 AI 的理解和生成能力。在视觉领域，多模态模型
        能够同时处理文本、图像和音频信息。产业应用方面，AI 已广泛应用于医疗、金融、
        教育等领域，推动了各行业的数字化转型。专家预测，未来 5 年 AI 将为全球经济
        贡献超过 15 万亿美元的价值。
        """
    },
    {
        "title": "Python 编程语言介绍",
        "content": """
        Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。Python 的
        设计哲学强调代码的可读性和简洁性，使用缩进来定义代码块。Python 支持多种
        编程范式，包括面向对象、函数式和过程式编程。在应用领域，Python 广泛用于
        Web 开发、数据分析、人工智能、科学计算等。Python 拥有丰富的第三方库生态
        系统，如 NumPy、Pandas、TensorFlow 等，大大提升了开发效率。
        """
    }
]

# 3.1 文档总结链
print("\n📄 子案例 3.1：文档总结链")

summarize_doc_prompt = PromptTemplate.from_template("""
请总结以下文档的核心内容，列出 3-5 个要点：

文档标题：{title}
文档内容：{content}

要点总结：
""")

summarize_chain = summarize_doc_prompt | llm | StrOutputParser()

for doc in sample_documents:
    print(f"\n📝 文档：《{doc['title']}》")
    summary = summarize_chain.invoke(doc)
    print(f"📋 总结：{summary[:150]}...\n")

# 3.2 文档问答链
print("\n📄 子案例 3.2：文档问答链")

qa_doc_prompt = PromptTemplate.from_template("""
请根据以下文档内容回答问题。如果文档中没有相关信息，请说明。

文档标题：{title}
文档内容：{content}

问题：{question}

回答：
""")

qa_chain = qa_doc_prompt | llm | StrOutputParser()

qa_pairs = [
    {"doc_index": 0, "question": "2024 年 AI 领域有哪些重要突破？"},
    {"doc_index": 0, "question": "AI 将为全球经济贡献多少价值？"},
    {"doc_index": 1, "question": "Python 是谁创建的？"},
    {"doc_index": 1, "question": "Python 在哪些领域应用广泛？"}
]

for qa in qa_pairs:
    doc = sample_documents[qa["doc_index"]]
    print(f"\n📝 文档：《{doc['title']}》")
    print(f"❓ 问题：{qa['question']}")
    answer = qa_chain.invoke({
        "title": doc["title"],
        "content": doc["content"],
        "question": qa["question"]
    })
    print(f"💬 回答：{answer[:100]}...\n")

# 3.3 文档分析链（多步骤处理）
print("\n📄 子案例 3.3：文档分析链（多步骤处理）")

def analyze_document(doc: dict) -> dict:
    """多步骤文档分析"""
    
    # 步骤 1：提取关键信息
    extract_prompt = PromptTemplate.from_template("""
    从以下文档中提取关键信息：
    
    标题：{title}
    内容：{content}
    
    请提取：
    1. 主要主题（1-2 个词）
    2. 关键实体（人名、机构名等）
    3. 时间信息
    4. 核心观点（1 句话）
    
    以 JSON 格式返回。
    """)
    
    extract_chain = extract_prompt | llm | JsonOutputParser()
    extracted_info = extract_chain.invoke(doc)
    
    print(f"📊 提取的信息：{extracted_info}")
    
    # 步骤 2：情感分析
    sentiment_prompt = PromptTemplate.from_template("""
    请分析以下文档的情感倾向（正面/负面/中性），并说明理由：
    
    {content}
    
    情感倾向：
    """)
    
    sentiment_chain = sentiment_prompt | llm | StrOutputParser()
    sentiment = sentiment_chain.invoke({"content": doc["content"]})
    
    print(f"💭 情感分析：{sentiment[:50]}...")
    
    # 步骤 3：生成标签
    tag_prompt = PromptTemplate.from_template("""
    请为以下文档生成 5 个标签（关键词）：
    
    {content}
    
    标签（用逗号分隔）：
    """)
    
    tag_chain = tag_prompt | llm | StrOutputParser()
    tags = tag_chain.invoke({"content": doc["content"]})
    
    print(f"🏷️ 标签：{tags}")
    
    return {
        "extracted_info": extracted_info,
        "sentiment": sentiment,
        "tags": tags
    }

print("\n🔍 多步骤文档分析：")
for i, doc in enumerate(sample_documents, 1):
    print(f"\n📄 文档 {i}：《{doc['title']}》")
    analysis = analyze_document(doc)
    print(f"✅ 分析完成\n")

# 3.4 文档对比链
print("\n📄 子案例 3.4：文档对比链")

compare_docs_prompt = PromptTemplate.from_template("""
请对比以下两个文档的异同点：

文档 1：
标题：{title1}
内容：{content1}

文档 2：
标题：{title2}
内容：{content2}

请从以下方面对比：
1. 主题差异
2. 内容重点
3. 写作风格
4. 目标受众

对比分析：
""")

compare_chain = compare_docs_prompt | llm | StrOutputParser()

print("\n🔄 文档对比：")
if len(sample_documents) >= 2:
    doc1, doc2 = sample_documents[0], sample_documents[1]
    print(f"对比：《{doc1['title']}》vs《{doc2['title']}》")
    
    comparison = compare_chain.invoke({
        "title1": doc1["title"],
        "content1": doc1["content"],
        "title2": doc2["title"],
        "content2": doc2["content"]
    })
    print(f"📊 对比结果：{comparison[:200]}...\n")

print("\n" + "=" * 60)
print("✅ 所有特殊 Chain 类型示例完成！")
print("=" * 60)

print("\n💡 关键要点：")
print("  1. 数学链 - 结合工具和提示词处理数学问题")
print("  2. 路由链 - 根据问题类型智能分发到不同处理链")
print("  3. 文档链 - 多步骤处理文档（总结、问答、分析、对比）")
print("\n🎉 根据实际需求选择合适的 Chain 类型！")
