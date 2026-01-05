from typing import Annotated, List, Optional, TypedDict, Dict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from app.schema.statistics import Statistic, StatisticItem, StatisticData


class FetchedItemData(TypedDict):
    item: StatisticItem
    data: StatisticData


class EcosState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    query: str

    found_statistics: Optional[List[Statistic]]
    selected_statistic: Optional[Statistic]
    found_items: Optional[List[StatisticItem]]

    # LLM-selected query parameters
    selected_parameters: Optional[List]  # List[StatisticQueryParameters]

    # Changed to support multiple items
    fetched_items: Optional[List[FetchedItemData]]

    retry_count: int = 0
    error_message: Optional[str]
