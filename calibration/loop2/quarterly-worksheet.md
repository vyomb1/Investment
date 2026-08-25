# Loop 2 quarterly worksheet — [YYYY]Q[N]

> Fill-in template (spec §11, §5). Copy per quarter (suggested: `loop2-YYYYqQ.md`), complete on the first R&R day after quarter-end, log via `/log`. All arithmetic runs in code with formulas shown (Constitution rule 6); this sheet records results and references the computation, it is never the computation.

**Quarter:** ____ · **Period covered:** ____ to ____ · **Run date:** ____ (first R&R after quarter-end: ☐ confirmed)
**system_version:** ____ · **/calibrate skill version:** ____ · **model_ids:** ____
**Ledger rows read (row/record refs):** ____ · **Coverage note:** ledger is the complete input set (C0 for scoring purposes); missing benchmark or ledger data is logged as a failed source, never proxied.

---

## 1. Decisions scored

| Item | Count |
| --- | --- |
| Resolved decisions scored this quarter | ____ |
| Unresolved (excluded, never imputed) | ____ |
| Cumulative scored decisions, trailing 12 months | ____ |

Target ≥20 scored decisions/year (§10 shadow-book rule) — a logging-discipline target on survivors, not a quota on names; fewer, or zero, remains an acceptable research output (§2.5).

## 2. Brier scores — Vyom and Claude, separately (never pooled)

Formula: `BS = (1/N) · Σ (pᵢ − oᵢ)²` — pᵢ = pre-registered confidence (0–1), oᵢ ∈ {0,1} resolved outcome. Computed in code; reference: ____

| Series | N (resolved) | Brier score | Prior quarter | Notes |
| --- | --- | --- | --- | --- |
| Vyom | ____ | ____ | ____ | |
| Claude | ____ | ____ | ____ | |

Small-N caveat recorded: ☐ (no significance claims below N set by Vyom via versioned edit)

## 3. Per-channel funnel (§5)

Leads → triage survival → shadow-book entries → 12-month result vs benchmark. Computed in code; reference: ____

| source_channel | Leads | Triage survivors | Shadow entries | 12m vs benchmark (N resolved) | Notes |
| --- | --- | --- | --- | --- | --- |
| lane1_bench_alert | | | | | |
| ch1_index_deletions | | | | | |
| ch2_insider_clusters | | | | | |
| ch3_capital_cycle | | | | | |
| ch4_multiyear_lows | | | | | |
| ch5_special_situations | | | | | |
| ch6_filing_deltas | | | | | |
| ch7_activist_holders | | | | | |
| ch8_tax_loss | | | | | |
| lane3_human | | | | | |
| vyom_direct | | | | | |

**Quarters of scored channel data now on record: ____ / 4.**
☐ Fewer than four quarters → **no weight changes recommended or made** (anti-overfit rule, §5 verbatim: *weights may not change until four quarters of scored data exist*).
☐ Four or more quarters → prune/feed proposals, if any, listed in §7 below for Vyom's versioned edit.

## 4. Gates reviewed

Observations only — no gate, threshold, cap, or policy number changes here (Constitution rule 13).

| Gate / kill rule / cap | Fired on (ticker, date) | Eventual outcome so far | Observation |
| --- | --- | --- | --- |
| | | | |

## 5. Reason-match tally

From this quarter's resolved `/results` rows (§10: a right answer for the wrong reason scores as luck).

| Verdict | Count |
| --- | --- |
| matched (succeeded for the pre-registered reason) | ____ |
| right_for_wrong_reason (luck) | ____ |
| failed_for_stated_reason | ____ |
| failed_for_other_reason | ____ |
| pending | ____ |

Patterns flagged (e.g. wins the Brier score flatters but reason-match calls luck): ____

## 6. Edge-claim status

☐ Before January 2027 — the edge is **unproven** (Constitution rule 12); this worksheet contains measurements, no edge claims.
☐ January 2027 or later — first edge-claim test reached: 6-month column on the July cohort vs benchmark: ____

## 7. Changes proposed — versioned-edit only, Vyom signs

No change in this table takes effect from this worksheet. Each requires Vyom's versioned edit (§16: version bump, change-log entry) and, where a skill is affected, a Loop 1 rerun before the new version researches anything live.

| Proposed change | Spec/policy section | Affected skills | Loop 1 rerun required | Vyom decision |
| --- | --- | --- | --- | --- |
| | | | ☐ | approved / rejected / deferred |

**Drafted by:** Claude (/calibrate) — computation and observations only.
**Judged and signed:** Vyom ____ · Date ____ · New version (if any change approved): ____

## 8. Logged

Ledger record for this calibration run (stage: calibrate): ____ — unlogged = doesn't exist (Constitution rule 11).
