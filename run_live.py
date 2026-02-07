#!/usr/bin/env python3
"""
Live scanner - run this to get real S&P 500 swing trade opportunities
"""

import sys
sys.path.insert(0, '/home/azureuser/swing-trade-scanner')

from swing_scanner.data_fetcher import DataFetcher
from swing_scanner.indicators import TechnicalIndicators
from swing_scanner.patterns import PatternDetector
from configs.settings import MIN_PRICE, MAX_PRICE, MIN_VOLUME, MIN_ATR_PERCENT
from datetime import datetime

print("=" * 80)
print("🚀 SWING TRADE SCANNER - LIVE RUN")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 80)
print("Scanning S&P 500 with real market data...")
print()

# Initialize
fetcher = DataFetcher()
indicators = TechnicalIndicators()
detector = PatternDetector()

# Fetch all S&P 500 stocks (limited to 50 for speed)
print("🔍 Loading S&P 500 data from Yahoo Finance...")
print("⏳ This may take a few minutes...")
print()

data = fetcher.fetch_all_stocks(max_workers=10, limit=50)

if not data:
    print("❌ Failed to fetch stock data")
    sys.exit(1)

print(f"\n📊 Analyzing {len(data)} stocks for swing trading setups...")
print("-" * 80)

opportunities = []

for symbol, df in data.items():
    try:
        # Add indicators
        df = indicators.add_indicators(df)
        
        # Basic filters
        latest = df.iloc[-1]
        if not (MIN_PRICE <= latest['Close'] <= MAX_PRICE):
            continue
        if latest['Volume_MA20'] < MIN_VOLUME:
            continue
        if latest['ATR_Percent'] < MIN_ATR_PERCENT:
            continue
        
        # Detect patterns
        patterns = detector.detect_all_patterns(df)
        
        if patterns:
            # Get best pattern
            best = max(patterns, key=lambda x: x['confidence'])
            
            if best['confidence'] >= 70:  # Only high confidence
                best['symbol'] = symbol
                best['price'] = round(latest['Close'], 2)
                best['date'] = datetime.now().isoformat()
                best['volume'] = int(latest['Volume'])
                best['atr'] = round(latest['ATR_Percent'], 2)
                
                opportunities.append(best)
                print(f"✅ {symbol}: {best['pattern']} ({best['confidence']}% confidence)")
                
    except Exception as e:
        pass  # Skip problematic stocks

# Sort by confidence
opportunities.sort(key=lambda x: x['confidence'], reverse=True)

# Display results
print(f"\n{'='*80}")
print(f"🎯 SCAN COMPLETE - FOUND {len(opportunities)} HIGH-CONFIDENCE OPPORTUNITIES")
print(f"{'='*80}\n")

if not opportunities:
    print("⚠️ No swing trading opportunities found right now.")
    print("   Try again later - markets change constantly!")
else:
    for i, opp in enumerate(opportunities[:10], 1):
        print(f"\n#{i} {opp['symbol']} - {opp['pattern']}")
        print(f"   📊 Confidence: {opp['confidence']}%")
        print(f"   💰 Current Price: ${opp['price']:.2f}")
        print(f"   💵 Entry: ${opp['entry']:.2f}")
        print(f"   🛑 Stop Loss: ${opp['stop_loss']:.2f}")
        print(f"   🎯 Take Profit: ${opp['take_profit']:.2f}")
        print(f"   💵 Risk/Reward: {opp.get('risk_reward', 0):.2f}:1")
        print(f"   📈 ATR: {opp['atr']}%")
        print(f"   📝 {opp['reason']}")

print(f"\n{'='*80}")

# Summary
if opportunities:
    avg_conf = sum(o['confidence'] for o in opportunities) / len(opportunities)
    print(f"\n📊 SUMMARY:")
    print(f"   Total Opportunities: {len(opportunities)}")
    print(f"   Avg Confidence: {avg_conf:.1f}%")
    print(f"   Best Setup: {opportunities[0]['symbol']} ({opportunities[0]['pattern']})")

print("\n💾 Saving results...")
import json
import os
os.makedirs('data', exist_ok=True)
with open('data/live_results.json', 'w') as f:
    json.dump(opportunities, f, indent=2)
print("✅ Results saved to: data/live_results.json")

print("\n⚠️ DISCLAIMER: This is for educational purposes only.")
print("   Not financial advice. Always do your own research!")
print("="*80)