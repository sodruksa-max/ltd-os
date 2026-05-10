"""
signals.py — BTC/USDT signal computation

Sources:
  VP-MACD    : arXiv 2604.26063 (1h bars)
  MA 20/100  : Grayscale Research 2023 (1d bars, trend filter)
  Momentum   : SSRN 4080253 (1h lagged return confirmation)

Output:
  get_signal(df_1h, df_1d) -> dict
    action : "long" | "exit" | "hold"
    reason : str (which signal triggered)
    vp_macd_val, signal_val, ma20, ma100, mom_1h
"""

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# 1. VP-MACD  (arXiv 2604.26063)
# ---------------------------------------------------------------------------

def vp_macd(df: pd.DataFrame, N: int = 20, fast: int = 12,
            slow: int = 26, signal: int = 9, lam: float = 0.9):
    """
    Compute VP-MACD on OHLCV DataFrame.

    P* = volume-weighted price adjusted by intraday vol (σ) and conviction (r)
    Buy  : VP-MACD crosses above λ·Signal  (early entry)
    Sell : VP-MACD crosses below Signal    (standard exit)

    Returns: vp_macd_line, signal_line, buy (bool Series), sell (bool Series)
    """
    sigma = df["high"].sub(df["low"]).rolling(N).std() / df["close"]
    r = (
        (df["close"] - df["open"]).abs()
        / (df["high"] - df["low"]).replace(0, np.nan)
    )
    p_star = (
        (df["close"] * df["volume"] * sigma * r).rolling(N).sum()
        / df["volume"].rolling(N).sum()
    )

    ema_fast = p_star.ewm(span=fast, adjust=False).mean()
    ema_slow = p_star.ewm(span=slow, adjust=False).mean()
    vp_line  = ema_fast - ema_slow
    sig_line = vp_line.ewm(span=signal, adjust=False).mean()

    buy  = (vp_line.shift(1) <= lam * sig_line.shift(1)) & (vp_line > lam * sig_line)
    sell = (vp_line.shift(1) >= sig_line.shift(1)) & (vp_line < sig_line)

    return vp_line, sig_line, buy, sell


# ---------------------------------------------------------------------------
# 2. MA 20/100 daily trend filter  (Grayscale Research 2023)
# ---------------------------------------------------------------------------

def ma_trend(df_1d: pd.DataFrame) -> pd.Series:
    """
    Bull = close > MA20 AND MA20 > MA100
    Returns bool Series (daily) — True = bull trend active
    Requires at least 100 bars.
    """
    ma20  = df_1d["close"].rolling(20).mean()
    ma100 = df_1d["close"].rolling(100).mean()
    return (df_1d["close"] > ma20) & (ma20 > ma100)


# ---------------------------------------------------------------------------
# 3. Intraday momentum confirmation  (SSRN 4080253)
# ---------------------------------------------------------------------------

def momentum_1h(df_1h: pd.DataFrame, lookback: int = 1) -> pd.Series:
    """
    1h lagged return — positive = momentum favors long.
    lookback=1 → ใช้ return ของชั่วโมงที่แล้ว
    Returns float Series (positive = bullish, negative = bearish)
    """
    return df_1h["close"].pct_change(lookback)


# ---------------------------------------------------------------------------
# 4. Combined signal
# ---------------------------------------------------------------------------

def get_signal(df_1h: pd.DataFrame, df_1d: pd.DataFrame) -> dict:
    """
    รวม 3 signals แล้วคืนคำสั่ง action ของแท่งล่าสุด

    Logic:
      LONG : VP-MACD buy crossover
             AND MA trend = Bull (1d)
             AND 1h momentum >= 0 (lagged return ไม่ติดลบ)

      EXIT : VP-MACD sell crossover
             OR MA trend = Bear (1d) หลังจาก hold อยู่

      HOLD : ไม่มี crossover เกิดขึ้น — รักษา position เดิม

    Execute at OPEN of next bar (ไม่ใช่ close ปัจจุบัน)
    """
    # --- VP-MACD (1h) ---
    vp_line, sig_line, buy_cross, sell_cross = vp_macd(df_1h)

    # --- MA trend (1d) — ใช้ค่าล่าสุดที่ confirmed ---
    trend = ma_trend(df_1d)
    is_bull_daily = bool(trend.iloc[-1])

    # --- Intraday momentum (1h) ---
    mom = momentum_1h(df_1h)
    mom_now = float(mom.iloc[-1])

    # --- ค่าล่าสุด ---
    vp_val  = float(vp_line.iloc[-1])
    sig_val = float(sig_line.iloc[-1])
    is_buy  = bool(buy_cross.iloc[-1])
    is_sell = bool(sell_cross.iloc[-1])
    ma20    = float(df_1d["close"].rolling(20).mean().iloc[-1])
    ma100   = float(df_1d["close"].rolling(100).mean().iloc[-1])

    # --- Decision ---
    if is_sell or not is_bull_daily:
        action = "exit"
        if is_sell and not is_bull_daily:
            reason = "VP-MACD sell crossover + daily trend Bear"
        elif is_sell:
            reason = "VP-MACD sell crossover"
        else:
            reason = "Daily trend flipped Bear (MA20 < MA100 or price < MA20)"

    elif is_buy and is_bull_daily and mom_now >= 0:
        action = "long"
        reason = f"VP-MACD buy crossover | daily Bull | 1h mom={mom_now:+.3%}"

    elif is_buy and is_bull_daily and mom_now < 0:
        action = "hold"
        reason = f"VP-MACD buy crossover BUT 1h momentum negative ({mom_now:+.3%}) — wait next bar"

    else:
        action = "hold"
        reason = "No crossover — maintain current position"

    return {
        "action":      action,
        "reason":      reason,
        "vp_macd_val": round(vp_val, 4),
        "signal_val":  round(sig_val, 4),
        "ma20":        round(ma20, 2),
        "ma100":       round(ma100, 2),
        "is_bull":     is_bull_daily,
        "mom_1h":      round(mom_now, 6),
    }


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from btc_bot.data import fetch_ohlcv

    print("Fetching data...")
    df_1h = fetch_ohlcv("1h", limit=200)
    df_1d = fetch_ohlcv("1d", limit=150)

    print(f"  1h bars: {len(df_1h)} | 1d bars: {len(df_1d)}\n")

    sig = get_signal(df_1h, df_1d)

    print("=== Signal (latest bar) ===")
    print(f"  Action  : {sig['action'].upper()}")
    print(f"  Reason  : {sig['reason']}")
    print(f"  VP-MACD : {sig['vp_macd_val']} vs Signal {sig['signal_val']}")
    print(f"  MA20    : ${sig['ma20']:,.2f} | MA100: ${sig['ma100']:,.2f}")
    print(f"  Bull?   : {sig['is_bull']}")
    print(f"  Mom 1h  : {sig['mom_1h']:+.4%}")
