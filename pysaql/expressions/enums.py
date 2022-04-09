from enum import Enum


class StrEnum(Enum):

    def __str__(self):
        return self.name



class Order(StrEnum):
    asc = "asc"
    desc = "desc"


class JoinType(StrEnum):
    inner = "inner"
    left = "left"
    right = "right"
    full = "full"
