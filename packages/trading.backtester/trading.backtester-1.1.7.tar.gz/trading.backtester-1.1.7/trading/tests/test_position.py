"""Tests for trading.backtester.position."""
# pylint: disable=missing-class-docstring,missing-function-docstring

from trading.backtester.position import LONG
from trading.backtester.position import SHORT
from trading.backtester.position import VALID_POSITION_TYPES


class TestBacktesterPosition:

    def test_constants(self):
        assert LONG == 1
        assert SHORT == -1
        assert isinstance(VALID_POSITION_TYPES, tuple)
