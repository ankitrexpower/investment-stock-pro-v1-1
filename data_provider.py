import pandas as pd
import yfinance as yf
from typing import Dict, Any, List

MIN_INST_HOLDING = 5.0
SMA_LEN = 121
CCI_LEN = 20
CCI_LEVEL = -192
TIMEFRAMES = {"D": "1d", "W": "1wk", "M": "1mo"}

def sample_holdings() -> pd.DataFrame:
    return pd.DataFrame([
        {"Stock":"RELIANCE", "FII": 21.90, "DII": 17.20},
        {"Stock":"HAL", "FII": 11.50, "DII": 9.80},
        {"Stock":"BEL", "FII": 17.10, "DII": 13.90},
        {"Stock":"TCS", "FII": 12.40, "DII": 7.30},
        {"Stock":"ABC", "FII": 2.00, "DII": 1.50},
    ])

def nse_symbol(stock: str) -> str:
    s = str(stock).strip().upper()
    if s.endswith(".NS"):
        return s
    return f"{s}.NS"

def cci(df: pd.DataFrame, length: int = 20) -> pd.Series:
    tp = (df["High"] + df["Low"] + df["Close"]) / 3
    sma = tp.rolling(length).mean()
    mad = tp.rolling(length).apply(lambda x: (abs(x - x.mean())).mean(), raw=False)
    return (tp - sma) / (0.015 * mad)

def scan_one_symbol(stock: str, tf_name: str, interval: str) -> Dict[str, Any]:
    ticker = nse_symbol(stock)
    try:
        hist = yf.download(ticker, period="3y", interval=interval, progress=False, auto_adjust=False)
        if hist.empty or len(hist) < SMA_LEN + CCI_LEN:
            return {"stock": stock, "tf": tf_name, "status": "NO DATA", "error": "insufficient data"}
        if isinstance(hist.columns, pd.MultiIndex):
            hist.columns = hist.columns.get_level_values(0)
        hist["SMA121"] = hist["Close"].rolling(SMA_LEN).mean()
        hist["CCI20"] = cci(hist, CCI_LEN)
        last = hist.dropna().iloc[-1]
        close = float(last["Close"])
        sma121 = float(last["SMA121"])
        cci20 = float(last["CCI20"])
        is_setup = close > sma121 and cci20 <= CCI_LEVEL
        return {
            "stock": stock,
            "tf": tf_name,
            "close": round(close, 2),
            "sma121": round(sma121, 2),
            "cci": round(cci20, 2),
            "status": "SETUP" if is_setup else "NO SETUP",
        }
    except Exception as e:
        return {"stock": stock, "tf": tf_name, "status": "ERROR", "error": str(e)[:180]}

def run_scan(holdings_df: pd.DataFrame) -> Dict[str, Any]:
    required = {"Stock", "FII", "DII"}
    missing = required - set(holdings_df.columns)
    if missing:
        return {"error": f"Missing columns: {', '.join(missing)}. Required: Stock,FII,DII"}

    df = holdings_df.copy()
    df["FII"] = pd.to_numeric(df["FII"], errors="coerce").fillna(0)
    df["DII"] = pd.to_numeric(df["DII"], errors="coerce").fillna(0)
    df["Total"] = df["FII"] + df["DII"]
    qualified = df[df["Total"] >= MIN_INST_HOLDING].copy()

    results: List[Dict[str, Any]] = []
    for _, row in qualified.iterrows():
        stock = str(row["Stock"]).strip().upper()
        total = round(float(row["Total"]), 2)
        for tf_name, interval in TIMEFRAMES.items():
            r = scan_one_symbol(stock, tf_name, interval)
            r["fii"] = round(float(row["FII"]), 2)
            r["dii"] = round(float(row["DII"]), 2)
            r["total_holding"] = total
            results.append(r)

    setups = [r for r in results if r.get("status") == "SETUP"]
    return {
        "app": "INVESTMENT STOCK PRO V2.0 REAL",
        "filter": "FII+DII >= 5%",
        "logic": "D/W/M: Close > SMA121 and CCI20 <= -192",
        "total_stocks": int(len(df)),
        "qualified_stocks": int(len(qualified)),
        "total_setup": int(len(setups)),
        "setups": setups,
        "all_results": results,
    }
