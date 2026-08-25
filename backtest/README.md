# Point-in-time gate backtest

**Spec:** open item 3 (§14 — Sharadar/Norgate gate backtest), greenlit by Vyom 25 Aug 2026.
**What it tests:** whether the system's *mechanical* rules — the channel-4 screen and the §6.4 trap-filter kills — would have added value historically, scored honestly. It does **not** test the judgment layers (thesis, red team, sizing): those have no mechanical form, and pretending otherwise would be backtest theatre. Per Constitution 12, no backtest result is an edge claim — the edge test is the live ledger, January 2027.

## The two lies ordinary databases tell, and the countermeasures coded here

1. **They delete the dead.** Bankrupt companies vanish, so a survivor-only backtest is never punished for the picks that went to zero — and this system's hunting ground (small, distressed) is exactly where deaths cluster, so the bias hits hardest here. **Countermeasure:** the universe includes delisted tickers (Sharadar keeps them); a cohort member that dies inside the scoring window stays in the cohort and takes its loss. Delisting terminal value is a pinned convention (below), never a silent drop.
2. **They overwrite the past.** Restated financials replace the originals, so the backtest "knows" clean numbers months before any real investor could. **Countermeasure:** as-reported dimension only (`ARQ`), and a fundamentals row is visible **only from its `datekey`** (the date the filing became public). Belt and braces: where the same (ticker, quarter) appears twice, the *earliest* `datekey` row wins — the original filing, never a revision.

Two more no-peeking rules: signals form at a quarter-end **as-of date** using only data visible by then; entry is the **next trading day's** close, never the signal day's.

## Data

**US (this harness):** Sharadar via Nasdaq Data Link — `SF1` (fundamentals, ARQ), `SEP` (equity prices incl. delisted, dividend+split-adjusted `closeadj`), `TICKERS` (universe + delisted flag), `SP500` (historical index add/remove — channel-1 study), `SFP` (SPY as benchmark). Roughly the only US dataset with both dead companies and known-when fundamentals at individual pricing — the institutional equivalents are the ones we can't access. This is a month-two purchase; the harness is built now so it runs the day the key exists.

**ASX (later leg, stub):** Norgate for prices and historical index/universe membership (that's all it carries) paired with EODHD fundamentals applied with explicit reporting lags. Not implemented yet — the config carries the slot.

> **Status (25 Aug 2026):** parked under Vyom's zero-cost directive — no paid data until the system has produced money. There is **no free substitute**: free datasets delete the dead and overwrite the past, and a survivor-biased "backtest" would poison calibration, so this waits for Sharadar rather than running dirty. The harness and its 16 offline tests are done; enabling is the two steps below whenever the directive lifts.

## Enabling access (two steps, once purchased)

1. In the Claude Code environment settings, add env var **`NASDAQ_DATA_LINK_API_KEY`** with your key.
2. Allow **`data.nasdaq.com`** in the environment's network policy.

Without both, `run_backtest.py` stops at a clear error; nothing is faked. Column names in `sharadar.py` are written against Sharadar's published schema and must be verified against a live pull on first run (`--smoke` does exactly that, cheaply).

## What runs

For each quarter-end from `start` to `end` (config):

1. **Candidates — channel-4 screen, §5 verbatim:** price within 15% of the 3-year low AND net debt / trough cash flow sane AND F-score ≥ 5. Trough cash flow = the worst rolling-4-quarter operating cash flow of the past 3 years.
2. **Kills — §6.4 mechanical proxies:** peak-earnings cheapness (TTM margin far above its own 5-yr median), melting ice cube (multi-year revenue decay), leverage mirage (net debt vs EBITDA). The fourth trap (value with no unlock) is judgment — excluded, stated here so the omission is never silent.
3. **Scoring:** 12-month forward `closeadj` return vs SPY, per name; cohort aggregates; deaths counted and reported per cohort. **Gate value** = excess return of what the gates passed minus what they killed. The gates earn their place only if the killed underperform the passed.
4. **Channel-1 study (`--deletions`):** S&P 500 removals per quarter, same scoring, no gates — measures the forced-seller mechanism itself.

## Pinned conventions and DRAFT parameters

| Item | Value | Status |
| --- | --- | --- |
| Fundamentals dimension | `ARQ`, earliest `datekey` per (ticker, quarter) | Pinned (the restatement rule) |
| Visibility | row visible iff `datekey` ≤ as-of | Pinned (the look-ahead rule) |
| Entry | next trading day close after as-of | Pinned |
| Horizon | 12 months (§5 channel scoring window) | Pinned |
| Delisting terminal value | last traded `closeadj` (default); `zero` mode for the bankruptcy-conservative sensitivity run — report both | Pinned convention, both runs required |
| Net debt / trough OCF "sane" | ≤ 3.0× (net cash always passes) | **DRAFT — spec says "sane" without a number; Vyom sets it by versioned edit** |
| Peak-earnings proxy | TTM net margin > 1.5× its 5-yr median (profitable names) | **DRAFT — Vyom** |
| Leverage-mirage proxy | net debt / TTM EBITDA > 4.0×, or net debt with non-positive EBITDA | **DRAFT — Vyom** |
| Melting-ice proxy | TTM revenue lower than the year-ago TTM for 3 consecutive years | **DRAFT — Vyom** |

Draft thresholds live in `config.json`; changing one is a versioned edit (Constitution 13) and the run report records the config hash it ran under.

## Running

```bash
pip install -r backtest/requirements.txt
python backtest/run_backtest.py --smoke          # 1 quarter, capped universe — verifies key, egress, schema
python backtest/run_backtest.py                  # full run per config.json
python backtest/run_backtest.py --deletions      # channel-1 index-deletion study
pytest backtest/tests -q                         # offline logic tests, no key needed
```

Outputs land in `backtest/out/` (gitignored): per-cohort member CSVs and a summary. The offline tests in `backtest/tests/` prove the PIT visibility rule, the restatement rule, survivorship handling (a dead ticker scoring its loss), F-score arithmetic, each trap gate, and the cohort scorer — on synthetic data with known answers, so the harness is verified before a dollar of data is bought.
