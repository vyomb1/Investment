"""Offline proof of the backtest's honesty rules, on synthetic data with known answers.

No API key, no network: these tests pin the point-in-time visibility rule, the
restatement rule, survivorship handling (a dead ticker scoring its loss),
F-score arithmetic, each trap gate, and the cohort scorer.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
import gates  # noqa: E402

CFG = {
    "horizon_months": 12,
    "benchmark_ticker": "SPY",
    "delisting_terminal": "last_price",
    "channel4": {"low_window_years": 3, "within_pct_of_low": 0.15,
                 "max_netdebt_to_trough_ocf": 3.0, "min_fscore": 5},
    "traps": {"peak_margin_multiple": 1.5, "leverage_max_netdebt_to_ebitda": 4.0,
              "ice_years_declining": 3},
}


def quarters(ticker, n, *, netinc, ncfo, revenue, gp, assets, assetsc, liabilitiesc,
             debt, cashneq, ebitda, sharesbas, start="2018-03-31", lag_days=45):
    """Build n ARQ quarters; each value may be a scalar or a length-n list."""
    dates = pd.date_range(start, periods=n, freq="QE")
    def col(v):
        return list(v) if isinstance(v, (list, tuple)) else [v] * n
    return pd.DataFrame({
        "ticker": ticker, "calendardate": dates,
        "datekey": dates + pd.Timedelta(days=lag_days),
        "netinc": col(netinc), "ncfo": col(ncfo), "revenue": col(revenue),
        "gp": col(gp), "assets": col(assets), "assetsc": col(assetsc),
        "liabilitiesc": col(liabilitiesc), "debt": col(debt), "cashneq": col(cashneq),
        "ebitda": col(ebitda), "sharesbas": col(sharesbas),
    })


def good_nine_quarters(ticker="GOOD"):
    """Nine quarters engineered so all nine Piotroski signals are true."""
    return quarters(
        ticker, 9,
        netinc=[10, 10, 10, 10, 20, 20, 20, 20, 30],
        ncfo=[15, 15, 15, 15, 25, 25, 25, 25, 35],
        revenue=[400] * 5 + [440] * 4,
        gp=[200] * 5 + [264] * 4,
        assets=1000, assetsc=300,
        liabilitiesc=[150] * 5 + [100] * 4,
        debt=[200] * 5 + [100] * 4, cashneq=50,
        ebitda=[30] * 9, sharesbas=100,
    )


def flat_prices(ticker, start, end, price):
    dates = pd.bdate_range(start, end)
    return pd.DataFrame({"ticker": ticker, "date": dates, "closeadj": price})


# ---------------------------------------------------------------- PIT honesty

def test_future_filings_are_invisible():
    sf1 = good_nine_quarters()
    pit = gates.pit_quarters(sf1, "2019-06-30")  # Q6 filed 2019-08-14 -> invisible
    assert pd.Timestamp("2019-06-30") not in set(pit["calendardate"])
    assert len(pit) == 5


def test_restatement_never_wins():
    sf1 = good_nine_quarters()
    restated = sf1.iloc[[0]].copy()
    restated["netinc"] = 999          # a "cleaner" number filed a year later
    restated["datekey"] = pd.Timestamp("2019-05-01")
    pit = gates.pit_quarters(pd.concat([sf1, restated]), "2020-12-31")
    q1 = pit[pit["calendardate"] == pd.Timestamp("2018-03-31")]
    assert q1["netinc"].iloc[0] == 10  # the original filing, not the restatement


# ---------------------------------------------------------------- F-score

def test_fscore_all_nine_signals():
    pit = gates.pit_quarters(good_nine_quarters(), "2021-12-31")
    assert gates.fscore(pit) == 9.0


def test_fscore_dilution_costs_a_point():
    sf1 = good_nine_quarters()
    sf1.loc[sf1.index[-1], "sharesbas"] = 110  # new shares issued
    pit = gates.pit_quarters(sf1, "2021-12-31")
    assert gates.fscore(pit) == 8.0


def test_fscore_needs_eight_quarters():
    pit = gates.pit_quarters(good_nine_quarters().head(6), "2021-12-31")
    assert np.isnan(gates.fscore(pit))


# ---------------------------------------------------------------- channel 4

def test_channel4_passes_near_low_survivor():
    sf1 = good_nine_quarters("SURV")
    prices = flat_prices("SURV", "2018-01-01", "2020-06-30", 10.0)
    prices.loc[prices.index[-1], "closeadj"] = 11.0  # within 15% of the 10.0 low
    out = gates.channel4_screen(prices, gates.pit_quarters(sf1, "2020-06-30"),
                                "2020-06-30", CFG["channel4"])
    row = out[out["ticker"] == "SURV"].iloc[0]
    assert row["near_low"] and row["survivable"] and row["passed_screen"]


def test_channel4_rejects_price_far_from_low():
    sf1 = good_nine_quarters("HIGH")
    prices = flat_prices("HIGH", "2018-01-01", "2020-06-30", 10.0)
    prices.loc[prices.index[-1], "closeadj"] = 20.0  # 2x the low
    out = gates.channel4_screen(prices, gates.pit_quarters(sf1, "2020-06-30"),
                                "2020-06-30", CFG["channel4"])
    assert not out[out["ticker"] == "HIGH"]["passed_screen"].iloc[0]


def test_channel4_rejects_unsurvivable_netdebt():
    sf1 = good_nine_quarters("DEBT")
    sf1["debt"] = 500
    sf1["cashneq"] = 0                # netdebt 500 vs trough 4q OCF 60-80 -> way over 3x
    prices = flat_prices("DEBT", "2018-01-01", "2020-06-30", 10.0)
    out = gates.channel4_screen(prices, gates.pit_quarters(sf1, "2020-06-30"),
                                "2020-06-30", CFG["channel4"])
    row = out[out["ticker"] == "DEBT"].iloc[0]
    assert not row["survivable"] and not row["passed_screen"]


# ---------------------------------------------------------------- trap gates

def test_peak_earnings_trap_fires():
    sf1 = quarters("PEAK", 12, netinc=[20] * 8 + [60] * 4, ncfo=25,
                   revenue=400, gp=200, assets=1000, assetsc=300, liabilitiesc=150,
                   debt=0, cashneq=50, ebitda=30, sharesbas=100)
    out = gates.trap_gates(gates.pit_quarters(sf1, "2022-12-31"), CFG["traps"])
    assert "peak_earnings" in out.iloc[0]["fired_traps"]


def test_leverage_mirage_trap_fires():
    sf1 = good_nine_quarters("LEV")
    sf1["debt"] = 600
    sf1["cashneq"] = 100              # netdebt 500 / ebitda_ttm 120 > 4x
    out = gates.trap_gates(gates.pit_quarters(sf1, "2021-12-31"), CFG["traps"])
    assert "leverage_mirage" in out.iloc[0]["fired_traps"]


def test_melting_ice_cube_trap_fires():
    rev = [1000 - 15 * i for i in range(17)]  # 3+ straight years of decay (needs 13 TTM points)
    sf1 = quarters("ICE", 17, netinc=10, ncfo=15, revenue=rev,
                   gp=[r / 2 for r in rev], assets=1000, assetsc=300, liabilitiesc=150,
                   debt=0, cashneq=50, ebitda=30, sharesbas=100)
    out = gates.trap_gates(gates.pit_quarters(sf1, "2023-12-31"), CFG["traps"])
    assert "melting_ice_cube" in out.iloc[0]["fired_traps"]


def test_clean_name_fires_nothing():
    out = gates.trap_gates(gates.pit_quarters(good_nine_quarters(), "2021-12-31"), CFG["traps"])
    assert out.iloc[0]["fired_traps"] == "" and not out.iloc[0]["killed"]


# ------------------------------------------------------- survivorship honesty

def test_dead_ticker_stays_and_scores_its_loss():
    px = flat_prices("DEADCO", "2019-01-02", "2020-06-30", 10.0)
    px.loc[px.index[-1], "closeadj"] = 2.0   # last trade before death
    fr = gates.forward_return(px, "DEADCO", "2020-03-31", "2021-03-31")
    assert fr["delisted"] and fr["ret"] == pytest.approx(-0.8)


def test_zero_terminal_mode_scores_total_loss():
    px = flat_prices("DEADCO", "2019-01-02", "2020-06-30", 10.0)
    fr = gates.forward_return(px, "DEADCO", "2020-03-31", "2021-03-31",
                              delisting_terminal="zero")
    assert fr["delisted"] and fr["ret"] == -1.0


def test_entry_is_next_trading_day_never_signal_day():
    px = flat_prices("T", "2020-03-25", "2021-04-30", 10.0)
    px.loc[px["date"] == "2020-04-01", "closeadj"] = 8.0   # first day after as-of
    fr = gates.forward_return(px, "T", "2020-03-31", "2021-03-31")
    assert fr["entry_date"] == "2020-04-01"
    assert fr["ret"] == pytest.approx(10.0 / 8.0 - 1)


# ------------------------------------------------------------- cohort scorer

def test_cohort_splits_passed_and_killed_and_scores_both():
    surv, lev = good_nine_quarters("SURV"), good_nine_quarters("LEV")
    lev["debt"], lev["cashneq"], lev["ebitda"] = 200, 30, 10
    # netdebt 170 vs trough OCF 60 -> survivable (2.8x <= 3x), but 170/40 EBITDA -> mirage fires
    sf1 = pd.concat([surv, lev])
    prices = pd.concat([flat_prices(t, "2018-01-01", "2021-07-31", 10.0) for t in ("SURV", "LEV")])
    bench = flat_prices("SPY", "2018-01-01", "2021-07-31", 100.0)
    out = gates.run_cohort("2020-06-30", prices, sf1, bench, CFG)
    assert set(out["ticker"]) == {"SURV", "LEV"}
    assert out.set_index("ticker").loc["SURV", "passed_gates"]
    assert not out.set_index("ticker").loc["LEV", "passed_gates"]
    assert out["excess"].notna().all()       # killed names are scored too - that's the point
