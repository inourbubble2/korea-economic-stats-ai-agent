from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agent.ecos_agent import ecos_agent
from app.agent.news_agent import news_agent
from app.core.config import settings
from app.mcp_server import create_mcp_app
from app.repository.statistics import get_statistics_repository

from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from copilotkit import LangGraphAGUIAgent

mcp_app = create_mcp_app()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize repository
    get_statistics_repository()

    # Initialize MCP app (starts session manager for Streamable HTTP)
    async with mcp_app.router.lifespan_context(mcp_app):
        yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    ecos = LangGraphAGUIAgent(
        name="ecos_agent",
        graph=ecos_agent,
    )
    news = LangGraphAGUIAgent(
        name="news_agent",
        graph=news_agent,
    )
    add_langgraph_fastapi_endpoint(app=app, agent=ecos, path="/ecos")
    add_langgraph_fastapi_endpoint(app=app, agent=news, path="/news")

    app.mount("", mcp_app)

    return app


app = create_app()
