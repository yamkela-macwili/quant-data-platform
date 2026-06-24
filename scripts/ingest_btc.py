"""Phase 1 — Download raw BTCUSDT 1h data from Binance and save to disk.

Usage:
    python scripts/ingest_btc.py
"""
from datetime import datetime, timezone, timedelta
from pathlib import Path

from src.ingestion.binance import fetch_ohlcv
from src.common.logger import get_logger

log = get_logger(__name__)

SYMBOL = "BTCUSDT"
INTERVAL = "1h"
RAW_DIR = Path("data/raw")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    end_dt = datetime.now(timezone.utc)
    start_dt = end_dt - timedelta(days=365)

    log.info(f"Starting ingestion for {SYMBOL} {INTERVAL}")
    df = fetch_ohlcv(symbol=SYMBOL, interval=INTERVAL, start_dt=start_dt, end_dt=end_dt)

    if df.empty:
        log.error("No data returned — check network connection or symbol name.")
        return

    out_path = RAW_DIR / f"{SYMBOL}_{INTERVAL}.parquet"
    df.to_parquet(out_path, index=False)
    log.info(f"Saved {len(df)} rows to {out_path}")


if __name__ == "__main__":
    main()
