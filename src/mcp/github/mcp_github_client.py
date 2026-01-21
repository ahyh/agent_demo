import asyncio

from langchain_classic.agents import initialize_agent, AgentType
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

from src.common import llm, local_qwen


# 获取github mcp tools
async def mcp_github_client():

    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN": "${github personal access token}"
        }
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
                "我的用户名是ahyh, 我有哪些public的代码仓库？star数是多少?"
            )
            print(resp)
            return resp

if __name__ == "__main__":
    asyncio.run(mcp_github_client())