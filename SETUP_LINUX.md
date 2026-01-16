# Setup Guide for Linux Server

## Quick Start

### 1. Clone the Repository
```bash
git clone YOUR_REPO_URL
cd freqtrade
```

### 2. Create Virtual Environment
```bash
python3 -m venv freq_env
source freq_env/bin/activate
```

### 3. Install Dependencies
```bash
# Install freqtrade
pip install freqtrade

# Fix compatibility issues for older freqtrade versions
pip install "numpy<2.0" --upgrade
pip install "cachetools<5.0" --upgrade
```

### 4. Setup Configuration
```bash
# Copy example config
cp user_data/config.example.json user_data/config.json

# Edit config with your API keys
nano user_data/config.json
# Or use vim: vim user_data/config.json
```

**Important:** Update these in `config.json`:
- `exchange.key` - Your Binance API key
- `exchange.secret` - Your Binance API secret
- `telegram.token` - Your Telegram bot token
- `telegram.chat_id` - Your Telegram chat ID
- `api_server.jwt_secret_key` - Generate random string
- `api_server.ws_token` - Generate random string
- `api_server.password` - Change to secure password

### 5. Run the Bot

#### Option A: Direct Python (Recommended for Linux)
```bash
source freq_env/bin/activate
freqtrade trade --strategy RealisticStrategy --userdir user_data --config user_data/config.json
```

#### Option B: Docker
```bash
docker-compose up -d
```

### 6. Run in Background (Using screen or tmux)

#### Using screen:
```bash
screen -S freqtrade
source freq_env/bin/activate
freqtrade trade --strategy RealisticStrategy --userdir user_data --config user_data/config.json
# Press Ctrl+A then D to detach
# Reattach: screen -r freqtrade
```

#### Using tmux:
```bash
tmux new -s freqtrade
source freq_env/bin/activate
freqtrade trade --strategy RealisticStrategy --userdir user_data --config user_data/config.json
# Press Ctrl+B then D to detach
# Reattach: tmux attach -t freqtrade
```

#### Using systemd (for permanent service):
Create `/etc/systemd/system/freqtrade.service`:
```ini
[Unit]
Description=Freqtrade Trading Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/freqtrade
Environment="PATH=/path/to/freqtrade/freq_env/bin"
ExecStart=/path/to/freqtrade/freq_env/bin/freqtrade trade --strategy RealisticStrategy --userdir user_data --config user_data/config.json
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable freqtrade
sudo systemctl start freqtrade
sudo systemctl status freqtrade
```

## Troubleshooting

### If you get numpy/cachetools errors:
```bash
pip install "numpy<2.0" --upgrade
pip install "cachetools<5.0" --upgrade
```

### Check if bot is running:
```bash
ps aux | grep freqtrade
```

### View logs:
```bash
# If using systemd
sudo journalctl -u freqtrade -f

# If running directly, logs go to console
```

## Strategy Details

- **Strategy Name:** RealisticStrategy
- **Timeframe:** 5m
- **Stoploss:** -12%
- **ROI Targets:** 20% immediate, scaling down to 5% after 2 hours
- **Trading Pair:** SOL/USDT
- **Stake Amount:** 100 USDT per trade
- **Max Open Trades:** 10

## Notes

- The bot runs in `dry_run` mode by default (simulated trading)
- Set `"dry_run": false` in config.json for live trading
- Make sure you have sufficient balance on your exchange
- Monitor the bot regularly, especially when starting
