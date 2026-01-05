from typing import Dict, List
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field


class Cycle(str, Enum):
    YEAR = "A"
    SEMI_ANNUAL = "S"
    QUARTER = "Q"
    MONTH = "M"
    SEMI_MONTH = "SM"
    DAY = "D"


class Statistic(BaseModel):
    stat_code: str = Field(alias="STAT_CODE")
    stat_name: str = Field(alias="STAT_NAME")
    cycle: Cycle = Field(alias="CYCLE", default=Cycle.MONTH)
    full_path: str = Field(alias="FULL_PATH")

    class Config:
        populate_by_name = True


class StatisticItem(BaseModel):
    code: str = Field(alias="ITEM_CODE")
    name: str = Field(alias="ITEM_NAME")
    start_time: str = Field(alias="START_TIME")
    end_time: str = Field(alias="END_TIME")
    cycle: Optional[Cycle] = Field(alias="CYCLE", default=None)

    __str__ = (
        lambda self: f"Name: {self.name}, Code: {self.code}, Range: {self.start_time}~{self.end_time}, Cycle: {self.cycle.value}"
    )

    class Config:
        populate_by_name = True


class StatisticData(BaseModel):
    unit: str
    data: Dict[str, Dict[str, str]] = Field(
        description="Dictionary of {ItemName: {Time: Value}}"
    )


class StatisticQueryParameters(BaseModel):
    cycle: Cycle = Field(description="The selected cycle (Y|S|Q|M|SM|D)")
    item_code: str = Field(description="The selected item code")
    item_name: str = Field(description="The selected item name")
    start_time: str = Field(description="Start time correctly formatted for cycle")
    end_time: str = Field(description="End time correctly formatted for cycle")


class StatisticQueryParametersList(BaseModel):
    """Multiple query parameters for fetching multiple items at once"""

    queries: List[StatisticQueryParameters] = Field(
        description="List of query parameters. Use multiple entries if user asks for multiple items (e.g., 'GDP and unemployment rate'). Use single entry for single item requests.",
        min_length=1,
    )


class SelectedStatistic(BaseModel):
    stat_code: Optional[str] = Field(
        description="The selected statistic code, or null if none match"
    )
    reason: str = Field(description="Reason for selection or failure")
