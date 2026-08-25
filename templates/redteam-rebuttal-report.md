# Rebuttal Red-Team Report (Pass 2) — {ticker}

**Template** · Stage: Red team [S5], Pass 2 · Skill: /redteam-rebuttal (strong) · Spec: v3.2.0 §7, §4

> Cost-gated (§7): run only for names heading toward a **real position**. A second fresh context receives the evidence pack **plus Vyom's thesis** — never the discovery transcript, never the blind report. Task, verbatim: **attack these exact assumptions, hardest first.** Coverage protection — the actual reason you want to own it gets attacked.

## 1. Inputs attestation (pack + Vyom's thesis, fresh context)

This context received, in full: the locked evidence pack ({pack ref}, as_of {date}) and Vyom's thesis memo ({memo ref}) for {ticker}. **Nothing else.**

- [ ] Brand-new context — not a branch, continuation, or fork of any prior session
- [ ] Received pack + thesis ONLY — no discovery transcript, no triage verdict, no underwrite draft, no blind-pass report
- [ ] Read-only research permissions; no execution tools, no ledger write (§10, §12)
- [ ] No contamination occurred (else VOID — declare, discard, restart fresh)

Supplementary primary retrieval this run: coverage class **{C1 / C2 / C3}** — {declaration}. Failed sources: {list / none} (§2.3).

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
- **Verdict:** {broken / wounded / survives on current evidence} — claims labelled per §2.2; any arithmetic in code, formulas shown (Constitution 6)

### A2 — {assumption}

- **What evidence would break it:** {—}
- **What already cuts against it:** {—}
- **Verdict:** {—}

### A3 — {assumption}

- **What evidence would break it:** {—}
- **What already cuts against it:** {—}
- **Verdict:** {—}

## 4. Surviving-assumption summary (for synthesis)

| Assumption | Verdict | What must stay true (feeds Vyom's falsifier review) |
| --- | --- | --- |
| A1 | {verdict} | {condition} |
| A2 | {verdict} | {condition} |
| A3 | {verdict} | {condition} |

Synthesis [S6/S9] sees this report alongside the blind report (§7); the passes never see each other. The ENGN rule applies here as everywhere: when fuller primary evidence defeats the framing, the system changes its mind and logs why, rather than rationalising — any missed primary-sourced FACT surfaced by this attack is flagged to Vyom explicitly.

**Consumed by:** Vyom and Synthesis [S6/S9]. **Never** /redteam-blind.
**Logged** via /log (`stage: redteam-rebuttal`) per [../schemas/ledger-record.schema.json](../schemas/ledger-record.schema.json), with `system_version`, `skill_versions`, `model_ids` attached — unlogged = didn't happen (Constitution 11).
