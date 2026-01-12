"""
使用@tool装饰器来绑定tool
"""

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.common import llm, prompt_template

class SubInputArgs(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")

# 通过@tool装饰器来注册tool
@tool(
    description="用于将两个数字相减并返回结果",
    args_schema=SubInputArgs
)
def sub_numbers(a: int, b: int) -> int:
    return a - b

llm_with_tools = llm.bind_tools([sub_numbers])

sub_chain = prompt_template | llm_with_tools

sub_resp = sub_chain.invoke(
    input={
        "role":"计算",
        "domain":"数学计算",
        "question":"15-7=?"
    }
)


print("\n", sub_resp)
for tool_call in sub_resp.tool_calls:
    print(f"调用工具: {tool_call['name']}")
    print(f"工具参数: {tool_call['args']}")

func_dict = {
    "sub_numbers": sub_numbers,
}

for tool_call in sub_resp.tool_calls:
    print(f"调用工具: {tool_call}")
    a = int(tool_call["args"]["a"])
    b = int(tool_call["args"]["b"])
    tool_func = func_dict.get(tool_call["name"])
    result = tool_func.invoke(tool_call["args"])
    print(f"工具返回结果: {result}")