"""
LangSmith 示例 - 追踪和监控 LangChain 应用
注意：使用 LangSmith 需要设置环境变量:
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your_api_key_here
export LANGCHAIN_PROJECT=your_project_name
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def setup_langsmith():
    """设置 LangSmith 环境变量"""
    
    # 检查是否已设置必要的环境变量
    if not os.getenv("LANGCHAIN_API_KEY"):
        print("警告: 未设置 LANGCHAIN_API_KEY")
        print("请在 .env 文件中设置以下环境变量:")
        print("LANGCHAIN_TRACING_V2=true")
        print("LANGCHAIN_API_KEY=your_api_key_here")
        print("LANGCHAIN_PROJECT=your_project_name")
        return False
    
    # 启用追踪
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    
    # 可选：设置项目名称（默认为 default）
    if not os.getenv("LANGCHAIN_PROJECT"):
        os.environ["LANGCHAIN_PROJECT"] = "langsmith-demo"
    
    print("LangSmith 追踪已启用")
    return True


def create_simple_chain_with_tracing():
    """创建带追踪的简单链"""
    
    print("\n=== 创建带 LangSmith 追踪的链 ===")
    
    # 创建 LLM 实例
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    
    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的助手，请简洁地回答用户的问题。"),
        ("user", "{question}")
    ])
    
    # 创建输出解析器
    output_parser = StrOutputParser()
    
    # 构建链
    chain = prompt | llm | output_parser
    
    return chain


def run_traced_example():
    """运行带追踪的示例"""
    
    print("=== LangSmith 追踪示例 ===\n")
    
    # 设置 LangSmith
    if not setup_langsmith():
        print("\n跳过示例运行，因为未配置 LangSmith API Key")
        print("要运行此示例，请:")
        print("1. 在 https://smith.langchain.com 注册账号")
        print("2. 获取 API Key")
        print("3. 在 demo/demo5-langSmith/.env 文件中配置环境变量")
        return
    
    try:
        # 创建链
        chain = create_simple_chain_with_tracing()
        
        # 运行多个示例，这些都会被追踪到 LangSmith
        questions = [
            "什么是机器学习？",
            "Python 的主要优势是什么？",
            "如何学习编程？"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\n问题 {i}: {question}")
            
            # 调用链（会自动追踪到 LangSmith）
            response = chain.invoke({"question": question})
            
            print(f"回答: {response[:100]}..." if len(response) > 100 else f"回答: {response}")
        
        print("\n✓ 所有调用已追踪到 LangSmith")
        print("访问 https://smith.langchain.com 查看追踪详情")
        
    except Exception as e:
        print(f"\n错误: {e}")
        print("请确保:")
        print("1. 已安装 langchain-openai: pip install langchain-openai")
        print("2. 已设置 OPENAI_API_KEY 环境变量")
        print("3. 已正确配置 LangSmith API Key")


def create_batch_processing_example():
    """批量处理示例 - 展示如何追踪批量调用"""
    
    print("\n=== 批量处理追踪示例 ===")
    
    if not setup_langsmith():
        return
    
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        
        prompt = ChatPromptTemplate.from_template("请将以下内容翻译成中文: {text}")
        chain = prompt | llm | StrOutputParser()
        
        texts = [
            "Hello, World!",
            "Machine Learning is fascinating.",
            "Python is a versatile programming language."
        ]
        
        print("\n批量翻译示例:")
        for text in texts:
            result = chain.invoke({"text": text})
            print(f"原文: {text}")
            print(f"翻译: {result}\n")
        
        print("✓ 批量调用已追踪")
        
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    run_traced_example()
    create_batch_processing_example()