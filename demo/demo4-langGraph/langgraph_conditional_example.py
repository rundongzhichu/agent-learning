"""
LangGraph 条件分支示例 - 根据输入内容选择不同的处理路径
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator


# 定义状态结构
class ConditionalState(TypedDict):
    """条件工作流的状态定义"""
    input_text: str  # 用户输入
    category: str  # 分类结果
    response: str  # 响应内容
    steps_taken: list  # 执行的步骤记录


def classify_input(state: ConditionalState) -> dict:
    """分类用户输入"""
    print(f"分类输入: {state['input_text']}")
    
    # 简单的关键词分类逻辑
    text_lower = state['input_text'].lower()
    
    if '问题' in text_lower or '疑问' in text_lower:
        category = "question"
    elif '命令' in text_lower or '指令' in text_lower:
        category = "command"
    else:
        category = "general"
    
    return {
        "category": category,
        "steps_taken": [f"classified_as_{category}"]
    }


def handle_question(state: ConditionalState) -> dict:
    """处理问题类型输入"""
    print("处理问题类型输入")
    return {
        "response": f"这是对问题 '{state['input_text']}' 的回答",
        "steps_taken": ["handled_question"]
    }


def handle_command(state: ConditionalState) -> dict:
    """处理命令类型输入"""
    print("处理命令类型输入")
    return {
        "response": f"执行命令: {state['input_text']}",
        "steps_taken": ["handled_command"]
    }


def handle_general(state: ConditionalState) -> dict:
    """处理一般类型输入"""
    print("处理一般类型输入")
    return {
        "response": f"收到一般信息: {state['input_text']}",
        "steps_taken": ["handled_general"]
    }


def route_by_category(state: ConditionalState) -> str:
    """根据分类路由到不同处理节点"""
    if state['category'] == 'question':
        return "handle_question"
    elif state['category'] == 'command':
        return "handle_command"
    else:
        return "handle_general"


def create_conditional_workflow():
    """创建带条件分支的工作流"""
    
    workflow = StateGraph(ConditionalState)
    
    # 添加节点
    workflow.add_node("classify", classify_input)
    workflow.add_node("handle_question", handle_question)
    workflow.add_node("handle_command", handle_command)
    workflow.add_node("handle_general", handle_general)
    
    # 设置入口点
    workflow.set_entry_point("classify")
    
    # 添加条件边
    workflow.add_conditional_edges(
        "classify",
        route_by_category,
        {
            "handle_question": "handle_question",
            "handle_command": "handle_command", 
            "handle_general": "handle_general"
        }
    )
    
    # 所有处理节点都连接到结束
    workflow.add_edge("handle_question", END)
    workflow.add_edge("handle_command", END)
    workflow.add_edge("handle_general", END)
    
    # 编译工作流
    app = workflow.compile()
    
    return app


def run_conditional_workflow():
    """运行条件分支工作流"""
    print("=== 运行条件分支 LangGraph 工作流 ===")
    
    app = create_conditional_workflow()
    
    # 测试不同类型的输入
    test_inputs = [
        "我有一个问题需要解答",
        "请执行这个命令操作", 
        "今天天气不错"
    ]
    
    for i, input_text in enumerate(test_inputs, 1):
        print(f"\n--- 测试 {i}: {input_text} ---")
        
        initial_state = {
            "input_text": input_text,
            "category": "",
            "response": "",
            "steps_taken": []
        }
        
        result = app.invoke(initial_state)
        
        print(f"分类结果: {result['category']}")
        print(f"响应内容: {result['response']}")
        print(f"执行步骤: {result['steps_taken']}")


if __name__ == "__main__":
    run_conditional_workflow()