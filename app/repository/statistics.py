from functools import lru_cache
from typing import List

from langchain_core.vectorstores import InMemoryVectorStore

from app.core.dependencies import get_stats_data, get_vector_store
from app.schema.statistics import Statistic


class StatisticsRepository:
    def __init__(self, data: List[Statistic], vector_store: InMemoryVectorStore):
        self._data = data
        self._vector_store = vector_store

    def get_all(self) -> List[Statistic]:
        return self._data

    def search(self, query: str, k: int = 10) -> List[Statistic]:
        docs = self._vector_store.similarity_search(query, k=k)

        results = []
        stat_map = {s.stat_code: s for s in self._data}

        for doc in docs:
            code = doc.metadata.get("stat_code")
            if code and code in stat_map:
                results.append(stat_map[code])

        return results


@lru_cache
def get_statistics_repository() -> StatisticsRepository:
    data = get_stats_data()
    vector_store = get_vector_store()

    return StatisticsRepository(data=data, vector_store=vector_store)
