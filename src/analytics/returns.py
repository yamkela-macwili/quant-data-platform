"""Returns and volatility calculations."""
import numpy as np
import pandas as pd


def daily_returns(df: pd.DataFrame, column: str = "close") -> pd.Series:
    """Compute percentage change (daily returns).

    Args:
        df:     DataFrame with price column.
        column: Price column to use. Defaults to 'close'.

    Returns:
        pd.Series of returns as decimals (e.g. 0.02 = 2%).
    """
    return df[column].pct_change().rename("returns")


def annualized_volatility(returns: pd.Series, periods_per_year: int = 8760) -> float:
    """Compute annualized volatility from a returns series.

    Args:
        returns:          Series of period returns.
        periods_per_year: Number of periods in a year. Default 8760 for hourly data.

    Returns:
        Annualized volatility as a decimal (e.g. 0.65 = 65%).
    """
    return float(returns.std() * np.sqrt(periods_per_year))
