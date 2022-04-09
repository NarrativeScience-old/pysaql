"""Contains utility functions for working with expressions"""

def escape_identifier(s: str) -> str:
    return "'" + s.replace("'", "\'") + "'"

def escape_string(s: str) -> str:
    return '"' + s.replace('"', '\"') + '"'
