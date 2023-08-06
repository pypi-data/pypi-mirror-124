"""Module containing position constants and classes for the backtester."""

__all__ = [
    # Constants export
    "LONG",
    "SHORT",
    "POSITION_WORD_MAPPING",
    "VALID_POSITION_TYPES",
]


LONG = 1
SHORT = -1
POSITION_WORD_MAPPING = {LONG: "long", SHORT: "short"}

# Consolidate into a list of string values that can be used
# for validation of newly created orders
VALID_POSITION_TYPES = (LONG, SHORT)
