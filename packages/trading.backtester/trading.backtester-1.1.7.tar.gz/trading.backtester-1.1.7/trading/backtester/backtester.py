"""Module containing the Backtester class."""

from __future__ import annotations

import inspect
import math

from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import quantstats as qs

from trading.backtester.position import LONG
from trading.backtester.position import SHORT

from trading.backtester.config import AttrDict
from trading.backtester.config import BacktesterConfig
from trading.backtester.exchange import BacktesterExchange
from trading.backtester.strategy import BacktesterStrategy


__all__ = [
    # Class exports
    "Backtester",
]


class Backtester:
    """Base backtester class."""

    def __init__(self, config: dict | str):
        """Creates an instance of a new strategy."""
        self._config = BacktesterConfig.load(config)

        self._exchange = BacktesterExchange(
            backtester=self,
            initial_balance=self.config.initial_balance,
            currency=self.config.initial_balance_currency)

        self._strat_class = None
        self._strat = None

    def run(self):
        """The core method to perform backtesting."""
        if self.strategy is None:
            raise ValueError("strategy is not set")

        if self.data is None:
            raise ValueError("data is not set")  # pragma: no cover

        for asset in self.config.assets:
            data = self.data[asset.signal_source_symbol]

            # Add current asset to the strategy
            setattr(self._strat, "trading_symbol", asset.trading_symbol)
            setattr(self._strat, "signal_source_symbol",
                asset.signal_source_symbol)

            # Add current asset to the exchange
            setattr(self._exchange, "trading_symbol", asset.trading_symbol)
            setattr(self._exchange, "signal_source_symbol",
                asset.signal_source_symbol)

            # Add data columns to strategy for initialization function
            for column in data.columns:
                setattr(self._strat, column, data[column])

            # Remember old attributes and then get the new attributes
            # all the newly added Series datasets should be added
            # manually to the data attribute
            old_attributes = dir(self._strat)
            self._strat.initialize()
            new_attributes = list(set(dir(self._strat)) - set(old_attributes))

            # Filter new data by its type, only process pd.Series types
            for new_attribute in new_attributes[:]:
                data_to_be_added = getattr(self._strat, new_attribute)
                if isinstance(data_to_be_added, pd.Series):
                    data[new_attribute] = data_to_be_added
                else:
                    new_attributes.remove(new_attribute)

            for i, _ in enumerate(data.index):
                # Add the same Trading View-like data but for the index
                setattr(
                    self._exchange,
                    data.index.name,
                    data.index[:(i + 1)][::-1])

                # Create a Trading View-like data object and assign
                # it to the strategy object for Trader's use
                for column in data.columns:
                    padded_data = data[column][:(i + 1)][::-1]
                    padded_data = np.pad(
                        padded_data,
                        (0, self.minimum_indicator_period),
                        mode="constant",
                        constant_values=(np.nan,))

                    setattr(self._strat, column, padded_data)
                    setattr(self._exchange, column, padded_data)

                setattr(
                    self._strat,
                    "position_size",
                    (
                        [0] * self.minimum_indicator_period
                        if self.exchange.position_size.empty
                        else self.exchange.position_size.tolist()[::-1]
                    )
                )

                # Very first period
                if i == 0:
                    self.exchange.start()
                    self.strategy.start()

                # Run next for the rest of the whole backtest
                if i > self.minimum_indicator_period:
                    self.exchange.nextstart()
                    self.strategy.next()
                    self.exchange.nextstop()

                # Run prenext if we"re still warming up
                elif i < self.minimum_indicator_period:
                    self.strategy.prenext()

                # Run nextstart if we just finished warming up
                else:
                    self.exchange.nextstart()
                    self.strategy.nextstart()
                    self.exchange.nextstop()

            # Ending function calls
            self.strategy.stop()
            self.exchange.stop()

            # Cleanup the added attributes for the next symbol
            for new_attribute in new_attributes:
                delattr(self._strat, new_attribute)

    def set_strategy(
        self,
        strategy: BacktesterStrategy,
        parameters: dict | None = None,
    ):

        """Sets the strategy to be used by the Backtester.

        Arguments:
            strategy: A subclass of the `bt.BacktesterStrategy` class.
            parameters: A dictionary containing a set of strategy
                parameters. If the configuration given to the Backtester
                already has a set of parameters and the user still
                entered another set of parameters in this function,
                the latter is the one we would use.

        Raises:
            ValueError: Raised when the strategy is not a subclass of
                `bt.BacktesterStrategy`, is not a class at all, or if
                the input strategy is already an instance.

        """
        if not inspect.isclass(strategy):
            raise ValueError(f"input strategy is not a class: {strategy}")

        if not issubclass(strategy, BacktesterStrategy):
            raise ValueError(f"not a strategy subclass: {type(strategy)}")

        if strategy == BacktesterStrategy:
            raise ValueError(f"invalid strategy type: {type(strategy)}")

        # Try to get the parameters from the configuration if not given
        if not parameters:
            parameters = self._config.strategy_parameters
        else:
            parameters = AttrDict(parameters)

        self._strat_class = strategy
        self._strat = strategy(self, parameters=parameters)

    def visualize(
        self,
        input_symbol: str | None = None,
        plots: list | dict | str | None = None,
    ) -> go.Figure | None:
        if plots and not isinstance(plots, (dict, list, tuple, str)):
            return None

        show_trades = False if not plots else "trades" in plots
        show_candlesticks = False if not plots else "candles" in plots
        show_positions = False if not plots else "position_size" in plots

        if not show_candlesticks and show_trades and input_symbol:
            show_candlesticks = True

        # Turn plots into configs
        if plots is None:
            if input_symbol is None:
                plots = ["equity", "drawdown"]
            else:
                plots = []
                show_candlesticks = True

        if isinstance(plots, dict):
            plot_configs = plots
        elif isinstance(plots, str):
            plot_configs = {str(plots): {}}
        else:
            plot_configs = {plot_name: {} for plot_name in plots}

        # Make sure the symbol is given for graphs other than equity and dd
        for plot_name in plot_configs.keys():
            if (plot_name not in ("equity", "drawdown") and
                input_symbol is None
            ):
                return None

        DEFAULT_CONFIG = {
            "color": "rgba(66,133,244,1)",
            "width": 2,
        }

        # Auto fetch trading and signal source symbols
        trading_symbol = None
        signal_source_symbol = None
        if input_symbol:
            for asset in self.config.assets:
                if (input_symbol == asset.trading_symbol or
                    input_symbol == asset.signal_source_symbol
               ):
                    trading_symbol = asset.trading_symbol
                    signal_source_symbol = asset.signal_source_symbol

            if trading_symbol is None and signal_source_symbol is None:
                return None

        # fig = go.Figure()
        if show_candlesticks and "equity" in plots and "drawdown" in plots:
            fig = make_subplots(rows=3, cols=1)
            drawdown_row, equity_row, ohlcv_row = (1, 2, 3)
        elif not show_candlesticks and "equity" in plots and "drawdown" in plots:
            if len(plots) >= 3:
                fig = make_subplots(rows=3, cols=1)
                drawdown_row, equity_row, ohlcv_row = (1, 2, 3)
            else:
                fig = make_subplots(rows=2, cols=1)
                drawdown_row, equity_row, ohlcv_row = (1, 2, None)
        elif len(plots) >= 2:
            if (("equity" in plots and "drawdown" not in plots) or
                ("drawdown" in plots and "equity" not in plots)
           ):
                fig = make_subplots(rows=2, cols=1)
                drawdown_row, equity_row, ohlcv_row = (1, 1, 2)
            else:
                fig = make_subplots(rows=1, cols=1)
                drawdown_row, equity_row, ohlcv_row = (1, 1, 1)
        else:
            fig = make_subplots(rows=1, cols=1)
            drawdown_row, equity_row, ohlcv_row = (1, 1, 1)

        if show_candlesticks and input_symbol is not None:
            ohlcv = go.Candlestick(
                x=self.exchange.data[signal_source_symbol].index,
                open=self.exchange.data[signal_source_symbol].open,
                high=self.exchange.data[signal_source_symbol].high,
                low=self.exchange.data[signal_source_symbol].low,
                close=self.exchange.data[signal_source_symbol].close,
                name="OHLCV")

            fig.add_trace(ohlcv, row=ohlcv_row, col=1)

            cs = fig.data[0]

            # Set line and fill colors for OHLCV
            cs.increasing.fillcolor = "rgba(38,166,154,0.6)"
            cs.increasing.line.color = "rgba(38,166,154,1)"
            cs.decreasing.fillcolor = "rgba(239,83,80,0.6)"
            cs.decreasing.line.color = "rgba(239,83,80,1)"

        if "candles" in plot_configs:
            del plot_configs["candles"]

        if "equity" in plot_configs:
            plot_config = DEFAULT_CONFIG.copy()
            plot_config.update({"color": "#222222"})
            if input_symbol is not None:
                equity_y = list(self.exchange.asset_equity[trading_symbol].values())
                # equity_y = [(e / self.exchange.initial_balance) - 1 for e in equity_y]
                equity = go.Scatter(
                    line=plot_config,
                    x=list(self.exchange.asset_equity[trading_symbol].keys()),
                    y=equity_y,
                    mode="lines",
                    fill="tozeroy",
                    fillcolor="rgba(0,0,0,0.1)",
                    name="Equity")

            else:
                first_symbol = list(self.exchange.asset_equity.keys())[0]
                equity_y = self.exchange.equity
                equity = go.Scatter(
                    line=plot_config,
                    x=list(self.exchange.asset_equity[first_symbol].keys()),
                    y=equity_y,
                    # y=equity_y / self.exchange.initial_balance) - 1,
                    mode="lines",
                    fill="tozeroy",
                    fillcolor="rgba(0,0,0,0.1)",
                    name="Equity")

            fig.add_trace(equity, row=equity_row, col=1)
            # fig.update_layout(**{
            #     f"yaxis{equity_row}": dict(range=[
            #         min(equity_y), max(equity_y)
            #     ])
            # })
            del plot_configs["equity"]

        if "drawdown" in plot_configs:
            if input_symbol is None:
                equity_series = self.exchange.equity
            else:
                equity_series = pd.Series(self.exchange.asset_equity[trading_symbol])

            first_symbol = list(self.exchange.asset_equity.keys())[0]
            drawdown = qs.stats.to_drawdown_series(equity_series) * 100
            plot_config = DEFAULT_CONFIG.copy()
            plot_config.update({"color": "rgba(239,67,55,1)"})
            equity = go.Scatter(
                line=plot_config,
                x=list(self.exchange.asset_equity[first_symbol].keys()),
                y=drawdown,
                mode="lines",
                fill="tozeroy",
                fillcolor="rgba(239,67,55,0.1)",
                name="Drawdown")

            fig.add_trace(equity, row=drawdown_row, col=1)
            del plot_configs["drawdown"]

        if show_trades:
            del plot_configs["trades"]

            arrow_length = (max(self.exchange.data[signal_source_symbol].close) / 6) / (3 / ohlcv_row)
            closed_timestamps = [t.closing_timestamp for t in self.exchange.closed_trades]

            for trade in self.exchange.closed_trades + self.exchange.open_trades:
                if trade.trading_symbol != trading_symbol:
                    continue

                if trade.closing_timestamp and trade.close:
                    if trade.execution_timestamp in closed_timestamps:
                        actual_trade_ay = 96
                        actual_trade_standoff = 58
                    else:
                        actual_trade_ay = 38
                        actual_trade_standoff = 0

                    fig.add_annotation(
                        x=trade.closing_timestamp,  # arrows' head
                        y=trade.close,
                        ax=trade.closing_timestamp,  # arrows' tail
                        ay=-38 if trade.position == LONG else 38,
                        xref=f"x{ohlcv_row}",
                        yref=f"y{ohlcv_row}",
                        axref=f"x{ohlcv_row}",
                        ayref="pixel",
                        text=(
                            f"Close {trade.id}<br>{(trade.position * -trade.qty):+.4f}"
                            if trade.position == SHORT
                            else f"{(trade.position * -trade.qty):+.4f}<br>Close {trade.id}"
                        ),
                        font=dict(
                            family="Trebuchet MS, Roboto, Ubuntu, sans-serif",
                            size=12,
                        ),
                        # text=f"{trade.position_word}<br>{(trade.position * trade.qty)}",  # if you want only the arrow
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor='#d500f9',
                    )

                else:
                    actual_trade_ay = 38
                    actual_trade_standoff = 0

                if (trade.closing_timestamp is None and
                    trade.execution_timestamp and
                    trade.execution_timestamp in closed_timestamps
                ):
                    actual_trade_ay = 96
                    actual_trade_standoff = 58

                fig.add_annotation(
                    x=trade.execution_timestamp,  # arrows' head
                    y=trade.limit,
                    ax=trade.execution_timestamp,  # arrows' tail
                    ay=actual_trade_ay * trade.position,
                    xref=f"x{ohlcv_row}",
                    yref=f"y{ohlcv_row}",
                    axref=f"x{ohlcv_row}",
                    text=(
                        f"{(trade.position * trade.qty):+.4f}<br>{trade.id}"
                        if trade.position == SHORT
                        else f"{trade.id}<br>{(trade.position * trade.qty):+.4f}"
                    ),
                    font=dict(
                        family="Segoe UI, Roboto, Ubuntu, sans-serif",
                        size=12,
                    ),
                    # text=f"{trade.position_word}<br>{(trade.position * trade.qty)}",  # if you want only the arrow
                    showarrow=True,
                    standoff=actual_trade_standoff,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor='rgba(66,133,244,1)' if trade.position == LONG else 'rgba(239,67,55,1)'
                )

        COLORS = ["#2962ff", "#673ab7", "#9c27b0", "#e91e63", "#f44336", "#ff9800", "#4caf50", "#009688", "#00bcd4"]
        for i, (plot_name, plot_config_override) in enumerate(plot_configs.items()):
            plot_config = {
                "color": COLORS[i % (len(COLORS) + 1)],
                "width": 2,
            }
            plot_config.update(plot_config_override)

            plot_obj = go.Scatter(
                line=plot_config,
                x=self.exchange.data[signal_source_symbol].index,
                y=self.exchange.data[signal_source_symbol][plot_name],
                name=plot_name.title())

            fig.add_trace(plot_obj, row=ohlcv_row, col=1)

        fig.update_layout(
            margin=dict(l=15, r=15, t=40, b=15),
            plot_bgcolor="rgba(255,255,255,1)",
            paper_bgcolor="rgba(255,255,255,0)",
        )

        fig.update_xaxes(showgrid=False, rangeslider_visible=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#dadce0")
        fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#dadce0")
        fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#dadce0")

        # fig.update_layout(legend_title_text='Subplots')
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ))

        return fig

    @property
    def config(self) -> BacktesterConfig:
        """Backtester configuration. An instance of `bt.BacktesterConfig`."""
        return self._config

    @property
    def data(self) -> dict[str, pd.DataFrame]:
        """OHLCV data exposure from the internal exchange."""
        return self._exchange.data

    @property
    def exchange(self):
        """Internal exchange representation for the backtester."""
        return self._exchange

    @property
    def minimum_indicator_period(self) -> int:
        """Minimum number of periods for indicator warmup.

        There are different indicators used in a strategy and some of
        these indicators have different required number of periods
        before they can be used. The largest required indicator period
        is called the "minimum indicator period".

        For Example, our strategy uses this list of indicators:
        - EMA 200 (required number of periods is 200)
        - SMA 50 (required number of periods is 50)
        - RSI 14 (required number of periods is 14)

        So for this strategy, the minimum indicator period is 200 since
        that's the largest required indicator period.
        """
        if not self._config.strategy_parameters:
            return 0
        return math.ceil(max(self._config.strategy_parameters.values())) - 1

    @property
    def strategy(self) -> BacktesterStrategy:
        """The strategy to be used for the backtester.

        To set the strategy properly, use `Backtester.set_strategy()`.
        """
        return self._strat
