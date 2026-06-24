"""Tests for data processing — cleaner and validator."""
import pandas as pd
import pytest

from src.processing.cleaner import clean
from src.processing.validator import validate


def make_df(**kwargs) -> pd.DataFrame:
    """Helper to build a minimal OHLCV DataFrame."""
    base = {
        "timestamp": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"], utc=True),
        "open":   [100.0, 110.0, 105.0],
        "high":   [115.0, 120.0, 112.0],
        "low":    [ 95.0, 108.0, 100.0],
        "close":  [110.0, 105.0, 108.0],
        "volume": [500.0, 600.0, 550.0],
    }
    base.update(kwargs)
    return pd.DataFrame(base)


# ─── cleaner tests ────────────────────────────────────────────────────────────

class TestCleaner:
    def test_drops_null_rows(self):
        df = make_df()
        df.loc[1, "close"] = None
        result = clean(df)
        assert len(result) == 2

    def test_drops_duplicate_timestamps(self):
        df = make_df()
        df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
        result = clean(df)
        assert len(result) == 3

    def test_sorts_ascending(self):
        df = make_df()
        df = df.iloc[::-1].reset_index(drop=True)  # reverse order
        result = clean(df)
        assert result["timestamp"].is_monotonic_increasing

    def test_clean_data_unchanged_length(self):
        df = make_df()
        result = clean(df)
        assert len(result) == 3


# ─── validator tests ──────────────────────────────────────────────────────────

class TestValidator:
    def test_valid_data_passes(self):
        report = validate(make_df())
        assert report.passed

    def test_negative_price_fails(self):
        df = make_df(close=[-1.0, 100.0, 100.0])
        report = validate(df)
        assert not report.passed
        assert any("close" in issue for issue in report.issues)

    def test_negative_volume_fails(self):
        df = make_df(volume=[-10.0, 500.0, 500.0])
        report = validate(df)
        assert not report.passed
        assert any("volume" in issue for issue in report.issues)

    def test_duplicate_timestamps_fail(self):
        df = make_df()
        df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
        report = validate(df)
        assert not report.passed
        assert any("Duplicate" in issue for issue in report.issues)

    def test_high_less_than_low_fails(self):
        df = make_df(high=[50.0, 110.0, 112.0], low=[95.0, 108.0, 100.0])
        report = validate(df)
        assert not report.passed
        assert any("high < low" in issue for issue in report.issues)

    def test_null_values_fail(self):
        df = make_df()
        df.loc[0, "open"] = None
        report = validate(df)
        assert not report.passed
