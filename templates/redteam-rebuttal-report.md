# Rebuttal Red-Team Report (Pass 2) — {ticker}

**Template** · Stage: Red team [S5], Pass 2 · Skill: /redteam-rebuttal (strong) · Spec: v3.2.0 §7, §4

> Cost-gated (§7): run only for names heading toward a **real position**. A second fresh context receives the evidence pack **plus Vyom's thesis** — never the discovery transcript, never the blind report. Task, verbatim: **attack these exact assumptions, hardest first.** Coverage protection — the actual reason you want to own it gets attacked.

## 1. Inputs attestation (pack + Vyom's thesis, fresh context)

This context received, in full: the locked evidence pack ({pack ref}, as_of {date}) and Vyom's thesis memo ({memo ref}) for {ticker}. **Nothing else.**

- [ ] **Cost gate (§7): Vyom declared this name heading toward a real position** — declaration recorded: {date / reference}
- [ ] Brand-new context — not a branch, continuation, or fork of any prior session
- [ ] Received pack + thesis ONLY — no discovery transcript, no triage verdict, no underwrite draft, no blind-pass report
- [ ] Read-only research permissions; no execution tools, no ledger write (§10, §12)
- [ ] No contamination occurred (else VOID — declare, discard, restart fresh)

Supplementary primary retrieval this run: coverage class **{C1 / C2 / C3}** — {declaration}. Failed sources: {list / none} (§2.3).

**Identity block restated** (Constitution 4): {company} · {ticker} · {exchange} · {security type} · {reporting currency} · price date {date} · filing date {date} · reporting period {period}.
**Pack's own declared coverage class:** {C0–C3}.

## 2. Load-bearing assumptions, extracted and ranked hardest-first

Extracted from the thesis paragraph and falsifiers as written — the assumptions the thesis actually stands on, not a strawman. "Hardest first" = the assumption carrying the most weight, whose failure most damages the thesis.

| Rank | Assumption (as the thesis relies on it) | Where it appears (thesis phrase / falsifier #) |
| --- | --- | --- |
| A1 | {assumption} | {ref} |
| A2 | {assumption} | {ref} |
| A3 | {assumption} | {ref} |

## 3. Attack on each assumption (hardest first)

### A1 — {assumption}

- **What evidence would break it:** {the concrete observable, document, or print that would falsify it}
- **What already cuts against it:** {existing evidence — pack claim IDs or primary sources with as-of dates — that weakens it now; NOT FOUND if nothing does, stated as such, not padded}
- **Verdict:** {broken / cracked / holds} — claims labelled per §2.2; any arithmetic in code, formulas shown (Constitution 6)
- **Confidence in this verdict (0–1):** {confidence} — Brier-scored in Loop 2 (§11)

### A2 — {assumption}

- **What evidence would break it:** {—}
- **What already cuts against it:** {—}
- **Verdict:** {—}
- **Confidence (0–1):** {—}

### A3 — {assumption}

- **What evidence would break it:** {—}
- **What already cuts against it:** {—}
- **Verdict:** {—}
- **Confidence (0–1):** {—}

## 3a. Falsifier-instrument findings

Each written falsifier tested as an instrument (skill step 6): is it observable, thresholded, dated — and would it trip **before** the loss it guards against is realised? A falsifier that fires only after the damage is an attack finding against the assumption it guards. Findings are attacks for Vyom to weigh; rewriting falsifiers remains his alone (Constitution 8).

| Falsifier (as written) | Guards assumption | Observable? | Thresholded? | Dated? | Trips before the loss? | Finding |
| --- | --- | --- | --- | --- | --- | --- |
| {falsifier} | {A#} | {y/n} | {y/n} | {y/n} | {y/n} | {finding / sound} |

**Missed-fact register (ENGN rule):** {any load-bearing, primary-sourced, dated FACT found this run that is absent from or contradicts the locked pack — flagged to Vyom for his re-lock call; none found → say so}

## 4. Surviving-assumption summary (for synthesis)

| Assumption | Verdict | What must stay true (feeds Vyom's falsifier review) |
| --- | --- | --- |
| A1 | {verdict} | {condition} |
| A2 | {verdict} | {condition} |
| A3 | {verdict} | {condition} |

Synthesis [S6/S9] sees this report alongside the blind report (§7); the passes never see each other. The ENGN rule applies here as everywhere: when fuller primary evidence defeats the framing, the system changes its mind and logs why, rather than rationalising — any missed primary-sourced FACT surfaced by this attack is flagged to Vyom explicitly.

**Consumed by:** Vyom and Synthesis [S6/S9]. **Never** /redteam-blind.
**Logged** via /log (`stage: redteam` — pass identified by `/redteam-rebuttal` in `skill_versions` and in the verdict text) per [../schemas/ledger-record.schema.json](../schemas/ledger-record.schema.json), with `system_version`, `skill_versions`, `model_ids` attached — unlogged = didn't happen (Constitution 11).
