from typing import Dict, List, Optional

import httpx
from langchain_core.tools import tool

from app.core.config import settings
from app.repository.statistics import get_statistics_repository


@tool
def search_statistics(query: str) -> List[Dict]:
    """
    Search for available economic statistics by a keyword.
    Use this tool to find the 'StatCode' and 'Cycle' needed for retrieval.

    Args:
        query: The search keyword (e.g., "GDP", "CPI", "Interest Rate").

    Returns:
        List of matching statistics with code, name, and cycle.
    """
    repo = get_statistics_repository()
    results = repo.search(query)
    return [stat.model_dump() for stat in results]


@tool
async def get_statistic_item_list(stat_code: str) -> List[Dict[str, str]]:
    """
    Search for available sub-items (Item Codes) for a specific Statistic Code.
    Use this BEFORE 'get_statistic_data' if you need to filter for specific items (e.g., 'Total GDP', 'Exports').

    Args:
        stat_code: The statistic code (e.g., "200Y105")

    Returns:
        List of dictionaries containing 'code', 'name', 'start_time', and 'end_time' of items.
    """
    api_key = settings.ECOS_API_KEY
    if not api_key:
        return [{"error": "ECOS_API_KEY is not configured."}]

    # ECOS API Format: /StatisticItemList/{KEY}/json/kr/1/1000/{STAT_CODE}
    url = f"http://ecos.bok.or.kr/api/StatisticItemList/{api_key}/json/kr/1/1000/{stat_code}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            if "StatisticItemList" in data:
                items = []
                for row in data["StatisticItemList"]["row"]:
                    items.append(
                        {
                            "code": row.get("ITEM_CODE"),
                            "name": row.get("ITEM_NAME"),
                            "start_time": row.get("START_TIME"),
                            "end_time": row.get("END_TIME"),
                            "cycle": row.get("CYCLE"),
                        }
                    )
                return items

            elif "RESULT" in data:
                return [
                    {"error": data["RESULT"]["MESSAGE"], "code": data["RESULT"]["CODE"]}
                ]

            return []

        except Exception as e:
            return [{"error": str(e)}]


@tool
async def get_statistic_data(
    stat_code: str,
    cycle: str,
    start_time: str,
    end_time: str,
    item_code: Optional[str] = None,
) -> Dict:
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
        The data values from the API (JSON).
    """
    api_key = settings.ECOS_API_KEY
    if not api_key:
        return {"error": "ECOS_API_KEY is not configured."}

    # ECOS API Format: /StatisticSearch/{KEY}/json/kr/1/1000/{STAT_CODE}/{CYCLE}/{START}/{END}/{ITEM_CODE}
    base_url = f"http://ecos.bok.or.kr/api/StatisticSearch/{api_key}/json/kr/1/1000/"

    # Construct URL path parts
    # If item_code is provided, append it.
    parts = [stat_code, cycle, start_time, end_time]
    if item_code:
        parts.append(item_code)

    url = base_url + "/".join(parts)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            if "StatisticSearch" in data:
                # Post-process for LLM consumption: Group by Item for Time Series
                raw_rows = data["StatisticSearch"]["row"]
                formatted_data = {}
                unit_name = raw_rows[0].get("UNIT_NAME", "")

                for row in raw_rows:
                    # Construct Item Label (e.g., "Total", "Manufacturing", "Agriculture")
                    items = [
                        row.get("ITEM_NAME1"),
                        row.get("ITEM_NAME2"),
                        row.get("ITEM_NAME3"),
                        row.get("ITEM_NAME4"),
                    ]
                    # Filter out None and join
                    item_label = " > ".join([i for i in items if i])
                    if not item_label:
                        item_label = "Total"

                    time = row.get("TIME")
                    value = row.get("DATA_VALUE")

                    if item_label not in formatted_data:
                        formatted_data[item_label] = {}

                    formatted_data[item_label][time] = value

                return {
                    # "stat_name": min([r.get("STAT_NAME") for r in raw_rows], default=""),
                    "unit": unit_name,
                    "data": formatted_data,
                }

            elif "RESULT" in data:
                error_code = data["RESULT"]["CODE"]
                message = data["RESULT"]["MESSAGE"]

                # Add hints for LLM to recover gracefully
                if error_code == "INFO-200":
                    message += " (Hint: Check the date.)"
                if error_code == "ERROR-101":
                    message += " (Hint: Check the cycle.)"

                return {"error": message, "code": error_code}
            else:
                return data

        except Exception as e:
            return {"error": f"Failed to fetch data: {str(e)}"}
