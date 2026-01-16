from freqtrade.strategy.interface import IStrategy
import pandas as pd
import talib.abstract as ta
import numpy as np

class RealisticStrategy(IStrategy):
    """
    ULTRA-AGGRESSIVE Strategy for 15% Monthly Profit:
    - High ROI targets (5-10% per trade)
    - Wide stoploss (OK with losses)
    - Relaxed entry filters for more trades
    - Focus on SOL/USDT (best performer)
    """

    # Timeframe for candlestick data
    timeframe = '5m'

    # Stoploss - VERY WIDE for extreme aggressive trading (OK with losses)
    stoploss = -0.12  # max 12% loss - extreme aggressive mode

    # Minimal ROI - REALISTIC targets for regular market movements
    minimal_roi = {
        "0": 0.020,   # 2.0% profit target immediately
        "5": 0.015,   # 1.5% after 5 minutes
        "10": 0.012,  # 1.2% after 10 minutes
        "20": 0.010,  # 1.0% after 20 minutes
        "30": 0.008,  # 0.8% after 30 minutes
        "60": 0.006,  # 0.6% after 1 hour
        "120": 0.005  # 0.5% after 2 hours (minimum - will close at 0.5%+)
    }

    # Disable sell signal - let ROI and stoploss handle exits
    use_sell_signal = False
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    # Enable trailing stop to lock in profits
    trailing_stop = True
    trailing_stop_positive = 0.020  # Start trailing after 2.0% profit
    trailing_stop_positive_offset = 0.030  # Trail by 3.0% (let winners run)
    trailing_only_offset_is_reached = True
    
    # Custom stoploss - aggressive, let big winners run
    use_custom_stoploss = True
    
    # Order types - required for freqtrade 2021.8
    order_types = {
        "entry": "market",
        "exit": "market",
        "stoploss": "market",
        "stoploss_on_exchange": False
    }
    
    # Order time in force - required for freqtrade 2021.8
    order_time_in_force = {
        "entry": "GTC",
        "exit": "GTC"
    }
    
    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: 'datetime',
                       current_rate: float, current_profit: float, **kwargs) -> float:
        """
        Custom stoploss logic - aggressive, let big winners run
        """
        # If we're in very good profit, use tighter stoploss to lock in gains
        if current_profit > 0.080:  # If profit > 8.0%
            return -0.020  # 2.0% stoploss when in very strong profit
        elif current_profit > 0.050:  # If profit > 5.0%
            return -0.030  # 3.0% stoploss when in strong profit
        elif current_profit > 0.030:  # If profit > 3.0%
            return -0.040  # 4.0% stoploss when in profit
        # Default wide stoploss when at loss (let it run)
        return self.stoploss

    # Number of candles needed before signals
    startup_candle_count = 50

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        EMA, RSI, MACD and Volume indicators
        """
        # Better EMA periods for trend following
        dataframe['ema8'] = ta.EMA(dataframe, timeperiod=8)
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
        
        # RSI for momentum
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        # MACD for trend confirmation
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']
        
        # Volume moving average
        dataframe['volume_ma'] = dataframe['volume'].rolling(window=20).mean()
        
        return dataframe

    def populate_buy_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        MAXIMUM-AGGRESSIVE Buy Conditions:
        - MINIMAL filters for MAXIMUM trades
        - Catch EVERY opportunity
        - More trades = more profit potential
        """
        dataframe['buy'] = np.where(
            # EMA crossover - main signal (minimal filter)
            (dataframe['ema8'] > dataframe['ema21']) &
            # RSI filter - extremely wide (20-80) for maximum opportunities
            (dataframe['rsi'] > 20) &
            (dataframe['rsi'] < 80) &
            # MACD confirmation - minimal (just not extremely bearish)
            (dataframe['macd'] > dataframe['macdsignal'] * 0.90) &
            # Volume filter - minimal (any volume at all)
            (dataframe['volume'] > dataframe['volume_ma'] * 0.2) &
            # Trend filter - minimal (price anywhere near EMA50)
            (dataframe['close'] > dataframe['ema50'] * 0.90),
            1, 0
        )
        return dataframe

    def populate_sell_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Disabled - let ROI and stoploss handle exits
        """
        dataframe['sell'] = 0
        return dataframe
