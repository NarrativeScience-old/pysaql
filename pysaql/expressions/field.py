from .scalar import Scalar
from .util import escape


class field(Scalar):
    name: str

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def to_string(self) -> str:
        return escape(self.name)
