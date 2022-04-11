"""Contains unit tests for the date_ module"""

import pysaql.saql.date_ as mod_ut
from pysaql.saql.enums import RelativeDateUnit, RelativeTimeframe
from pysaql.saql.field import field


def test_date():
    """Should render a date string"""
    assert (
        str(mod_ut.date(field("Year"), field("Month"), field("Day")))
        == "date('Year', 'Month', 'Day')"
    )
    assert str(mod_ut.date(2022, 4, 11)) == "date(2022, 4, 11)"
    assert str(mod_ut.date(2022)) == "2022"


def test_relative_date():
    """Should render a relative date string"""
    assert (
        str(mod_ut.relative_date(RelativeTimeframe.current, RelativeDateUnit.month))
        == '"current month"'
    )
    assert (
        str(mod_ut.relative_date(RelativeTimeframe.future, RelativeDateUnit.month))
        == '"1 month ahead"'
    )
    assert (
        str(mod_ut.relative_date(RelativeTimeframe.past, RelativeDateUnit.month))
        == '"1 month ago"'
    )
    assert (
        str(
            mod_ut.relative_date(
                RelativeTimeframe.past, RelativeDateUnit.month, quantity=2
            )
        )
        == '"2 months ago"'
    )


def test_date_range__relative():
    """Should render a relative date range string"""
    assert (
        str(
            mod_ut.date_range(
                mod_ut.relative_date(
                    RelativeTimeframe.past, RelativeDateUnit.month, quantity=2
                ),
                mod_ut.relative_date(
                    RelativeTimeframe.past, RelativeDateUnit.month, quantity=1
                ),
            )
        )
        == '["2 months ago".."1 month ago"]'
    )


def test_date_range__fixed():
    """Should render a fixed date range string"""
    assert (
        str(mod_ut.date_range(mod_ut.date(2022, 3, 1), mod_ut.date(2022, 4, 1)))
        == "[dateRange([2022,3,1], [2022,4,1])]"
    )


def test_date_range__open():
    """Should render open-ended date range strings"""
    assert (
        str(
            mod_ut.date_range(
                start_date=mod_ut.relative_date(
                    RelativeTimeframe.past, RelativeDateUnit.month, quantity=2
                )
            )
        )
        == '["2 months ago"..]'
    )
    assert (
        str(
            mod_ut.date_range(
                end_date=mod_ut.relative_date(
                    RelativeTimeframe.past, RelativeDateUnit.month, quantity=2
                )
            )
        )
        == '[.."2 months ago"]'
    )
