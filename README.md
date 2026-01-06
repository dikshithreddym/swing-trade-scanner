# swing-trade-scanner

**swing-trade-scanner** is an automated tool for finding trade ideas. It fetches daily stock data, calculates technical indicators (RSI, MACD, ATR, ADX), and filters for specific strategies:

*   **Trend Pullbacks:** Buying the dip on strong stocks.
*   **Breakouts:** Identifying volume-backed moves to new highs.
*   **Support Retests:** Catching stocks testing previous resistance as support.

Includes built-in risk management calculations (Stop/Entry/Target) and sector relative strength scoring.

## Features

- **Market Regime Analysis**: Scrapes current index constituents (SPY & TSX).
- **Technical Indicators**: Calculates RSI, MACD, Bollinger Bands, ATR, Stochastics, ADX, CCI, and AVWAP.
- **Strategy Filters**:
    - Breakout with Volume
    - Pullback in Super Trend
    - Mean Reversion (Oversold)
    - Breakout Retest
- **Scoring Engine**: Ranks candidates based on technical strength, sector momentum, and Risk/Reward ratios.

## Usage

Open the `scrape.ipynb` notebook and run all cells. The scanner will fetch the latest data and display the top candidates sorted by score.
