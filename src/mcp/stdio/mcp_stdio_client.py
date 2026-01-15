import asyncio

from langchain_classic.agents import initialize_agent, AgentType
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

from src.common import local_qwen


async def create_stdio_client():
    server_params = StdioServerParameters(
        command="python",
        args=["D:\\source_code\\git_code\\python_code\\agent_demo\\src\\mcp\\stdio\\mcp_stdio_server.py"],
    )

    # 注意：当前 mcp 版本的 stdio_client 不再接受关键字参数 server_params，
    # 需要以位置参数方式传入 StdioServerParameters 实例。
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print(tools)

            agent = initialize_agent(
                llm=local_qwen,
                tools=tools,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True
            )

            resp = await agent.ainvoke("3 + 2 * 5 = ?")
            print(resp)
            return resp



if __name__ == '__main__':
    asyncio.run(create_stdio_client())