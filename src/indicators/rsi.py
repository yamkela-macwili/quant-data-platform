"""Relative Strength Index (RSI)."""
import pandas as pd


def compute_rsi(df: pd.DataFrame, period: int = 14, column: str = "close") -> pd.Series:
    """Compute the Relative Strength Index using Wilder's smoothing method.

    Args:
        df:      DataFrame containing the target column.
        period:  Lookback period. Default is 14 (standard).
        column:  Column to compute RSI on. Defaults to 'close'.

    Returns:
        pd.Series of RSI values (0–100), named f'rsi_{period}'.
    """
    delta = df[column].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Wilder's smoothing (equivalent to EMA with alpha=1/period)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()

    # When avg_loss is zero (no losses), RS is infinite → RSI = 100
    # Fill zero avg_loss with NaN temporarily to avoid division errors,
    # then restore RSI = 100 where avg_loss was 0.
    zero_loss = avg_loss == 0.0
    safe_loss = avg_loss.replace(0.0, float("nan"))

    rs = avg_gain / safe_loss
    rsi = 100 - (100 / (1 + rs))
    rsi[zero_loss & (avg_gain > 0)] = 100.0  # pure uptrend → RSI 100

    return rsi.rename(f"rsi_{period}")
