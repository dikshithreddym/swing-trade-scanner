#!/usr/bin/env python3
"""
Demo scanner with sample data (no dependencies needed)
"""

import random
import json
from datetime import datetime

# Sample S&P 500 symbols
SP500_SYMBOLS = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "META", "NVDA", "JPM", "V", "JNJ",
    "UNH", "HD", "PG", "MA", "BAC", "DIS", "ADBE", "CRM", "NFLX", "INTC",
    "VZ", "T", "KO", "PEP", "WMT", "CSCO", "PFE", "ABT", "CVX", "XOM",
    "LLY", "MRK", "TMO", "ACN", "COST", "AVGO", "TXN", "QCOM", "AMD", "INTU"
]

def generate_sample_opportunity(symbol):
    """Generate a realistic swing trading opportunity"""
    patterns = [
        "Breakout_Play", "Pullback_to_EMA50", "Trend_Continuation", 
        "Oversold_Reversal", "Volume_Spike_Bullish"
    ]
    
    base_price = round(random.uniform(50, 500), 2)
    pattern = random.choice(patterns)
    
    # Calculate risk/reward
    stop_loss = round(base_price * random.uniform(0.92, 0.97), 2)
    take_profit = round(base_price * random.uniform(1.12, 1.25), 2)
    
    risk = base_price - stop_loss
    reward = take_profit - base_price
    risk_reward = round(reward / risk, 2) if risk > 0 else 0
    
    # Confidence based on pattern
    confidence_map = {
        "Breakout_Play": random.randint(75, 95),
        "Pullback_to_EMA50": random.randint(78, 94),
        "Trend_Continuation": random.randint(80, 96),
        "Oversold_Reversal": random.randint(70, 88),
        "Volume_Spike_Bullish": random.randint(72, 90)
    }
    
    confidence = confidence_map[pattern]
    
    reasons = {
        "Breakout_Play": f"Price at resistance with volume spike ({random.uniform(1.2, 2.5):.1f}x avg)",
        "Pullback_to_EMA50": f"Healthy pullback to EMA50 (${base_price * 0.98:.2f}) in uptrend",
        "Trend_Continuation": "Strong uptrend with healthy momentum",
        "Oversold_Reversal": f"Oversold bounce (RSI: {random.uniform(25, 35):.1f})",
        "Volume_Spike_Bullish": f"Bullish volume spike ({random.uniform(2.0, 3.5):.1f}x avg)"
    }
    
    return {
        "symbol": symbol,
        "pattern": pattern,
        "confidence": confidence,
        "price": base_price,
        "entry": base_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_reward": risk_reward,
        "reason": reasons[pattern],
        "market_cap": random.choice(["Large Cap", "Mega Cap", "Mid Cap"]),
        "avg_volume": random.randint(2000000, 50000000),
        "date": datetime.now().isoformat()
    }

print("=" * 80)
print("🚀 SWING TRADE SCANNER - DEMO RUN")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print()

# Simulate scanning
print("🔍 Fetching S&P 500 constituents...")
print(f"✅ Loaded {len(SP500_SYMBOLS)} symbols")
print()

print("🔄 Scanning stocks for swing trading opportunities...")
print("-" * 60)

opportunities = []

for i, symbol in enumerate(SP500_SYMBOLS, 1):
    # Simulate analysis delay
    if i % 10 == 0:
        print(f"   Analyzed {i}/{len(SP500_SYMBOLS)} stocks...")
    
    # Random chance of finding an opportunity (30%)
    if random.random() < 0.30:
        opp = generate_sample_opportunity(symbol)
        if opp['confidence'] >= 70:  # Only high confidence
            opportunities.append(opp)

# Sort by confidence
opportunities.sort(key=lambda x: x['confidence'], reverse=True)

print()
print("=" * 80)
print(f"🎯 SCAN COMPLETE - FOUND {len(opportunities)} HIGH-CONFIDENCE OPPORTUNITIES")
print("=" * 80)
print()

# Display top 10
for i, opp in enumerate(opportunities[:10], 1):
    print(f"\n#{i} {opp['symbol']} - {opp['pattern']}")
    print(f"   📊 Confidence: {opp['confidence']}%")
    print(f"   💰 Current Price: ${opp['price']:.2f}")
    print(f"   💵 Entry Point: ${opp['entry']:.2f}")
    print(f"   🛑 Stop Loss: ${opp['stop_loss']:.2f} ({((opp['entry']-opp['stop_loss'])/opp['entry']*100):.1f}% risk)")
    print(f"   🎯 Take Profit: ${opp['take_profit']:.2f} ({((opp['take_profit']-opp['entry'])/opp['entry']*100):.1f}% reward)")
    print(f"   💵 Risk/Reward: {opp['risk_reward']}:1")
    print(f"   📝 Setup: {opp['reason']}")
    print(f"   📈 Market Cap: {opp['market_cap']}")
    print(f"   📊 Avg Volume: {opp['avg_volume']:,}")

print()
print("=" * 80)
print("⚠️ DISCLAIMER: This is a DEMO with simulated data.")
print("   Real run will use live S&P 500 data from Yahoo Finance.")
print("=" * 80)

# Save results
with open('/home/azureuser/swing-trade-scanner/data/demo_results.json', 'w') as f:
    json.dump(opportunities, f, indent=2)

print(f"\n💾 Results saved to: data/demo_results.json")

# Summary
print("\n📊 SUMMARY:")
print(f"   Total Opportunities: {len(opportunities)}")
avg_conf = sum(o['confidence'] for o in opportunities) / len(opportunities) if opportunities else 0
print(f"   Avg Confidence: {avg_conf:.1f}%")
print(f"   Best Setup: {opportunities[0]['symbol']} ({opportunities[0]['pattern']})" if opportunities else "")
