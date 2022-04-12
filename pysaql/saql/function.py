"""Contains core function definitions"""

from typing import Any, List, Optional

from .scalar import Scalar


class Function(Scalar):
    """Base function definition"""

    _args: List[Any]
    _name: Optional[str] = None

    def __init__(self, *args: Any) -> None:
        """Initializer that accepts any number of arguments"""
        super().__init__()
        self._args = args

    def to_string(self) -> str:
        """Cast the function to a string"""
        args = [str(arg) for arg in self._args if arg is not None]
        name = self._name or self.__class__.__name__
        return f"{name}({', '.join(args)})"


class NullaryFunction(Function):
    """Base function definition that takes no arguments"""

    def __init__(self) -> None:
        """Initializer"""
        super().__init__()


class coalesce(Function):
    """Get the first non-null value from a list of parameters

    See: https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_saql.meta/bi_dev_guide_saql/bi_saql_functions_coalesce.htm
    """

    pass
