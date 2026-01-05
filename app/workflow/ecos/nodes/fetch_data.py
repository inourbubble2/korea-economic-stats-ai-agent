from app.services.ecos_service import ecos_service
from app.workflow.ecos.state import EcosState
from app.core.utils import format_date
from app.core.logger import get_logger
from app.schema.statistics import Statistic, StatisticItem, StatisticQueryParametersList
from typing import List

logger = get_logger(__name__)


async def fetch_data_node(state: EcosState) -> dict:
    """Fetch data for all selected parameters"""
    stat: Statistic = state.get("selected_statistic")
    items: List[StatisticItem] = state.get("found_items")
    selected_params: StatisticQueryParametersList = state.get("selected_parameters")

    fetched_items = []

    for params in selected_params:
        start_fmt = format_date(params.start_time, params.cycle.value)
        end_fmt = format_date(params.end_time, params.cycle.value)

        try:
            data = await ecos_service.get_statistic_data(
                stat_code=stat.stat_code,
                cycle=params.cycle.value,
                start_time=start_fmt,
                end_time=end_fmt,
                item_code=params.item_code,
            )
        except Exception as e:
            return {
                "error_message": f"Failed to fetch data for {params.item_name or params.item_code}: {e}",
                "fetched_items": None,
            }

        logger.debug(
            f"Fetched Data for {params.item_name or params.item_code}: {str(data)[:500]}..."
        )

        selected_item = next((i for i in items if i.code == params.item_code), None)

        if data and data.data and selected_item:
            fetched_items.append({"item": selected_item, "data": data})

    return {
        "fetched_items": fetched_items,
        "error_message": None,
    }
