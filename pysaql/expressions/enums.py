from asyncio import futures
from enum import Enum


class StrEnum(Enum):
    def __str__(self):
        return self.value


class Order(StrEnum):
    asc = "asc"
    desc = "desc"


class JoinType(StrEnum):
    inner = "inner"
    left = "left"
    right = "right"
    full = "full"


class DateDiffUnit(StrEnum):
    year = "year"
    quarter = "quarter"
    month = "month"
    day = "day"
    week = "week"
    hour = "hour"
    minute = "minute"
    second = "second"


class Timeframe(StrEnum):
    current = "current"
    future = "ahead"
    past = "ago"


class DateUnit(StrEnum):
    year = "year"
    quarter = "quarter"
    month = "month"
    day = "day"
    week = "week"
    fiscal_year = "year"
    fiscal_quarter = "quarter"


class DateTypeString(StrEnum):
    y_m = "Y-M"
    y_q = "Y-Q"
    y = "Y"
    y_w = "Y-W"
    y_m_d = "Y-M-D"
