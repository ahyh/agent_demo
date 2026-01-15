from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math Tools")

@mcp.tool()
def add(a: int, b: int) -> int:
    """ Add two numbers """
    return a + b

@mcp.tool()
def mul(a: int, b: int) -> int:
    """ Multiply two numbers """
    return a * b


# 将当前的方法变成mcp

if __name__ == "__main__":
    mcp.run(transport="stdio")
