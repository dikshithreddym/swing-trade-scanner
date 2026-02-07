"""
Technical indicator calculations for swing trading
Using 'ta' library instead of talib for easier installation
"""

import pandas as pd
import numpy as np
from ta import trend, momentum, volatility, volume


class TechnicalIndicators:
    """Calculate technical indicators for swing trading"""
    
    @staticmethod
    def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """Add all technical indicators to dataframe"""
        df = df.copy()
        
        close = df['Close']
        high = df['High']
        low = df['Low']
        
        # Moving Averages
        df['EMA20'] = trend.EMAIndicator(close, window=20).ema_indicator()
        df['EMA50'] = trend.EMAIndicator(close, window=50).ema_indicator()
        df['EMA200'] = trend.EMAIndicator(close, window=200).ema_indicator()
        df['SMA200'] = trend.SMAIndicator(close, window=200).sma_indicator()
        
        # RSI
        df['RSI'] = momentum.RSIIndicator(close, window=14).rsi()
        df['RSI_MA'] = df['RSI'].rolling(14).mean()
        
        # MACD
        macd = trend.MACD(close)
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        df['MACD_Hist'] = macd.macd_diff()
        
        # Bollinger Bands
        bb = volatility.BollingerBands(close, window=20, window_dev=2)
        df['BB_Upper'] = bb.bollinger_hband()
        df['BB_Middle'] = bb.bollinger_mavg()
        df['BB_Lower'] = bb.bollinger_lband()
        df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Middle']
        
        # Volume Analysis
        df['Volume_MA20'] = df['Volume'].rolling(20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_MA20']
        df['Volume_Trend'] = df['Volume'].rolling(10).mean() / df['Volume'].rolling(50).mean()
        
        # ATR for volatility
        atrade = volatility.AverageTrueRange(high, low, close, window=14)
        df['ATR'] = atrade.average_true_range()
        df['ATR_Percent'] = df['ATR'] / close * 100
        
        # Support & Resistance
        df['Resistance'] = df['High'].rolling(20).max()
        df['Support'] = df['Low'].rolling(20).min()
        df['Near_Resistance'] = close >= df['Resistance'] * 0.98
        df['Near_Support'] = close <= df['Support'] * 1.02
        
        # Trend Analysis
        df['Trend'] = np.where(close > df['EMA50'], 'Uptrend',
                              np.where(close < df['EMA50'], 'Downtrend', 'Sideways'))
        
        # Price Action
        df['Price_Change'] = df['Close'].pct_change()
        df['Price_Change_5d'] = df['Close'].pct_change(5)
        df['Price_Change_20d'] = df['Close'].pct_change(20)
        
        # Candlestick patterns
        df['Body'] = abs(df['Close'] - df['Open'])
        df['Upper_Shadow'] = df['High'] - df[['Open', 'Close']].max(axis=1)
        df['Lower_Shadow'] = df[['Open', 'Close']].min(axis=1) - df['Low']
        df['Doji'] = df['Body'] < (df['High'] - df['Low']) * 0.1
        
        return df