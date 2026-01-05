from typing import List, Optional
import httpx
from app.core.logger import get_logger
from app.core.config import settings
from app.schema.statistics import Statistic, StatisticItem, StatisticData
from app.repository.statistics import get_statistics_repository

logger = get_logger(__name__)


class EcosService:
    def __init__(self):
        self.api_key = settings.ECOS_API_KEY
        self.base_url = "http://ecos.bok.or.kr/api"

    def search_statistics(self, query: str, limit: int = 5) -> List[Statistic]:
        """
        Search for available economic statistics by a keyword.
        """
        logger.info(f"🔍 Searching Statistics: {query}")
        repo = get_statistics_repository()
        return repo.search(query, limit)

    async def get_statistic_item_list(self, stat_code: str) -> List[StatisticItem]:
        """
        Fetch sub-items for a specific statistic.
        """
        # ECOS API Format: /StatisticItemList/{KEY}/json/kr/1/1000/{STAT_CODE}
        url = f"{self.base_url}/StatisticItemList/{self.api_key}/json/kr/1/1000/{stat_code}"
        logger.info(f"📡 Fetching Statistics Item List: {stat_code}")

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            if "StatisticItemList" in data:
                items = []
                for row in data["StatisticItemList"]["row"]:
                    items.append(StatisticItem(**row))
                return items

            elif "RESULT" in data:
                logger.error(f"ECOS API Error (Items): {data['RESULT']['MESSAGE']}")
                raise Exception(
                    f"{data['RESULT']['MESSAGE']} (Code: {data['RESULT']['CODE']})"
                )

            return []

    async def get_statistic_data(
        self,
        stat_code: str,
        cycle: str,
        start_time: str,
        end_time: str,
        item_code: Optional[str] = None,
    ) -> StatisticData:
        """
        Fetch specific statistical data values.
        """
        if not self.api_key:
            raise ValueError("ECOS_API_KEY is not configured.")

        # ECOS API Format: /StatisticSearch/{KEY}/json/kr/1/1000/{STAT_CODE}/{CYCLE}/{START}/{END}/{ITEM_CODE}
        base_search_url = (
            f"{self.base_url}/StatisticSearch/{self.api_key}/json/kr/1/1000/"
        )

        parts = [stat_code, cycle, start_time, end_time]
        if item_code:
            parts.append(item_code)

        url = base_search_url + "/".join(parts)
        logger.info(f"📡 Fetching Statistics Data: {url}")

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            if "StatisticSearch" in data:
                raw_rows = data["StatisticSearch"]["row"]
                formatted_data = {}
                unit_name = raw_rows[0].get("UNIT_NAME", "")

                for row in raw_rows:
                    items = [
                        row.get("ITEM_NAME1"),
                        row.get("ITEM_NAME2"),
                        row.get("ITEM_NAME3"),
                        row.get("ITEM_NAME4"),
                    ]
                    item_label = " > ".join([i for i in items if i])
                    if not item_label:
                        item_label = "Total"

                    time = row.get("TIME")
                    value = row.get("DATA_VALUE")

                    if item_label not in formatted_data:
                        formatted_data[item_label] = {}

                    formatted_data[item_label][time] = value

                return StatisticData(unit=unit_name, data=formatted_data)

            elif "RESULT" in data:
                error_code = data["RESULT"]["CODE"]
                message = data["RESULT"]["MESSAGE"]

                # Add hints for LLM to recover gracefully
                if error_code == "INFO-200":
                    message += " (Hint: Check the date. DO NOT RETRY with the exact same parameters.)"
                if error_code == "ERROR-101":
                    message += " (Hint: Check the cycle. DO NOT RETRY with the exact same parameters.)"

                logger.error(f"ECOS API Error (Data): {message}")
                raise Exception(f"{message} (Code: {error_code})")

            logger.error("Unknown ECOS response format")
            raise Exception("Unknown response format")


ecos_service = EcosService()
