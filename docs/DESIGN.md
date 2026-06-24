# Design - Quant Data Platform

## Architecture

```mermaid
flowchart TD

    API["Binance Public REST API"]

    subgraph Ingestion
        ING["src/ingestion/<br/>(fetch OHLCV)"]
        RAW["data/raw/*.parquet"]
    end

    subgraph Processing
        PROC["src/processing/<br/>(clean + validate)"]
        CLEAN["data/processed/*.parquet"]
    end

    subgraph FeatureEngineering
        FEAT["src/indicators/<br/>(SMA, EMA, RSI)"]
        FEATURED["data/processed/*_featured.parquet"]
    end

    subgraph Analytics
        ANALYTICS["src/analytics/<br/>(returns, charts, reports)"]
        REPORTS["reports/"]
    end

    API --> ING
    ING --> RAW
    RAW --> PROC
    PROC --> CLEAN
    CLEAN --> FEAT
    FEAT --> FEATURED
    FEATURED --> ANALYTICS
    ANALYTICS --> REPORTS
```

## Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `src/ingestion/binance.py` | Paginated fetch from Binance `/api/v3/klines` |
| `src/processing/cleaner.py` | Dedup, null-drop, sort |
| `src/processing/validator.py` | Data integrity checks |
| `src/indicators/pipeline.py` | Orchestrate SMA/EMA/RSI |
| `src/analytics/charts.py` | Matplotlib chart output |
| `src/analytics/returns.py` | Returns and volatility |
| `src/analytics/summary.py` | Top moves, indicator snapshots |

## Data Storage

- **Format:** Parquet (via `pyarrow`)
- **Raw:** `data/raw/`
- **Processed:** `data/processed/`
- **Reports:** `reports/`


