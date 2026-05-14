"""
LangGraph 示例 - 构建一个简单的对话代理工作流
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator


# 定义状态结构
class AgentState(TypedDict):
    """代理的状态定义"""
    messages: Annotated[list, operator.add]  # 消息列表，使用 add 操作符进行累积
    current_step: str  # 当前步骤
    result: str  # 最终结果


def step_one(state: AgentState) -> dict:
    """第一步：处理输入"""
    print("执行步骤一：处理用户输入")
    return {
        "messages": ["步骤一完成"],
        "current_step": "step_one_completed"
    }


def step_two(state: AgentState) -> dict:
    """第二步：分析内容"""
    print("执行步骤二：分析内容")
    return {
        "messages": ["步骤二完成"],
        "current_step": "step_two_completed"
    }


def step_three(state: AgentState) -> dict:
    """第三步：生成响应"""
    print("执行步骤三：生成响应")
    return {
        "messages": ["步骤三完成"],
        "result": "这是最终的处理结果",
        "current_step": "completed"
    }


def create_simple_workflow():
    """创建简单的工作流图"""
    
    # 创建工作流图
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("step_one", step_one)
    workflow.add_node("step_two", step_two)
    workflow.add_node("step_three", step_three)
    
    # 设置入口点
    workflow.set_entry_point("step_one")
    
    # 添加边（连接节点）
    workflow.add_edge("step_one", "step_two")
    workflow.add_edge("step_two", "step_three")
    workflow.add_edge("step_three", END)
    
    # 编译工作流
    app = workflow.compile()
    
    return app


def run_simple_workflow():
    """运行简单工作流"""
    print("=== 运行简单 LangGraph 工作流 ===")
    
    app = create_simple_workflow()
    
    # 初始状态
    initial_state = {
        "messages": [],
        "current_step": "start",
        "result": ""
    }
    
    # 运行工作流
    result = app.invoke(initial_state)
    
    print(f"最终结果: {result['result']}")
    print(f"所有消息: {result['messages']}")
    print(f"当前步骤: {result['current_step']}")
    
    return result


if __name__ == "__main__":
    run_simple_workflow()