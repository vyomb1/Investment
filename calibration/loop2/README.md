# Loop 2 — judgment calibration (quarterly)

**Spec:** [§11 Loop 2, §5 channel scoring, §13 cadence](../../spec/investment-os-v3.2-master-spec.md) · **Run by:** [/calibrate](../../.claude/skills/calibrate/SKILL.md) · **Worksheet:** [`quarterly-worksheet.md`](quarterly-worksheet.md)

Loop 2 answers: *are the stated confidences — Vyom's and Claude's, separately — worth anything, and which discovery channels earn their place?* It is distinct from Loop 1 (golden-set accuracy on version changes) and the two are never blended.

**Cadence:** quarterly, on the **first R&R day after quarter-end** (§13). One completed copy of [`quarterly-worksheet.md`](quarterly-worksheet.md) per quarter, filed in this directory (suggested name: `loop2-YYYYqQ.md`) and logged via [/log](../../.claude/skills/log/SKILL.md) with `system_version`, `skill_versions`, `model_ids` — an unlogged calibration run measured nothing (Constitution rule 11).

**Inputs:** the ledger only — read-only ([`ledger/`](../../ledger/), per [`schemas/ledger-record.schema.json`](../../schemas/ledger-record.schema.json)): pre-registered confidences, resolved `/results` outcomes, outcome-column marks, channel-tagged lead history, and the §10 benchmark series. What was never logged cannot be scored — unlogged decisions don't exist.

---

## Section 1 — Brier scores on stated confidences

Scored **separately for Vyom and for Claude** — two series, never pooled. Each confidence was pre-registered in the ledger at logging time; only confidences whose outcomes have resolved are scored.

**Formula (arithmetic runs in code, not in prose — Constitution rule 6):**

```
BS = (1/N) · Σᵢ (pᵢ − oᵢ)²

pᵢ = stated confidence at logging (0–1)
oᵢ = resolved outcome (1 = the pre-registered claim held, 0 = it failed)
N  = resolved decisions scored in the series
```

Lower is better; 0.0 is perfect; always answering 0.5 scores 0.25. Report `N` beside every score. Unresolved confidences are **excluded and counted, never imputed**. Small-N honesty: no significance claims from a handful of names; zero resolved outcomes is a reportable result (§2.5), not a gap to fill.

## Section 2 — channel hit rates (§5)

Per-channel funnel, computed in code from `source_channel` tags carried through every row:

**leads → triage survival → shadow-book entries → 12-month result vs benchmark**, per channel.

Channels are the `source_channel` enum in [`schemas/inbox-row.schema.json`](../../schemas/inbox-row.schema.json) (Lane 1 bench alerts, Lane 2 channels 1–8, Lane 3 human flow, Vyom direct). Kills count — they are data for channel scoring, which is why every kill is logged with its reason.

**Anti-overfit rule, verbatim (§5): weights may not change until four quarters of scored data exist.** Until the fourth quarter is on record, this section computes and reports the funnels and refuses to recommend any weight change. From the fourth quarter: prune losers, feed winners — by Vyom's versioned edit only (Constitution rule 13).

## Section 3 — gate/threshold review

Which kill rules, trap filters, caps, and gates fired this quarter, on what names, with what eventual outcome. **Observations only.** Any change to a gate, threshold, or policy number is Vyom's versioned edit under §16 — never this report's side effect, never mid-analysis, never from one outcome.

## Section 4 — reason-match audit

Across the quarter's resolved `/results` rows, tally the reason-match verdicts (§10): did each name succeed/fail *for the pre-registered reason?* **A right answer for the wrong reason scores as luck.** Flag any pattern of winning for wrong reasons — that is noise the Brier score alone will flatter.

---

## First edge-claim test: January 2027

The first test of the system's edge is the **6-month column on the July cohort, January 2027** (§11). Until benchmark-adjusted ledger data exists, the only permitted description of the system's edge is **unproven** (Constitution rule 12). No worksheet filed in this directory before that date contains edge language.

## Anti-overfit summary (binding on every quarter)

- **No channel-weight changes until four quarters of scored data exist** (§5, verbatim rule).
- Gates, thresholds, and policy numbers change only by versioned edit, signed by Vyom — never inside this report (Constitution rule 13).
- Every proposed change that touches a skill triggers the §16 gate: version bump + Loop 1 rerun on affected skills before the new version researches anything live.
- Claude computes, Vyom judges (Constitution rule 14): everything in the worksheet is input to his decisions, not a decision.
