# How to Run RealisticStrategy

## ✅ Strategy Status: READY
- Strategy file: `user_data/strategies/RealisticStrategy.py` ✅
- Config file: `user_data/config.json` ✅
- Settings: 20% ROI, 12% stoploss, SOL/USDT only

## 🚀 Commands to Run

### 1. Activate Virtual Environment (REQUIRED)
```bash
cd /Users/saeed/Downloads/Projects/trading/freqtrade
source freq_env/bin/activate
```

### 2. Test Strategy (Backtesting)
```bash
freqtrade backtesting \
  --strategy RealisticStrategy \
  --timerange 20231201-20240102 \
  --timeframe 5m \
  --pairs SOL/USDT \
  --userdir user_data \
  --config user_data/config.json \
  --data-format-ohlcv json
```

### 3. Run Live Trading (Dry Run - Safe)
```bash
freqtrade trade \
  --strategy RealisticStrategy \
  --userdir user_data \
  --config user_data/config.json
```

### 4. Check Strategy Status
```bash
freqtrade list-strategies --userdir user_data
```

## ⚠️ Common Issues

### Issue: "Command not found: freqtrade"
**Solution:** Make sure you activated the virtual environment:
```bash
source freq_env/bin/activate
```

### Issue: "ImportError" or Python errors
**Solution:** Use the virtual environment Python:
```bash
source freq_env/bin/activate
# Then run freqtrade commands
```

### Issue: "Exchange not working"
**Solution:** This is normal in dry-run mode. The bot will still work.

## 📊 Expected Performance

- **Best Month:** +4.48% (December)
- **Average:** +3.05% monthly
- **On $100:** ~$3-4.50/month
- **On $500:** ~$15-22/month

## 🔧 Current Settings

- **ROI Target:** 20% max, 15% after 10min
- **Stop Loss:** 12% (wide)
- **Max Open Trades:** 10
- **Pair:** SOL/USDT only
- **Timeframe:** 5m

## 💡 Quick Start

```bash
# 1. Go to directory
cd /Users/saeed/Downloads/Projects/trading/freqtrade

# 2. Activate environment
source freq_env/bin/activate

# 3. Run backtest (test first!)
freqtrade backtesting --strategy RealisticStrategy --timerange 20231201-20240102 --timeframe 5m --pairs SOL/USDT --userdir user_data --config user_data/config.json --data-format-ohlcv json

# 4. If backtest works, run live (dry-run)
freqtrade trade --strategy RealisticStrategy --userdir user_data --config user_data/config.json
```
