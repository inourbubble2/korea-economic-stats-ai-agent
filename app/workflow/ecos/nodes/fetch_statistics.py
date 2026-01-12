from app.core.logger import get_logger
from app.services.statistics_service import statistics_service
from app.workflow.ecos.state import EcosState

logger = get_logger(__name__)


async def fetch_statistics_node(state: EcosState) -> dict:
    query = state["query"]

    found_statistics = statistics_service.search(query, 10)

    return {
        "found_statistics": found_statistics,
        "error_message": None if found_statistics else f"No statistics found for keyword: {query}",
    }
