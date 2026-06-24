"""Full pipeline - Phases 1 through 4.

Runs the complete end-to-end workflow:
  Phase 1: Ingest raw data from Binance
  Phase 2: Validate and clean
  Phase 3: Compute technical indicators
  Phase 4: Generate analytics and charts

"""
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from src.ingestion.binance import fetch_ohlcv
from src.processing.cleaner import clean
from src.processing.validator import validate
from src.indicators import pipeline as indicator_pipeline
from src.analytics.returns import daily_returns, annualized_volatility
from src.analytics.summary import largest_moves, indicator_summary
from src.analytics import charts
from src.common.logger import get_logger

log = get_logger(__name__)

SYMBOL = "BTCUSDT"
INTERVAL = "1h"
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
REPORTS_DIR = Path("reports")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # ── Phase 1: Ingestion ───────────────────────────────────────────────────
    raw_path = RAW_DIR / f"{SYMBOL}_{INTERVAL}.parquet"

    if raw_path.exists():
        import pandas as pd
        log.info(f"Raw file already exists - loading from {raw_path}")
        df_raw = pd.read_parquet(raw_path)
    else:
        log.info("Phase 1 - Fetching raw data from Binance")
        end_dt = datetime.now(timezone.utc)
        start_dt = end_dt - timedelta(days=365)
        df_raw = fetch_ohlcv(symbol=SYMBOL, interval=INTERVAL, start_dt=start_dt, end_dt=end_dt)

        if df_raw.empty:
            log.error("Ingestion returned no data - aborting.")
            sys.exit(1)

        df_raw.to_parquet(raw_path, index=False)
        log.info(f"Phase 1 complete - {len(df_raw)} rows saved to {raw_path}")

    # ── Phase 2: Validate & Clean ────────────────────────────────────────────
    log.info("Phase 2 - Validating raw data")
    report = validate(df_raw)
    log.info(str(report))

    df_clean = clean(df_raw)
    processed_path = PROCESSED_DIR / f"{SYMBOL}_{INTERVAL}.parquet"
    df_clean.to_parquet(processed_path, index=False)
    log.info(f"Phase 2 complete - {len(df_clean)} rows saved to {processed_path}")

    # ── Phase 3: Feature Engineering ─────────────────────────────────────────
    log.info("Phase 3 - Computing indicators")
    df_featured = indicator_pipeline.run(df_clean)
    featured_path = PROCESSED_DIR / f"{SYMBOL}_{INTERVAL}_featured.parquet"
    df_featured.to_parquet(featured_path, index=False)
    log.info(f"Phase 3 complete - featured data saved to {featured_path}")

    # ── Phase 4: Analytics & Reports ─────────────────────────────────────────
    log.info("Phase 4 - Generating analytics and charts")

    returns = daily_returns(df_featured)
    vol = annualized_volatility(returns)
    log.info(f"Annualized volatility: {vol:.2%}")

    moves = largest_moves(df_featured, returns, n=5)
    moves.to_csv(REPORTS_DIR / "largest_moves.csv", index=False)
    log.info(f"Top price moves saved to {REPORTS_DIR / 'largest_moves.csv'}")

    # TODO: Add more indicators, like ATR, Bollinger Bands, MACD, etc.
    ind_summary = indicator_summary(df_featured, ["sma_20", "sma_50", "ema_12", "ema_26", "rsi_14"])
    ind_summary.to_csv(REPORTS_DIR / "indicator_summary.csv")
    log.info(f"Indicator summary saved to {REPORTS_DIR / 'indicator_summary.csv'}")
    print("\n── Indicator Summary ──────────────────")
    print(ind_summary.to_string())

    # TODO: Add more charts, like ATR, Bollinger Bands, MACD, etc.
    # TODO: Add more chart like correlation matrix, etc.
    chart1 = charts.price_with_mas(df_featured, REPORTS_DIR)
    log.info(f"Chart saved: {chart1}")
    chart2 = charts.rsi_chart(df_featured, REPORTS_DIR)
    log.info(f"Chart saved: {chart2}")

    log.info("Pipeline complete ✓")
    print(f"\nOutputs:")
    print(f"  Raw data:       {raw_path}")
    print(f"  Processed:      {processed_path}")
    print(f"  Featured:       {featured_path}")
    print(f"  Charts:         {REPORTS_DIR}/price_sma_ema.png, {REPORTS_DIR}/rsi.png")
    print(f"  Reports:        {REPORTS_DIR}/largest_moves.csv, {REPORTS_DIR}/indicator_summary.csv")


if __name__ == "__main__":
    main()
