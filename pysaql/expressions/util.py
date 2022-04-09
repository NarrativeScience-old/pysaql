"""Contains utility functions for working with expressions"""

def escape(s: str) -> str:
    return "'" + s.replace("'", "\'") + "'"
