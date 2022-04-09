"""
q = load "DTC_Opportunity_SAMPLE";
q = foreach q generate day_in_week(toDate(Mail_sent_sec_epoch)) as 'Day in Week';
q = group q by 'Day in Week';
q = foreach q generate 'Day in Week', count() as 'count';
"""

from pysaql.expressions.aggregation import sum
from pysaql.expressions.enums import DateUnit, JoinType, Timeframe
from pysaql.expressions.stream import cogroup, load
from pysaql.expressions.date_ import (
    date,
    date_range,
    day_in_week,
    relative_date,
    to_date,
)
from pysaql.expressions.field import field

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
    .foreach(field("name"))
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
)

q = cogroup(
    (q0, field("Day in Week")), (q1, field("Day in Week")), join_type=JoinType.full
)

print(q)
