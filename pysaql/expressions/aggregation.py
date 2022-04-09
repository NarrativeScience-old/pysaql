from abc import ABC
from typing import Optional
from .scalar import Scalar


class FieldAggregation(Scalar, ABC):
    def __init__(self, field: Optional[Scalar] = None) -> None:
        super().__init__()
        self.field = field

    def to_string(self) -> str:
        field = self.field or ""
        return f"{self.__class__.__name__}({field})"


class count(FieldAggregation):
    pass


class avg(FieldAggregation):
    pass


average = avg


class min(FieldAggregation):
    pass


class max(FieldAggregation):
    pass


class median(FieldAggregation):
    pass


class sum(FieldAggregation):
    pass


class unique(FieldAggregation):
    pass


class first(FieldAggregation):
    pass


class last(FieldAggregation):
    pass
