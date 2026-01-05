from typing import List, Optional
import httpx
from app.core.logger import get_logger
from app.core.config import settings
from app.schema.statistics import Statistic, StatisticItem, StatisticData
from app.repository.statistics import get_statistics_repository

logger = get_logger(__name__)


class StatisticsService:
    def __init__(self):
        self.repository = get_statistics_repository()

    def search(self, query: str, limit: int = 5) -> List[Statistic]:
        """
        Search for available economic statistics by a keyword.
        """
        return self.repository.search(query, limit)

    def get_all(self) -> List[Statistic]:
        return self.repository.get_all()


statistics_service = StatisticsService()
