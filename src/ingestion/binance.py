"""Binance public REST API client for historical OHLCV data.

No API key required — uses the public klines endpoint.
"""
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests
import pandas as pd

from src.common.logger import get_logger

log = get_logger(__name__)

BASE_URL = "https://api.binance.com"
KLINES_ENDPOINT = "/api/v3/klines"
MAX_LIMIT = 1000  # Binance max rows per request


def fetch_ohlcv(
    symbol: str,
    interval: str,
    start_dt: datetime,
    end_dt: Optional[datetime] = None,
) -> pd.DataFrame:
    """Download historical OHLCV candles from Binance.

    Args:
        symbol:    Trading pair, e.g. "BTCUSDT".
        interval:  Candle interval: "1h", "4h", "1d", etc.
        start_dt:  Start of the historical range (UTC).
        end_dt:    End of the historical range (UTC). Defaults to now.

    Returns:
        DataFrame with columns: timestamp, open, high, low, close, volume.
        timestamp is a UTC-aware datetime.
    """
    if end_dt is None:
        end_dt = datetime.now(timezone.utc)

    start_ms = int(start_dt.timestamp() * 1000)
    end_ms = int(end_dt.timestamp() * 1000)

    all_candles: list[list] = []
    current_ms = start_ms

    log.info(f"Fetching {symbol} {interval} from {start_dt.date()} to {end_dt.date()}")

    while current_ms < end_ms:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": current_ms,
            "endTime": end_ms,
            "limit": MAX_LIMIT,
        }

        response = requests.get(
            BASE_URL + KLINES_ENDPOINT,
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        batch = response.json()

        if not batch:
            break

        all_candles.extend(batch)
        # Next page starts after the last candle's close time
        current_ms = batch[-1][6] + 1  # index 6 = close time ms

        log.info(f"  Fetched {len(batch)} candles — total so far: {len(all_candles)}")

        if len(batch) < MAX_LIMIT:
            break

        time.sleep(0.2)  # polite rate limiting

    if not all_candles:
        log.warning(f"No data returned for {symbol} {interval}")
        return pd.DataFrame()

    df = _parse_klines(all_candles)
    log.info(f"Done — {len(df)} candles fetched for {symbol} {interval}")
    return df


def _parse_klines(raw: list[list]) -> pd.DataFrame:
    """Convert raw Binance klines response to a clean DataFrame."""
    df = pd.DataFrame(raw, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "trade_count",
        "taker_buy_base", "taker_buy_quote", "ignore",
    ])

    # Keep only the essential OHLCV columns
    df = df[["timestamp", "open", "high", "low", "close", "volume"]].copy()

    # Cast types
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    return df.reset_index(drop=True)
