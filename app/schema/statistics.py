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
