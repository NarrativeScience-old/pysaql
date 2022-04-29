"""Contains unit tests for the stream module"""

import pytest

from pysaql.enums import FillDateTypeString, JoinType, Order
from pysaql.scalar import field
from pysaql.stream import cogroup, load, Stream


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


def test_cogroup__all():
    """Should cogroup by all"""

    q0 = load("q0_dataset")
    q1 = load("q1_dataset")

    c0 = cogroup((q0, "all"), (q1, "all"))

    assert str(c0).split("\n") == [
        """q0 = load "q0_dataset";""",
        """q1 = load "q1_dataset";""",
        """q2 = cogroup q0 by all, q1 by all;""",
    ]


def test_cogroup__multiple():
    """Should cogroup by multiple fields"""

    q0 = load("q0_dataset")
    q1 = load("q1_dataset")

    c0 = cogroup((q0, [field("a"), field("b")]), (q1, [field("a"), field("b")]))

    assert str(c0).split("\n") == [
        """q0 = load "q0_dataset";""",
        """q1 = load "q1_dataset";""",
        """q2 = cogroup q0 by ('a', 'b'), q1 by ('a', 'b');""",
    ]


def test_foreach__invalid():
    """Should raise when no fields provided"""
    stream = Stream()
    with pytest.raises(ValueError):
        stream.foreach()


def test_foreach():
    """Should generate field projections"""
    stream = Stream()
    stream.foreach(field("name"), field("number").alias("n"))
    assert str(stream) == "q0 = foreach q0 generate 'name', 'number' as 'n';"


def test_group__all():
    """Should group by all when no fields are provided"""
    stream = Stream()
    stream.group()
    assert str(stream) == "q0 = group q0 by all;"


def test_group():
    """Should group by fields"""
    stream = Stream()
    stream.group(field("name"), field("date"))
    assert str(stream) == "q0 = group q0 by ('name', 'date');"


def test_filter__invalid():
    """Should raise when no fields provided"""
    stream = Stream()
    with pytest.raises(ValueError):
        stream.filter()


def test_filter__single():
    """Should filter by a single condition"""
    stream = Stream()
    stream.filter(field("name") == "foo")
    assert str(stream) == """q0 = filter q0 by 'name' == "foo";"""


def test_filter__multiple():
    """Should filter by a multiple conditions"""
    stream = Stream()
    stream.filter(field("name") == "foo", field("bar") == "baz")
    assert str(stream) == """q0 = filter q0 by ('name' == "foo") && ('bar' == "baz");"""


def test_limit__invalid():
    """Should raise when invalid limit provided"""
    stream = Stream()
    with pytest.raises(ValueError):
        stream.limit(0)

    with pytest.raises(ValueError):
        stream.limit(10_0001)


def test_limit():
    """Should limit by a row count"""
    stream = Stream()
    stream.limit(10)
    assert str(stream) == """q0 = limit q0 10;"""


def test_order__invalid():
    """Should raise when no fields provided"""
    stream = Stream()
    with pytest.raises(ValueError):
        stream.order()


def test_order():
    """Should order by different fields"""
    stream = Stream()
    stream.order(field("name"))
    stream.order((field("name"), Order.desc))
    stream.order(field("name"), field("bar"))
    stream.order((field("name"), Order.desc), (field("bar"), Order.asc))
    assert str(stream).split("\n") == [
        """q0 = order q0 by 'name' asc;""",
        """q0 = order q0 by 'name' desc;""",
        """q0 = order q0 by ('name' asc, 'bar' asc);""",
        """q0 = order q0 by ('name' desc, 'bar' asc);""",
    ]


def test_fill__no_partition():
    """Should include fill statement without a partition"""
    stream = Stream()
    stream.fill(
        [field("Year"), field("Month")],
        FillDateTypeString.y_m,
    )
    assert str(stream) == """q0 = fill q0 by (dateCols=('Year', 'Month', "Y-M"));"""


def test_fill__partition():
    """Should include fill statement with a partition"""
    stream = Stream()
    stream.fill(
        [field("Year"), field("Month")],
        FillDateTypeString.y_m,
        partition=field("Type"),
    )
    assert (
        str(stream)
        == """q0 = fill q0 by (dateCols=('Year', 'Month', "Y-M"), partition='Type');"""
    )
