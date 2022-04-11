"""Contains unit tests for the scalar module"""


from pysaql.saql.scalar import field


def test_alias():
    """Should include alias string"""
    assert str(field("name").alias("NAME")) == "'name' as 'NAME'"
