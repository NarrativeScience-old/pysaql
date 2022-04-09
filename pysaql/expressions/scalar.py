from abc import ABC, abstractmethod
import operator
from typing import Any, Callable, Optional
from typing_extensions import Self

from .expression import Expression
from .util import escape_identifier, escape_string

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
    operator.and_: "and",
    operator.or_: "or",
    operator.not_: "not",
}

class Operation:
    pass

class BinaryOperation(Operation):

    def __init__(self, op: Callable, left: Any, right: Any) -> None:
        super().__init__()
        self.op = op
        self.left = left
        self.right = right

    def __str__(self) -> str:
        if hasattr(self.left, "to_string"):
            left = self.left.to_string()
        elif isinstance(self.left, str):
            left = escape_string(self.left)
        else:
            left = self.left

        if hasattr(self.right, "to_string"):
            right = self.right.to_string()
        elif isinstance(self.right, str):
            right = escape_string(self.right)
        else:
            right = self.right

        return f"{left} {OPERATOR_STRINGS[self.op]} {right}"


class Scalar(Expression, ABC):
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
        return BinaryOperation(operator.eq, self, obj)

    def __ne__(self, obj: Any) -> BinaryOperation:
        return BinaryOperation(operator.ne, self, obj)

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
