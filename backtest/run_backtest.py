"""Point-in-time gate backtest runner. See backtest/README.md.

  python backtest/run_backtest.py --smoke       # 1 quarter, capped universe
  python backtest/run_backtest.py               # full run per config.json
  python backtest/run_backtest.py --deletions   # channel-1 S&P 500 removal study
"""

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

import gates
import sharadar

HERE = Path(__file__).parent
OUT = HERE / "out"


def load_config() -> dict:
    cfg = json.loads((HERE / "config.json").read_text())
    cfg["_hash"] = hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()[:12]
    return cfg


def universe_tickers(cfg: dict, cap: int | None) -> list[str]:
    tickers = sharadar.fetch("TICKERS", table_="SF1")
    tickers = tickers[tickers["category"].isin(cfg["universe"]["categories"])]
    names = sorted(tickers["ticker"].dropna().unique().tolist())
    return names[:cap] if cap else names


def fetch_batched(table: str, tickers: list[str], batch: int = 100, **filters) -> pd.DataFrame:
    frames = [
        sharadar.fetch(table, ticker=",".join(tickers[i:i + batch]), **filters)
        for i in range(0, len(tickers), batch)
    ]
    return pd.concat(frames, ignore_index=True)


def run_gates(cfg: dict, smoke: bool) -> None:
    quarter_ends = pd.date_range(cfg["start"], cfg["end"], freq="QE")
    if smoke:
        quarter_ends = quarter_ends[:1]
    tickers = universe_tickers(cfg, cap=200 if smoke else None)

    sf1 = fetch_batched("SF1", tickers, dimension="ARQ",
                        **{"qopts.columns": ",".join(gates.SF1_COLS)})
    prices = fetch_batched("SEP", tickers,
                           **{"date.gte": (pd.Timestamp(cfg["start"]) - pd.DateOffset(years=4)).date().isoformat(),
                              "qopts.columns": "ticker,date,closeadj"})
    bench = sharadar.fetch("SFP", ticker=cfg["benchmark_ticker"],
                           **{"qopts.columns": "ticker,date,closeadj"})

    cohorts = [gates.run_cohort(q, prices, sf1, bench, cfg) for q in quarter_ends]
    members = pd.concat([c for c in cohorts if not c.empty], ignore_index=True)
    OUT.mkdir(exist_ok=True)
    members.to_csv(OUT / f"gate-cohorts-{cfg['_hash']}.csv", index=False)
    print(summarise(members, cfg))


def summarise(members: pd.DataFrame, cfg: dict) -> str:
    scored = members.dropna(subset=["excess"])
    lines = [f"config {cfg['_hash']} · {members['asof'].nunique()} cohorts · "
             f"{len(members)} member-entries · {int(members['delisted'].sum())} deaths in-window"]
    for label, part in [("PASSED by gates", scored[scored["passed_gates"]]),
                        ("KILLED by gates", scored[~scored["passed_gates"]])]:
        if part.empty:
            lines.append(f"{label}: none")
            continue
        lines.append(
            f"{label}: n={len(part)} · mean excess {part['excess'].mean():+.1%} · "
            f"median {part['excess'].median():+.1%} · positive {(part['excess'] > 0).mean():.0%} · "
            f"deaths {int(part['delisted'].sum())}"
        )
    p, k = scored[scored["passed_gates"]], scored[~scored["passed_gates"]]
    if not p.empty and not k.empty:
        lines.append(f"GATE VALUE (passed minus killed, mean excess): {p['excess'].mean() - k['excess'].mean():+.1%}")
    lines.append("Constitution 12: this is a gate test on history, not an edge claim.")
    return "\n".join(lines)


def run_deletions(cfg: dict) -> None:
    sp = sharadar.fetch("SP500", action="removed")
    sp["date"] = pd.to_datetime(sp["date"])
    sp = sp[(sp["date"] >= cfg["start"]) & (sp["date"] <= cfg["end"])]
    tickers = sorted(sp["ticker"].dropna().unique().tolist())
    prices = fetch_batched("SEP", tickers, **{"qopts.columns": "ticker,date,closeadj"})
    bench = sharadar.fetch("SFP", ticker=cfg["benchmark_ticker"],
                           **{"qopts.columns": "ticker,date,closeadj"})
    rows = []
    for _, r in sp.iterrows():
        horizon = r["date"] + pd.DateOffset(months=cfg["horizon_months"])
        fr = gates.forward_return(prices, r["ticker"], r["date"], horizon, cfg["delisting_terminal"])
        br = gates.forward_return(bench, cfg["benchmark_ticker"], r["date"], horizon)
        rows.append({"ticker": r["ticker"], "removed": r["date"].date().isoformat(),
                     "ret": fr["ret"], "bench_ret": br["ret"],
                     "excess": fr["ret"] - br["ret"] if pd.notna(fr["ret"]) else None,
                     "delisted": fr["delisted"]})
    out = pd.DataFrame(rows)
    OUT.mkdir(exist_ok=True)
    out.to_csv(OUT / f"deletions-{cfg['_hash']}.csv", index=False)
    scored = out.dropna(subset=["excess"])
    print(f"Channel-1 removals: n={len(scored)} · mean excess {scored['excess'].mean():+.1%} · "
          f"median {scored['excess'].median():+.1%} · deaths {int(out['delisted'].sum())}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--deletions", action="store_true")
    args = ap.parse_args()
    cfg = load_config()
    if args.deletions:
        run_deletions(cfg)
    else:
        run_gates(cfg, smoke=args.smoke)
