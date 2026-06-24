# Quant Data Platform

A portfolio data engineering project demonstrating a clean, reproducible market data pipeline.  
Fetches BTCUSDT historical data from Binance, validates it, computes technical indicators, and produces charts and summary reports - all from the command line.

---

## Quickstart

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
make install

# 3. Run the full pipeline
make pipeline
```

This downloads the last 12 months of BTCUSDT 1h candles from Binance, processes them, and saves charts and reports to `reports/`.

---

## Pipeline Phases

| Phase | Command | What it does |
|-------|---------|--------------|
| 1 | `make ingest` | Download raw BTCUSDT 1h candles → `data/raw/` |
| 1–4 | `make pipeline` | Full pipeline: ingest → clean → indicators → charts |

---

## Project Structure

```
quant-data-platform/
├── src/
│   ├── ingestion/       # Binance REST API client
│   ├── processing/      # Data cleaning and validation
│   ├── indicators/      # SMA, EMA, RSI calculations
│   ├── analytics/       # Returns, volatility, charts
│   └── common/          # Shared logger
│
├── scripts/
│   ├── ingest_btc.py    # Phase 1: download raw data
│   └── run_pipeline.py  # Phases 1–4: full workflow
│
├── data/
│   ├── raw/             # Raw Parquet files from Binance
│   └── processed/       # Cleaned + featured datasets
│
├── reports/             # Generated charts and CSVs
├── tests/               # pytest test suite
├── requirements.txt
└── Makefile
```

---

## Output Files

After running `make pipeline`:

| File | Description |
|------|-------------|
| `data/raw/BTCUSDT_1h.parquet` | Raw OHLCV from Binance |
| `data/processed/BTCUSDT_1h.parquet` | Cleaned dataset |
| `data/processed/BTCUSDT_1h_featured.parquet` | With SMA, EMA, RSI columns |
| `reports/price_sma_ema.png` | Price chart with MA overlays |
| `reports/rsi.png` | RSI indicator chart |
| `reports/largest_moves.csv` | Top 5 up/down days |
| `reports/indicator_summary.csv` | Last, min, max, mean of each indicator |

---

## Running Tests

```bash
make test
```

---

## Technology Stack

| Concern | Library |
|---------|---------|
| Data fetching | `requests` (Binance public REST API) |
| Data processing | `pandas`, `numpy` |
| Storage | `pyarrow` (Parquet) |
| Visualization | `matplotlib` |
| Testing | `pytest` |

--- 
## Future Ideas (not committed)
- [ ] Additional symbols (ETHUSDT, etc.)
- [ ] Additional intervals (4h, 1d)
- [ ] Bollinger Bands, MACD
- [ ] Jupyter notebook for exploration
---
NOTE: No API key required - all data comes from Binance's public endpoints.
---