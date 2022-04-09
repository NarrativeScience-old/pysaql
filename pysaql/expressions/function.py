from typing import Optional

from .scalar import Scalar


class day_in_week(Scalar):
    date: Scalar

    def __init__(self, date: Scalar):
        super().__init__()
        self.date = date

    def to_string(self) -> str:
        return f"day_in_week({self.date.to_string()})"


class to_date(Scalar):
    string: Scalar
    format_string: Optional[str] = None

    def __init__(self, string: Scalar, format_string: Optional[str] = None):
        super().__init__()
        self.string = string
        self.format_string = format_string

    def to_string(self) -> str:
        args = [self.string.to_string()]
        if self.format_string:
            args.append(self.format_string)
        return f"toDate({', '.join(args)})"
