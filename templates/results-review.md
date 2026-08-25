# Results Review — {ticker} · {event}

**Template** · Stage: Results interpreter [S8] (consumed by Maintenance [S16]) · Skill: /results (strong) · Spec: v3.2.0 §4, §10, §11

> The yardstick is the **pre-registered record in the ledger** — never a story assembled after the event. No pre-registered record → nothing to interpret; refuse the run. Thresholds and falsifiers are never edited mid-review or from one outcome (Constitution 13).

## 1. The event

| Field | Value |
| --- | --- |
| Event | {earnings print / clinical readout / restructuring outcome / falsifier check_date} |
| Primary source · as-of | {document} · {date} — tool-verified from the source itself, never a headline (§2.3, §2.4) |
| Identity confirmed (Constitution 4) | {company, ticker, exchange, security type, currency}; price date {—}, filing date {—}, reporting period {—} distinguished |
| Coverage class of this retrieval | {C0 / C1 / C2 / C3} · failed sources: {list / none} |

## 2. Pre-registered thesis and falsifiers — quoted VERBATIM from the ledger

Ledger row ref: **{row id / record date + stage}** — pulled before opening the print.

**Thesis (verbatim, no paraphrase):**

> {quoted exactly as registered}

**Falsifiers (verbatim):**

| # | observable | threshold | check_date |
| --- | --- | --- | --- |
| F1 | {observable} | {threshold} | {check_date} |
| F2 | {observable} | {threshold} | {check_date} |

Pre-registered confidence: {x} (Vyom) · {x} (Claude, where recorded separately)

## 3. Held / failed per falsifier

Every delta a CALC run in code, formula shown (Constitution 6). No "close enough": a near-miss resolves **failed** with the exact delta shown; whether it changes anything is Vyom's judgment at the 7-day review. An observable absent from what was published resolves **not yet resolvable** with NOT FOUND recorded and a next_check — never filled from guidance, consensus, or memory.

| # | Observable | Pre-registered threshold | Actual (source + as-of) | Delta (CALC, formula shown) | Resolution (held / failed / not yet resolvable) |
| --- | --- | --- | --- | --- | --- |
| F1 | {observable} | {threshold} | {actual} | {delta · formula} | {resolution} |
| F2 | {observable} | {threshold} | {actual} | {delta · formula} | {resolution} |

**Gate overall:** {held / failed / partially resolved — NOT FOUND items carry next_check {date}}

## 4. Delta analysis — what actually happened vs predicted

{What the pre-registered record predicted; what the print actually shows; where and by how much they diverge. Claims labelled per §2.2; scored against the registered wording only — never re-scored against a better story the print now makes available.}

## 5. Reason-match verdict (§10) — labelled INFERENCE

Pre-registered reason: {from the thesis and falsifiers} · Actual driver of the outcome: {from the evidence, cited}

**Verdict:** {matched / right-for-wrong-reason (= luck) / failed-for-stated-reason / failed-for-other-reason}

A right answer for the wrong reason scores as **luck** (§10 verbatim). Feeds the outcome columns and Loop 2's reason-match audit (§11). Where a 6/12/24/36-month mark falls due: mark vs benchmark computed in code — {position return, benchmark return, benchmark name, as-of / not due}. Benchmarks (§10): S&P/ASX 300 accumulation (AU sleeve), S&P 500 total return + an energy/materials index (US sleeve), money-weighted.

## 6. Resulting action — VYOM'S ALONE, logged before any trade

Falsifier hit → review within 7 days, **logged before any trade** (§4 Maintenance; Constitution 9). This review resolves gates and computes deltas; it never proposes an order and never sizes anything.

| Field | Value |
| --- | --- |
| Decision (hold / add / exit) vs pre-registered criteria | {Vyom's decision} |
| Rationale vs the pre-registered criteria | {—} |
| Logged on (before any trade) | {date} · ledger row {ref} |
| Signed (Vyom) | __________ |

**Logged** via /log (`stage: results`) per [../schemas/ledger-record.schema.json](../schemas/ledger-record.schema.json), `next_check` {date} for unresolved falsifiers, `system_version`, `skill_versions`, `model_ids` attached — unlogged = doesn't exist (Constitution 11).
