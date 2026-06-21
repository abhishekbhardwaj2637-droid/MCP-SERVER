import asyncio
# pyrefly: ignore [missing-import]
from mcp import ClientSession
from mcp.client.sse import sse_client

async def list_tools():
    url = "https://groww-review-project-production.up.railway.app/sse"
    print(f"Connecting to MCP Server at {url}...")
    try:
        async with sse_client(url) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                print("Session initialized.")
                
                tools = await session.list_tools()
                print("\n--- Available Tools ---")
                for tool in tools.tools:
                    print(f"- {tool.name}: {tool.description}")
                    print(f"  Schema: {tool.inputSchema}")
    except Exception as e:
        print(f"Failed to connect to MCP Server: {e}")

if __name__ == "__main__":
    asyncio.run(list_tools())
