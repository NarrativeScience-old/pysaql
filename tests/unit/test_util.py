"""Contains unit tests for the util module"""


import pysaql.util as mod_ut


def test_escape_identifier():
    """Should return escaped identifier"""
    assert mod_ut.escape_identifier("foo") == "'foo'"
    assert mod_ut.escape_identifier("foo's world's bar") == "'foo\\'s world\\'s bar'"


def test_escape_string():
    """Should return escaped string"""
    assert mod_ut.escape_string("foo") == '"foo"'
    assert mod_ut.escape_string('foo "world" bar') == '"foo \\"world\\" bar"'


def test_stringify__to_string():
    """Should stringify an object with a to_string method"""

    class Foo:
        def to_string(self):
            return "foo"

    assert mod_ut.stringify(Foo()) == "foo"


def test_stringify__literal():
    """Should stringify literal objects"""
    assert mod_ut.stringify("foo") == '"foo"'
    assert mod_ut.stringify(("foo",)) == '["foo"]'
    assert mod_ut.stringify(["foo"]) == '["foo"]'
    assert mod_ut.stringify(1) == "1"
    assert mod_ut.stringify(1.23) == "1.23"


def test_stringify__default():
    """Should no-op"""

    class Foo:
        pass

    foo = Foo()
    assert mod_ut.stringify(foo) is foo


def test_stringify_list__one():
    """Should stringify a list with one item"""
    assert mod_ut.stringify_list(["foo"]) == "foo"
    assert mod_ut.stringify_list("foo") == "foo"


def test_stringify_list__multiple():
    """Should stringify a list with one item"""
    assert mod_ut.stringify_list(["foo", "bar"]) == "(foo, bar)"


def test_flatten__empty():
    """Should return empty list"""
    assert mod_ut.flatten([]) == []


def test_flatten__nested():
    """Should flatten nested list"""
    assert mod_ut.flatten([1, [2, [3, [4, 5]], 6], 7]) == [1, 2, 3, 4, 5, 6, 7]
