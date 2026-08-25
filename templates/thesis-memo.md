# Thesis Memo — {ticker}

**Template** · Stage: Synthesis [S6/S9] · Skill: none — spec §4 lists "template" (this file) · Spec: v3.2.0 §1, §4, §7, §9, §10 · Actor: **Vyom, unaided wording**

> **THE PARAGRAPH IS VYOM'S ALONE, IN HIS OWN WORDS.** Claude never drafts, autocompletes, or edits it — not a phrase, not a suggested opening, not a polish. If the paragraph can't be written, the name goes to **bench or bin** (§4 kill rule, verbatim: "Can't write the paragraph → bench or bin"). A position without that paragraph does not exist, even in the shadow book (§1; Constitution 8). Claude drafts every other section of this memo.

## 1. Identity (Constitution 4)

| Field | Value |
| --- | --- |
| Company | {company} |
| Ticker · exchange | {ticker} · {exchange} |
| Security type | {security_type} |
| Reporting currency | {currency} |
| Price · price date | {price} · {price_date} |
| Latest filing · filing date | {filing} · {filing_date} |
| Reporting period covered | {reporting_period} |

## 2. Route

**{A / B / lens-bio / lens-exp / lens-ss / lens-dx / lens-fin / lens-resources / lens-tech}**, per the triage verdict of {triage_date}. Lens vocabulary applied (lenses are vocabularies, not exclusive routes, §3): {lens / none}. Peak never reaches this memo — elevated-earnings cheapness is a default pass (§3).

## 3. Inputs on the desk (synthesis sees both red-team reports — §7)

- Evidence pack: {ref} · as_of {date} · `verified_by_vyom = true`
- Blind report (Pass 1, [redteam-blind-report.md](redteam-blind-report.md)): {ref} — missed-FACT register: {empty / resolved by re-lock on {date}}
- Rebuttal report (Pass 2, [redteam-rebuttal-report.md](redteam-rebuttal-report.md)): {ref / not run — cost-gated; §7 requires it only for names heading toward a real position}
- Underwrite output (§8 ordering + scenario bridge): {ref}

## 4. The one-paragraph thesis — Vyom, unaided

*Why is the price's implied forecast wrong? A stock price is a compressed forecast (§1); state the specific, checkable way the implication fails.*

> {thesis_paragraph — handwritten by Vyom. If this box cannot be filled, stop: bench or bin.}

## 5. Falsifiers — written and signed by Vyom

Observable, thresholded, dated. A triggered falsifier forces a logged review within 7 days, before any trade (§4 Maintenance; Constitution 9).

| # | observable | threshold | check_date |
| --- | --- | --- | --- |
| F1 | {observable} | {threshold} | {check_date} |
| F2 | {observable} | {threshold} | {check_date} |
| F3 | {observable} | {threshold} | {check_date} |

**Falsifiers signed by Vyom:** __________ · date {date}

## 6. Size proposal (§9 arithmetic — run in code, formulas shown; Constitution 6)

Sizing = **loss under the plausible break scenario, including gap and liquidity risk** — not the price at which the falsifier becomes observable (§9).

| Item | Value | Rule (§9) |
| --- | --- | --- |
| Plausible break scenario | {description} | what the break actually looks like, not the falsifier print |
| Exit price under break | {exit_price} | illiquid small caps: assume exit **25% below the falsifier price** |
| Binary? (Bio lens, event shells) | {yes/no} | if yes: **loss = 100% of position** → maximum size 1.5% NAV |
| Loss at proposed size | {x}% NAV — CALC: {formula} | cap: loss ≤ **1.5% of portfolio NAV** per position |
| Proposed size · tranches | {size} · {tranches} | entry tranches anchor to bear/base scenario values (§8) |

**Portfolio gate [U6] checks — Vyom, all must pass (kill rule: breaches any §9 cap):**

- [ ] Per-position cap: loss under plausible break ≤ 1.5% NAV
- [ ] Theme cap: correlated cluster this name joins — {cluster / none}; cluster counts as one exposure ≤ 20% NAV
- [ ] Liquidity cap: exit completes within 5 trading days at 20% of ADV (ADV {adv}, CALC: {formula})
- [ ] Cash floor: post-entry cash ≥ 10% NAV — breachable by no single opportunity

## 7. Pre-registered confidence (0–1)

**{confidence}** — Vyom's own number, registered before the outcome; Brier-scored in Loop 2 (§11) separately from Claude's.

## 8. next_check

{next_check_date} — earliest falsifier check_date or scheduled review; drives Maintenance [S16] alerts.

## 9. Ledger handoff

This memo becomes one ledger record (`stage: synthesis`) per [../schemas/ledger-record.schema.json](../schemas/ledger-record.schema.json), validated in code and written only by the separate insert-only logger (week one: Vyom pastes the validated JSON himself, §10). `system_version`, `skill_versions`, `model_ids` attached — unlogged = doesn't exist (Constitution 11). Shadow-book rule (§10): log this **bought or not**.
