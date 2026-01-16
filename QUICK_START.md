# Quick Start - Clone and Run

## On Linux Server:

```bash
# 1. Clone the repository
git clone YOUR_REPO_URL
cd freqtrade

# 2. Create virtual environment
python3 -m venv freq_env
source freq_env/bin/activate

# 3. Install freqtrade and fix dependencies
pip install freqtrade
pip install "numpy<2.0" --upgrade
pip install "cachetools<5.0" --upgrade

# 4. Run the bot (everything is already configured!)
freqtrade trade --strategy RealisticStrategy --userdir user_data --config user_data/config.json
```

## Run in Background:

### Using screen:
```bash
screen -S freqtrade
source freq_env/bin/activate
freqtrade trade --strategy RealisticStrategy --userdir user_data --config user_data/config.json
# Press Ctrl+A then D to detach
```

### Using tmux:
```bash
tmux new -s freqtrade
source freq_env/bin/activate
freqtrade trade --strategy RealisticStrategy --userdir user_data --config user_data/config.json
# Press Ctrl+B then D to detach
```

That's it! Everything is pre-configured and ready to run.
