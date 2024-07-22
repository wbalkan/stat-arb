# stat-arb

Statistical arbitrage script to analyze stock historical data and backtest long/short entry and exit signals. Current iteration opens a position at 1.7x mean residual and closes position at mean residual. Constants and securities used can be adjusted for further testing. Note yfinance api data is limited to 1m intervals at highest frequency. Values normalized around 100 points.

## example output:
![image](https://github.com/wbalkan/stat-arb/assets/96204851/8ca2f934-90fa-43e7-ac00-ff3a9499f65b)

RTX price (red line) with long and short buy/sell signals plotted against average of LMT and RTX (black line). Holding results in loss: -1.319808317060179 points (normalized) while statistical arbitrage strategy results in gain: +11.924843796603668 points (normalized)
