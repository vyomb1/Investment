"""Mechanical gates of the v3.2 funnel, in point-in-time form.

Implements, honestly and only, what has a mechanical form:
  - channel-4 screen (spec §5 verbatim): within 15% of 3-yr low AND
    net debt / trough cash flow sane AND F-score >= min
  - §6.4 trap proxies: peak-earnings, melting ice cube, leverage mirage
    (trap 4, "value with no unlock", is judgment - deliberately absent)

Point-in-time rules (see backtest/README.md):
  - a fundamentals row is visible only from its datekey (filing date)
  - as-reported: earliest datekey per (ticker, quarter) wins, never a restatement
  - dead tickers stay in cohorts and score their losses

Expected frames (Sharadar column names):
  sf1:    ticker, calendardate, datekey, netinc, ncfo, revenue, gp, assets,
          assetsc, liabilitiesc, debt, cashneq, ebitda, sharesbas   (dimension ARQ)
  prices: ticker, date, closeadj
"""

import numpy as np
import pandas as pd

SF1_COLS = [
    "ticker", "calendardate", "datekey", "netinc", "ncfo", "revenue", "gp",
    "assets", "assetsc", "liabilitiesc", "debt", "cashneq", "ebitda", "sharesbas",
]


def pit_quarters(sf1: pd.DataFrame, asof) -> pd.DataFrame:
    """As-reported snapshot at `asof`: only rows already filed, original filing wins."""
    asof = pd.Timestamp(asof)
    df = sf1.copy()
    df["calendardate"] = pd.to_datetime(df["calendardate"])
    df["datekey"] = pd.to_datetime(df["datekey"])
    df = df[df["datekey"] <= asof]                       # the look-ahead rule
    df = df.sort_values(["ticker", "calendardate", "datekey"])
    df = df.drop_duplicates(["ticker", "calendardate"], keep="first")  # the restatement rule
    return df.sort_values(["ticker", "calendardate"]).reset_index(drop=True)


def _with_ttm(g: pd.DataFrame) -> pd.DataFrame:
    g = g.sort_values("calendardate").copy()
    for col in ("netinc", "ncfo", "revenue", "gp", "ebitda"):
        g[f"{col}_ttm"] = g[col].rolling(4).sum()
    g["netdebt"] = g["debt"] - g["cashneq"]
    return g


def fscore(g: pd.DataFrame) -> float:
    """Piotroski F-score on the latest quarter of one ticker's PIT frame.

    TTM at t vs TTM one year earlier (t-4 quarters). NaN if < 8 quarters.
    """
    g = _with_ttm(g)
    if len(g) < 8:
        return np.nan
    now, yr = g.iloc[-1], g.iloc[-5]
    roa_now = now["netinc_ttm"] / now["assets"]
    roa_yr = yr["netinc_ttm"] / yr["assets"]
    checks = [
        roa_now > 0,
        now["ncfo_ttm"] > 0,
        roa_now > roa_yr,
        now["ncfo_ttm"] > now["netinc_ttm"],
        (now["debt"] / now["assets"]) < (yr["debt"] / yr["assets"]),
        (now["assetsc"] / now["liabilitiesc"]) > (yr["assetsc"] / yr["liabilitiesc"]),
        now["sharesbas"] <= yr["sharesbas"],
        (now["gp_ttm"] / now["revenue_ttm"]) > (yr["gp_ttm"] / yr["revenue_ttm"]),
        (now["revenue_ttm"] / now["assets"]) > (yr["revenue_ttm"] / yr["assets"]),
    ]
    return float(sum(bool(c) for c in checks))


def channel4_screen(prices: pd.DataFrame, pit: pd.DataFrame, asof, cfg: dict) -> pd.DataFrame:
    """Spec §5 channel 4: within 15% of 3-yr low AND survivability AND F-score >= min.

    Returns one row per ticker with pass/fail and the three components.
    """
    asof = pd.Timestamp(asof)
    px = prices.copy()
    px["date"] = pd.to_datetime(px["date"])
    px = px[(px["date"] <= asof) & (px["date"] > asof - pd.DateOffset(years=cfg["low_window_years"]))]

    rows = []
    for ticker, ppx in px.groupby("ticker"):
        g = pit[pit["ticker"] == ticker]
        if g.empty or ppx.empty:
            continue
        last_px = ppx.sort_values("date")["closeadj"].iloc[-1]
        low = ppx["closeadj"].min()
        near_low = last_px <= low * (1 + cfg["within_pct_of_low"])

        gt = _with_ttm(g)
        netdebt = gt["netdebt"].iloc[-1]
        trough = gt["ncfo_ttm"].dropna().tail(12).min() if gt["ncfo_ttm"].notna().any() else np.nan
        survivable = bool(
            netdebt <= 0
            or (pd.notna(trough) and trough > 0 and netdebt / trough <= cfg["max_netdebt_to_trough_ocf"])
        )
        f = fscore(g)
        f_ok = pd.notna(f) and f >= cfg["min_fscore"]
        rows.append({
            "ticker": ticker, "near_low": bool(near_low), "survivable": survivable,
            "fscore": f, "passed_screen": bool(near_low and survivable and f_ok),
        })
    return pd.DataFrame(rows)


def trap_gates(pit: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """§6.4 mechanical proxies. One row per ticker; fired trap => downstream kill."""
    rows = []
    for ticker, g in pit.groupby("ticker"):
        gt = _with_ttm(g)
        now = gt.iloc[-1]

        margins = (gt["netinc_ttm"] / gt["revenue_ttm"]).dropna().tail(20)
        peak = bool(
            len(margins) >= 8 and now["netinc_ttm"] > 0 and margins.median() > 0
            and (now["netinc_ttm"] / now["revenue_ttm"]) > cfg["peak_margin_multiple"] * margins.median()
        )

        rev = gt["revenue_ttm"].dropna()
        n = cfg["ice_years_declining"]
        ice = bool(
            len(rev) >= 4 * n + 1
            and all(rev.iloc[-1 - 4 * k] < rev.iloc[-5 - 4 * k] for k in range(n))
        )

        ebitda = now["ebitda_ttm"]
        leverage = bool(
            now["netdebt"] > 0
            and (pd.isna(ebitda) or ebitda <= 0 or now["netdebt"] / ebitda > cfg["leverage_max_netdebt_to_ebitda"])
        )

        fired = [name for name, hit in
                 [("peak_earnings", peak), ("melting_ice_cube", ice), ("leverage_mirage", leverage)] if hit]
        rows.append({"ticker": ticker, "fired_traps": ",".join(fired), "killed": bool(fired)})
    return pd.DataFrame(rows)


def forward_return(prices: pd.DataFrame, ticker: str, asof, horizon_end,
                   delisting_terminal: str = "last_price") -> dict:
    """Entry next trading day after `asof`; exit at horizon or at death.

    The dead stay in: a ticker whose prices stop before the horizon is scored
    to its last trade (default) or to zero (bankruptcy-conservative mode).
    """
    asof, horizon_end = pd.Timestamp(asof), pd.Timestamp(horizon_end)
    px = prices[prices["ticker"] == ticker].copy()
    px["date"] = pd.to_datetime(px["date"])
    px = px.sort_values("date")

    entry_rows = px[px["date"] > asof]                    # never the signal day
    if entry_rows.empty:
        return {"ret": np.nan, "delisted": True, "entry_date": None}
    entry = entry_rows.iloc[0]
    window = px[(px["date"] >= entry["date"]) & (px["date"] <= horizon_end)]
    last = window.iloc[-1]
    delisted = px["date"].max() < horizon_end             # traded its last day inside the window
    exit_px = 0.0 if (delisted and delisting_terminal == "zero") else last["closeadj"]
    return {
        "ret": exit_px / entry["closeadj"] - 1.0,
        "delisted": bool(delisted),
        "entry_date": entry["date"].date().isoformat(),
    }


def run_cohort(asof, prices, sf1, bench_prices, cfg: dict) -> pd.DataFrame:
    """One quarter-end: screen -> traps -> score everyone, passed and killed alike."""
    asof = pd.Timestamp(asof)
    horizon_end = asof + pd.DateOffset(months=cfg["horizon_months"])
    pit = pit_quarters(sf1, asof)
    screen = channel4_screen(prices, pit, asof, cfg["channel4"])
    candidates = screen[screen["passed_screen"]]
    if candidates.empty:
        return pd.DataFrame()
    traps = trap_gates(pit[pit["ticker"].isin(candidates["ticker"])], cfg["traps"])
    bench = forward_return(bench_prices, cfg["benchmark_ticker"], asof, horizon_end)

    rows = []
    for _, c in candidates.merge(traps, on="ticker").iterrows():
        fr = forward_return(prices, c["ticker"], asof, horizon_end, cfg["delisting_terminal"])
        rows.append({
            "asof": asof.date().isoformat(), "ticker": c["ticker"],
            "passed_gates": not c["killed"], "fired_traps": c["fired_traps"],
            "fscore": c["fscore"], "ret": fr["ret"], "bench_ret": bench["ret"],
            "excess": (fr["ret"] - bench["ret"]) if pd.notna(fr["ret"]) else np.nan,
            "delisted": fr["delisted"],
        })
    return pd.DataFrame(rows)
