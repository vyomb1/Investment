# Blind Red-Team Report (Pass 1) — {ticker}

**Template** · Stage: Red team [S5], Pass 1 · Skill: /redteam-blind (strong) · Spec: v3.2.0 §7, §4, §2

> **This context never saw the thesis or the discovery transcript** (§7, verbatim: "receives the evidence pack only — never the thesis, never the discovery transcript"). If forbidden material entered — however it arrived — the pass is VOID: declare the contamination, discard the run, restart in a new context. Mandatory for everything reaching underwriting.

## 1. Inputs attestation (evidence pack only, fresh context — checklist)

This context received, in full: the locked evidence pack for {ticker} ({pack ref}, as_of {date}). **Nothing else.**

- [ ] Brand-new context — not a branch, continuation, or fork of any prior session
- [ ] Carried only the Constitution and the /redteam-blind skill
- [ ] Received the evidence pack ONLY — no thesis, no discovery transcript, no triage verdict, no underwrite output, no other red-team report
- [ ] Invocation prompt was neutral — no framing, no route mention, no hint of pipeline position
- [ ] Read-only research permissions; no execution tools, no ledger write (§10, §12)
- [ ] No contamination occurred at any point of the run

Supplementary primary retrieval this run: coverage class **{C1 / C2 / C3}** — {declaration}. Failed sources: {list / none} (logged, never substituted, §2.3).

**Identity block restated** (Constitution 4): {company} · {ticker} · {exchange} · {security type} · {reporting currency} · price date {date} · filing date {date} · reporting period {period}.
**Pack's own declared coverage class:** {C0–C3}.

## 2. Independent investment conclusion

Formed from the pack and primary documents alone. No reconstruction of the hidden thesis; no shadow-boxing what the owner probably believes.

**Conclusion:** {attractive / unattractive / cannot conclude on this evidence — a full-value answer}
**Confidence (0–1):** {confidence} — Brier-scored in Loop 2 (§11)
**Reasoning:** {every material claim labelled FACT/CALC/EST/INFERENCE/NOT FOUND/CONFLICT; every load-bearing number with source + as-of date; CALCs run in code, formulas shown}

## 3. The three most likely ways an owner loses money (ranked)

§7 task, verbatim and unconditional: rank three. Each path rests on a specific evidence line — a pack claim ID or a primary source found this run — with the observable that would show it happening. Generic market risk is not a loss path. Where the third path rests on materially weaker evidence than the first two, say so explicitly rather than dressing it up.

| Rank | Loss path | Evidence line it rests on (pack ID / source + as-of) | Observable that would show it happening |
| --- | --- | --- | --- |
| 1 | {path} | {C.. / source, date} | {observable} |
| 2 | {path} | {C.. / source, date} | {observable} |
| 3 | {path} | {C.. / source, date} | {observable} |

## 4. Missed-FACT flag

Binding rule (§7/§4, verbatim): **a blind-pass discovery of a missed *fact* (not opinion) forces a return to evidence lock.** Only primary-sourced, dated, load-bearing FACTs absent from or contradicted by the pack qualify; interpretation differences are opinion and belong in §2 above.

| Claim | Label | Source | As-of | Pack status (absent / contradicted) | Flag |
| --- | --- | --- | --- | --- | --- |
| {claim} | FACT | {source} | {date} | {status} | **FORCES RE-LOCK** |

{No missed FACT found — no re-lock forced.}
Borderline fact-vs-inference items for Vyom's adjudication: {list / none}

## 5. Closing attestation

I confirm this report was produced without sight of Vyom's thesis, the discovery transcript, or any other pipeline output for {ticker}, and that no part of it goes into the rebuttal context — the passes never see each other; only Synthesis [S6/S9] sees both (§7).

**Consumed by:** Vyom and Synthesis [S6/S9]; on any missed FACT, /lock for the forced re-lock. **Never** /redteam-rebuttal.
**Logged** via /log (`stage: redteam` — pass identified by `/redteam-blind` in `skill_versions` and in the verdict text) per [../schemas/ledger-record.schema.json](../schemas/ledger-record.schema.json), with `system_version`, `skill_versions`, `model_ids` attached — unlogged = didn't happen (Constitution 11).
