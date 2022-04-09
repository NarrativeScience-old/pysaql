"""Contains date functions"""

from typing import Optional, Union

from .enums import DateDiffUnit, DateUnit, Timeframe
from .expression import Expression
from .function import Function
from .scalar import Scalar
from .util import escape_string


class day_in_week(Function):
    def __init__(self, date: Scalar):
        super().__init__(date)


class day_in_month(Function):
    def __init__(self, date: Scalar):
        super().__init__(date)


class day_in_quarter(Function):
    def __init__(self, date: Scalar):
        super().__init__(date)


class day_in_year(Function):
    def __init__(self, date: Scalar):
        super().__init__(date)


class week_first_day(Function):
    def __init__(self, date: Scalar):
        super().__init__(date)


class fiscal_week_first_day(Function):
    def __init__(self, date: Scalar):
        super().__init__(date)


class fiscal_month_first_day(Function):
    def __init__(self, date: Scalar):
        super().__init__(date)


class quarter_first_day(Function):
    def __init__(self, date: Scalar):
        super().__init__(date)


class fiscal_quarter_first_day(Function):
    def __init__(self, date: Scalar):
        super().__init__(date)


class year_first_day(Function):
    def __init__(self, date: Scalar):
        super().__init__(date)


class fiscal_year_first_day(Function):
    def __init__(self, date: Scalar):
        super().__init__(date)


class to_date(Function):
    _name: str = "toDate"

    def __init__(self, string: Scalar, format_string: Optional[str] = None):
        super().__init__(string, format_string)


class date_diff(Function):
    def __init__(
        self, date_part: DateDiffUnit, start_date: Scalar, end_date: Scalar
    ) -> None:
        super().__init__(date_part, start_date, end_date)


class days_between(Function):
    _name = "daysBetween"

    def __init__(self, start_date: Scalar, end_date: Scalar) -> None:
        super().__init__(start_date, end_date)


class now(Function):
    pass


class year(Function):
    pass


class quarter(Function):
    pass


class month(Function):
    pass


class week(Function):
    pass


class day(Function):
    pass


class minute(Function):
    pass


class second(Function):
    pass


class fiscal_year(Function):
    _name = "fiscalYear"


class fiscal_quarter(Function):
    _name = "fiscalQuarter"


class fiscal_month(Function):
    _name = "fiscalMonth"


class fiscal_week(Function):
    _name = "fiscalWeek"


class epoch_day(Function):
    _name = "epochDay"


class epoch_second(Function):
    _name = "epochSecond"


class date(Function):
    def __init__(
        self, year: Scalar, month: Optional[Scalar] = None, day: Optional[Scalar] = None
    ) -> None:
        super().__init__(year, month, day)

    def to_string(self) -> str:
        args = [str(arg) for arg in self._args if arg is not None]
        name = self._name or self.__class__.__name__
        s = f"{', '.join(args)}"
        if len(args) > 1:
            s = f"{name}({s})"

        return s


class relative_date(Expression):
    def __init__(self, timeframe: Timeframe, unit: DateUnit, quantity: int = 1) -> None:
        super().__init__()
        self.timeframe = timeframe
        self.unit = unit
        self.quantity = quantity

    def __str__(self) -> str:
        if self.timeframe is Timeframe.current:
            return escape_string(f"{self.timeframe} {self.unit}")
        else:
            unit = f"{self.unit}s" if self.quantity > 1 else self.unit
            return escape_string(f"{self.quantity} {unit} {self.timeframe}")


class date_range(Expression):
    def __init__(
        self,
        start_date: Optional[Union[date, relative_date]] = None,
        end_date: Optional[Union[date, relative_date]] = None,
    ) -> None:
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self) -> str:
        if isinstance(self.start_date, date) and isinstance(self.end_date, date):
            start = ",".join(str(arg) for arg in self.start_date._args)
            end = ",".join(str(arg) for arg in self.end_date._args)
            return f"[dateRange([{start}], [{end}])]"
        else:
            start = self.start_date or ""
            end = self.end_date or ""
            return f"[{start}..{end}]"
