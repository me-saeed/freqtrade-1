# import ccxt
# import pandas as pd
# import os
# from datetime import datetime, timedelta

# # ---------------- CONFIG ----------------
# pairs = ["BTC/USDT", "ETH/USDT", "TRX/USDT", "SOL/USDT"]
# timeframe = "5m"
# exchange_name = "binance"
# data_dir = "user_data/data/binance"
# start_date = "2023-01-01"
# end_date = "2023-12-31"
# chunk_days = 15  # max chunk to avoid API limits
# # ----------------------------------------

# # Initialize exchange
# exchange = getattr(ccxt, exchange_name)({'enableRateLimit': True})

# # Create data directory if it doesn't exist
# os.makedirs(data_dir, exist_ok=True)

# # Convert string dates to datetime
# start = datetime.strptime(start_date, "%Y-%m-%d")
# end = datetime.strptime(end_date, "%Y-%m-%d")

# for pair in pairs:
#     print(f"Downloading {pair}...")
#     current_start = start
#     all_data = []

#     while current_start < end:
#         current_end = min(current_start + timedelta(days=chunk_days), end)
#         print(f"  Chunk: {current_start.date()} -> {current_end.date()}")

#         # Binance requires milliseconds timestamp
#         since = int(current_start.timestamp() * 1000)
#         ohlcv = []
#         while True:
#             # Fetch data
#             candles = exchange.fetch_ohlcv(pair, timeframe, since=since, limit=1000)
#             if not candles:
#                 break
#             ohlcv.extend(candles)
#             # Move 'since' to last candle + 1ms
#             since = candles[-1][0] + 1
#             # Stop if we passed current_end
#             if datetime.utcfromtimestamp(candles[-1][0] / 1000) >= current_end:
#                 break

#         # Convert to DataFrame
#         df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
#         df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
#         all_data.append(df)

#         current_start = current_end

#     # Concatenate all chunks and save CSV
#     final_df = pd.concat(all_data, ignore_index=True)
#     filename = os.path.join(data_dir, f"{pair.replace('/', '')}-{timeframe}.csv")
#     final_df.to_csv(filename, index=False)
#     print(f"Saved {len(final_df)} candles to {filename}\n")

# print("All done!")


import pandas as pd
from pathlib import Path

# folder with your feather files
data_folder = Path("user_data/data/binance")

# convert all .feather to .json
for f in data_folder.glob("*.feather"):
    df = pd.read_feather(f)
    # Freqtrade expects columns: date, open, high, low, close, volume
    df.to_json(f.with_suffix(".json"), orient="records", date_format="iso")
    print(f"Converted {f.name} -> {f.with_suffix('.json').name}")
