from abc import ABC, abstractmethod
import operator
from typing import Any, Callable, Optional
from typing_extensions import Self

from .expression import Expression
from .util import escape_identifier, stringify

OPERATOR_STRINGS = {
    operator.eq: "==",
    operator.ne: "!=",
    operator.lt: "<",
    operator.le: "<=",
    operator.gt: ">",
    operator.ge: ">=",
    operator.add: "+",
    operator.sub: "-",
    operator.mul: "*",
    operator.truediv: "/",
    operator.and_: "&&",
    operator.or_: "||",
    operator.inv: "!",
    operator.is_: "is",
    operator.is_not: "is not",
    operator.contains: "in",
}


class Operation:
    pass


class BooleanOperation(Operation):
    def __and__(self, obj: Any) -> "BinaryOperation":
        return BinaryOperation(operator.and_, self, obj)

    def __or__(self, obj: Any) -> "BinaryOperation":
        return BinaryOperation(operator.or_, self, obj, wrap=True)

    def __invert__(self) -> "BinaryOperation":
        return UnaryOperation(operator.inv, self)


class BinaryOperation(BooleanOperation):
    def __init__(self, op: Callable, left: Any, right: Any, wrap: bool = False) -> None:
        super().__init__()
        self.op = op
        self.left = left
        self.right = right
        self.wrap = wrap

    def __str__(self) -> str:
        s = f"{stringify(self.left)} {OPERATOR_STRINGS[self.op]} {stringify(self.right)}"
        if self.wrap:
            s = f"({s})"

        return s


class UnaryOperation(BooleanOperation):
    def __init__(self, op: Callable, value: Any) -> None:
        super().__init__()
        self.op = op
        self.value = value

    def __str__(self) -> str:
        return f"{OPERATOR_STRINGS[self.op]} {stringify(self.value)}"


class Scalar(Expression, BooleanOperation, ABC):
    _alias: Optional[str] = None

    def alias(self, value: str) -> Self:
        self._alias = value
        return self

    @abstractmethod
    def to_string(self) -> str:
        pass

    def __str__(self) -> str:
        s = self.to_string()
        if self._alias:
            s += f" as {escape_identifier(self._alias)}"

        return s

    def __eq__(self, obj: Any) -> BinaryOperation:
        op = operator.is_ if obj is None else operator.eq
        return BinaryOperation(op, self, obj)

    def __ne__(self, obj: Any) -> BinaryOperation:
        op = operator.is_not if obj is None else operator.ne
        return BinaryOperation(op, self, obj)

    def __lt__(self, obj: Any) -> BinaryOperation:
        return BinaryOperation(operator.lt, self, obj)

    def __le__(self, obj: Any) -> BinaryOperation:
        return BinaryOperation(operator.le, self, obj)

    def __gt__(self, obj: Any) -> BinaryOperation:
        return BinaryOperation(operator.gt, self, obj)

    def __ge__(self, obj: Any) -> BinaryOperation:
        return BinaryOperation(operator.ge, self, obj)

    def __add__(self, obj: Any) -> BinaryOperation:
        return BinaryOperation(operator.add, self, obj)

    def __sub__(self, obj: Any) -> BinaryOperation:
        return BinaryOperation(operator.sub, self, obj)

    def __mul__(self, obj: Any) -> BinaryOperation:
        return BinaryOperation(operator.mul, self, obj)

    def __truediv__(self, obj: Any) -> BinaryOperation:
        return BinaryOperation(operator.truediv, self, obj)

    def __neg__(self, obj: Any) -> BinaryOperation:
        return BinaryOperation(operator.neg, self, obj)

    def in_(self, iterable: Expression) -> BinaryOperation:
        return BinaryOperation(operator.contains, self, iterable)
