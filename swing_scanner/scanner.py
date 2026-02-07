"""
Main Swing Trade Scanner
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
import os

from .data_fetcher import DataFetcher
from .indicators import TechnicalIndicators
from .patterns import PatternDetector
from configs.settings import *


class SwingScanner:
    """Main swing trading scanner"""
    
    def __init__(self):
        self.fetcher = DataFetcher()
        self.indicators = TechnicalIndicators()
        self.detector = PatternDetector()
        self.results = []
        
    def scan_sp500(self, max_stocks: int = 50) -> List[Dict]:
        """Scan S&P 500 for swing trading opportunities"""
        print("🔍 Starting S&P 500 Swing Trade Scan...")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        # Fetch data
        stocks_data = self.fetcher.fetch_all_stocks(max_workers=MAX_WORKERS)
        
        opportunities = []
        
        for symbol, df in stocks_data.items():
            try:
                # Skip if insufficient data
                if len(df) < 50:
                    continue
                
                # Add indicators
                df = self.indicators.add_indicators(df)
                
                # Check filters
                if not self._passes_filters(df):
                    continue
                
                # Detect patterns
                patterns = self.detector.detect_all_patterns(df)
                
                if patterns:
                    # Find highest confidence pattern
                    best_pattern = max(patterns, key=lambda x: x['confidence'])
                    best_pattern['symbol'] = symbol
                    best_pattern['date'] = datetime.now().isoformat()
                    best_pattern['price'] = df['Close'].iloc[-1]
                    best_pattern['market_cap'] = self._get_market_cap(df)
                    best_pattern['avg_volume'] = int(df['Volume'].tail(20).mean())
                    
                    opportunities.append(best_pattern)
                    
            except Exception as e:
                print(f"⚠️ Error processing {symbol}: {e}")
                continue
        
        # Sort by confidence
        opportunities.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Filter to high confidence only
        high_confidence = [o for o in opportunities if o['confidence'] >= 70]
        
        print(f"\n✅ Scan Complete!")
        print(f"📊 Total stocks analyzed: {len(stocks_data)}")
        print(f"🎯 Opportunities found: {len(opportunities)}")
        print(f"🌟 High confidence (70%+): {len(high_confidence)}")
        
        self.results = high_confidence
        return high_confidence
    
    def _passes_filters(self, df: pd.DataFrame) -> bool:
        """Check if stock passes basic filters"""
        latest = df.iloc[-1]
        
        # Price filter
        if not (MIN_PRICE <= latest['Close'] <= MAX_PRICE):
            return False
        
        # Volume filter
        if latest['Volume_MA20'] < MIN_VOLUME:
            return False
        
        # Volatility filter
        if latest['ATR_Percent'] < MIN_ATR_PERCENT:
            return False
        
        return True
    
    def _get_market_cap(self, df: pd.DataFrame) -> str:
        """Estimate market cap category"""
        avg_volume = df['Volume'].tail(20).mean()
        price = df['Close'].iloc[-1]
        
        # Rough estimation
        estimated_shares = avg_volume * 20  # Rough estimate
        market_cap = estimated_shares * price
        
        if market_cap > 200e9:
            return "Mega Cap"
        elif market_cap > 10e9:
            return "Large Cap"
        elif market_cap > 2e9:
            return "Mid Cap"
        else:
            return "Small Cap"
    
    def generate_report(self, opportunities: List[Dict]) -> str:
        """Generate formatted report"""
        report = []
        report.append("=" * 80)
        report.append("🚀 SWING TRADE SCANNER REPORT")
        report.append(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        report.append("")
        
        if not opportunities:
            report.append("⚠️ No opportunities found matching criteria.")
            return "\n".join(report)
        
        report.append(f"🎯 TOP {min(10, len(opportunities))} OPPORTUNITIES")
        report.append("-" * 80)
        report.append("")
        
        for i, opp in enumerate(opportunities[:10], 1):
            report.append(f"\n#{i} {opp['symbol']} - {opp['pattern']}")
            report.append(f"   📊 Confidence: {opp['confidence']}%")
            report.append(f"   💰 Price: ${opp['price']:.2f}")
            report.append(f"   💰 Entry: ${opp['entry']:.2f}")
            report.append(f"   🛑 Stop Loss: ${opp['stop_loss']:.2f}")
            report.append(f"   🎯 Take Profit: ${opp['take_profit']:.2f}")
            report.append(f"   💵 Risk/Reward: {(opp['take_profit'] - opp['entry']) / (opp['entry'] - opp['stop_loss']):.2f}:1")
            report.append(f"   📝 Reason: {opp['reason']}")
            report.append(f"   📈 Market Cap: {opp['market_cap']}")
            report.append(f"   📊 Avg Volume: {opp['avg_volume']:,}")
            report.append("")
        
        report.append("=" * 80)
        report.append("⚠️ DISCLAIMER: This is for educational purposes only.")
        report.append("   Always do your own research before trading.")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_results(self, opportunities: List[Dict], filename: str = None):
        """Save results to file"""
        if filename is None:
            filename = f"swing_opportunities_{datetime.now().strftime('%Y%m%d')}.json"
        
        filepath = os.path.join('data', filename)
        os.makedirs('data', exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(opportunities, f, indent=2)
        
        print(f"\n💾 Results saved to: {filepath}")
        return filepath
    
    def get_summary(self, opportunities: List[Dict]) -> Dict:
        """Get summary statistics"""
        if not opportunities:
            return {
                'total': 0,
                'avg_confidence': 0,
                'avg_risk_reward': 0,
                'top_sector': 'N/A'
            }
        
        avg_confidence = np.mean([o['confidence'] for o in opportunities])
        
        # Calculate average risk/reward
        ratios = []
        for o in opportunities:
            risk = o['entry'] - o['stop_loss']
            reward = o['take_profit'] - o['entry']
            if risk > 0:
                ratios.append(reward / risk)
        
        avg_rr = np.mean(ratios) if ratios else 0
        
        return {
            'total': len(opportunities),
            'avg_confidence': round(avg_confidence, 1),
            'avg_risk_reward': round(avg_rr, 2),
            'best_setup': opportunities[0]['pattern'] if opportunities else 'N/A',
            'best_symbol': opportunities[0]['symbol'] if opportunities else 'N/A'
        }