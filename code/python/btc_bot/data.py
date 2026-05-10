"""
data.py — BTC/USDT OHLCV fetcher via Binance (ccxt public API)

ไม่ต้องการ API key สำหรับ OHLCV (public endpoint)
API key ต้องการเฉพาะตอนสั่ง order (executor.py)

Usage:
    from btc_bot.data import fetch_ohlcv, fetch_price

    df_1h = fetch_ohlcv("1h", limit=200)   # 200 แท่ง 1 ชั่วโมง
    df_1d = fetch_ohlcv("1d", limit=100)   # 100 วัน
    price  = fetch_price()                  # ราคา BTC ล่าสุด
"""

import time
import pandas as pd
import ccxt

SYMBOL   = "BTC/USDT"
EXCHANGE = "binance"

_exchange: ccxt.Exchange | None = None


def _get_exchange() -> ccxt.Exchange:
    global _exchange
    if _exchange is None:
        _exchange = ccxt.binance({
            "enableRateLimit": True,
            "options": {"defaultType": "spot"},
        })
    return _exchange


def fetch_ohlcv(timeframe: str = "1h", limit: int = 200) -> pd.DataFrame:
    """
    ดึง OHLCV จาก Binance และคืน DataFrame พร้อมใช้

    timeframe: "1m","5m","15m","1h","4h","1d"
    limit:     จำนวนแท่ง (สูงสุด 1000)
    columns:   timestamp, open, high, low, close, volume
    """
    ex = _get_exchange()
    raw = ex.fetch_ohlcv(SYMBOL, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df = df.set_index("timestamp").sort_index()
    df = df.astype(float)
    return df


def fetch_price() -> float:
    """คืนราคา BTC/USDT ปัจจุบัน (last trade price)"""
    ex = _get_exchange()
    ticker = ex.fetch_ticker(SYMBOL)
    return float(ticker["last"])


def fetch_multi(timeframes: list[str], limit: int = 200) -> dict[str, pd.DataFrame]:
    """
    ดึงหลาย timeframe พร้อมกัน
    คืน dict: {"1h": df_1h, "1d": df_1d}
    """
    result = {}
    for tf in timeframes:
        result[tf] = fetch_ohlcv(tf, limit=limit)
        time.sleep(0.2)   # เว้นช่วง rate limit เล็กน้อย
    return result


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== BTC/USDT data test ===\n")

    print("Latest price:")
    price = fetch_price()
    print(f"  BTC/USDT = ${price:,.2f}\n")

    for tf in ["1h", "1d"]:
        print(f"OHLCV {tf} (last 5 bars):")
        df = fetch_ohlcv(tf, limit=50)
        print(df.tail(5).to_string())
        print(f"  -> {len(df)} bars | latest close: ${df['close'].iloc[-1]:,.2f}\n")
