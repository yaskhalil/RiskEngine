# 🧠 MojoQuantBacktester

## Overview
This project simulates a **quantitative trading workflow** using **Modular Mojo** for high-performance computation, paired with **KDB+** for trade logging and performance analytics.

The workflow includes:
- LSTM-based trade signal generation (Python)
- Modular Mojo backtesting engine
- Risk metric computation (Sharpe, volatility, drawdown)
- KDB+-formatted trade logs for querying/evaluation

---

## Tech Stack
- **Mojo** – High-performance backtesting engine and risk metrics
- **Python** – LSTM model training and prediction generation
- **KDB+** – Trade logging and querying
- **CSV Data** – Historical OHLCV price data (e.g., AAPL)
- **NumPy / PyTorch** – Data processing and model training

---

## System Architecture
1. **Data Load** – Historical CSV (e.g., `data/aapl.csv`)
2. **Preprocessing** – Rolling z-score normalization
3. **LSTM Model (Python)** – Train model to forecast returns
4. **Signal Generation** – Output `BUY`, `SELL`, or `HOLD`
5. **Backtesting (Mojo)** – Simulate trades and track equity
6. **Risk Metrics** – Compute Sharpe, volatility, drawdown
7. **KDB+ Logging** – Save trade logs in structured format

---

## Project Structure
data/ # Historical CSV price data
logs/ # Output trade logs (CSV / JSON)
life/ # Mojo backtesting files
make_predictions.py # Python script for LSTM model
backtest.mojo # Mojo backtest engine
README.md # Project documentation

---

## How to Run

### 1️⃣ Generate Predictions (Python)
```bash
python make_predictions.py data/aapl.csv
Outputs data/preds.txt containing predictions with timestamps.
2️⃣ Run Backtest (Mojo)
mojo life/backtest.mojo
Reads data/preds.txt and data/close.txt
Outputs performance metrics and saves logs/kdb_trades.csv
Example Output
[mojo] preds parsed:  210
[mojo] close parsed:  210
[mojo] aligned length:  210
[mojo] step  0  ts= 2025-06-11  action= HOLD  pred= -0.912047  price= 198.78
[mojo] step  100  ts= 2025-01-16  action= HOLD  pred= -0.739704  price= 228.26
[mojo] trades written:  210
[mojo] final equity:  0.8780
[mojo] max drawdown:  0.1792
[mojo] volatility:  0.0107
[mojo] wrote logs/kdb_trades.csv
Metrics Computed
Final Equity – Ending capital after backtest
Max Drawdown – Largest equity peak-to-trough decline
Volatility – Standard deviation of returns
PnL per Trade – Profit or loss of each execution
Future Improvements
Integrate direct KDB+ write from Mojo
Add alternative models (SMA, momentum)
Support multi-asset portfolios
Add real-time streaming mode
Why This Project?
Showcases Mojo + KDB+ integration
Demonstrates end-to-end quant workflow
Optimized for Two Sigma / HRT / Citadel internship portfolios
Combines AI modeling and risk management