import uuid
from typing import Optional

from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette

from app.workflow.ecos.graph import ecos_graph
from app.agent.news_agent import news_agent
from app.core.config import settings
from app.core.logger import get_logger
from app.core.callbacks import AgentLoggingCallback

logger = get_logger(__name__)

mcp = FastMCP(settings.PROJECT_NAME, host="0.0.0.0")


@mcp.tool()
async def ask_news_agent(query: str, thread_id: Optional[str] = None) -> str:
    """
    Ask the News Agent to search and analyze latest economic news.
    Use this tool when you need to find specific statistical facts, recent events, or hidden details
    that might be available in news articles but not yet in official broad statistics.
    """
    logger.info(f"🗣️ User Query (News): {query}")

    if not thread_id:
        thread_id = str(uuid.uuid4())

    # Inject logging callback for the news agent
    news_logger = get_logger("app.agent.news_agent")
    callback = AgentLoggingCallback(news_logger)

    config = {"configurable": {"thread_id": thread_id}, "callbacks": [callback]}
    inputs = {"messages": [("user", query)]}
    result = await news_agent.ainvoke(inputs, config=config)

    messages = result.get("messages", [])
    if messages:
        response = messages[-1].content
        logger.info(f"🤖 Agent Answer (News): {response}")
        return response

    logger.warning("Agent returned no messages.")
    return "No response generated."


@mcp.tool()
async def ask_ecos_agent(query: str, thread_id: Optional[str] = None) -> str:
    """
    Ask the ECOS Agent to search and analyze economic statistics.
    Use this tool when you need to retrieve vast, official economic statistics,
    analyze long-term trends, or get comprehensive data sets from the Bank of Korea.
    """
    logger.info(f"🗣️ User Query (ECOS): {query}")

    if not thread_id:
        thread_id = str(uuid.uuid4())

    # Inject logging callback for the ecos agent
    ecos_logger = get_logger("app.agent.ecos_agent")
    callback = AgentLoggingCallback(ecos_logger)

    config = {"configurable": {"thread_id": thread_id}, "callbacks": [callback]}
    inputs = {"query": query, "messages": [], "retry_count": 0}
    result = await ecos_graph.ainvoke(inputs, config=config)

    messages = result.get("messages", [])
    if messages:
        response = messages[-1].content
        logger.info(f"🤖 Agent Answer (ECOS): {response}")
        return response

    logger.warning("Agent returned no messages.")
    return "No response generated."


def create_mcp_app() -> Starlette:
    return mcp.streamable_http_app()


if __name__ == "__main__":
    mcp.run()
