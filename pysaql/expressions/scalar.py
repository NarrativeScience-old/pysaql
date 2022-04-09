from abc import ABC, abstractmethod
from typing import Optional
from typing_extensions import Self

from .expression import Expression
from .util import escape


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
           s += f" as {escape(self._alias)}"

        return s

