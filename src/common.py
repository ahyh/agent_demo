import os

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, ChatMessagePromptTemplate
from pydantic import BaseModel, Field
from langchain_ollama.chat_models import ChatOllama

local_qwen = ChatOllama(model="deepseek-r1:14b")

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-R1",
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn",
    streaming=True,
)

deepseek = ChatOpenAI(
    model="deepseek-ai/DeepSeek-R1",
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn",
    streaming=True,
)

system_message_template = ChatMessagePromptTemplate.from_template(
    template="你是一位{role}专家，擅长回答{domain}领域的问题",
    role="system",
)

human_message_template = ChatMessagePromptTemplate.from_template(
    template="用户问题: {question}",
    role="user",
)


prompt_template = ChatPromptTemplate.from_messages([
    system_message_template,
    human_message_template,
])

class AddInputArgs(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")

@tool(
    description="用于将两个数字相减并返回结果",
    args_schema=AddInputArgs,
    return_direct=True
)
def add_numbers(a: int, b: int) -> int:
    return a + b

def create_calc_tools():
    return [add_numbers]

calc_tools = create_calc_tools()