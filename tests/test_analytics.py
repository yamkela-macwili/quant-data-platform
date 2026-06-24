"""Tests for analytics — returns and volatility."""
import pandas as pd
import pytest

from src.analytics.returns import daily_returns, annualized_volatility
from src.analytics.summary import largest_moves, indicator_summary


def make_df(closes: list[float]) -> pd.DataFrame:
    return pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=len(closes), freq="1D", tz="UTC"),
        "close": closes,
    })


class TestReturns:
    def test_returns_length(self):
        df = make_df([100.0, 110.0, 121.0])
        result = daily_returns(df)
        assert len(result) == 3

    def test_first_return_is_nan(self):
        df = make_df([100.0, 110.0, 121.0])
        result = daily_returns(df)
        assert pd.isna(result.iloc[0])

    def test_known_return_values(self):
        # 100 → 110 = +10%, 110 → 121 = +10%
        df = make_df([100.0, 110.0, 121.0])
        result = daily_returns(df)
        assert result.iloc[1] == pytest.approx(0.10)
        assert result.iloc[2] == pytest.approx(0.10)

    def test_volatility_flat_market(self):
        # Flat market → zero returns → zero volatility
        df = make_df([100.0] * 10)
        returns = daily_returns(df)
        vol = annualized_volatility(returns.dropna(), periods_per_year=365)
        assert vol == pytest.approx(0.0)

    def test_volatility_positive(self):
        df = make_df([100.0, 90.0, 110.0, 95.0, 105.0])
        returns = daily_returns(df)
        vol = annualized_volatility(returns.dropna(), periods_per_year=365)
        assert vol > 0


class TestSummary:
    def test_largest_moves_count(self):
        df = make_df([100.0, 110.0, 90.0, 120.0, 85.0, 130.0])
        returns = daily_returns(df)
        result = largest_moves(df, returns, n=2)
        # 2 up + 2 down = 4 rows
        assert len(result) == 4

    def test_indicator_summary_columns(self):
        df = pd.DataFrame({
            "sma_20": [1.0, 2.0, 3.0],
            "rsi_14": [40.0, 50.0, 60.0],
        })
        result = indicator_summary(df, ["sma_20", "rsi_14"])
        assert "last" in result.columns
        assert "min" in result.columns
        assert "max" in result.columns
        assert "mean" in result.columns
        assert len(result) == 2

    def test_indicator_summary_skips_missing_columns(self):
        df = pd.DataFrame({"sma_20": [1.0, 2.0]})
        result = indicator_summary(df, ["sma_20", "nonexistent"])
        assert len(result) == 1
