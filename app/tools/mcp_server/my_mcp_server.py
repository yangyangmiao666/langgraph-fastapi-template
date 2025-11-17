from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")


@mcp.tool(name="get_weather", description="获取指定位置的天气信息")
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return f"{location}的天气是晴天"


if __name__ == "__main__":
    mcp.run(transport="sse")
