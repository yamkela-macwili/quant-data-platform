"""Exponential Moving Average (EMA)."""
import pandas as pd


def compute_ema(df: pd.DataFrame, period: int, column: str = "close") -> pd.Series:
    """Compute the Exponential Moving Average.

    Args:
        df:      DataFrame containing the target column.
        period:  Span (smoothing window) for the EMA.
        column:  Column to compute EMA on. Defaults to 'close'.

    Returns:
        pd.Series of EMA values, named f'ema_{period}'.
    """
    return (
        df[column]
        .ewm(span=period, adjust=False)
        .mean()
        .rename(f"ema_{period}")
    )
