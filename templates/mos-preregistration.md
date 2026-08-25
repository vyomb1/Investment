# MOS Pre-Registration — Margin of Safety

**Template · DRAFT** · Becomes a ledger row via /log · Spec: v3.2.0 §1, §8, §9, §14, Open item 1

> ## DRAFT — NOT IN FORCE
>
> This pre-registration binds nothing until **Vyom signs it and it is logged**. Policy numbers are Vyom's alone (decision-rights table; Constitution 13) — every value below not quoted from the spec is **set by Vyom via versioned edit**. Spec §14, cycle 1, verbatim: "**pre-register MOS in the ledger (first mandatory action — it is overdue)**" — open item 1. This document exists so that later entries are checkable against a rule that predates them.

## 1. The definition being pre-registered (§1, verbatim)

> Margin of safety is an error budget: buy only where being ~25–30% wrong on the key assumption still produces a tolerable outcome.

Operationally, before any entry: name the **key assumption**, shock it by the error budget, and show — in code, formula shown (Constitution 6) — that the outcome at the shocked value is still tolerable. "Tolerable" is bounded by the §9 sizing rule: loss under the plausible break scenario, including gap and illiquidity, ≤ 1.5% NAV.

Error budget: **~25–30%** on the key assumption (§1). Any narrowing of the band, per route or globally: set by Vyom via versioned edit.

## 2. How it applies per route

| Route | Where the error budget bites | MOS test at entry |
| --- | --- | --- |
| **A — durability** | The durability assumption behind the §8 slot-1 reverse-DCF read | **Bear-price entry from the §8 bridge:** entry at/below the bear scenario value (bear metric × multiple ± net cash — the cross-check and tranche-anchor layer, never the primary engine); Bench names carry pre-computed bear/base buy prices (§5 Lane 1); tranches anchor to bear/base scenario values (§8) |
| **B — reversion** | Normalised earnings power (mid-cycle price × volume × margin) and the clock | **Entry vs normalised-earnings value** (§6.2.5: normalised earnings power × conservative mid-cycle multiple; or NAV at conservative decks; or EV/replacement cost — never spot P/E), at a discount such that a ~25–30% miss on normalisation still produces a tolerable outcome |
| **Lenses — non-earnings** | The carrying asset/event/option/claim itself | **Downside floor** where one verifiably exists (special situation/cash shell: cash/asset backing vs economic cap; distressed: position in the priority waterfall, equity priced as an option); **total-loss sizing** where none does (binaries — Bio lens, event shells: loss = 100% of position, maximum size 1.5% NAV, §9) |
| **Peak** | — | No MOS test exists at peak: elevated-earnings cheapness is a default pass (§3, §6.4) |

The exact per-route entry discounts and floor tests, where tighter than the spec text above: set by Vyom via versioned edit.

## 3. The ledger row this pre-registration becomes

On signature, this document is logged as one record per [../schemas/ledger-record.schema.json](../schemas/ledger-record.schema.json) — validated in code, written by the sanctioned logger (week one: Vyom pasting the validated JSON himself, §10). Draft skeleton, values finalised at signing:

```json
{
  "ticker": "{policy row marker, e.g. SYSTEM-MOS — set by Vyom}",
  "date": "{signing date}",
  "stage": "log",
  "route": null,
  "verdict": "MOS pre-registered: error budget ~25-30% on the key assumption; per-route tests per templates/mos-preregistration.md as signed",
  "confidence": "{0-1 — Vyom's}",
  "key_evidence": [
    {
      "claim": "Margin of safety is an error budget: buy only where being ~25-30% wrong on the key assumption still produces a tolerable outcome.",
      "label": "FACT",
      "source": "spec/investment-os-v3.2-master-spec.md §1 (v3.2.0)",
      "as_of": "2026-08-25"
    }
  ],
  "falsifiers": [],
  "size_or_shadow": "n/a — policy pre-registration",
  "source_channel": "vyom_direct",
  "coverage_class": "C0",
  "system_version": "3.2.0",
  "skill_versions": { "/log": "1.0" },
  "model_ids": ["{exact model IDs of the contexts involved}"],
  "next_check": null,
  "outcome": { "reason_match": "pending" }
}
```

## 4. Signature block

| Field | Value |
| --- | --- |
| Pre-registered by | **Vyom alone** (decision-rights table; Constitution 13) |
| Signature | __________ |
| Date signed | {date} |
| Logged as ledger row | {row ref} — unlogged = not in force (Constitution 11) |
| Versions | spec v3.2.0 · this pre-registration v{—} |
| Change control | Any later change to the error budget or per-route tests: versioned edit by Vyom only — never mid-analysis, never from one outcome (§16; Constitution 13) |

Until the signed row exists in the ledger, this remains a **DRAFT** and no MOS policy is in force.
