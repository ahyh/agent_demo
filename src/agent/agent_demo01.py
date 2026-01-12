"""
创建智能体
"""
import json

from langchain_classic.agents import initialize_agent, AgentType
from pydantic import BaseModel, Field

from src.common import llm, create_calc_tools, prompt_template

# 返回结果json
from langchain_core.output_parsers import JsonOutputParser

class Output(BaseModel):
    args: str = Field("工具的入参")
    result: str = Field("计算的结果")

parser = JsonOutputParser(pydantic_object=Output)
format_instructions = parser.get_format_instructions()
# print(format_instructions)

tools = create_calc_tools()

llm_with_tools = llm.bind_tools(tools)

# 定义一个简单的智能体
agent = initialize_agent(
    tools=tools,
    llm=llm_with_tools,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

prompt = prompt_template.format_messages(
    role="计算",
    domain="使用工具进行数学计算",
    question=f"""
请阅读下面的问题，并返回一个严格的JSON对象，不要使用markdown代码块包裹！
格式要求:
{format_instructions}

问题:
100+200=?
"""
)

resp = agent.invoke(prompt)
print(resp)
print(resp["output"])
# print(type(resp["output"]))
# print(json.loads(resp["output"]))