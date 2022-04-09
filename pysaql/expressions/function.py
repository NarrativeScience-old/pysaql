from typing import Any, List, Optional

from .scalar import Scalar


class Function(Scalar):
    _args: List[Any]
    _name: Optional[str] = None

    def __init__(self, *args: Any) -> None:
        super().__init__()
        self._args = args

    def to_string(self) -> str:
        args = [str(arg) for arg in self._args if arg is not None]
        name = self._name or self.__class__.__name__
        return f"{name}({', '.join(args)})"


class coalesce(Function):
    pass
