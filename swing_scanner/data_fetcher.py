"""
Data fetching module for S&P 500 stocks
"""

import yfinance as yf
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from typing import Dict, List, Optional
import time


class DataFetcher:
    """Fetch and manage stock data"""
    
    def __init__(self):
        self.sp500_symbols = self._get_sp500_symbols()
        self.cache = {}
        
    def _get_sp500_symbols(self) -> List[str]:
        """Fetch current S&P 500 constituents from Wikipedia"""
        try:
            tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
            df = tables[0]
            symbols = df['Symbol'].tolist()
            print(f"✅ Loaded {len(symbols)} S&P 500 symbols")
            return symbols
        except Exception as e:
            print(f"❌ Error fetching S&P 500: {e}")
            # Fallback to common symbols for demo
            return [
                "AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "META", "NVDA", "JPM", "V", "JNJ",
                "UNH", "HD", "PG", "MA", "BAC", "DIS", "ADBE", "CRM", "NFLX", "INTC"
            ]
    
    def fetch_stock_data(self, symbol: str, period: str = "6mo", interval: str = "1d") -> Optional[pd.DataFrame]:
        """Fetch historical data for a single stock"""
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            if df.empty:
                return None
            df['Symbol'] = symbol
            return df
        except Exception as e:
            print(f"⚠️ Error fetching {symbol}: {e}")
            return None
    
    def fetch_all_stocks(self, max_workers: int = 10, limit: int = 50) -> Dict[str, pd.DataFrame]:
        """Fetch data for S&P 500 stocks in parallel"""
        results = {}
        symbols_to_fetch = self.sp500_symbols[:limit]  # Limit for demo
        
        print(f"🔍 Scanning {len(symbols_to_fetch)} stocks...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_symbol = {
                executor.submit(self.fetch_stock_data, symbol): symbol 
                for symbol in symbols_to_fetch
            }
            
            for future in tqdm(as_completed(future_to_symbol), total=len(future_to_symbol), desc="Analyzing"):
                symbol = future_to_symbol[future]
                try:
                    data = future.result()
                    if data is not None:
                        results[symbol] = data
                except Exception as e:
                    pass
        
        print(f"✅ Analyzed {len(results)} stocks successfully")
        return results