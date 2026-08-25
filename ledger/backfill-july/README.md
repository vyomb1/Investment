# July backfill — ledger rows 1–13, 25-Aug marks

**Spec:** [§10, §14 cycle 1, open items 1–2](../../spec/investment-os-v3.2-master-spec.md) · **Columns:** [`../ledger.csv`](../ledger.csv) per [`../README.md`](../README.md) · **Logger:** week-one = Vyom pasting each validated row himself.

Spec §10/§14, verbatim intent: **the July workbook is backfilled as ledger rows 1–13 (25-Aug marks) and thereafter becomes a view/export layer, not the database.**

## Where the data lives

**With Vyom — the July workbook.** This directory holds instructions only; no July data is stored in the repo scaffold, and none of it may be reconstructed from model memory. A field the workbook does not contain is NOT FOUND — a plausible reconstruction is not (§2.2).

## Procedure

1. Vyom (as week-one logger) creates rows 1–13 in the ledger sheet, one row per July name, columns exactly per [`../ledger.csv`](../ledger.csv).
2. Fill each column per the table below. Claude may assist with flattening and code-run mark arithmetic from workbook data Vyom supplies (C0 — user-supplied evidence set); the paste is Vyom's.
3. **WOR and WTC rows land first — before 26 Aug** (see the flag below).
4. Once rows 1–13 exist, the July workbook is a view/export layer only. Corrections from that point are new superseding ledger rows, never workbook edits.

## What each row needs

| Column | Rule for the backfill |
| --- | --- |
| `ticker`, `date` | As in the workbook. `date` = the **original July decision date**, not the backfill date. |
| `stage` | The furthest pipeline stage the July record represents (schema enum). |
| `route` | As routed in July (A/B/Peak/lens); the July routing, not a re-route under v3.2. |
| `verdict` | As recorded in July, in July's wording. |
| `confidence` | The confidence **as stated in July**, if one was stated. Never assigned retrospectively — a retro-fitted confidence poisons Loop 2's Brier inputs. Not stated → blank, noted as NOT FOUND. |
| `key_evidence_json` | The July evidence claims, labelled per §2.2, with sources and July as-of dates. **Plus one CALC entry per row for the 25-Aug mark** (see below). |
| `falsifiers_json` | **The pre-registered falsifiers exactly as they were written in July — verbatim. No retrofitting**, no tightening, no tidying, no unit "clarifications". `/results` scores against this wording; a better falsifier written today is a new row under v3.2, not an edit of history. |
| `size_or_shadow` | The real size or shadow marker as decided in July. |
| `source_channel` | As captured in July. Where the workbook predates channel tagging, the backfill convention is `vyom_direct` (the July run entered through Vyom) — Vyom confirms at paste time; never back-assign a flattering channel. |
| `coverage_class` | As declared for the July retrieval, if declared; otherwise per the same NOT-FOUND-honest convention, confirmed by Vyom. |
| `system_version` | The version that actually produced the July decision, as recorded in the workbook — the July run predates v3.2, so **do not stamp 3.2.0 onto July decisions** (§16: outcomes must stay attributable to the system that produced them). |
| `skill_versions_json`, `model_ids_json` | As recorded in July; unrecorded → noted NOT FOUND. The backfill act itself changes nothing here. |
| `next_check` | The nearest future falsifier `check_date` for the name. **WOR and WTC: 2026-08-26.** |
| `mark_6m` … `mark_36m` | **Blank — not yet due.** The July cohort's 6-month column lands **January 2027**, the first edge-claim test (§11). The 25-Aug marks do not go in these columns. |
| `benchmark` | Assigned now, per §10 sleeve (AU: S&P/ASX 300 accumulation; US: S&P 500 TR + energy/materials index; money-weighted) — declared before any outcome column exists. |
| `reason_match` | `pending` for every backfilled row. |

**The 25-Aug marks:** for each row, one `key_evidence_json` CALC entry recording position return and benchmark return **as of 2026-08-25**, computed in code with the formula shown, price sources dated (§2.4). This is the backfill baseline mark; the 6/12/24/36-month outcome columns fill only when due.

## Flag — WOR and WTC report 26 Aug

Two of the thirteen names have known events on **26 Aug 2026**, and their [`/results`](../../.claude/skills/results/SKILL.md) runs are the system's first live ones (spec open item 2): **run /results on the WOR and WTC 26-Aug prints against their pre-registered falsifiers (85% cash conversion; ~3x leverage + FCF conversion)** — execute on whatever exists that day.

Order of operations matters: `/results` refuses any run with no pre-registered record, so **the WOR and WTC rows must be in the ledger before the prints land**. The spec's parenthetical thresholds are the pointer; the yardstick is each row's `falsifiers_json` in July's exact wording. If the rest of the backfill slips, do these two rows first.

## Corrections

New rows only. The ledger is insert-only end to end; a backfill mistake is superseded by a fresh row, and the original stays as history.
