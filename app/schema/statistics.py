from typing import Dict
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

    class Config:
        populate_by_name = True


class StatisticItem(BaseModel):
    code: str = Field(alias="ITEM_CODE")
    name: str = Field(alias="ITEM_NAME")
    start_time: str = Field(alias="START_TIME")
    end_time: str = Field(alias="END_TIME")
    cycle: Optional[Cycle] = Field(alias="CYCLE", default=None)

    class Config:
        populate_by_name = True


class StatisticData(BaseModel):
    unit: str
    data: Dict[str, Dict[str, str]] = Field(
        description="Dictionary of {ItemName: {Time: Value}}"
    )
