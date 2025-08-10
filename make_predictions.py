import csv
import argparse
import os
from typing import List, Dict, Tuple

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


def log(msg: str):
    print(f"[make_predictions] {msg}")


def load_ohlcv(path: str) -> List[Dict[str, str]]:
    out = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        exp = {"timestamp", "open", "high", "low", "close", "volume"}
        if not exp.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"CSV must contain columns: {sorted(exp)}")
        for row in reader:
            try:
                out.append({
                    "timestamp": row["timestamp"],
                    "close": float(row["close"])
                })
            except Exception:
                continue
    return out


def zscore_close(rows: List[Dict[str, str]], lookback: int = 20) -> Tuple[np.ndarray, List[str]]:
    closes = np.array([r["close"] for r in rows], dtype=np.float32)
    ts = [r["timestamp"] for r in rows]
    z = []
    kept_ts = []
    for i in range(lookback, len(closes)):
        window = closes[i-lookback:i]
        m = window.mean()
        s = window.std()
        z.append(0.0 if s == 0 else (closes[i] - m) / s)
        kept_ts.append(ts[i])
    return np.array(z, dtype=np.float32), kept_ts


def build_windows(series: np.ndarray, ts: List[str], win: int = 20, horizon: int = 1):
    X, y, yts = [], [], []
    n = len(series)
    for i in range(n - win - horizon + 1):
        X.append(series[i:i+win])
        y.append(series[i+win+horizon-1])
        yts.append(ts[i+win+horizon-1])
    X = np.asarray(X, dtype=np.float32)
    y = np.asarray(y, dtype=np.float32)
    return X, y, yts


class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_size=48, num_layers=1):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        return self.fc(out)


def train_lstm(X, y, epochs=8, batch=32, lr=1e-3):
    X_t = torch.tensor(X, dtype=torch.float32).unsqueeze(-1)
    y_t = torch.tensor(y, dtype=torch.float32).unsqueeze(-1)
    ds = TensorDataset(X_t, y_t)
    dl = DataLoader(ds, batch_size=batch, shuffle=True)
    model = LSTMModel()
    crit = nn.MSELoss()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    log(f"Training LSTM: epochs={epochs}, batch={batch}, lr={lr}, samples={len(ds)}")
    model.train()
    for e in range(epochs):
        tot = 0.0
        for xb, yb in dl:
            opt.zero_grad()
            pred = model(xb)
            loss = crit(pred, yb)
            loss.backward()
            opt.step()
            tot += float(loss.item())
        log(f"epoch {e+1}/{epochs} loss={tot:.4f}")
    return model


def write_txt(path: str, lines: List[str]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for ln in lines:
            f.write(ln + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("aapl_csv", help="Path to data/aapl.csv with timestamp,open,high,low,close,volume")
    ap.add_argument("--lookback", type=int, default=20)
    ap.add_argument("--win", type=int, default=20)
    ap.add_argument("--horizon", type=int, default=1)
    ap.add_argument("--epochs", type=int, default=8)
    args = ap.parse_args()

    log(f"Loading {args.aapl_csv}")
    rows = load_ohlcv(args.aapl_csv)
    log(f"Loaded {len(rows)} rows")

    log("Computing z-score normalization")
    z, ts_z = zscore_close(rows, lookback=args.lookback)
    log(f"Normalized series length={len(z)}")

    log("Building LSTM windows")
    X, y, yts = build_windows(z, ts_z, win=args.win, horizon=args.horizon)
    log(f"Windows: X={X.shape}, y={y.shape}")

    log("Training model")
    model = train_lstm(X, y, epochs=args.epochs)

    log("Predicting")
    model.eval()
    with torch.no_grad():
        preds = model(torch.tensor(X, dtype=torch.float32).unsqueeze(-1)).squeeze(-1).numpy()

    # Align closes to yts
    ts_to_close = {r["timestamp"]: r["close"] for r in rows}
    close_lines = []
    pred_lines = []
    kept = 0
    for t, p in zip(yts, preds):
        if t in ts_to_close:
            close_lines.append(f"{t},{ts_to_close[t]}")
            pred_lines.append(f"{t},{float(p):.6f}")
            kept += 1

    log(f"Writing data/preds.txt and data/close.txt with {kept} aligned rows")
    write_txt("data/preds.txt", pred_lines)
    write_txt("data/close.txt", close_lines)
    log("Done")


if __name__ == "__main__":
    main()
