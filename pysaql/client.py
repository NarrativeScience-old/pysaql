"""
q = load "DTC_Opportunity_SAMPLE";
q = foreach q generate day_in_week(toDate(Mail_sent_sec_epoch)) as 'Day in Week';
q = group q by 'Day in Week';
q = foreach q generate 'Day in Week', count() as 'count';
"""

from pysaql.expressions.aggregations import count
from pysaql.expressions.enums import JoinType
from pysaql.expressions.stream import cogroup, dataset
from pysaql.expressions import function as fn
from pysaql.expressions.field import field

q0 = dataset("DTC_Opportunity_SAMPLE").foreach(
    fn.day_in_week(fn.to_date(field("Mail_sent_sec_epoch"))).alias("Day in Week")
).group(field("Day in Week")).foreach(field("Day in Week"), count().alias("count")).order(field("count")).limit(5)

q1 = dataset("DTC_Opportunity_SAMPLE").foreach(
    fn.day_in_week(fn.to_date(field("Mail_sent_sec_epoch"))).alias("Day in Week")
).group(field("Day in Week")).foreach(field("Day in Week"), count().alias("count")).order(field("count")).limit(5)

q = cogroup((q0, field("Day in Week")), (q1, field("Day in Week")), join_type=JoinType.full)

print(q)
