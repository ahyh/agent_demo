import asyncio
import os

from langchain_classic.agents import initialize_agent, AgentType
from langchain_core.prompts import PromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
from src.common import local_qwen

# 创建客户端
async def create_amap_client():
    amap_key = os.getenv("amap_key")
    mcp_config = {
        "amap": {
            "url": "https://mcp.amap.com/sse?key=" + amap_key,
            "transport": "sse"
        }
    }
    client = MultiServerMCPClient(mcp_config)

    tools = await client.get_tools()

    return client, tools

async def create_amap_agent(question: str):
    client, tools = await create_amap_client()

    # 创建agent
    agent = initialize_agent(
        llm=local_qwen,
        tools=tools,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    template = PromptTemplate.from_template(
        "你是一个智能助手，可以调用高德MCP工具。\n\n 问题：{question}"
    )
    prompt = template.format(
        question=question
    )

    print(prompt)

    resp = await agent.ainvoke(prompt)
    print(resp)
    return resp



if __name__ == "__main__":
    question = """
    提供北京南站的坐标信息
    """
    asyncio.run(create_amap_agent(question=question))