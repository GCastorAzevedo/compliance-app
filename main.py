from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
import asyncio

from corpus import LawCode, get_law_code_raw_content

mcp = FastMCP(name="Compliance App")


@mcp.tool()
async def get_law_code(code: LawCode, ctx: Context[ServerSession, None]) -> dict:
    return {"content": get_law_code_raw_content(code)}


async def main():
    content = await get_law_code_raw_content(code=LawCode.forest)
    print(content)


if __name__ == "__main__":
    asyncio.run(main())
