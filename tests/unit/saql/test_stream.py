"""Contains unit tests for the stream module"""

from pysaql.saql.enums import JoinType
from pysaql.saql.field import field
from pysaql.saql.stream import cogroup, load


def test_load():
    """Should return a stream"""
    assert str(load("foo")) == 'q0 = load "foo";'


def test_cogroup():
    """Should return a combined stream"""

    q0 = load("q0_dataset")
    q1 = load("q1_dataset")
    q2 = load("q2_dataset")
    q3 = load("q3_dataset")
    q4 = load("q4_dataset")

    c0 = cogroup((q0, field("q0_pk")), (q1, field("q1_pk")))
    c1 = cogroup(
        (c0, field("c0_pk")),
        (q2, field("q2_pk")),
        (q3, field("q3_pk")),
        join_type=JoinType.full,
    )
    c2 = cogroup(
        (c1, field("c1_pk")),
        (q4, field("q4_pk")),
        join_type=JoinType.left,
    )

    assert str(c2).split("\n") == [
        """q0 = load "q0_dataset";""",
        """q1 = load "q1_dataset";""",
        """q2 = cogroup q0 by 'q0_pk', q1 by 'q1_pk';""",
        """q3 = load "q2_dataset";""",
        """q4 = load "q3_dataset";""",
        """q5 = cogroup q2 by 'c0_pk' full, q3 by 'q2_pk', q4 by 'q3_pk';""",
        """q6 = load "q4_dataset";""",
        """q7 = cogroup q5 by 'c1_pk' left, q6 by 'q4_pk';""",
    ]