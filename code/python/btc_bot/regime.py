"""
regime.py — BTC daily HMM regime classifier

Source:
  3-state HMM (Bull/Neutral/Bear) on BTC daily returns + realized vol
  Preprints 202603.0831 (2026)

Output:
  get_regime(df_1d) -> dict
    state      : "bull" | "neutral" | "bear"
    prob_bull  : float  (probability of bull state)
    allow_long : bool   (True = regime allows entering long)
"""

import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# State labels assigned after fit by mapping mean return → regime name
_BULL    = "bull"
_NEUTRAL = "neutral"
_BEAR    = "bear"


def _build_features(df_1d: pd.DataFrame, vol_window: int = 5) -> np.ndarray:
    """
    Two features per bar:
      1. Log daily return
      2. Realized vol = rolling std of log returns (vol_window bars)
    Drop NaNs — first vol_window rows will be empty.
    """
    log_ret = np.log(df_1d["close"] / df_1d["close"].shift(1))
    realized_vol = log_ret.rolling(vol_window).std()
    features = pd.concat([log_ret, realized_vol], axis=1).dropna()
    features.columns = ["log_ret", "realized_vol"]
    return features.values, features.index


def _label_states(model: GaussianHMM) -> dict[int, str]:
    """
    Map HMM integer state → regime label by mean log return.
    Highest mean = bull, lowest = bear, middle = neutral.
    """
    means = model.means_[:, 0]          # first feature = log return
    order = np.argsort(means)           # ascending: bear, neutral, bull
    return {
        int(order[0]): _BEAR,
        int(order[1]): _NEUTRAL,
        int(order[2]): _BULL,
    }


def get_regime(df_1d: pd.DataFrame,
               n_components: int = 3,
               min_train_bars: int = 60,
               random_state: int = 42) -> dict:
    """
    Fit a 3-state Gaussian HMM on daily BTC returns then classify latest bar.

    Parameters
    ----------
    df_1d         : DataFrame with at least 'close' column, daily bars
    n_components  : number of HMM states (default 3 = Bull/Neutral/Bear)
    min_train_bars: minimum bars required to fit (raises if too few)
    random_state  : reproducibility seed

    Returns
    -------
    dict with keys:
      state, prob_bull, prob_neutral, prob_bear, allow_long, n_bars_used
    """
    features, idx = _build_features(df_1d)

    if len(features) < min_train_bars:
        raise ValueError(
            f"Need at least {min_train_bars} bars after dropna, got {len(features)}"
        )

    model = GaussianHMM(
        n_components=n_components,
        covariance_type="diag",
        n_iter=200,
        random_state=random_state,
        tol=1e-4,
    )
    model.fit(features)

    state_map = _label_states(model)

    # Posterior probabilities for latest bar
    log_prob, posteriors = model.score_samples(features)
    last_posteriors = posteriors[-1]          # shape (n_components,)

    # Map state index → label probabilities
    prob = {label: 0.0 for label in [_BULL, _NEUTRAL, _BEAR]}
    for state_idx, label in state_map.items():
        prob[label] += float(last_posteriors[state_idx])

    # Most likely state for latest bar
    predicted_state_idx = int(model.predict(features)[-1])
    state_label = state_map[predicted_state_idx]

    # Allow long only if bull regime (bear or neutral = stay out or exit)
    allow_long = (state_label == _BULL)

    return {
        "state":        state_label,
        "prob_bull":    round(prob[_BULL],    4),
        "prob_neutral": round(prob[_NEUTRAL], 4),
        "prob_bear":    round(prob[_BEAR],    4),
        "allow_long":   allow_long,
        "n_bars_used":  len(features),
    }


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from btc_bot.data import fetch_ohlcv

    print("Fetching 1d data...")
    df_1d = fetch_ohlcv("1d", limit=200)
    print(f"  {len(df_1d)} bars fetched\n")

    result = get_regime(df_1d)

    print("=== HMM Regime (latest bar) ===")
    print(f"  State      : {result['state'].upper()}")
    print(f"  Allow long : {result['allow_long']}")
    print(f"  Prob Bull  : {result['prob_bull']:.1%}")
    print(f"  Prob Neutral: {result['prob_neutral']:.1%}")
    print(f"  Prob Bear  : {result['prob_bear']:.1%}")
    print(f"  Bars used  : {result['n_bars_used']}")
