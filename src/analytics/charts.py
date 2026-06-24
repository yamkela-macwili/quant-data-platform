"""Matplotlib chart generation — save to reports/."""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def price_with_mas(df: pd.DataFrame, output_dir: Path) -> Path:
    """Plot price history with SMA and EMA overlays.

    Args:
        df:         Featured DataFrame with close, sma_20, sma_50, ema_12, ema_26.
        output_dir: Directory to save the chart.

    Returns:
        Path to the saved chart file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "price_sma_ema.png"

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(df["timestamp"], df["close"], label="Close", linewidth=1.2, color="#1f77b4")

    if "sma_20" in df.columns:
        ax.plot(df["timestamp"], df["sma_20"], label="SMA 20", linewidth=1.0, linestyle="--", color="#ff7f0e")
    if "sma_50" in df.columns:
        ax.plot(df["timestamp"], df["sma_50"], label="SMA 50", linewidth=1.0, linestyle="--", color="#2ca02c")
    if "ema_12" in df.columns:
        ax.plot(df["timestamp"], df["ema_12"], label="EMA 12", linewidth=1.0, linestyle=":", color="#d62728")
    if "ema_26" in df.columns:
        ax.plot(df["timestamp"], df["ema_26"], label="EMA 26", linewidth=1.0, linestyle=":", color="#9467bd")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()

    ax.set_title("BTCUSDT — Price with SMA & EMA Overlays", fontsize=14)
    ax.set_ylabel("Price (USDT)")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

    return out_path


def rsi_chart(df: pd.DataFrame, output_dir: Path) -> Path:
    """Plot RSI with overbought/oversold reference lines.

    Args:
        df:         Featured DataFrame with rsi_14 column.
        output_dir: Directory to save the chart.

    Returns:
        Path to the saved chart file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "rsi.png"

    if "rsi_14" not in df.columns:
        raise ValueError("DataFrame does not contain 'rsi_14' column.")

    fig, ax = plt.subplots(figsize=(14, 4))

    ax.plot(df["timestamp"], df["rsi_14"], label="RSI 14", linewidth=1.0, color="#1f77b4")
    ax.axhline(70, color="#d62728", linestyle="--", linewidth=0.8, label="Overbought (70)")
    ax.axhline(30, color="#2ca02c", linestyle="--", linewidth=0.8, label="Oversold (30)")
    ax.fill_between(df["timestamp"], df["rsi_14"], 70, where=(df["rsi_14"] >= 70), alpha=0.15, color="#d62728")
    ax.fill_between(df["timestamp"], df["rsi_14"], 30, where=(df["rsi_14"] <= 30), alpha=0.15, color="#2ca02c")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()

    ax.set_title("BTCUSDT — RSI (14)", fontsize=14)
    ax.set_ylabel("RSI")
    ax.set_ylim(0, 100)
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

    return out_path
