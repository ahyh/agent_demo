"""
使用传统的Tool方式向llm中添加tool
"""
from langchain_core.tools import Tool
from src.common import llm, prompt_template

def add_numbers(a: int, b: int) -> int:
    return a + b

# 定义一个tool
add_tool = Tool.from_function(
    func=add_numbers,
    name="add_numbers",
    description="用于将两个数字相加并返回结果"
)

# bind tools to llm
llm_with_tools = llm.bind_tools([add_tool])

chain = prompt_template | llm_with_tools

add_resp = chain.invoke(
    input={
        "role":"计算",
        "domain":"数学计算",
        "question":"算5加7等于多少？"
    }
)

# 返回的是tool message, 大模型只会告诉你应该要调用哪个工具，大模型不会自己调用tool
print("\n", add_resp)

for tool_call in add_resp.tool_calls:
    print(f"调用工具: {tool_call['name']}")
    print(f"工具参数: {tool_call['args']}")

    # 手动调用工具
    if tool_call["name"] == "add_numbers":
        a = int(tool_call["args"]["__arg1"])
        b = int(tool_call["args"]["__arg2"])
        result = add_numbers(a, b)
        print(f"工具返回结果: {result}")