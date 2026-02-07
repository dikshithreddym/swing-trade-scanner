# Swing Trade Scanner Configuration

# S&P 500 Settings
SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
MAX_WORKERS = 10  # Parallel scanning threads

# Timeframes
TIMEFRAMES = {
    'daily': '1d',
    'weekly': '1wk',
    'monthly': '1mo'
}

# Analysis Period
LOOKBACK_DAYS = 120  # 6 months for analysis

# Technical Indicator Settings
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

EMA_SHORT = 20
EMA_MEDIUM = 50
EMA_LONG = 200

VOLUME_AVG_PERIOD = 20
VOLUME_SPIKE_THRESHOLD = 1.5  # 150% of average volume

# Swing Trading Setup Criteria
MIN_PRICE = 5.0  # Minimum stock price
MAX_PRICE = 2000.0  # Maximum stock price
MIN_VOLUME = 1000000  # Minimum daily volume
MIN_ATR_PERCENT = 2.0  # Minimum volatility

# Risk Management
MAX_POSITION_SIZE = 0.2  # 20% max portfolio allocation
DEFAULT_STOP_LOSS = 0.08  # 8% stop loss
DEFAULT_TAKE_PROFIT = 0.20  # 20% take profit
RISK_REWARD_MIN = 2.0  # Minimum 2:1 risk/reward

# Scoring Weights
SCORING = {
    'trend_aligned': 25,
    'volume_confirmation': 20,
    'technical_setup': 25,
    'risk_reward': 15,
    'market_context': 15
}

# Alert Settings
ALERT_COOLDOWN_HOURS = 4