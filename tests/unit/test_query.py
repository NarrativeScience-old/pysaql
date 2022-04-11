"""Contains tests rendered queries"""

from pysaql.saql.aggregation import count, dense_rank, sum
from pysaql.saql.date_ import date, date_range, day_in_week, relative_date, to_date
from pysaql.saql.enums import (
    FillDateTypeString,
    JoinType,
    Order,
    RelativeDateUnit,
    RelativeTimeframe,
)
from pysaql.saql.field import field
from pysaql.saql.function import coalesce
from pysaql.saql.stream import cogroup, load


def test_complex():
    """Should render a complex query"""
    q0 = (
        load("DTC_Opportunity_SAMPLE")
        .foreach(
            day_in_week(to_date(field("Mail_sent_sec_epoch"))).alias("Day in Week")
        )
        .group(field("Day in Week"))
        .foreach(
            field("Day in Week"),
            sum(field("amount")).alias("total_amount"),
            count().alias("count"),
        )
        .order(field("count"))
        .limit(5)
    )

    q1 = (
        load("opportunities")
        .foreach(field("name"), coalesce(field("number"), field("other number"), 0))
        .fill(
            [field("Year"), field("Month")],
            FillDateTypeString.y_m,
            partition=field("Type"),
        )
        .filter(
            field("name") == "abc",
            ~field("flag"),
            (field("number") > 0) | (field("number") < 0),
            field("empty") == None,  # noqa: E711
            field("list").in_(["ny", "ma"]),
            field("closed_date").in_(
                date_range(
                    date(2022, 1),
                    relative_date(RelativeTimeframe.past, RelativeDateUnit.month, 2),
                )
            ),
        )
        .foreach(
            sum(field("amount"))
            .over(
                (None, 2),
                [field("region"), field("state")],
                [(sum(field("amount")), Order.desc)],
            )
            .alias("total amount"),
            dense_rank()
            .over(
                (None, None),
                field("county"),
                field("region"),
            )
            .alias("total amount"),
        )
    )

    q = cogroup(
        (q0, field("Day in Week")), (q1, field("Day in Week")), join_type=JoinType.full
    )

    assert str(q).split("\n") == [
        """q0 = load "DTC_Opportunity_SAMPLE";""",
        """q0 = foreach q0 generate day_in_week(toDate('Mail_sent_sec_epoch')) as 'Day in Week';""",
        """q0 = group q0 by 'Day in Week';""",
        """q0 = foreach q0 generate 'Day in Week', sum('amount') as 'total_amount', count() as 'count';""",
        """q0 = order q0 by 'count' asc;""",
        """q0 = limit q0 5;""",
        """q1 = load "opportunities";""",
        """q1 = foreach q1 generate 'name', coalesce('number', 'other number', 0);""",
        """q1 = fill q1 by (dateCols=('Year','Month', "Y-M"), partition='Type');""",
        """q1 = filter q1 by 'name' == "abc" && ! 'flag' && ('number' > 0 || 'number' < 0) && 'empty' is null && 'list' in ["ny", "ma"] && 'closed_date' in [date(2022, 1).."2 months ago"];""",
        """q1 = foreach q1 generate sum('amount') over ([..2] partition by ('region', 'state') order by sum('amount') desc) as 'total amount', dense_rank() over ([..] partition by 'county' order by 'region' asc) as 'total amount';""",
        """q2 = cogroup q0 by 'Day in Week' full, q1 by 'Day in Week';""",
    ]
