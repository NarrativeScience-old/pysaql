"""Contains unit tests for the util module"""
from typing import Union

from hypothesis import assume, given, note, strategies as st

import pysaql.util as mod_ut


@given(...)
def test_escape_no_except(s: str):
    """Shouldn't raise any exceptions"""
    s1 = mod_ut.escape_identifier(s)
    s2 = mod_ut.escape_string(s)
    note(f"{s1=}")
    note(f"{s2=}")
    # ensure quotes are added
    assert s1[0] == s1[-1] == "'"
    assert s2[0] == s2[-1] == '"'
    # slice to avoid counting first and last quotes
    s1 = s1[1:-1]
    s2 = s2[1:-1]
    # assert any quotes are escaped
    assert s1.count("'") == s1.count("\\'")
    assert s2.count('"') == s2.count('\\"')
    # assert backslashes are escaped
    assert (s1.count("\\") - s1.count("'")) % 2 == 0
    assert (s2.count("\\") - s2.count('"')) % 2 == 0


literals = Union[float, str, bool, int]
_nested_list = st.deferred(lambda: st.from_type(literals) | st.lists(nested_list))
nested_list = st.lists(_nested_list)


@given(...)
def test_stringify(
    s: Union[dict[str, literals], list[literals], str, float, bool, set[literals]]
):
    """Shouldn't raise any exceptions"""
    mod_ut.stringify(s)


@given(nested_list)
def test_stringify_nested(s):
    """Shouldn't raise any exceptions"""
    mod_ut.stringify(s)


@given(...)
def test_stringify_list_noexcept(list_: list[literals]):
    """Shouldn't raise any exceptions"""
    assume(list_)
    mod_ut.stringify_list(list_)


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


@given(nested_list)
def test_flatten__nested_noexcept(list_):
    """Should flatten nested list without throwing an exception"""
    mod_ut.flatten(list_)
