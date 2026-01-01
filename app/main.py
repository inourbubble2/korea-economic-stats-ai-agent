from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agent.ecos_agent import ecos_agent
from app.api.routes import router as api_router
from app.core.config import settings
from app.repository.statistics import get_statistics_repository

from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from copilotkit import LangGraphAGUIAgent


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_statistics_repository()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.include_router(api_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    agent = LangGraphAGUIAgent(
        name="ecos_agent",
        graph=ecos_agent,
    )
    add_langgraph_fastapi_endpoint(app=app, agent=agent, path="")

    return app


app = create_app()
