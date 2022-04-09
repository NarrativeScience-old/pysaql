"""Contains utility functions for working with expressions"""

from typing import Any


def escape_identifier(s: str) -> str:
    return "'" + s.replace("'", "\'") + "'"

def escape_string(s: str) -> str:
    return '"' + s.replace('"', '\"') + '"'

def stringify(s: Any) -> str:
    if hasattr(s, "to_string"):
        return s.to_string()
    elif isinstance(s, str):
        return escape_string(s)
    elif s is None:
        return "null"
    else:
        return s
