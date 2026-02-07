"""
Data fetching module for S&P 500 stocks
"""
import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import requests
from datetime import datetime, timedelta

class DataFetcher:
    """Fetches stock data and S&P 500 constituents"""
    
    def __init__(self):
        self.sp500_symbols = None
        
    def get_sp500_symbols(self) -> List[str]:
        """Fetch current S&P 500 constituents from Wikipedia"""
        try:
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            tables = pd.read_html(url)
            df = tables[0]
            symbols = df['Symbol'].tolist()
            self.sp500_symbols = symbols
            print(f"✅ Loaded {len(symbols)} S&P 500 stocks")
            return symbols
        except Exception as e:
            print(f"⚠️  Could not fetch S&P 500: {e}")
            # Fallback to common stocks
            return self._get_fallback_symbols()
    
    def _get_fallback_symbols(self) -> List[str]:
        """Fallback list of major stocks"""
        return [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B',
            'UNH', 'JNJ', 'XOM', 'JPM', 'V', 'PG', 'HD', 'CVX', 'MA', 'LLY',
            'ABBV', 'PFE', 'MRK', 'PEP', 'KO', 'COST', 'TMO', 'AVGO', 'DIS',
            'ADBE', 'CRM', 'ACN', 'VZ', 'WMT', 'NKE', 'ABT', 'CMCSA', 'WFC',
            'TXN', 'NEE', 'PM', 'RTX', 'IBM', 'AMGN', 'HON', 'QCOM', 'SLB',
            'T', 'CAT', 'GS', 'MS', 'BA', 'LMT', 'SPGI', 'CI', 'AXP', 'INTC'
        ]
    
    def fetch_stock_data(self, symbol: str, period: str = "3mo") -> Optional[pd.DataFrame]:
        """
        Fetch OHLCV data for a symbol
        
        Args:
            symbol: Stock ticker
            period: Lookback period (1mo, 3mo, 6mo, 1y)
            
        Returns:
            DataFrame with OHLCV data or None if failed
        """
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            if df.empty:
                return None
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            df.index = df.index.tz_localize(None)  # Remove timezone
            return df
        except Exception as e:
            print(f"❌ Error fetching {symbol}: {e}")
            return None
    
    def fetch_multiple(self, symbols: List[str], progress: bool = True) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple symbols
        
        Args:
            symbols: List of stock tickers
            progress: Show progress bar
            
        Returns:
            Dict mapping symbol to DataFrame
        """
        data = {}
        iterator = symbols
        
        if progress:
            from tqdm import tqdm
            iterator = tqdm(symbols, desc="Fetching stock data")
        
        for symbol in iterator:
            df = self.fetch_stock_data(symbol)
            if df is not None and len(df) >= 50:  # Need at least 50 days
                data[symbol] = df
                
        return data
    
    def get_stock_info(self, symbol: str) -> Dict:
        """Get basic stock information"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'beta': info.get('beta', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'avg_volume': info.get('averageVolume', 0)
            }
        except:
            return {}
