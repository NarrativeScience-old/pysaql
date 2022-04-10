from .scalar import Scalar
from .util import escape_identifier


class field(Scalar):
    name: str

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def to_string(self) -> str:
        return escape_identifier(self.name)
