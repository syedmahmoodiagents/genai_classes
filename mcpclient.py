import asyncio
from fastmcp import Client

async def main():
    client = Client("http://localhost:8000/mcp")

    async with client:
        tools = await client.list_tools()
        print("Tools:", tools)

        query="Python programming language"
        result = await client.call_tool(
            "search_wikipedia", {"query": query}
        )
        print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())


