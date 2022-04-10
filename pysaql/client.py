"""
q = load "DTC_Opportunity_SAMPLE";
q = foreach q generate day_in_week(toDate(Mail_sent_sec_epoch)) as 'Day in Week';
q = group q by 'Day in Week';
q = foreach q generate 'Day in Week', count() as 'count';
"""

from pysaql.saql.aggregation import dense_rank, sum
from pysaql.saql.enums import DateTypeString, DateUnit, JoinType, Order, Timeframe
from pysaql.saql.function import coalesce
from pysaql.saql.stream import cogroup, load
from pysaql.saql.date_ import (
    date,
    date_range,
    day_in_week,
    relative_date,
    to_date,
)
from pysaql.saql.field import field

q0 = (
    load("DTC_Opportunity_SAMPLE")
    .foreach(day_in_week(to_date(field("Mail_sent_sec_epoch"))).alias("Day in Week"))
    .group(field("Day in Week"))
    .foreach(field("Day in Week"), sum(field("amount")).alias("count"))
    .order(field("count"))
    .limit(5)
)

q1 = (
    load("opps")
    .foreach(field("name"), coalesce(field("number"), field("other number"), 0))
    .fill([field("Year"), field("Month")], DateTypeString.y_m, partition=field("Type"))
    .filter(
        field("name") == "abc",
        ~field("flag"),
        (field("number") > 0) | (field("number") < 0),
        field("empty") == None,
        field("list").in_(["ny", "ma"]),
        field("closed_date").in_(
            date_range(date(2022, 1), relative_date(Timeframe.past, DateUnit.month, 2))
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

print(q)
