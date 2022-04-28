"""Contains unit tests for the scalar module"""


from pysaql.scalar import field, literal


def test_alias():
    """Should include alias string"""
    assert str(field("name").alias("NAME")) == "'name' as 'NAME'"


def test_eq():
    """Should return string for eq operation"""
    assert str(field("foo") == "bar") == """'foo' == \"bar\""""


def test_ne():
    """Should return string for ne operation"""
    assert str(field("foo") != "bar") == """'foo' != \"bar\""""


def test_lt():
    """Should return string for lt operation"""
    assert str(field("foo") < 123) == """'foo' < 123"""


def test_le():
    """Should return string for le operation"""
    assert str(field("foo") <= 123) == """'foo' <= 123"""


def test_gt():
    """Should return string for gt operation"""
    assert str(field("foo") > 123) == """'foo' > 123"""


def test_ge():
    """Should return string for ge operation"""
    assert str(field("foo") >= 123) == """'foo' >= 123"""


def test_add():
    """Should return string for add operation"""
    assert str(field("foo") + 10) == """'foo' + 10"""


def test_sub():
    """Should return string for sub operation"""
    assert str(field("foo") - 10) == """'foo' - 10"""


def test_mul():
    """Should return string for mul operation"""
    assert str(field("foo") * 10) == """'foo' * 10"""


def test_truediv():
    """Should return string for truediv operation"""
    assert str(field("foo") / 10) == """'foo' / 10"""


def test_truediv__literal_right():
    """Should allow a literal value as the right operand when the left operand is a binary operation"""
    assert str((field("foo") / 10) * 100) == """('foo' / 10) * 100"""


def test_truediv__literal_left():
    """Should require a literal value as the left operand when the right operand is a binary operation"""
    assert str(literal(100) * (field("foo") / 10)) == """100 * ('foo' / 10)"""


def test_neg():
    """Should return string for neg operation"""
    assert str(-field("foo")) == """- 'foo'"""


def test_in():
    """Should return string for in operation"""
    assert str(field("foo").in_(["bar"])) == """'foo' in ["bar"]"""


def test_and():
    """Should return string for and operation"""
    assert (
        str((field("foo") > 0) & (field("foo") < 10))
        == """('foo' > 0) && ('foo' < 10)"""
    )


def test_or():
    """Should return string for or operation"""
    assert (
        str((field("foo") > 0) | (field("foo") < 10))
        == """('foo' > 0) || ('foo' < 10)"""
    )


def test_inv():
    """Should return string for inv operation"""
    assert str(~field("foo")) == """! 'foo'"""
