# Portfolio Policy v1

> **Policy v1 — change only by versioned edit, by Vyom alone** (Constitution rule 13; spec §16).
> Source of truth: [`spec/investment-os-v3.2-master-spec.md`](../spec/investment-os-v3.2-master-spec.md) §9. Where this file and the spec ever disagree, the spec wins and this file gets a versioned fix.
>
> **This layer produces a SIZE DECISION ONLY.** It emits a number, tranches, and a checklist verdict — nothing else. Every order is placed manually by Vyom at his broker, outside the system. The system executes nothing: no broker connector, no order tool, anywhere (see [`security-model.md`](security-model.md)).

Applied at the **Portfolio gate [U6]** (spec §4): actor is **Vyom alone**; kill rule is *breaches any §9 cap → no entry / resize*. Sizing is set **before entry** (Constitution rule 9) and nothing counts unless logged (rule 11).

---

## 1. The rules (spec §9, verbatim)

| # | Rule | Value |
| --- | --- | --- |
| 1 | **Sizing basis** | Sizing = **loss under the plausible break scenario**, including gap and liquidity risk — **not** the price at which the falsifier becomes observable. |
| 2 | **Illiquid small caps** | Assume exit **25% below the falsifier price**. |
| 3 | **Binaries** (Bio lens, event shells) | Loss = **100% of position**. |
| 4 | **Per-position cap** | Loss ≤ **1.5% of portfolio NAV** per position (so a binary's maximum size is **1.5% NAV**). |
| 5 | **Theme cap** | A correlated cluster (e.g., uranium + met coal + gas + PGMs + offshore drilling = **one global energy-capex bet**) counts as **one exposure**, capped at **20% NAV**. |
| 6 | **Liquidity cap** | Position exit must complete within **5 trading days at 20% of ADV**. |
| 7 | **Cash floor** | **10% of NAV**, breachable by **no single opportunity**. |
| 8 | **FX policy** | **AUD base**; USD exposure **unhedged by default** (commodity book has natural USD linkage); reviewed **annually**; changed **only in writing**. |
| 9 | **Downturn deployment ladder** (pre-committed) | At **−15% / −25% / −35%** from the reference index high, deploy **20% / 30% / 50%** of reserve cash into Bench names at their pre-set prices. *"The ladder converts the strategy's hardest moment into clerical work."* |

Values the spec leaves to the human, all **set by Vyom via versioned edit**: the reference index for rule 9; the definition and size of the reserve-cash pool; the illiquidity determination for rule 2 where borderline.

**Sizing basis, spelled out (rules 1–3).** The question is never *"where does the falsifier trip?"* but *"what does the position actually lose by the time I am out?"* — including the gap through the falsifier level and the market impact of selling into weakness. Falsifier level (the observable) and expected exit (the realised price) are two different numbers; policy sizes on the second. Binaries have no partial-loss path: model the position at zero.

---

## 2. Worked examples (CALC — formulas shown; arithmetic run in code per Constitution rule 6)

All numbers below are illustrative round numbers, not recommendations. Live sizing uses live NAV, live falsifier levels, and live ADV — every input tool-verified with an as-of date (spec §2.4).

### (a) Illiquid small cap

Inputs: NAV = A$200,000 · entry price = A$1.00 · falsifier observable at A$0.60 · name is an illiquid small cap.

```
assumed_exit   = falsifier_price × (1 − 0.25) = 0.60 × 0.75        = A$0.45
loss_fraction  = (entry − assumed_exit) / entry = (1.00 − 0.45)/1.00 = 0.55
max_loss       = 1.5% × NAV = 0.015 × 200,000                       = A$3,000
max_position   = max_loss / loss_fraction = 3,000 / 0.55            = A$5,454.55  (≈ 2.73% NAV)
```

Round **down** to broker lot size. Wrong-way contrast: sizing off the falsifier price itself (exit A$0.60, loss fraction 0.40) gives max_position = 3,000 / 0.40 = A$7,500 — **37.5% oversized**. That is exactly the error rule 1 forbids.

### (b) Binary at the cap

Inputs: NAV = A$200,000 · Bio-lens name (Phase-3 readout) routed per spec §6.3.

```
loss_fraction  = 1.00  (binary: loss = 100% of position)
max_position   = 1.5% × NAV = 0.015 × 200,000 = A$3,000
```

No further arithmetic exists for a binary: maximum size **is** the cap. No conviction adjustment, no "the market is mispricing the odds" upsize — that argument belongs in the thesis, not the sizing.

### (c) Theme-cluster accounting

Inputs: NAV = A$200,000 · theme cap = 20% × 200,000 = A$40,000 · declared cluster "global energy-capex" already holds:

| Position | % NAV | A$ |
| --- | --- | --- |
| Uranium producer | 6% | 12,000 |
| Met coal producer | 5% | 10,000 |
| Gas producer | 4% | 8,000 |
| Offshore driller | 3% | 6,000 |
| **Cluster total** | **18%** | **36,000** |

Candidate: PGM miner, proposed at 4% NAV (A$8,000). PGMs belong to the same cluster (spec §9's own example).

```
would_be_cluster = 36,000 + 8,000 = A$44,000 = 22% NAV  →  breaches 20% cap
max_addition     = cap − current = 40,000 − 36,000 = A$4,000 = 2% NAV
```

Verdict: enter at ≤ 2% NAV, or Vyom trims another cluster member first (his call, manually), or the name goes to the shadow book at full intended size with `size_or_shadow` recording the cap as the reason. Five separate tickers; **one** exposure.

---

## 3. Portfolio gate [U6] — entry checklist

Run by **Vyom, alone**, after synthesis and before any order. Preconditions: Vyom's own one-paragraph thesis and written falsifiers exist (Constitution rule 8); red-team passes complete (spec §7). Any **No** → no entry, or resize until every line is Yes. The verdict is logged either way (rule 11).

| # | Check | Yes/No |
| --- | --- | --- |
| 1 | Plausible break scenario written down, including gap and liquidity risk — sized on realised exit, **not** the falsifier-observable price? | ☐ |
| 2 | If illiquid small cap: exit assumed **25% below** the falsifier price? | ☐ |
| 3 | If binary (Bio lens, event shell): loss modelled as **100% of position**? | ☐ |
| 4 | Loss under the break scenario ≤ **1.5% of NAV** (CALC in code, formula shown, inputs dated)? | ☐ |
| 5 | Name assigned to a correlation cluster (or explicitly to none), and post-entry cluster exposure ≤ **20% NAV**? | ☐ |
| 6 | Exit completes within **5 trading days at 20% of ADV** at intended size (ADV tool-verified, as-of date recorded)? | ☐ |
| 7 | Post-entry cash ≥ **10% NAV**? (No single opportunity breaches the floor — this one included.) | ☐ |
| 8 | FX consistent with policy (AUD base, USD unhedged by default) — no ad-hoc hedge attached to this entry? | ☐ |
| 9 | Tranche prices anchored to bear/base scenario values (spec §8)? | ☐ |
| 10 | Ledger row prepared with size, falsifiers, `system_version`, `skill_versions`, `model_ids` — will be logged via the logger before the position "exists"? | ☐ |

Output of the gate: **a size (or "no entry") and tranche prices. Nothing here places, queues, or transmits an order.** Vyom then goes to his broker — outside this system — by hand.

---

## 4. Downturn deployment ladder — clerical checklist

Pre-committed (spec §9): the decisions were made in calm; execution during a drawdown is clerical. **Pre-committed does not mean automated** — each rung is executed by Vyom manually; the system's role stops at the alert.

Reference index and reserve-cash pool: **set by Vyom via versioned edit**, in writing, before the ladder is armed. Operational convention, fixed here until a versioned edit says otherwise: rung percentages apply to the reserve as measured at arming, so the three rungs together commit 20% + 30% + 50% = 100% of the reserve.

| Rung | Trigger (drawdown from reference index high) | Deploy | Into |
| --- | --- | --- | --- |
| 1 | **−15%** | **20%** of reserve cash | Bench names at their pre-set prices |
| 2 | **−25%** | **30%** of reserve cash | Bench names at their pre-set prices |
| 3 | **−35%** | **50%** of reserve cash | Bench names at their pre-set prices |

Per rung, in order:

1. ☐ Confirm the drawdown from the reference index high with a dated market source — **tool-verified, never recalled** (spec §2.4).
2. ☐ Compute the rung's deployment amount in code: `deploy = rung_% × reserve_cash_at_arming` — formula and inputs logged.
3. ☐ Pull the Bench list (spec §5 Lane 1) and each name's **pre-computed** bear/base buy prices. No new analysis, no re-underwriting mid-panic — prices were set in advance; that is the point.
4. ☐ Buy only Bench names trading **at or below** their pre-set prices. A name above its price is skipped, not chased. Fewer names, or zero, is acceptable (spec §2.5).
5. ☐ Each purchase still passes the full [U6] checklist above — per-position cap, theme cap, liquidity cap, and the 10% cash floor all remain binding at every rung.
6. ☐ Vyom places each order manually at the broker. **The system has no execution path; the ladder emits alerts and this checklist, nothing else.**
7. ☐ Log every fill (and every skip, with reason) via the logger, versions attached. Unlogged = doesn't exist.

No improvisation between rungs: intermediate drawdowns deploy nothing. Changing rungs, percentages, the reference index, or the reserve definition mid-drawdown is prohibited — versioned edit only, never mid-analysis, never from one outcome (Constitution rule 13).

---

## 5. Constitution bindings (which rules bite hardest here)

- **9** — Sizing is loss-at-plausible-break including gaps and illiquidity (binaries = total loss), within §9 caps, set before entry; a triggered falsifier forces a logged review within seven days, before any trade.
- **13** — Policy numbers in this file change only by versioned edit — never mid-analysis, never from one outcome.
- **14** — Judgment, sizing, and every trigger belong to Vyom; Claude drafts and computes, nothing more.
- **11** — Nothing counts unless logged with versions attached; the gate verdict and every ladder action are ledger rows.
- **6** — Every sizing number is a CALC run in code with its formula shown.
- **8** — No position, real or shadow, exists without Vyom's own thesis paragraph and written falsifiers; the gate never runs without them.
