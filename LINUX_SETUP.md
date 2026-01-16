# Linux Server Setup Guide

## Quick Start

### 1. Clone the Repository
```bash
git clone <YOUR_GIT_REPO_URL>
cd freqtrade
```

### 2. Setup Python Environment

#### Option A: Using Virtual Environment (Recommended)
```bash
# Install Python 3.9+ if not already installed
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip -y

# Create virtual environment
python3.9 -m venv freq_env

# Activate virtual environment
source freq_env/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Option B: Using Docker (Easiest - Recommended)
```bash
# Install Docker if not already installed
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker

# Run with Docker
docker-compose up -d
```

### 3. Configure the Bot

```bash
# Copy example config
cp user_data/config.example.json user_data/config.json

# Edit config with your API keys
nano user_data/config.json
# or
vim user_data/config.json
```

**Important:** Update these values in `config.json`:
- `exchange.key`: Your Binance API key
- `exchange.secret`: Your Binance API secret
- `telegram.token`: Your Telegram bot token (if using Telegram)
- `telegram.chat_id`: Your Telegram chat ID (if using Telegram)
- `api_server.jwt_secret_key`: Generate a random secret
- `api_server.ws_token`: Generate a random token
- `api_server.password`: Change to a secure password

### 4. Download Market Data (Optional but Recommended)

```bash
# Activate virtual environment first
source freq_env/bin/activate

# Download data for backtesting
freqtrade download-data --exchange binance --pairs SOL/USDT --timeframes 5m --days 30
```

### 5. Run the Bot

#### Using Virtual Environment:
```bash
source freq_env/bin/activate
freqtrade trade --strategy RealisticStrategy --userdir user_data --config user_data/config.json
```

#### Using Docker:
```bash
docker-compose run --rm freqtrade trade --strategy RealisticStrategy
```

### 6. Run in Background (Production)

#### Using systemd (Virtual Environment):
```bash
# Create systemd service file
sudo nano /etc/systemd/system/freqtrade.service
```

Add this content:
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

#### Using Docker (Background):
```bash
docker-compose up -d
docker-compose logs -f freqtrade
```

### 7. Monitor the Bot

```bash
# View logs (Virtual Environment)
tail -f ~/.freqtrade/logs/freqtrade.log

# View logs (Docker)
docker-compose logs -f freqtrade

# Check status
freqtrade status --userdir user_data --config user_data/config.json
```

## Troubleshooting

### Fix NumPy Compatibility (if needed)
```bash
source freq_env/bin/activate
pip install "numpy<2.0" --upgrade
```

### Fix cachetools Compatibility (if needed)
```bash
source freq_env/bin/activate
pip install "cachetools<5.0" --upgrade
```

### Check Strategy Syntax
```bash
source freq_env/bin/activate
python3 -m py_compile user_data/strategies/RealisticStrategy.py
```

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `user_data/config.json` to git (it's already in .gitignore)
- Keep your API keys and passwords secure
- Use strong passwords for API server
- Consider using environment variables for sensitive data

## Useful Commands

```bash
# Backtest
freqtrade backtesting --strategy RealisticStrategy --timerange 20240101-20240201

# List strategies
freqtrade list-strategies --userdir user_data

# Test pairlist
freqtrade test-pairlist --config user_data/config.json

# View trades
freqtrade show-trades --userdir user_data --config user_data/config.json
```
