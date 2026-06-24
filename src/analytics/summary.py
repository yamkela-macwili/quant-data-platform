"""Summary statistics — largest moves and indicator snapshots."""
import pandas as pd


def largest_moves(df: pd.DataFrame, returns: pd.Series, n: int = 5) -> pd.DataFrame:
    """Return the N largest daily up and down moves.

    Args:
        df:      Processed DataFrame (must include 'timestamp' and 'close').
        returns: Returns series aligned with df.
        n:       Number of top moves to return each direction.

    Returns:
        DataFrame with columns [timestamp, close, return] for top N + and - moves.
    """
    combined = df[["timestamp", "close"]].copy()
    combined["return"] = returns.values

    top_up = combined.nlargest(n, "return")
    top_down = combined.nsmallest(n, "return")

    result = pd.concat([top_up, top_down]).sort_values("return", ascending=False)
    return result.reset_index(drop=True)


def indicator_summary(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Produce a summary table for indicator columns.

    Args:
        df:      Featured DataFrame containing indicator columns.
        columns: List of column names to summarise.

    Returns:
        DataFrame with index=column names and columns [last, min, max, mean].
    """
    rows = []
    for col in columns:
        if col not in df.columns:
            continue
        series = df[col].dropna()
        rows.append({
            "indicator": col,
            "last": round(series.iloc[-1], 4) if len(series) > 0 else None,
            "min": round(series.min(), 4),
            "max": round(series.max(), 4),
            "mean": round(series.mean(), 4),
        })
    return pd.DataFrame(rows).set_index("indicator")
