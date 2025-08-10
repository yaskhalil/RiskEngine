import math
from math import sqrt

fn read_file(path: String) -> String:
    # NOTE: open(...) may raise. We'll call it only from main() which is marked raises.
    # So we *don’t* mark this function raises to avoid duplicate effect complaints.
    # We’ll pass the file handle in from main instead (simplest).
    return ""  # (unused in this example; see main for actual open/read)

fn parse_float(s: String) -> Float64:
    try:
        return Float64(s)
    except e:
        print("[mojo] Error parsing float from: ", s, " - ", e)
        return 0.0

fn f64str(x: Float64) -> String:
    # Try the simplest form first:
    return String(x)
    

fn main() raises:
    # --- Read files (only main is raises) ---
    var f_pred = open("../data/preds.txt", "r")
    var preds_content = f_pred.read()

    var f_close = open("../data/close.txt", "r")
    var close_content = f_close.read()

    # --- Split lines ---
    var pred_lines = preds_content.split("\n")
    var close_lines = close_content.split("\n")

    # --- Parse to arrays ---
    var timestamps: List[String] = []
    var preds: List[Float64] = []
    var prices: List[Float64] = []

    var n_pred = 0
    for s in pred_lines:
        var line = String(s).strip()
        if line == "":
            continue
        var parts = line.split(",")
        if len(parts) >= 2:                     
            var ts = String(parts[0])
            var pv = parse_float(String(parts[1]))
            timestamps.append(ts)
            preds.append(pv)
            n_pred += 1

    var n_close = 0
    for s in close_lines:
        var line = String(s).strip()
        if line == "":
            continue
        var parts = line.split(",")
        if len(parts) >= 2:
            var px = parse_float(String(parts[1]))
            prices.append(px)
            n_close += 1

    print("[mojo] preds parsed: ", n_pred)
    print("[mojo] close parsed: ", n_close)

    # --- Align length safely ---
    var n = n_pred
    if n_close < n:
        n = n_close
    if len(timestamps) < n:
        n = len(timestamps)
    print("[mojo] aligned length: ", n)

    # --- Backtest (unchanged logic) ---
    var threshold = 0.05
    var pos = 0
    var cash = 1.0
    var entry_price = 0.0
    var last_equity = cash

    var equity_series: List[Float64] = []
    var out_rows: List[String] = []
    out_rows.append("timestamp,action,prediction,price,pnl,equity")

    var i = 0
    while i < n:
        var ts = timestamps[i]
        var pred = preds[i]
        var px = prices[i]
        var action = "HOLD"

        if pred > threshold and pos == 0:
            action = "BUY"
            pos = 1
            entry_price = px
        elif pred < -threshold and pos == 1:
            action = "SELL"
            var ret = (px / entry_price) - 1.0
            cash = cash * (1.0 + ret)
            pos = 0
            entry_price = px

        var eq_now = cash
        if pos == 1 and entry_price > 0.0:
            var uret = (px / entry_price) - 1.0
            eq_now = cash * (1.0 + uret)
        equity_series.append(eq_now)

        var pnl_step = eq_now - last_equity
        last_equity = eq_now

        out_rows.append(
            ts + "," +
            action + "," +
            f64str(pred) + "," +
            f64str(px) + "," +
            f64str(pnl_step) + "," +
            f64str(eq_now)
        )

        if (i % 100) == 0:
            print("[mojo] step ", i, " ts=", ts, " action=", action, " pred=", pred, " price=", px)
        i += 1

    # --- Metrics--
    var max_equity = equity_series[0]
    var max_dd = 0.0

    var j = 1
    while j < len(equity_series):
        if equity_series[j] > max_equity:
            max_equity = equity_series[j]
        var dd = (max_equity - equity_series[j]) / max_equity
        if dd > max_dd:
            max_dd = dd
        j += 1

    var rets: List[Float64] = []
    j = 1
    while j < len(equity_series):
        var r = (equity_series[j] / equity_series[j-1]) - 1.0
        rets.append(r)
        j += 1

    var mean = 0.0
    for r in rets:
        mean += r
    if len(rets) > 0:
        mean = mean / len(rets)

    var varsum = 0.0
    for r in rets:
        var d = r - mean
        varsum += d * d
    var vol = 0.0
    if len(rets) > 0:
        vol = sqrt(varsum / len(rets))

    print("[mojo] trades written: ", n)
    print("[mojo] final equity: ", equity_series[len(equity_series)-1])
    print("[mojo] max drawdown: ", max_dd)
    print("[mojo] volatility: ", vol)

    # --- Write output CSV ---
    var csv_out = String()
    for row in out_rows:
        csv_out += row + "\n"

    var out_path = "logs/kdb_trades.csv"
    var f_out = open(out_path, "w")
    f_out.write(csv_out)
    print("[mojo] wrote ", out_path)
