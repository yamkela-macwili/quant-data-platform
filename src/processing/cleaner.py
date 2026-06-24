"""Data cleaner — produce a consistent, analysis-ready DataFrame."""
import pandas as pd

from src.common.logger import get_logger

log = get_logger(__name__)

OHLCV_COLS = ["open", "high", "low", "close", "volume"]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Clean an OHLCV DataFrame.

    Steps:
    1. Drop rows where any OHLCV column is null.
    2. Drop duplicate timestamps (keep first occurrence).
    3. Sort by timestamp ascending.
    4. Reset index.

    Args:
        df: Raw OHLCV DataFrame.

    Returns:
        Cleaned DataFrame.
    """
    original_len = len(df)

    # Drop nulls in OHLCV columns
    df = df.dropna(subset=OHLCV_COLS)
    after_null = len(df)
    if original_len - after_null > 0:
        log.info(f"Dropped {original_len - after_null} rows with null OHLCV values")

    # Drop duplicate timestamps
    df = df.drop_duplicates(subset=["timestamp"], keep="first")
    after_dedup = len(df)
    if after_null - after_dedup > 0:
        log.info(f"Dropped {after_null - after_dedup} duplicate timestamp rows")

    # Sort ascending
    df = df.sort_values("timestamp").reset_index(drop=True)

    log.info(f"Clean complete — {len(df)} rows (from {original_len})")
    return df
