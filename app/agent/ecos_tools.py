from typing import List, Optional, Union

from langchain_core.tools import tool

from app.schema.statistics import Statistic, StatisticData, StatisticItem
from app.services.ecos_service import ecos_service


@tool
def search_statistics(query: str) -> List[Statistic]:
    """
    Search for available economic statistics by a keyword.
    Use this tool to find the 'StatCode' and 'Cycle' needed for retrieval.

    Args:
        query: The search keyword (e.g., "GDP", "CPI", "Interest Rate").

    Returns:
        List of matching statistics with code, name, and cycle.
    """
    return ecos_service.search_statistics(query)


@tool
async def get_statistic_item_list(
    stat_code: str,
) -> Union[List[StatisticItem], str]:
    """
    Search for available sub-items (Item Codes) for a specific Statistic Code.
    Use this BEFORE 'get_statistic_data' if you need to filter for specific items (e.g., 'Total GDP', 'Exports').

    Args:
        stat_code: The statistic code (e.g., "200Y105")

    Returns:
        List of items containing 'code', 'name', 'start_time', and 'end_time'.
        Or an error string if failed.
    """
    try:
        return await ecos_service.get_statistic_item_list(stat_code)
    except Exception as e:
        return f"Error fetching item list: {str(e)}"


@tool
async def get_statistic_data(
    stat_code: str,
    cycle: str,
    start_time: str,
    end_time: str,
    item_code: Optional[str] = None,
) -> Union[StatisticData, str]:
    """
    Fetch specific statistical data values from the Bank of Korea ECOS API.

    Args:
        stat_code: The 6-digit statistic code (e.g., '200Y001') found via search.
        cycle: The cycle of the data. Must be one of:
               - 'A' (Annual): format YYYY (e.g., '2023')
               - 'Q' (Quarterly): format YYYYQn (e.g., '2023Q1')
               - 'M' (Monthly): format YYYYMM (e.g., '202301')
               - 'D' (Daily): format YYYYMMDD (e.g., '20230101')
        start_time: Start date in the format corresponding to the Cycle.
        end_time: End date in the format corresponding to the Cycle.
        item_code: (Optional) Specific Item Code to filter (e.g., "1400" for GDP).
                   If NOT provided, fetches ALL data (which might be huge).
                   STRONGLY RECOMMENDED to use this for aggregate stats like GDP.

    Returns:
        The data values object (unit and time-series data).
        Or an error string if failed.
    """
    try:
        return await ecos_service.get_statistic_data(
            stat_code, cycle, start_time, end_time, item_code
        )
    except Exception as e:
        return f"Error fetching data: {str(e)}"
