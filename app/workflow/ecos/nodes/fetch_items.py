from app.services.ecos_service import ecos_service
from app.workflow.ecos.state import EcosState
from app.core.logger import get_logger

logger = get_logger(__name__)


async def fetch_items_node(state: EcosState) -> dict:
    """Fetch item list for the selected statistic"""
    selected_stat = state.get("selected_statistic")

    try:
        items = await ecos_service.get_statistic_item_list(selected_stat.stat_code)
        logger.debug(f"Items: {','.join(item.name for item in items)}")

        return {
            "found_items": items if isinstance(items, list) else [],
            "error_message": None,
        }
    except Exception as e:
        return {"error_message": f"Failed to fetch items: {str(e)}"}
