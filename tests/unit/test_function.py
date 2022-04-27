"""Contains unit tests for the function module"""


import pysaql.function as fn
from pysaql.scalar import field


def test_coalesce():
    """Should coalesce values"""
    assert (
        str(fn.coalesce(field("name"), field("other"), "empty").alias("NAME"))
        == """coalesce('name', 'other', "empty") as 'NAME'"""
    )


def test_concat():
    """Should concatenate values"""
    assert (
        str(fn.concat(field("name"), field("other"), "empty").alias("NAME"))
        == """'name' + "-" + 'other' + "-" + "empty" as 'NAME'"""
    )
    assert (
        str(
            fn.concat(field("name"), field("other"), "empty", delimiter="~").alias(
                "NAME"
            )
        )
        == """'name' + "~" + 'other' + "~" + "empty" as 'NAME'"""
    )


def test_abs():
    """Should render abs function"""
    assert str(fn.abs_(field("num")).alias("NAME")) == """abs('num') as 'NAME'"""


def test_ceil():
    """Should render ceil function"""
    assert str(fn.ceil(field("num")).alias("NAME")) == """ceil('num') as 'NAME'"""


def test_floor():
    """Should render floor function"""
    assert str(fn.floor(field("num")).alias("NAME")) == """floor('num') as 'NAME'"""


def test_power():
    """Should render power function"""
    assert (
        str(fn.power(field("num"), 12).alias("NAME"))
        == """power('num', 12) as 'NAME'"""
    )


def test_round():
    """Should render round function"""
    assert (
        str(fn.round_(field("num"), 0).alias("NAME")) == """round('num', 0) as 'NAME'"""
    )


def test_trunc():
    """Should render trunc function"""
    assert (
        str(fn.trunc(field("num"), 0).alias("NAME")) == """trunc('num', 0) as 'NAME'"""
    )
