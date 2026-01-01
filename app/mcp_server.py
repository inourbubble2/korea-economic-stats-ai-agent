import uuid
from typing import Optional

from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette

from app.agent.ecos_agent import ecos_agent
from app.core.config import settings


mcp = FastMCP(settings.PROJECT_NAME, host="0.0.0.0")


@mcp.tool()
async def ask_ecos_agent(query: str, thread_id: Optional[str] = None) -> str:
    """
    Ask the ECOS (Korea Economic Statistics) Agent a question.
    The agent can search for statistics, retrieve data, and analyze trends.

    Args:
        query: The user's question about economic statistics.
        thread_id: Optional ID to maintain conversation context. If not provided, a new one is generated.
    """
    if not thread_id:
        thread_id = str(uuid.uuid4())

    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [("user", query)]}
    result = await ecos_agent.ainvoke(inputs, config=config)

    messages = result.get("messages", [])
    if messages:
        return messages[-1].content
    return "No response generated."


def create_mcp_app() -> Starlette:
    return mcp.streamable_http_app()


if __name__ == "__main__":
    mcp.run()
