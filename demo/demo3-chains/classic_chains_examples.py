"""
LangChain Classic Chain 类型示例
============================================
本示例展示 LLMMathChain、LLMRouterChain、StuffDocumentsChain、
SequentialChain 和 SimpleSequentialChain 的使用
"""
from langchain_classic.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_classic.chains.llm_math.base import LLMMathChain
from langchain_classic.chains.router import LLMRouterChain
from langchain_classic.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_classic.chains.sequential import SequentialChain, SimpleSequentialChain
import os
import dotenv

# 加载环境变量
dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

# 创建聊天模型实例
llm = ChatOpenAI(model="deepseek-chat", temperature=0)

print("=" * 60)
print("🔢 LangChain Classic Chain 示例")
print("=" * 60)

# ==================== 1. LLMMathChain - 数学计算链 ====================
print("\n" + "=" * 60)
print("案例 1：LLMMathChain - 数学计算链")
print("=" * 60)

print("\n📌 特点：专门用于解决数学计算问题，使用 Python 表达式精确计算")

# 创建 LLMMathChain
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

# 测试数学问题
math_questions = [
    "25 乘以 38 等于多少？",
    "如果一件商品原价 200 元，先打 9 折再减 20 元，最终价格是多少？",
    "计算：(15 + 25) * 3 - 20 / 4",
    "100 的 15% 是多少？",
    "一个长方形的长是 12.5 米，宽是 8.3 米，面积是多少？"
]

print("\n🧮 数学计算测试：")
for i, question in enumerate(math_questions, 1):
    print(f"\n{i}. ❓ 问题：{question}")
    try:
        result = llm_math_chain.invoke(question)
        print(f"   ✅ 答案：{result['answer']}")
    except Exception as e:
        print(f"   ❌ 错误：{e}")

# ==================== 2. LLMRouterChain - 路由链 ====================
print("\n" + "=" * 60)
print("案例 2：LLMRouterChain - 路由链")
print("=" * 60)

print("\n📌 特点：根据输入内容自动路由到最合适的处理链")

# 定义不同的目标链
# 物理学链
physics_prompt = PromptTemplate.from_template("""
你是一位物理学家。请解释以下物理学问题：

{input}

解释：
""")

# 数学链
math_prompt = PromptTemplate.from_template("""
你是一位数学家。请解决以下数学问题：

{input}

解答：
""")

# 历史学链
history_prompt = PromptTemplate.from_template("""
你是一位历史学家。请回答以下历史学问题：

{input}

回答：
""")

# 创建路由链
# 定义路由信息
router_info = {
    "physics": {
        "name": "物理学",
        "description": "物理学相关问题，如力学、电磁学、量子物理等",
        "prompt": physics_prompt
    },
    "math": {
        "name": "数学",
        "description": "数学相关问题，如代数、几何、微积分等",
        "prompt": math_prompt
    },
    "history": {
        "name": "历史学",
        "description": "历史学相关问题，如古代文明、战争、重要事件等",
        "prompt": history_prompt
    }
}

# 路由提示词
router_prompt = PromptTemplate.from_template("""
你是一个路由助手。请分析用户的问题，并将其路由到最合适的专家链。

可用选项：
- physics: {physics_desc}
- math: {math_desc}
- history: {history_desc}

问题：{input}

你应该路由到哪个选项？（只返回选项名称：physics、math 或 history）
""")

# 创建 LLMRouterChain
class CustomLLMRouterChain(LLMRouterChain):
    """自定义 LLM 路由链"""
    
    @classmethod
    def from_llm(cls, llm, router_prompt, routes, verbose=False):
        """从 LLM 创建路由链"""
        return cls(
            llm=llm,
            route_prompt=router_prompt,
            routes=routes,
            verbose=verbose
        )

# 简化版本：使用 RunnableLambda 实现路由
from langchain_core.runnables import RunnableLambda

def route_function(input_data: dict) -> str:
    """路由函数"""
    query = input_data["input"].lower()
    
    # 关键词路由
    math_keywords = ['计算', '多少', '数学', '价格', '数量', '等于', '面积', '体积']
    physics_keywords = ['物理', '力', '电', '磁', '光', '热', '能量', '速度']
    history_keywords = ['历史', '古代', '战争', '朝代', '皇帝', '文明', '事件']
    
    if any(kw in query for kw in physics_keywords):
        return "physics"
    elif any(kw in query for kw in math_keywords):
        return "math"
    elif any(kw in query for kw in history_keywords):
        return "history"
    else:
        return "math"  # 默认

# 创建路由链
physics_chain = physics_prompt | llm | StrOutputParser()
math_chain = math_prompt | llm | StrOutputParser()
history_chain = history_prompt | llm | StrOutputParser()

def router_chain(input_data: dict) -> str:
    """路由处理"""
    route = route_function(input_data)
    print(f"  🎯 路由到：{route}")
    
    if route == "physics":
        return physics_chain.invoke(input_data)
    elif route == "math":
        return math_chain.invoke(input_data)
    else:
        return history_chain.invoke(input_data)

# 测试路由链
test_queries = [
    "牛顿第二定律是什么？",
    "计算 25 乘以 38 等于多少？",
    "唐朝的建立者是谁？",
    "什么是量子力学？",
    "圆的面积公式是什么？"
]

print("\n🔀 路由链测试：")
for query in test_queries:
    print(f"\n❓ 问题：{query}")
    try:
        result = router_chain({"input": query})
        print(f"  💬 回答：{result[:100]}...")
    except Exception as e:
        print(f"  ❌ 错误：{e}")

# ==================== 3. StuffDocumentsChain - 文档组合链 ====================
print("\n" + "=" * 60)
print("案例 3：StuffDocumentsChain - 文档组合链")
print("=" * 60)

print("\n📌 特点：将多个文档组合在一起，一次性处理")

# 准备文档
from langchain_core.documents import Document

documents = [
    Document(page_content="Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。", metadata={"source": "python_intro.txt"}),
    Document(page_content="Python 使用简洁的语法，强调代码可读性。", metadata={"source": "python_syntax.txt"}),
    Document(page_content="Python 广泛应用于 Web 开发、数据分析、人工智能等领域。", metadata={"source": "python_apps.txt"})
]

# 定义文档提示词
document_prompt = PromptTemplate.from_template("来源：{source}\n内容：{page_content}")

# 定义最终提示词
final_prompt = PromptTemplate.from_template("""
请基于以下文档信息回答问题：

{context}

问题：{question}

请综合所有文档信息，给出完整回答：
""")

# 创建 StuffDocumentsChain
stuff_chain = StuffDocumentsChain.from_orm(
    llm=llm,
    document_prompt=document_prompt,
    final_prompt=final_prompt
)

# 测试
question = "Python 语言有什么特点？它应用在哪些领域？"

print(f"\n📄 文档数量：{len(documents)}")
print(f"❓ 问题：{question}")

try:
    result = stuff_chain.invoke({
        "input_documents": documents,
        "question": question
    })
    print(f"\n💬 回答：{result['output_text']}")
except Exception as e:
    print(f"❌ 错误：{e}")
    print("\n💡 使用简化版本：")
    
    # 简化版本
    context = "\n\n".join([f"来源：{doc.metadata['source']}\n内容：{doc.page_content}" for doc in documents])
    simple_chain = final_prompt | llm | StrOutputParser()
    result = simple_chain.invoke({"context": context, "question": question})
    print(f"💬 回答：{result}")

# ==================== 4. SequentialChain - 顺序链 ====================
print("\n" + "=" * 60)
print("案例 4：SequentialChain - 顺序链")
print("=" * 60)

print("\n📌 特点：按顺序执行多个链，前一个的输出作为后一个的输入")

# 创建多个链
# 链 1：总结
summarize_prompt = PromptTemplate.from_template("""
请总结以下文本，列出 3 个要点：

{text}

要点：
""")

# 链 2：翻译
translate_prompt = PromptTemplate.from_template("""
请将以下总结翻译成英文：

{summary}

英文翻译：
""")

# 链 3：简化
simplify_prompt = PromptTemplate.from_template("""
请用更简单的语言重写以下英文：

{text}

简化版本：
""")

# 创建 SequentialChain

summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt, output_key="summary")
translate_chain = LLMChain(llm=llm, prompt=translate_prompt, output_key="translation")
simplify_chain = LLMChain(llm=llm, prompt=simplify_prompt, output_key="simplified")

# 组合成顺序链
sequential_chain = SequentialChain(
    chains=[summarize_chain, translate_chain, simplify_chain],
    input_variables=["text"],
    output_variables=["simplified"],
    verbose=True
)

# 测试文本
text = """
机器学习是人工智能的一个分支，它使用统计技术让计算机系统能够从数据中学习，
而无需明确编程。机器学习算法通过训练数据建立模型，然后使用该模型进行预测
或决策。主要类型包括监督学习、无监督学习和强化学习。
"""

print(f"\n📄 原始文本：{text[:50]}...")
print("\n🔗 处理流程：总结 → 翻译 → 简化")

try:
    result = sequential_chain.invoke({"text": text})
    print(f"\n✅ 最终结果：{result['simplified']}")
except Exception as e:
    print(f"❌ 错误：{e}")
    print("\n💡 使用 LCEL 实现：")
    
    # LCEL 实现
    from langchain_core.runnables import RunnablePassthrough
    
    lcel_chain = (
        summarize_prompt
        | llm
        | StrOutputParser()
        | (lambda x: {"summary": x})
        | translate_prompt
        | llm
        | StrOutputParser()
        | (lambda x: {"text": x})
        | simplify_prompt
        | llm
        | StrOutputParser()
    )
    
    result = lcel_chain.invoke({"text": text})
    print(f"✅ 最终结果：{result}")

# ==================== 5. SimpleSequentialChain - 简单顺序链 ====================
print("\n" + "=" * 60)
print("案例 5：SimpleSequentialChain - 简单顺序链")
print("=" * 60)

print("\n📌 特点：单输入单输出的顺序链，每个步骤只有一个输入和输出")

# 创建简单的处理步骤
# 步骤 1：生成标题
title_prompt = PromptTemplate.from_template("""
请为以下内容生成一个吸引人的标题：

{content}

标题：
""")

# 步骤 2：生成简介
intro_prompt = PromptTemplate.from_template("""
请根据以下标题写一段简短的介绍（50 字以内）：

{title}

介绍：
""")

# 步骤 3：生成标签
tags_prompt = PromptTemplate.from_template("""
请为以下内容生成 5 个标签（用逗号分隔）：

{content}

标签：
""")

# 创建 SimpleSequentialChain
title_chain = LLMChain(llm=llm, prompt=title_prompt, output_key="title")
intro_chain = LLMChain(llm=llm, prompt=intro_prompt, output_key="intro")
tags_chain = LLMChain(llm=llm, prompt=tags_prompt, output_key="tags")

# 简单顺序链（单输入单输出）
simple_sequential = SimpleSequentialChain(
    chains=[title_chain, intro_chain],
    verbose=True
)

# 测试内容
content = "人工智能技术在医疗领域的应用，包括疾病诊断、药物研发和个性化治疗"

print(f"\n📝 内容：{content[:50]}...")
print("\n🔗 处理流程：生成标题 → 生成简介")

try:
    result = simple_sequential.invoke({"content": content})
    print(f"\n✅ 标题：{result['title']}")
    print(f"✅ 简介：{result['intro']}")
except Exception as e:
    print(f"❌ 错误：{e}")

# 多步骤简单顺序链
print("\n" + "-" * 60)
print("多步骤简单顺序链：生成标题 → 生成简介 → 生成标签")

# 使用 LCEL 实现多步骤
multi_step_chain = (
    {"content": lambda x: x["content"]}
    | title_prompt
    | llm
    | StrOutputParser()
    | (lambda x: {"title": x, "content": x})
    | intro_prompt
    | llm
    | StrOutputParser()
)

result = multi_step_chain.invoke({"content": content})
print(f"\n✅ 标题：{result[:50]}...")

print("\n" + "=" * 60)
print("✅ 所有 Classic Chain 示例完成！")
print("=" * 60)

print("\n💡 关键要点：")
print("  1. LLMMathChain - 精确数学计算，使用 Python 表达式")
print("  2. LLMRouterChain - 智能路由到专业处理链")
print("  3. StuffDocumentsChain - 组合多个文档一起处理")
print("  4. SequentialChain - 多步骤顺序处理，支持多输入输出")
print("  5. SimpleSequentialChain - 简单顺序链，单输入单输出")
print("\n🎉 Classic Chain 提供了丰富的预置链类型！")
