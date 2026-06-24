"""Indicator pipeline — attach all indicators to a processed DataFrame."""
import pandas as pd

from src.indicators.sma import compute_sma
from src.indicators.ema import compute_ema
from src.indicators.rsi import compute_rsi
from src.common.logger import get_logger

log = get_logger(__name__)


def run(df: pd.DataFrame) -> pd.DataFrame:
    """Compute and attach all indicators to the DataFrame.

    Adds columns:
        sma_20, sma_50, ema_12, ema_26, rsi_14

    Args:
        df: Cleaned OHLCV DataFrame.

    Returns:
        DataFrame with additional indicator columns.
    """
    df = df.copy()

    df["sma_20"] = compute_sma(df, period=20)
    df["sma_50"] = compute_sma(df, period=50)
    df["ema_12"] = compute_ema(df, period=12)
    df["ema_26"] = compute_ema(df, period=26)
    df["rsi_14"] = compute_rsi(df, period=14)

    log.info("Indicators computed: sma_20, sma_50, ema_12, ema_26, rsi_14")
    return df
