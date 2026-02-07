"""
Pattern detection for swing trading setups
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


class PatternDetector:
    """Detect swing trading patterns and setups"""
    
    def __init__(self):
        self.setups = []
    
    def detect_all_patterns(self, df: pd.DataFrame) -> List[Dict]:
        """Detect all swing trading patterns in data"""
        patterns = []
        
        if len(df) < 50:
            return patterns
        
        latest = df.iloc[-1]
        
        # Pattern 1: Breakout Play
        breakout = self._check_breakout(df, latest)
        if breakout:
            patterns.append(breakout)
        
        # Pattern 2: Pullback to Support
        pullback = self._check_pullback(df, latest)
        if pullback:
            patterns.append(pullback)
        
        # Pattern 3: Trend Continuation
        continuation = self._check_continuation(df, latest)
        if continuation:
            patterns.append(continuation)
        
        # Pattern 4: Oversold Bounce (RSI divergence)
        reversal = self._check_reversal(df, latest)
        if reversal:
            patterns.append(reversal)
        
        # Pattern 5: Volume Spike
        volume_spike = self._check_volume_spike(df, latest)
        if volume_spike:
            patterns.append(volume_spike)
        
        return patterns
    
    def _check_breakout(self, df: pd.DataFrame, latest: pd.Series) -> Optional[Dict]:
        """Detect breakout above resistance pattern"""
        if pd.isna(latest['Resistance']) or latest['Resistance'] == 0:
            return None
        
        # Price within 2% of resistance
        price_vs_resistance = latest['Close'] / latest['Resistance']
        
        if 0.98 <= price_vs_resistance <= 1.05:
            volume_confirm = latest['Volume_Ratio'] > 1.2
            trend_up = latest['Close'] > latest['EMA50']
            
            if trend_up and volume_confirm:
                return {
                    'pattern': 'Breakout_Play',
                    'confidence': self._calc_confidence(price_vs_resistance, latest),
                    'entry': latest['Close'],
                    'stop_loss': latest['Support'] * 0.98,
                    'take_profit': latest['Close'] * 1.15,
                    'reason': f"Price at resistance (${latest['Resistance']:.2f}) with volume spike"
                }
        return None
    
    def _check_pullback(self, df: pd.DataFrame, latest: pd.Series) -> Optional[Dict]:
        """Detect pullback to support/EMA pattern"""
        price_vs_ema50 = latest['Close'] / latest['EMA50'] if latest['EMA50'] > 0 else 1
        
        # Pullback to EMA50 in uptrend
        if 0.97 <= price_vs_ema50 <= 1.03:
            trend = latest['EMA20'] > latest['EMA50'] > latest['EMA200']
            rsi_healthy = 30 < latest['RSI'] < 60
            
            if trend and rsi_healthy:
                return {
                    'pattern': 'Pullback_to_EMA50',
                    'confidence': min(95, int(100 - abs(price_vs_ema50 - 1) * 1000)),
                    'entry': latest['Close'],
                    'stop_loss': latest['EMA50'] * 0.97,
                    'take_profit': latest['Close'] * 1.12,
                    'reason': f"Healthy pullback to EMA50 (${latest['EMA50']:.2f}) in uptrend"
                }
        return None
    
    def _check_continuation(self, df: pd.DataFrame, latest: pd.Series) -> Optional[Dict]:
        """Detect trend continuation pattern"""
        # Strong uptrend
        strong_trend = (
            latest['Close'] > latest['EMA20'] > latest['EMA50'] > latest['EMA200'] and
            latest['EMA20'] > latest['EMA20_5d_ago']  # EMA rising
        )
        
        # Consistent volume
        volume_trend = latest['Volume_Trend'] > 1.0
        
        # Not overbought
        not_overbought = latest['RSI'] < 65
        
        if strong_trend and volume_trend and not_overbought:
            return {
                'pattern': 'Trend_Continuation',
                'confidence': int(latest['RSI']),
                'entry': latest['Close'],
                'stop_loss': latest['EMA50'] * 0.95,
                'take_profit': latest['Close'] * 1.20,
                'reason': "Strong uptrend with healthy momentum"
            }
        return None
    
    def _check_reversal(self, df: pd.DataFrame, latest: pd.Series) -> Optional[Dict]:
        """Detect oversold reversal pattern"""
        oversold = latest['RSI'] < 35
        near_support = latest['Near_Support'] or latest['Close'] <= latest['BB_Lower'] * 1.05
        
        # Bullish candlestick (green candle)
        bullish_candle = latest['Close'] > latest['Open']
        
        if oversold and near_support and bullish_candle:
            # Check for RSI divergence
            rsi_divergence = self._check_rsi_divergence(df)
            
            return {
                'pattern': 'Oversold_Reversal',
                'confidence': 70 + (10 if rsi_divergence else 0),
                'entry': latest['Close'],
                'stop_loss': latest['Support'] * 0.97,
                'take_profit': latest['Close'] * 1.15,
                'reason': f"Oversold bounce (RSI: {latest['RSI']:.1f})" + (" + divergence" if rsi_divergence else "")
            }
        return None
    
    def _check_volume_spike(self, df: pd.DataFrame, latest: pd.Series) -> Optional[Dict]:
        """Detect unusual volume activity"""
        if latest['Volume_Ratio'] > 2.0:  # 2x average volume
            price_change = abs(latest['Price_Change']) * 100
            
            if price_change > 3:  # Significant price move
                direction = "Bullish" if latest['Close'] > latest['Open'] else "Bearish"
                
                return {
                    'pattern': f'Volume_Spike_{direction}',
                    'confidence': min(90, int(latest['Volume_Ratio'] * 30)),
                    'entry': latest['Close'],
                    'stop_loss': latest['Low'] * 0.995 if direction == "Bullish" else latest['High'] * 1.005,
                    'take_profit': latest['Close'] * (1.10 if direction == "Bullish" else 0.90),
                    'reason': f"{direction} volume spike ({latest['Volume_Ratio']:.1f}x avg)"
                }
        return None
    
    def _check_rsi_divergence(self, df: pd.DataFrame) -> bool:
        """Check for RSI bullish divergence"""
        if len(df) < 20:
            return False
        
        # Compare last 10 days
        recent = df.tail(10)
        price_low_1 = recent['Close'].iloc[0]
        price_low_2 = recent['Close'].iloc[-1]
        rsi_low_1 = recent['RSI'].iloc[0]
        rsi_low_2 = recent['RSI'].iloc[-1]
        
        # Bullish divergence: price makes lower low, RSI makes higher low
        return price_low_2 < price_low_1 and rsi_low_2 > rsi_low_1
    
    def _calc_confidence(self, ratio: float, latest: pd.Series) -> int:
        """Calculate confidence score"""
        base = 80
        volume_bonus = min(15, int(latest['Volume_Ratio'] * 5))
        trend_bonus = 10 if latest['Close'] > latest['EMA50'] else 0
        return min(100, base + volume_bonus + trend_bonus)