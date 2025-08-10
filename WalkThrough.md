# 🧠 MojoQuantBacktester

## Overview

This project simulates a quantitative trading workflow using **Modular Mojo**, a high-performance ML language, paired with **KDP+** for trade logging and performance analytics.

It includes:

* LSTM-based trade signal generation
* Modular Mojo backtesting engine
* Risk metric computation (Sharpe, volatility, drawdown)
* KDP+-formatted trade logs for querying/evaluation

---

## Tech Stack

* **Mojo**: Signal generation and fast simulation
* **Python (optional)**: For prototyping or metrics
* **KDP+**: Trade log schema and storage
* **CSV (e.g. AAPL OHLCV)**: Input data
* **NumPy / Pandas (optional)**: Risk analytics

---

## System Architecture

1. Load historical market data (e.g., AAPL.csv)
2. Preprocess using rolling normalization
3. Train LSTM model in Mojo
4. Generate "BUY", "SELL", or "HOLD" signals
5. Simulate trades through backtesting loop
6. Log trades and risk metrics to KDP+ format
7. Evaluate using metrics like Sharpe, drawdown, volatility

---

## Project Structure

* `data/`: Historical price data (CSV)
* `models/`: LSTM model definition in Mojo
* `logs/`: Output trade logs (KDP+ JSON)
* `risk/`: Risk metric calculators (e.g., Sharpe)
* `main.mojo`: Orchestrates strategy + backtest loop
* `README.md`: You're reading it

---

## Build Phases

### Phase 1 – Setup

* Install Mojo CLI from [Modular](https://www.modular.com/mojo)
* Set up file structure:

  * `data/`, `models/`, `logs/`, `risk/`, `main.mojo`
* Download AAPL OHLCV data and place it in `data/aapl.csv`

### Phase 2 – LSTM Model in Mojo

* Implement a basic LSTM in Mojo using fixed window input (e.g. 20 past bars)
* Input features: close price normalized by rolling mean/volatility
* Output target: next-day return or up/down classification
* Convert signal to `BUY`, `SELL`, or `HOLD`

### Phase 3 – Backtest Engine

* Load data and apply LSTM model to generate signals
* Track positions (e.g. long, flat) and calculate returns
* Execute a virtual trade if signal changes
* Log each trade using KDP+ schema with:

  * timestamp, action, price, reason, and associated risk stats

Example KDP+ Log:

```json
{
  "timestamp": "2025-08-06T13:00:00Z",
  "symbol": "AAPL",
  "action": "BUY",
  "price": 205.40,
  "position": "LONG",
  "reason": "LSTM:0.91",
  "risk": {
    "vol": 0.023,
    "drawdown": 0.03
  }
}
```

### Phase 4 – Risk Model

* Compute Sharpe Ratio: mean return / std deviation of returns
* Calculate max drawdown: peak-to-trough drop in equity curve
* Estimate volatility: rolling standard deviation of returns
* Output summary stats to log or CLI

### Phase 5 – Evaluation

* Parse `logs/trades.json` to aggregate metrics
* Output PnL, win/loss rate, Sharpe, drawdown
* Optional: use Python/Streamlit to chart equity curve, trade points, and histograms

---

## Example Output

```
--- Backtest Results ---
Total Trades:        104
Win Rate:            58%
Sharpe Ratio:        1.45
Max Drawdown:        -6.2%
Volatility:          2.1%
Total Return:        12.4%
```

---

## Stretch Goals

* Add strategy toggle (SMA vs LSTM)
* Add volatility filter
* Support multiple tickers or assets
* Dashboard with Plotly or Streamlit
* Upload logs to Supabase or Firebase for querying

---

## Why This Project?

* Highlights cutting-edge tooling (Mojo, KDP+)
* Demonstrates real quant skills: modeling, simulation, risk
* Aligns with Two Sigma, HRT, Citadel internship pipelines
* Optimized for resume, application portals, and GitHub

---

## Resources

* [Modular Mojo Docs](https://docs.modular.com/mojo)
* [KDP+ Spec](#) – insert link to your internal spec or JSON schema
* [Two Sigma Early ID Program](https://www.twosigma.com/join-us/events-and-programs/early-id/)
