import asyncio

from langchain_classic.agents import initialize_agent, AgentType
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

from src.common import llm, local_qwen


# 获取playwright mcp tools
async def mcp_playwright_client():

    server_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp@latest"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print(tools)

            agent = initialize_agent(
                llm=llm,
                tools=tools,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True
            )

            resp = await agent.ainvoke(
                "在百度中查询合肥的天气"
            )
            print(resp)
            return resp

if __name__ == "__main__":
    asyncio.run(mcp_playwright_client())