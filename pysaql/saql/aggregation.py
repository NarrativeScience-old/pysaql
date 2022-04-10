from typing import Optional, Sequence, Tuple, Union
from typing_extensions import Self

from .enums import Order
from .function import Function
from .scalar import Scalar
from .util import stringify_list


class FieldAggregation(Function):
    def __init__(self, field: Scalar) -> None:
        super().__init__(field)


class WindowFunction(Function):
    def over(
        self,
        row_range: Tuple[Optional[int], Optional[int]],
        reset_groups: Union[str, Sequence[Scalar]],
        order_by: Sequence[Union[Scalar, Tuple[Scalar, Order]]],
    ) -> Self:
        self._row_range = row_range
        self._reset_groups = reset_groups
        self._order_by = [order_by] if isinstance(order_by, Scalar) else order_by
        return self

    def to_string(self) -> str:
        s = super().to_string()

        if (
            getattr(self, "_row_range", None)
            and getattr(self, "_reset_groups", None)
            and getattr(self, "_order_by", None)
        ):
            start = "" if self._row_range[0] is None else self._row_range[0]
            stop = "" if self._row_range[1] is None else self._row_range[1]
            row_range = f"[{start}..{stop}]"

            reset_groups = (
                [self._reset_groups]
                if isinstance(self._reset_groups, str)
                else self._reset_groups
            )

            order_by = []
            for clause in self._order_by:
                if isinstance(clause, Scalar):
                    order_by.append(f"{clause} asc")
                else:
                    order_by.append(f"{clause[0]} {clause[1]}")

            s = f"{s} over ({row_range} partition by {stringify_list(reset_groups)} order by {stringify_list(order_by)})"

        return s


class RankFunction(Function):
    def __init__(self) -> None:
        super().__init__()


class count(FieldAggregation, WindowFunction):
    pass


class avg(FieldAggregation, WindowFunction):
    pass


average = avg


class min(FieldAggregation, WindowFunction):
    pass


class max(FieldAggregation, WindowFunction):
    pass


class median(FieldAggregation, WindowFunction):
    pass


class sum(FieldAggregation, WindowFunction):
    pass


class unique(FieldAggregation):
    pass


class first(FieldAggregation):
    pass


class last(FieldAggregation):
    pass


class rank(RankFunction, WindowFunction):
    pass


class dense_rank(RankFunction, WindowFunction):
    pass


class cume_dist(RankFunction, WindowFunction):
    pass


class row_number(RankFunction, WindowFunction):
    pass
