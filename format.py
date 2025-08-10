import sys, re, datetime as dt

MONTHS = {m:i for i,m in enumerate(
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], start=1)}

def parse_date(s):
    # "Aug 8, 2025" -> "2025-08-08"
    m, d, y = s.replace(',', '').split()
    return f"{y}-{MONTHS[m]:02d}-{int(d):02d}"

def clean_num(s):
    # remove thousands commas
    return s.replace(',', '')

def main():
    print("timestamp,open,high,low,close,volume")
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith("Date") or "Dividend" in line:
            continue
        # split on tabs or multiple spaces
        parts = re.split(r'\s{2,}|\t', line)
        if len(parts) < 7:  # try fallback: single spaces
            parts = re.split(r'\s+', line)
        # Expect: Date Open High Low Close AdjClose Volume
        if len(parts) >= 7:
            date, open_, high, low, close, _adj, vol = parts[:7]
            try:
                ts = parse_date(date)
                print(",".join([ts,
                                clean_num(open_),
                                clean_num(high),
                                clean_num(low),
                                clean_num(close),
                                clean_num(vol)]))
            except Exception:
                continue

if __name__ == "__main__":
    main()
