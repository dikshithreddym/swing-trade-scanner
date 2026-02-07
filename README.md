# 📈 Swing Trade Scanner

An intelligent swing trading opportunity scanner for S&P 500 stocks.

## 🎯 Features

- **Real-time S&P 500 scanning** - Automatically fetches current S&P 500 constituents
- **Technical Analysis** - Multi-timeframe analysis with key swing trading indicators
- **Pattern Recognition** - Detects swing trading setups (breakouts, pullbacks, reversals)
- **Risk Management** - Calculates stop-loss levels and position sizing
- **Sentiment Analysis** - Optional news sentiment integration
- **Alerts** - Email/Telegram notifications for opportunities

## 🔧 Technical Indicators

- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Moving Averages (20, 50, 200 EMA/SMA)
- Volume Analysis
- Support/Resistance Levels
- Bollinger Bands
- ATR (Average True Range) for volatility

## 📦 Installation

```bash
git clone https://github.com/dikshithreddym/swing-trade-scanner.git
cd swing-trade-scanner
pip install -r requirements.txt
```

## 🚀 Usage

```python
from swing_scanner import Scanner

# Initialize scanner
scanner = Scanner()

# Scan for opportunities
opportunities = scanner.scan_sp500()

# Get detailed analysis
for opp in opportunities:
    print(f"{opp['symbol']}: {opp['setup_type']} - Confidence: {opp['confidence']}%")
```

## 📊 Swing Trading Setups Detected

1. **Breakout Play** - Price breaking above resistance with volume
2. **Pullback to Support** - Price retracing to key support (EMA50/200)
3. **Trend Continuation** - Strong trend with healthy pullback
4. **Reversal Setup** - Oversold bounce with RSI divergence
5. **Volume Spike** - Unusual volume with price action

## ⚠️ Disclaimer

This tool is for educational purposes only. Not financial advice. Always do your own research.

## 📝 License

MIT License
