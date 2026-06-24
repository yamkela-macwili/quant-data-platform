"""Canonical data models for market data."""
from typing import TypedDict


class Candle(TypedDict):
    """A single OHLCV candle."""
    timestamp: int   # Unix timestamp in milliseconds (open time)
    open: float
    high: float
    low: float
    close: float
    volume: float
