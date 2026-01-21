import os

from langchain_openai import ChatOpenAI
from langchain_ollama.chat_models import ChatOllama

local_qwen = ChatOllama(model="qwen3:8b")

local_deepseek = ChatOllama(model="deepseek-r1:14b")

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