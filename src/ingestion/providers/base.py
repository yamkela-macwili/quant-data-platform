from binance.client import Client
import pandas as pd

client = Client()

symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1DAY

klines = client.get_historical_klines(
    symbol,
    interval,
    "1 Jan, 2020"
)


columns = [
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base", "taker_buy_quote", "ignore"
]

df = pd.DataFrame(klines, columns=columns)

# Convert timestamps
df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)

# Convert numeric columns
numeric_cols = [
    "open", "high", "low", "close", "volume",
    "quote_asset_volume", "taker_buy_base", "taker_buy_quote"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col])

df["number_of_trades"] = df["number_of_trades"].astype("int32")

# Remove unused column
df = df.drop(columns=["ignore"])

# Save as parquet
df.to_parquet(
    "src/storage/raw/BTCUSDT_1h_2024.parquet",
    engine="pyarrow",
    compression="snappy",
    index=False
)

print(df.head())
print(f"Saved {len(df)} rows")