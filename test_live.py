#!/usr/bin/env python3
"""
Test live data fetching (requires yfinance)
"""

from swing_scanner.data_fetcher import DataFetcher
from swing_scanner.indicators import TechnicalIndicators
from swing_scanner.patterns import PatternDetector
from swing_scanner.scanner import SwingScanner
from datetime import datetime
import sys

print("=" * 80)
print("🚀 SWING TRADE SCANNER - LIVE TEST")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 80)
print("Testing with live S&P 500 data...")
print()

try:
    # Test data fetching
    print("🔍 Testing data fetcher...")
    fetcher = DataFetcher()
    print(f"✅ Loaded {len(fetcher.sp500_symbols)} S&P 500 symbols")
    
    # Fetch first 10 stocks only for quick test
    print("\n📊 Fetching first 10 stocks for test...")
    data = fetcher.fetch_all_stocks(max_workers=5, limit=10)
    
    if not data:
        print("❌ No data retrieved")
        sys.exit(1)
    
    print(f"✅ Retrieved data for {len(data)} stocks")
    
    # Test indicators
    print("\n📈 Calculating technical indicators...")
    indicators = TechnicalIndicators()
    sample_symbol = list(data.keys())[0]
    sample_df = data[sample_symbol]
    df_with_indicators = indicators.add_indicators(sample_df)
    print(f"✅ Added indicators to {sample_symbol}")
    print(f"   RSI: {df_with_indicators['RSI'].iloc[-1]:.2f}")
    print(f"   MACD: {df_with_indicators['MACD'].iloc[-1]:.2f}")
    print(f"   EMA20: ${df_with_indicators['EMA20'].iloc[-1]:.2f}")
    
    # Test pattern detection
    print("\n🔍 Testing pattern detection...")
    detector = PatternDetector()
    patterns = detector.detect_all_patterns(df_with_indicators)
    print(f"✅ Found {len(patterns)} patterns in {sample_symbol}")
    
    # Test full scan
    print("\n🎯 Running full scan (first 10 stocks)...")
    scanner = SwingScanner()
    
    # Override fetcher to use limited data
    scanner.fetcher = DataFetcher()
    opportunities = []
    
    for symbol, df in data.items():
        try:
            df = indicators.add_indicators(df)
            patterns = detector.detect_all_patterns(df)
            if patterns:
                best = max(patterns, key=lambda x: x['confidence'])
                best['symbol'] = symbol
                best['price'] = df['Close'].iloc[-1]
                best['date'] = datetime.now().isoformat()
                opportunities.append(best)
        except:
            continue
    
    # Sort and display
    opportunities.sort(key=lambda x: x['confidence'], reverse=True)
    
    print(f"\n{'='*80}")
    print(f"🎯 SCAN COMPLETE - FOUND {len(opportunities)} OPPORTUNITIES")
    print(f"{'='*80}\n")
    
    for i, opp in enumerate(opportunities[:5], 1):
        print(f"#{i} {opp['symbol']} - {opp['pattern']} ({opp['confidence']}%)")
        print(f"   💰 Price: ${opp['price']:.2f}")
        print(f"   🎯 R/R: {opp.get('risk_reward', 0):.2f}:1")
    
    print(f"\n✅ TEST COMPLETE - Scanner works!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()