"""Data validation — check dataset integrity before processing."""
from dataclasses import dataclass, field

import pandas as pd

from src.common.logger import get_logger

log = get_logger(__name__)

OHLCV_COLS = ["open", "high", "low", "close", "volume"]


@dataclass
class ValidationReport:
    """Result of a validation run."""
    passed: bool
    issues: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        if self.passed:
            return "Validation passed — no issues found."
        return "Validation failed:\n" + "\n".join(f"  - {i}" for i in self.issues)


def validate(df: pd.DataFrame) -> ValidationReport:
    """Run integrity checks on an OHLCV DataFrame.

    Checks:
    - No missing values in OHLCV columns.
    - All prices (open, high, low, close) are strictly positive.
    - Volume is non-negative.
    - Timestamps are strictly ascending (no duplicates, correct ordering).
    - High >= Low for every candle.

    Args:
        df: DataFrame with columns [timestamp, open, high, low, close, volume].

    Returns:
        ValidationReport describing all issues found.
    """
    issues: list[str] = []

    # Missing values
    null_counts = df[OHLCV_COLS].isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            issues.append(f"Missing values in '{col}': {count} rows")

    # Price positivity
    for col in ["open", "high", "low", "close"]:
        if col in df.columns:
            bad = (df[col] <= 0).sum()
            if bad > 0:
                issues.append(f"Non-positive values in '{col}': {bad} rows")

    # Volume non-negative
    if "volume" in df.columns:
        bad_vol = (df["volume"] < 0).sum()
        if bad_vol > 0:
            issues.append(f"Negative volume values: {bad_vol} rows")

    # High >= Low
    if "high" in df.columns and "low" in df.columns:
        bad_hl = (df["high"] < df["low"]).sum()
        if bad_hl > 0:
            issues.append(f"high < low in {bad_hl} rows")

    # Timestamp ordering
    if "timestamp" in df.columns:
        ts = df["timestamp"]
        if ts.duplicated().any():
            issues.append(f"Duplicate timestamps: {ts.duplicated().sum()} rows")
        if not ts.is_monotonic_increasing:
            issues.append("Timestamps are not strictly ascending")

    report = ValidationReport(passed=len(issues) == 0, issues=issues)
    if report.passed:
        log.info("Validation passed")
    else:
        for issue in issues:
            log.warning(f"Validation issue: {issue}")
    return report
