# Minimal Freqtrade strategy for testing
from freqtrade.strategy.interface import IStrategy
import pandas as pd

class SampleStrategy(IStrategy):
    # Use 1-minute candles for fast testing
    timeframe = '1m'

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # no indicators, just return dataframe
        return dataframe

    def populate_buy_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # no buy signals yet
        dataframe['buy'] = 0
        return dataframe

    def populate_sell_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # no sell signals yet
        dataframe['sell'] = 0
        return dataframe
