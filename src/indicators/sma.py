"""Simple Moving Average (SMA)."""
import pandas as pd


def compute_sma(df: pd.DataFrame, period: int, column: str = "close") -> pd.Series:
    """Compute the Simple Moving Average.

    Args:
        df:      DataFrame containing the target column.
        period:  Lookback window size.
        column:  Column to compute SMA on. Defaults to 'close'.

    Returns:
        pd.Series of SMA values, named f'sma_{period}'.
    """
    return df[column].rolling(window=period).mean().rename(f"sma_{period}")
