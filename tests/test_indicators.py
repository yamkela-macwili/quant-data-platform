"""Tests for technical indicators — SMA, EMA, RSI."""
import pandas as pd
import pytest

from src.indicators.sma import compute_sma
from src.indicators.ema import compute_ema
from src.indicators.rsi import compute_rsi
from src.indicators.pipeline import run as run_pipeline


def make_df(closes: list[float]) -> pd.DataFrame:
    """Build a minimal DataFrame with the given close prices."""
    return pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=len(closes), freq="1h", tz="UTC"),
        "open":   closes,
        "high":   [c * 1.01 for c in closes],
        "low":    [c * 0.99 for c in closes],
        "close":  closes,
        "volume": [1000.0] * len(closes),
    })


class TestSMA:
    def test_sma_length(self):
        df = make_df(list(range(1, 11)))
        result = compute_sma(df, period=3)
        assert len(result) == 10

    def test_sma_known_value(self):
        # Close prices: 1,2,3,4,5 → SMA(3) at index 2 = (1+2+3)/3 = 2.0
        df = make_df([1.0, 2.0, 3.0, 4.0, 5.0])
        result = compute_sma(df, period=3)
        assert result.iloc[2] == pytest.approx(2.0)
        assert result.iloc[4] == pytest.approx(4.0)

    def test_sma_first_values_nan(self):
        df = make_df([1.0, 2.0, 3.0, 4.0, 5.0])
        result = compute_sma(df, period=3)
        assert pd.isna(result.iloc[0])
        assert pd.isna(result.iloc[1])

    def test_sma_name(self):
        df = make_df([1.0, 2.0, 3.0])
        result = compute_sma(df, period=3)
        assert result.name == "sma_3"


class TestEMA:
    def test_ema_length(self):
        df = make_df(list(range(1, 21)))
        result = compute_ema(df, period=5)
        assert len(result) == 20

    def test_ema_first_value_equals_close(self):
        # With adjust=False, the first EMA value equals the first close price
        df = make_df([100.0, 110.0, 120.0])
        result = compute_ema(df, period=2)
        assert result.iloc[0] == pytest.approx(100.0)

    def test_ema_name(self):
        df = make_df([1.0, 2.0, 3.0])
        result = compute_ema(df, period=5)
        assert result.name == "ema_5"


class TestRSI:
    def test_rsi_range(self):
        # RSI values must be between 0 and 100
        df = make_df([float(i) for i in range(1, 31)])
        result = compute_rsi(df, period=14)
        valid = result.dropna()
        assert (valid >= 0).all() and (valid <= 100).all()

    def test_rsi_rising_market(self):
        # Consistently rising prices → RSI should be high (>50)
        # Use realistic scale prices so EWM doesn't collapse to NaN
        prices = [10000.0 + i * 100 for i in range(30)]
        df = make_df(prices)
        result = compute_rsi(df, period=14)
        valid = result.dropna()
        assert len(valid) > 0, "RSI produced only NaN values"
        assert valid.iloc[-1] > 50

    def test_rsi_falling_market(self):
        # Consistently falling prices → RSI should be low (<50)
        df = make_df([float(i) for i in range(30, 0, -1)])
        result = compute_rsi(df, period=14)
        assert result.iloc[-1] < 50

    def test_rsi_name(self):
        df = make_df([1.0, 2.0, 3.0])
        result = compute_rsi(df, period=14)
        assert result.name == "rsi_14"


class TestIndicatorPipeline:
    def test_pipeline_adds_all_columns(self):
        df = make_df([float(i) for i in range(1, 60)])
        result = run_pipeline(df)
        for col in ["sma_20", "sma_50", "ema_12", "ema_26", "rsi_14"]:
            assert col in result.columns

    def test_pipeline_does_not_modify_original(self):
        df = make_df([float(i) for i in range(1, 60)])
        _ = run_pipeline(df)
        assert "sma_20" not in df.columns
