"""Module containing metrics for the Backtester."""

import numpy as np
import quantstats as qs


class Metrics:
    def __init__(self, backtester):
        self._backtester = backtester

    @property
    def score(self):
        return (
            0.4 * self.sortino() +
            0.2 * (
                self.sharpe() +
                self.total_pnl() +
                self.average_return / self.max_drawdown()
            )
        )

    @property
    def average_return(self):
        return self.returns.mean()

    def cagr(self, rf: float = 0.0, compounded: bool = True):
        return qs.stats.cagr(self.returns, rf=rf, compounded=compounded)

    def calmar(self, prepare_returns: bool = True):
        return qs.stats.calmar(self.returns, prepare_returns=prepare_returns)

    def common_sense_ratio(self, prepare_returns: bool = True):
        return qs.stats.common_sense_ratio(
            self.returns, prepare_returns=prepare_returns)

    def cpc_index(self, prepare_returns: bool = True):
        return qs.stats.cpc_index(
            self.returns, prepare_returns=prepare_returns)

    def gain_to_pain_ratio(self, rf: float = 0, resolution: str = "D"):
        return qs.stats.gain_to_pain_ratio(
            self.returns, rf=rf, resolution=resolution)

    def kelly_criterion(self, prepare_returns: bool = True):
        return qs.stats.kelly_criterion(
            self.returns, prepare_returns=prepare_returns)

    def kurtosis(self, prepare_returns: bool = True):
        return qs.stats.kurtosis(self.returns, prepare_returns=prepare_returns)

    def max_drawdown(self):
        return qs.stats.max_drawdown(self.returns)

    def omega(self, rf: float = 0.0, required_return=0.0):
        return qs.stats.omega(
            self.returns, rf=rf, required_return=required_return, periods=365)

    def outlier_loss_ratio(
        self,
        quantile: float = 0.01,
        prepare_returns: bool = True,
    ):

        return qs.stats.outlier_loss_ratio(
            self.returns, quantile=quantile, prepare_returns=prepare_returns)

    def outlier_win_ratio(
        self,
        quantile: float = 0.99,
        prepare_returns: bool = True,
    ):

        return qs.stats.outlier_win_ratio(
            self.returns, quantile=quantile, prepare_returns=prepare_returns)

    def payoff_ratio(self, prepare_returns: bool = True):
        return qs.stats.payoff_ratio(
            self.returns, prepare_returns=prepare_returns)

    def profit_factor(self, prepare_returns: bool = True):
        return qs.stats.profit_factor(
            self.returns, prepare_returns=prepare_returns)

    def profit_ratio(self, prepare_returns: bool = True):
        return qs.stats.profit_ratio(
            self.returns, prepare_returns=prepare_returns)

    def rar(self, rf: float = 0.0):
        return qs.stats.rar(self.returns, rf=rf)

    def recovery_factor(self, prepare_returns: bool = True):
        return qs.stats.recovery_factor(
            self.returns, prepare_returns=prepare_returns)

    def risk_of_ruin(self, prepare_returns: bool = True):
        return qs.stats.risk_of_ruin(
            self.returns, prepare_returns=prepare_returns)

    def risk_return_ratio(self, prepare_returns: bool = True):
        return qs.stats.risk_return_ratio(
            self.returns, prepare_returns=prepare_returns)

    def ror(self):
        return qs.stats.ror(self.returns)

    def rolling_sortino(self):
        return qs.stats.rolling_sortino(
            self.returns, rolling_periods=182.5, periods=365, annualize=True)

    def serenity_index(self, rf: float = 0.0):
        return qs.stats.serenity_index(self.returns, rf=rf)

    def sharpe(self):
        return qs.stats.sharpe(self.returns, periods=365, annualize=True)

    def skew(self, prepare_returns: bool = True):
        return qs.stats.skew(self.returns, prepare_returns=prepare_returns)

    def sortino(self):
        return qs.stats.sortino(self.returns, periods=365, annualize=True)

    def total_pnl(self):
        return qs.stats.comp(self.returns) + 1

    def ulcer_index(self, rf: float = 0.0):
        return qs.stats.ulcer_index(self.returns, rf=rf)

    def ulcer_performance_index(self, rf: float = 0.0):
        return qs.stats.ulcer_performance_index(self.returns, rf=rf)

    def upi(self, rf: float = 0.0):
        return qs.stats.upi(self.returns, rf=rf)

    def value_at_risk(
        self,
        sigma: float = 1,
        confidence: float = 0.95,
        prepare_returns: bool = True,
    ):

        return value_at_risk(
            self.returns,
            sigma=sigma,
            confidence=confidence,
            prepare_returns=prepare_returns)

    def win_loss_ratio(self, prepare_returns: bool = True):
        return qs.stats.win_loss_ratio(
            self.returns, prepare_returns=prepare_returns)
