from abc import ABC
import functools
import operator
from typing import List, Tuple, Union
from typing_extensions import Self

from attr import field

from .enums import JoinType, Order
from .scalar import BinaryOperation, Scalar
from .expression import Expression


class StreamStatement(ABC):
    stream: "Stream"


class Stream(Expression):
    _id: int
    _statements: List[StreamStatement] = []

    def __init__(self):
        super().__init__()
        self._id = 0
        self._statements: List[StreamStatement] = []

    def __str__(self) -> str:
        return "\n".join(str(op) for op in self._statements)

    @property
    def ref(self) -> str:
        return f"q{self._id}"

    def foreach(self, *fields: Scalar) -> Self:
        self._statements.append(ProjectionStatement(self, fields))
        return self

    def group(self, *fields: Scalar) -> Self:
        self._statements.append(GroupStatement(self, fields))
        return self

    def filter(self, *filters: BinaryOperation) -> Self:
        self._statements.append(FilterStatement(self, filters))
        return self

    def order(self, *fields: Union[Scalar, Tuple[Scalar, Order]]) -> Self:
        self._statements.append(OrderStatement(self, fields))
        return self

    def limit(self, limit: int) -> Self:
        self._statements.append(LimitStatement(self, limit))
        return self

class LoadStatement(StreamStatement):
    def __init__(self, stream: Stream, name: str):
        super().__init__()
        self.stream = stream
        self.name = name

    def __str__(self) -> str:
        return f"{self.stream.ref} = load \"{self.name}\";"


class ProjectionStatement(StreamStatement):
    def __init__(self, stream: Stream, fields: List[Scalar]):
        super().__init__()
        self.stream = stream
        self.fields = fields

    def __str__(self) -> str:
        fields = ", ".join(str(f) for f in self.fields)
        return f"{self.stream.ref} = foreach {self.stream.ref} generate {fields};"


class OrderStatement(StreamStatement):
    def __init__(self, stream: Stream, fields: Union[Scalar, List[Scalar], List[Tuple[Scalar, Order]]]) -> None:
        super().__init__()
        self.stream = stream
        self.fields = fields

    def __str__(self) -> str:
        fields = []
        for field in self.fields:
            if isinstance(field, Scalar):
                fields.append(f"{field} asc")
            else:
                fields.append(f"{field[0]} {field[1]}")

        if len(fields) > 1:
            fields = f"({', '.join(fields)})"
        else:
            fields = fields[0]

        return f"{self.stream.ref} = order {self.stream.ref} by {fields};"


class LimitStatement(StreamStatement):
    def __init__(self, stream: Stream, limit: int):
        super().__init__()
        self.stream = stream
        self.limit = limit

    def __str__(self) -> str:
        return f"{self.stream.ref} = limit {self.stream.ref} {self.limit};"


class GroupStatement(StreamStatement):
    def __init__(self, stream: Stream, fields: List[Scalar]):
        super().__init__()
        self.stream = stream
        self.fields = fields

    def __str__(self) -> str:
        fields = ", ".join(str(f) for f in self.fields)
        return f"{self.stream.ref} = group {self.stream.ref} by {fields};"


class FilterStatement(StreamStatement):
    def __init__(self, stream: Stream, filters: List[BinaryOperation]):
        super().__init__()
        self.stream = stream
        self.filters = filters

    def __str__(self) -> str:
        expr = functools.reduce(lambda left, right: BinaryOperation(operator.and_, left, right), self.filters)
        return f"{self.stream.ref} = filter {self.stream.ref} by {expr};"


class CogroupStatement(StreamStatement):
    def __init__(self, stream: Stream, streams: List[Tuple[Stream, Scalar]], join_type: JoinType = JoinType.inner):
        super().__init__()
        self.stream = stream
        self.streams = streams
        self.join_type = join_type

    def __str__(self) -> str:
        lines = []
        streams = []
        for i, item in enumerate(self.streams):
            stream, field = item
            s = f"{stream.ref} by {field}"
            if i == 0 and self.join_type != JoinType.inner:
                s += f" {self.join_type}"

            streams.append(s)
            lines.append(str(stream))

        lines.append(f"{self.stream.ref} = cogroup {', '.join(streams)};")

        return "\n".join(lines)


class dataset(Stream):

    def __init__(self, name: str):
        super().__init__()
        self._statements.append(LoadStatement(self, name))


class cogroup(Stream):
    join_type: JoinType

    def __init__(self, *streams: Tuple[Stream, Scalar], join_type: JoinType = JoinType.inner):
        super().__init__()
        max_id = 0
        for i, (stream, _) in enumerate(streams):
            stream._id += i
            max_id = max(max_id, stream._id)
        self._id = max_id + 1
        self._statements.append(CogroupStatement(self, streams, join_type))
