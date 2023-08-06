"""Tests for trading.backtester.exchange."""
# pylint: disable=missing-class-docstring,missing-function-docstring

from collections import namedtuple

import pandas as pd
import pytest

from trading.backtester.order import LIMIT
from trading.backtester.order import MARKET
from trading.backtester.order import STOP_LIMIT
from trading.backtester.order import STOP_MARKET

from trading.backtester.position import LONG
from trading.backtester.position import SHORT

from trading.backtester.backtester import Backtester
from trading.backtester.config import BacktesterConfig
from trading.backtester.errors import InsufficientBalanceError
from trading.backtester.exchange import BacktesterExchange


INPUT_BACKTESTER_CONFIG = {
    "strategy_parameters": {
        "time_period": 34,
        "multiplier": 1.5
    },
    "initial_balance": 53.0091,
    "initial_balance_currency": "USD",
    "trading_exchange": "bitmex",
    "starting_timestamp": "2020-01-01 00:00:00",
    "ending_timestamp": "2021-01-01 00:00:00",
    "assets": [
        {
            "trading_symbol": "ADAUSD",
            "trading_timeframe": "4h",
            "signal_source_exchange": "binance",
            "signal_source_symbol": "ADA/USDT",
            "signal_timeframe": "4h",
            "percent_allocation": 45,
        },
        {
            "trading_symbol": "ETHUSD",
            "trading_timeframe": "4h",
            "signal_source_exchange": "binance",
            "signal_source_symbol": "ETH/USDT",
            "signal_timeframe": "4h",
            "percent_allocation": 55,
        }
    ]
}


@pytest.fixture(name="backtester", scope="class")
def fixture_backtester():
    config = BacktesterConfig.from_dict(INPUT_BACKTESTER_CONFIG)

    Backtester = namedtuple(
        "Backtester", ("config", "minimum_indicator_period"))

    return Backtester(config=config, minimum_indicator_period=200)


class TestBacktesterExchange:

    def test_required_backtester_properties(self, backtester):
        """Required for class tests that need the Backtester class."""
        for mock_property in backtester._fields:
            assert mock_property in dir(Backtester)

    def test_initialization(self, backtester):
        exchange = BacktesterExchange(backtester)
        assert isinstance(exchange, BacktesterExchange)

    def test_successful_order_creation(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        # Make sure the wallet balance is 10000 before any orders
        assert len(exchange.pending_orders) == 0
        assert exchange.wallet_balance == 10000

        order_1 = exchange.order("test-order", LONG, amount=1000)
        assert order_1.type == MARKET
        assert len(exchange.pending_orders) == 1
        assert exchange.wallet_balance == 9000
        assert exchange.pending_orders[0] == order_1
        assert exchange.pending_orders[0].id == order_1.id

        order_2 = exchange.order("test-order-2", LONG, limit=1234)
        assert order_2.type == LIMIT
        assert len(exchange.pending_orders) == 2
        assert exchange.wallet_balance == 4500
        assert exchange.pending_orders[1] == order_2
        assert exchange.pending_orders[1].id == order_2.id

        exchange.trading_symbol = "ADAUSD"
        exchange.signal_source_symbol = "ADA/USDT"

        order_3 = exchange.order("test-order_ada", LONG, amount=1000, stop=12)
        assert order_3.type == STOP_MARKET
        assert len(exchange.pending_orders) == 3
        assert exchange.wallet_balance == 3500
        assert exchange.pending_orders[2] == order_3
        assert exchange.pending_orders[2].id == order_3.id

        order_4 = exchange.order("test-order_ada_3", LONG, amount_percent=50)
        assert order_4.type == MARKET
        assert len(exchange.pending_orders) == 4
        assert exchange.wallet_balance == 1750
        assert exchange.pending_orders[3] == order_4
        assert exchange.pending_orders[3].id == order_4.id

        order_5 = exchange.order("test-order_ada", LONG, stop=124, limit=123)
        assert order_5.type == STOP_LIMIT
        assert len(exchange.pending_orders) == 5
        assert exchange.wallet_balance == 0
        assert exchange.pending_orders[4] == order_5
        assert exchange.pending_orders[4].id == order_5.id

    def test_unsuccessful_order_creation(self, backtester):
        exchange = BacktesterExchange(backtester=backtester, initial_balance=9)
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        # Unknown position value
        with pytest.raises(ValueError):
            exchange.order("id", "unknown_position")

        with pytest.raises(InsufficientBalanceError):
            exchange.order("id", LONG, amount=100)

        # Amount percent is not between 100
        with pytest.raises(ValueError):
            exchange.order("id", LONG, amount_percent=-1)

        # Amount percent is not between 100
        with pytest.raises(ValueError):
            exchange.order("id", LONG, amount_percent=101)

        # Amount percent is invalid
        with pytest.raises(ValueError):
            exchange.order("id", LONG, amount_percent=[1])

        # Amount is negative, should be positive
        with pytest.raises(ValueError):
            exchange.order("id", LONG, amount=-10)

        # Amount is zero, should be positive
        with pytest.raises(ValueError):
            exchange.order("id", LONG, amount=0)

        # Amount is invalid
        with pytest.raises(ValueError):
            exchange.order("id", LONG, amount=[1])

        # Price is negative, should be positive
        with pytest.raises(ValueError):
            exchange.order("id", LONG, limit=-10)

        # Price is zero, should be positive
        with pytest.raises(ValueError):
            exchange.order("id", LONG, limit=0)

        # Invalid price type
        with pytest.raises(ValueError):
            exchange.order("id", LONG, limit=[1])

        exchange.trading_symbol = "ADAUSD"
        exchange.signal_source_symbol = "ADA/USDT"

        # stop is negative, should be positive
        with pytest.raises(ValueError):
            exchange.order("id", LONG, stop=-10)

        # stop is zero, should be positive
        with pytest.raises(ValueError):
            exchange.order("id", LONG, stop=0)

        # Invalid stop type
        with pytest.raises(ValueError):
            exchange.order("id", LONG, stop=[1])

    def test_successful_order_cancellation(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        order_1 = exchange.order("test-order", LONG, amount=3000)
        assert len(exchange.pending_orders) == 1
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[0] == order_1
        assert exchange.pending_orders[0].id == order_1.id

        order_2 = exchange.order("test-order-2", LONG)
        assert len(exchange.pending_orders) == 2
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[1] == order_2
        assert exchange.pending_orders[1].id == order_2.id

        exchange.cancel(order_1)
        assert len(exchange.pending_orders) == 1
        assert len(exchange.cancelled_orders) == 1
        assert exchange.pending_orders[0] == order_2
        assert exchange.pending_orders[0].id == order_2.id

        exchange.cancel("test-order-2")
        assert len(exchange.pending_orders) == 0
        assert len(exchange.cancelled_orders) == 2

    def test_unsuccessful_order_cancellation(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        with pytest.warns(None) as record:
            exchange.cancel("some-unknown-order-id")

        assert len(record) == 1

        with pytest.warns(None) as record:
            exchange.cancel([1, 2, 3])

        assert len(record) == 1

        order = exchange.order("test-order-2", LONG)
        with pytest.warns(None) as record:
            exchange.cancel("different-id")

        assert len(record) == 1

    def test_all_order_cancellation(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        order_1 = exchange.order("test-order", LONG, amount=3000)
        assert len(exchange.pending_orders) == 1
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[0] == order_1
        assert exchange.pending_orders[0].id == order_1.id

        order_2 = exchange.order("test-order-2", LONG)
        assert len(exchange.pending_orders) == 2
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[1] == order_2
        assert exchange.pending_orders[1].id == order_2.id

        exchange.cancel_all()
        assert len(exchange.pending_orders) == 0
        assert len(exchange.cancelled_orders) == 2

    def test_successful_order_exit(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ADAUSD"
        exchange.signal_source_symbol = "ADA/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        assert exchange.wallet_balance == 10000

        exchange.exit("test-order")

        assert exchange.wallet_balance == 10000

        order_1 = exchange.order("test-order", LONG, amount=3000)
        assert len(exchange.pending_orders) == 1
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[0] == order_1
        assert exchange.pending_orders[0].id == order_1.id

        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"

        order_2 = exchange.order("test-order-2", LONG)
        assert len(exchange.pending_orders) == 2
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[1] == order_2
        assert exchange.pending_orders[1].id == order_2.id

        # Force buy to avoid dependency on nextstop or next start
        order_1.execution_timestamp = "2021-10-19 00:00:00"
        order_2.execution_timestamp = "2021-10-19 00:00:00"
        order_1.limit = 1.23
        order_2.limit = 3020
        exchange._open_trades.append(order_1)
        exchange._open_trades.append(order_2)
        exchange._positions = {
            "ADAUSD": {
                "price": 1.23,
                "total_amount": 3000.0,
                "position_amount": 3000.0,
            },
            "ETHUSD": {
                "price": 3020,
                "total_amount": 5500.0,
                "position_amount": 5500.0,
            }
        }

        assert len(exchange.open_trades) == 2
        assert len(exchange.closed_trades) == 0
        assert exchange.wallet_balance == 1500

        exchange.close = [1.35]
        exchange.exit("test-order")

        assert len(exchange.open_trades) == 2
        assert len(exchange.closed_trades) == 0

        exchange.exit("test-order-2")

        assert len(exchange.open_trades) == 1
        assert len(exchange.closed_trades) == 1

    def test_unsuccessful_order_exit(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ADAUSD"
        exchange.signal_source_symbol = "ADA/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

    def test_order_exit_all(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ADAUSD"
        exchange.signal_source_symbol = "ADA/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        assert exchange.wallet_balance == 10000

        exchange.exit("test-order")

        assert exchange.wallet_balance == 10000

        order_1 = exchange.order("test-order", LONG, amount=3000)
        assert len(exchange.pending_orders) == 1
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[0] == order_1
        assert exchange.pending_orders[0].id == order_1.id

        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"

        order_2 = exchange.order("test-order-2", LONG)
        assert len(exchange.pending_orders) == 2
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[1] == order_2
        assert exchange.pending_orders[1].id == order_2.id

        # Force buy to avoid dependency on nextstop or next start
        order_1.execution_timestamp = "2021-10-19 00:00:00"
        order_2.execution_timestamp = "2021-10-19 00:00:00"
        order_1.limit = 1.23
        order_2.limit = 3020
        exchange._open_trades.append(order_1)
        exchange._open_trades.append(order_2)
        exchange._positions = {
            "ADAUSD": {
                "price": 1.23,
                "total_amount": 3000.0,
                "position_amount": 3000.0,
            },
            "ETHUSD": {
                "price": 3020,
                "total_amount": 5500.0,
                "position_amount": 5500.0,
            }
        }

        assert len(exchange.open_trades) == 2
        assert len(exchange.closed_trades) == 0
        assert exchange.wallet_balance == 1500

        exchange.close = [1.35]
        exchange.exit_all()

        assert len(exchange.open_trades) == 1
        assert len(exchange.closed_trades) == 1

    def test__backtester_exchange_nextstop__tradingview_btcusd(self):
        """Golden Cross Strategy Test Case

        Backtester Configuration:
            Start Time: 2018-03-04 00:00:00
            End Time: 2018-04-09 00:00:00
            Stating Balance: 100,000
            Signal Source Symbol:
                - BTC/USDT
            Signal Source Exchange: Binance
            Timeframe: 1d
            Indicators:
                - Fast MA: SMA(50)
                - Slow MA: SMA(200)

        Pine Script Equivalent Code:

        ```pinescript
        //@version=5
        strategy("Golden Cross", process_orders_on_close=true)

        fast_ma = ta.sma(close, 50)
        slow_ma = ta.sma(close, 200)

        if ta.crossover(fast_ma, slow_ma)
            strategy.close("short")
            strategy.entry("long", strategy.long)

        if ta.crossunder(fast_ma, slow_ma)
            strategy.close("long")
            strategy.entry("short", strategy.short)
        ```
        """

        backtester = Backtester({
            "strategy_parameters": {
                "fast_period": 50,
                "slow_period": 200
            },
            "initial_balance": 100000,
            "initial_balance_currency": "USD",
            "trading_exchange": "bitmex",
            "starting_timestamp": "2018-03-04 00:00:00",
            "ending_timestamp": "2018-04-09 00:00:00",
            "assets": [
                {
                    "trading_symbol": "XBTUSD",
                    "trading_timeframe": "1d",
                    "signal_source_exchange": "binance",
                    "signal_source_symbol": "BTC/USDT",
                    "signal_timeframe": "1d",
                    "percent_allocation": 100,
                }
            ]
        })
        exchange = BacktesterExchange(
            backtester=backtester,
            initial_balance=backtester.config.initial_balance,
            currency=backtester.config.initial_balance_currency)

        # Simulate backtester data: add low, high, close, datetime
        # trading_symbol, and trading_signal_source property to exchange
        exchange.trading_symbol = "XBTUSD"
        exchange.signal_source_symbol = "BTC/USDT"

        exchange.datetime = ["2018-03-31 00:00:00", "2018-03-30 00:00:00"]
        exchange.high = [7223.36, 7292,43]
        exchange.low = [6777.00, 6600.10]
        exchange.close = [6923.91, 6840.23]

        exchange.order("sell", SHORT, amount=6923.91)
        exchange.nextstop()

        assert exchange.asset_balances == {"XBTUSD": 93076.09}
        assert exchange.asset_equity == {
            "XBTUSD": {
                "2018-03-31 00:00:00": 100000.0,
            },
        }

        exchange.datetime = ["2018-04-01 00:00:00", "2018-03-31 00:00:00"]
        exchange.high = [7049.98, 7223.36]
        exchange.low = [6430.00, 6777.00]
        exchange.close = [6813.01, 6923.91]

        exchange.nextstop()

        assert exchange.asset_balances == {"XBTUSD": 93076.09}
        assert exchange.asset_equity == {
            "XBTUSD": {
                "2018-03-31 00:00:00": 100000.0,
                "2018-04-01 00:00:00": 100110.9,
            },
        }

        exchange.datetime = ["2018-04-02 00:00:00", "2018-04-01 00:00:00"]
        exchange.high = [7125.00, 7049.98]
        exchange.low = [6765.00, 6430.00]
        exchange.close = [7056.00, 6813.01]

        exchange.nextstop()

        assert exchange.asset_balances == {"XBTUSD": 93076.09}
        assert exchange.asset_equity == {
            "XBTUSD": {
                "2018-03-31 00:00:00": 100000.0,
                "2018-04-01 00:00:00": 100110.9,
                "2018-04-02 00:00:00": 99867.91,
            },
        }

        exchange.datetime = ["2018-06-28 00:00:00", "2018-06-27 00:00:00"]
        exchange.high = [6173.01, 6190.43]
        exchange.low = [5827.00, 5971.00]
        exchange.close = [5853.98, 6133.73]

        exchange.nextstop()

        assert exchange.asset_balances == {"XBTUSD": 93076.09}
        assert exchange.asset_equity == {
            "XBTUSD": {
                "2018-03-31 00:00:00": 100000.0,
                "2018-04-01 00:00:00": 100110.9,
                "2018-04-02 00:00:00": 99867.91,
                "2018-06-28 00:00:00": 101069.93,
            },
        }

        exchange.datetime = ["2019-04-23 00:00:00", "2019-04-22 00:00:00"]
        exchange.high = [5600.00, 5400.00]
        exchange.low = [5332.41, 5208.35]
        exchange.close = [5493.31, 5357.14]

        exchange.nextstop()

        assert exchange.asset_balances == {"XBTUSD": 93076.09}
        assert exchange.asset_equity == {
            "XBTUSD": {
                "2018-03-31 00:00:00": 100000.0,
                "2018-04-01 00:00:00": 100110.9,
                "2018-04-02 00:00:00": 99867.91,
                "2018-06-28 00:00:00": 101069.93,
                "2019-04-23 00:00:00": 101430.59999999999,
            },
        }

        exchange.datetime = ["2019-04-24 00:00:00", "2019-04-23 00:00:00"]
        exchange.high = [5582.20, 5600.00]
        exchange.low = [5333.35, 5332.41]
        exchange.close = [5415.00, 5493.31]

        # Make sure balance is correct on reversal
        exchange.exit("sell")
        assert exchange.asset_balances == {"XBTUSD": 101508.91}

        exchange.order("buy", LONG, amount=5415.00)
        exchange.nextstop()

        assert exchange.asset_balances == {"XBTUSD": 96093.91}
        assert exchange.asset_equity == {
            "XBTUSD": {
                "2018-03-31 00:00:00": 100000.0,
                "2018-04-01 00:00:00": 100110.9,
                "2018-04-02 00:00:00": 99867.91,
                "2018-06-28 00:00:00": 101069.93,
                "2019-04-23 00:00:00": 101430.59999999999,
                "2019-04-24 00:00:00": 101508.91,
            },
        }

        exchange.datetime = ["2019-06-26 00:00:00", "2019-06-25 00:00:00"]
        exchange.high = [13970.00, 11850.00]
        exchange.low = [11741.00, 11026.00]
        exchange.close = [13093.80, 11820.86]

        exchange.nextstop()

        assert exchange.asset_balances == {"XBTUSD": 96093.91}
        assert exchange.asset_equity == {
            "XBTUSD": {
                "2018-03-31 00:00:00": 100000.0,
                "2018-04-01 00:00:00": 100110.9,
                "2018-04-02 00:00:00": 99867.91,
                "2018-06-28 00:00:00": 101069.93,
                "2019-04-23 00:00:00": 101430.59999999999,
                "2019-04-24 00:00:00": 101508.91,
                "2019-06-26 00:00:00": 109187.71,
            },
        }

        exchange.datetime = ["2019-10-26 00:00:00", "2019-10-25 00:00:00"]
        exchange.high = [10370.00, 8799.00]
        exchange.low = [8470.38, 7361.00]
        exchange.close = [9230.00, 8655.02]

        # Make sure balance is correct on reversal
        exchange.exit("buy")
        assert exchange.asset_balances == {"XBTUSD": 105323.91}

        exchange.order("sell", SHORT, amount=9230.00)
        exchange.nextstop()

        assert exchange.asset_balances == {"XBTUSD": 96093.91}
        assert exchange.asset_equity == {
            "XBTUSD": {
                "2018-03-31 00:00:00": 100000.0,
                "2018-04-01 00:00:00": 100110.9,
                "2018-04-02 00:00:00": 99867.91,
                "2018-06-28 00:00:00": 101069.93,
                "2019-04-23 00:00:00": 101430.59999999999,
                "2019-04-24 00:00:00": 101508.91,
                "2019-06-26 00:00:00": 109187.71,
                "2019-10-26 00:00:00": 105323.91,
            },
        }

        exchange.datetime = ["2019-10-27 00:00:00", "2019-10-26 00:00:00"]
        exchange.high = [9794.98, 13970.00]
        exchange.low = [9074.34, 11741.00]
        exchange.close = [9529.93, 13093.80]

        exchange.nextstop()

        assert exchange.asset_balances == {"XBTUSD": 96093.91}
        assert exchange.asset_equity == {
            "XBTUSD": {
                "2018-03-31 00:00:00": 100000.0,
                "2018-04-01 00:00:00": 100110.9,
                "2018-04-02 00:00:00": 99867.91,
                "2018-06-28 00:00:00": 101069.93,
                "2019-04-23 00:00:00": 101430.59999999999,
                "2019-04-24 00:00:00": 101508.91,
                "2019-06-26 00:00:00": 109187.71,
                "2019-10-26 00:00:00": 105323.91,
                "2019-10-27 00:00:00": 105023.98000000001,
            },
        }

    def test_exchange_properties(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        assert isinstance(exchange.data["ADA/USDT"], pd.DataFrame)
        assert exchange.initial_balance == 10000
        assert exchange.wallet_balance == 10000
        assert exchange.asset_balances["ADAUSD"] == 4500
        assert exchange.asset_balances["ETHUSD"] == 5500
        assert exchange.currency == "USD"
        assert exchange.asset_equity["ADAUSD"] == {}
        assert exchange.asset_equity["ETHUSD"] == {}
        assert exchange.pending_orders == []
        assert exchange.positions == {
            "ADAUSD": {
                "price": None,
                "total_amount": 0,
                "position_amount": 0,
            },
            "ETHUSD": {
                "price": None,
                "total_amount": 0,
                "position_amount": 0,
            }
        }
        assert exchange.open_trades == []
        assert exchange.cancelled_orders == []
        assert exchange.closed_trades == []

        assert len(exchange.equity) == 0
