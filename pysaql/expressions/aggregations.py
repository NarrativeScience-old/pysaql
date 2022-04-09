from .scalar import Scalar


class count(Scalar):
    def to_string(self) -> str:
        return "count()"
