# Inbox Capture — the 10-second phone capture

**Template** · Stage: Discovery [S1A] · Skill: /sweep (fast) for Lane-2 rows; Vyom by hand for the rest · Spec: v3.2.0 §5, §13 · Machine form: [../schemas/inbox-row.schema.json](../schemas/inbox-row.schema.json)

> **Capture and analysis are never the same activity. No analysis on site** (§5, §13). Ten seconds from a phone, one line, done. The mechanism field is a suspicion tag, not research — the full case belongs to later stages.

## The line

```
{date} | {ticker} | {market} | {source_channel} | {C-class} | {one-line mechanism} | status=new
```

| Field | Rule |
| --- | --- |
| {date} | Capture date, YYYY-MM-DD |
| {ticker} | As supplied by the stream — never originated from model memory (Constitution 2) |
| {market} | Listing exchange (e.g. ASX, NYSE, NASDAQ) |
| {source_channel} | One tag from the list below — every lead carries one (§5) |
| {C-class} | Coverage class of the run/stream that surfaced it (§2.1); Lane-2 sweeps are C2 unless run against an enumerated feed |
| {one-line mechanism} | One line: the suspected **cause** of mispricing — we hunt causes, not cheapness (§1, §5) |
| status | Always `new` at capture; /triage moves it on |

## source_channel tags (§5)

| Tag | Stream |
| --- | --- |
| `lane1_bench_alert` | Lane 1 — Bench price alert (pre-set §8 buy price hit) |
| `ch1_index_deletions` | Lane 2 ch.1 — index deletions (trackers must sell at any price) |
| `ch2_insider_clusters` | Lane 2 ch.2 — insider clusters (signal ≠ thesis) |
| `ch3_capital_cycle` | Lane 2 ch.3 — capital-cycle signals (capex/D&A < 1, closures, trigger phrases) |
| `ch4_multiyear_lows` | Lane 2 ch.4 — multi-year lows ∩ survivability |
| `ch5_special_situations` | Lane 2 ch.5 — special situations (spin-offs, post-bankruptcy, delistings, rights overhangs) |
| `ch6_filing_deltas` | Lane 2 ch.6 — filing deltas (/delta over watchlist + new-lows list) |
| `ch7_activist_holders` | Lane 2 ch.7 — activist/substantial holders (13D US, 604 ASX) |
| `ch8_tax_loss` | Lane 2 ch.8 — tax-loss windows (Dec US, Jun AU) |
| `lane3_human` | Lane 3 — human flow: **forums supply tickers, never theses** |
| `vyom_direct` | Supplied directly by Vyom |

## Rules at capture

- **No analysis on site.** If a second line is forming, stop — that is a later stage's job (on-swing rhythm is 15 min/day, phone only, §13).
- Claude never originates tickers from memory: a row exists because a named stream or Vyom supplied it (§5; Constitution 2).
- Everything enters the same inbox with its tag — Lane 1, Lane 2, Lane 3 alike (§5).
- Fewer names, or zero, is always acceptable (§2.5 — no quotas).
- The tag feeds quarterly channel scoring (leads → triage survival → shadow-book entries → 12-month result vs benchmark); **weights may not change until four quarters of scored data exist** (§5 anti-overfit rule).
- Consumed by /triage on R&R day 1 (≤15 min/name, §13).
