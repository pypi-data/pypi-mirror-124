"""Module containing order constants and classes for the backtester."""

from __future__ import annotations

from dataclasses import dataclass

from trading.backtester.position import SHORT
from trading.backtester.position import POSITION_WORD_MAPPING


__all__ = [
    # Constants export
    "LIMIT",
    "MARKET",
    "STOP_LIMIT",
    "STOP_MARKET",
    "VALID_ORDER_TYPES",
]


LIMIT = "limit"
MARKET = "market"
STOP_LIMIT = "stop_limit"
STOP_MARKET = "stop_market"

# Consolidate into a list of string values that can be used
# for validation of newly created orders
VALID_ORDER_TYPES = (MARKET, LIMIT, STOP_LIMIT, STOP_MARKET)


@dataclass
class Order:
    order_id: str
    position: str
    ordertype: str
    amount: float
    trading_symbol: str
    signal_source_symbol: str
    limit: float | None = None
    stop: float | None = None
    close: float | None = None
    closing_timestamp: str | None = None
    creation_timestamp: str | None = None
    execution_timestamp: str | None = None
    cancellation_timestamp: str | None = None

    def value(self, current_price: float):
        if self.limit is None or self.execution_timestamp is None:
            return self.amount

        return abs((current_price / self.limit) * self.amount)

    def openprofit(self, current_price) -> float:
        """Returns the open profits amount of this open trade.

        If the trade is not yet executed, or the limit price is not
        yet set, the open profit is equal to zero.
        """
        if self.limit is None or self.execution_timestamp is None:
            return 0.0

        return self.get_profit(
            current_price, self.limit, self.qty, self.position)

    @property
    def id(self) -> str:
        return self.order_id

    @property
    def type(self) -> str:
        return self.ordertype

    @property
    def netprofit(self) -> float:
        """Returns the net profits amount of this closed trade.

        If the trade is not yet closed - there's no closing price or
        closing timestamp set yet, then raise an error to the user.
        """

        # This trade is not yet closed, raise an error
        if self.close is None or self.closing_timestamp is None:
            raise ValueError(f"trade is not closed yet: {self!r}")

        return self.get_profit(self.close, self.limit, self.qty, self.position)

    @property
    def position_amount(self) -> str:
        return self.amount * self.position

    @property
    def position_word(self) -> str:
        return POSITION_WORD_MAPPING[self.position]

    @property
    def qty(self) -> float:
        if self.limit is None:
            raise ValueError(f"limit price is not set yet: {self!r}")

        return float(self.amount / self.limit)

    @staticmethod
    def get_profit(
        exit_price: float,
        entry_price: float,
        qty: float,
        position: int,
    ) -> float:

        # multiplier = -1 if short position, 1 if long position
        # profit = exit price - entry price * qty * multiplier
        return float((exit_price - entry_price) * qty * position)
