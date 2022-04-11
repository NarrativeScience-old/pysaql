"""Contains field class"""

from .scalar import Scalar
from .util import escape_identifier


class field(Scalar):
    """Represents a field (column) in the data stream"""

    name: str

    def __init__(self, name: str) -> None:
        """Initializer

        Args:
            name: Name of the field

        """
        super().__init__()
        self.name = name

    def to_string(self) -> str:
        """Cast the field to a string"""
        return escape_identifier(self.name)
