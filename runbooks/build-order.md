# Build Order — Cycles 1–6

**Runbook** · Owner of every gate and greenlight: **Vyom** · Spec: [`../spec/investment-os-v3.2-master-spec.md`](../spec/investment-os-v3.2-master-spec.md) v3.2.0 **§14** (normative), with §10, §11, §13, §16 and the spec's Open Items section. Where this file and the spec disagree, the spec wins and this file gets a versioned fix (§16).

> **Written ≠ live.** This repo ships all 16 skills at v1.0 ([`../ARCHITECTURE.md`](../ARCHITECTURE.md) §5 registry). The cycle plan below governs when each skill **enters live use**, not when it is written. The §16 gate applies throughout: Loop 1 runs on every version change **before the new version researches anything live** — the Loop-1 baseline lands in cycle 2, and from then on no changed skill touches live research without its Loop-1 rerun. Cycles 1–2 run the **Minimum Viable Loop only** — mandatory before extras ([`operating-rhythm.md`](operating-rhythm.md)).

---

## Cycle 1 — MVL foundations

- [ ] **1.1 Paste the Constitution into the Project.** [`../CONSTITUTION.md`](../CONSTITUTION.md), the 14 rules **verbatim**, as the Claude Project instruction block (§15).
- [ ] **1.2 Create the inbox + ledger sheet.** Google Sheet is the operational store for cycles 1–2 (§10). Columns are the contract: [`../schemas/inbox-row.schema.json`](../schemas/inbox-row.schema.json), [`../schemas/ledger-record.schema.json`](../schemas/ledger-record.schema.json), mirrored as CSV headers in [`../ledger/`](../ledger/).
- [ ] **1.3 Build /triage and /log** — [/triage](../.claude/skills/triage/SKILL.md) and [/log](../.claude/skills/log/SKILL.md) enter live use. Week-one sanctioned logger: **Vyom pasting the validated JSON himself** — same architecture, human as logger (§10).
- [ ] **1.4 PRE-REGISTER MOS IN THE LEDGER — first mandatory action; it is overdue** (§14 verbatim; open item 1). Draft awaiting signature: [`../templates/mos-preregistration.md`](../templates/mos-preregistration.md). Vyom signs; the record is logged via /log. Until the signed row exists, no MOS policy is in force.
- [ ] **1.5 Backfill the July run** as ledger rows 1–13 with **25-Aug marks** (scaffold: [`../ledger/`](../ledger/)). The July workbook thereafter becomes a view/export layer, not the database (§10).
- [ ] **1.6 Run /results on the WOR and WTC 26-Aug prints** against their pre-registered falsifiers — **85% cash conversion; ~3x leverage + FCF conversion** (§14 verbatim) — quoting the falsifier wording verbatim from the backfilled rows, never paraphrased ([`../templates/results-review.md`](../templates/results-review.md)). **Execute on whatever exists that day** (open item 2). Depends on 1.3 and 1.5.

## Cycle 2 — the loop closes

- [ ] **2.1 /sweep, /delta, /redteam-blind enter live use** ([/sweep](../.claude/skills/sweep/SKILL.md), [/delta](../.claude/skills/delta/SKILL.md), [/redteam-blind](../.claude/skills/redteam-blind/SKILL.md)).
- [ ] **2.2 First full end-to-end candidate** — one live name through the whole MVL: capture → triage → evidence lock ([/lock](../.claude/skills/lock/SKILL.md)) → blind red team → **Vyom's thesis** → log. Logged bought or not (shadow-book rule, §10).
- [ ] **2.3 Build the 25-question golden set** (open item 4): 25 filing-based questions **Vyom has hand-verified** — single-right-answer items across US/ASX filings — alongside the 8 historical process cases of §11 (ENGN, KMX, NKE seed, FULC, WTC, LEN, GHY, one past personal trade). Scaffold: [`../calibration/`](../calibration/).
- [ ] **2.4 Run the Loop-1 baseline** via [/calibrate](../.claude/skills/calibrate/SKILL.md): exact-match/tolerance for facts, refusals counted separately from errors, per-skill scores recorded (§11). This baseline is the reference every later version change is checked against before live research (§16).

## Cycle 3 — analytical depth + bench start

- [ ] **3.1 Underwriting + lens skills and /redteam-rebuttal enter live use:** [/underwrite-a](../.claude/skills/underwrite-a/SKILL.md), [-b](../.claude/skills/underwrite-b/SKILL.md), [-bio](../.claude/skills/underwrite-bio/SKILL.md), [-exp](../.claude/skills/underwrite-exp/SKILL.md), [-ss](../.claude/skills/underwrite-ss/SKILL.md), [-dx](../.claude/skills/underwrite-dx/SKILL.md), [-fin](../.claude/skills/underwrite-fin/SKILL.md); [/redteam-rebuttal](../.claude/skills/redteam-rebuttal/SKILL.md) (cost-gated, §7).
- [ ] **3.2 EODHD** — subscribe when /sweep outgrows free data (§14): screens for channels 2 and 4, ASX Appendix 3Y.
- [ ] **3.3 Bench construction begins** — ~5 names/cycle, one bench-building deep block per [`operating-rhythm.md`](operating-rhythm.md); method and targets in [`../discovery/channels.md`](../discovery/channels.md) Lane 1.

## Cycles 4–6 — scale + hard storage

- [ ] **4.1 Bench to ≥15 names — unlocks A-entries** (§5: no A-entries before ~15 bench names exist).
- [ ] **4.2 Supabase migration with logger separation** — [`../db/001_init.sql`](../db/001_init.sql): `leads`, `ledger`, `reviews`; `research_ro` (SELECT only) vs `logger_writer` (INSERT only); **service-role keys never touch any agent** (§10). Run the post-apply verification in [`../db/README.md`](../db/README.md) before handing out any credential.
- [ ] **4.3 Sharadar/Norgate decision** for the point-in-time gate backtest (open item 3) — subscribe **only if the backtest is greenlit**, month 2–3+.

---

## Connectors (§14)

| Connector | Cost model | When | Purpose | Status |
| --- | --- | --- | --- | --- |
| EDGAR MCP | free | **now** | US filings; Form 4 clusters (channel 2) | adopt now |
| Bigdata.com | pay-as-you-go | **now** | trigger phrases (channel 3) | adopt now |
| EODHD | subscription | **~cycle 3**, when /sweep outgrows free data | screens (channels 2, 4); ASX Appendix 3Y | scheduled (3.2) |
| Sharadar / Norgate | subscription | **month 2–3+, only if the point-in-time backtest is greenlit** | gate backtest | decision pending (open item 3) |
| FactSet | — | never | — | **skip** — enterprise-gated |
| S&P / Kensho | — | never | — | **skip** — enterprise-gated |
| Daloopa MCP | — | never | — | **skip** — paid-tier only |

All connectors are read-only research inputs. No connector has write or trade scope — there is nothing to revoke because nothing was granted ([`../ARCHITECTURE.md`](../ARCHITECTURE.md) §6.3; spec §12).

## Open items (spec: "owned, not hidden")

Owners follow the spec's decision-rights table: Claude drafts, Vyom decides, signs, and spends.

| # | Item (spec wording) | Owner | Status |
| --- | --- | --- | --- |
| 1 | MOS pre-registration — cycle 1, first action, **overdue** | **Vyom** signs + logs; Claude drafted | DRAFT at [`../templates/mos-preregistration.md`](../templates/mos-preregistration.md); not in force until signed and logged (checklist 1.4) |
| 2 | WOR/WTC 26-Aug prints — first live /results run; **execute on whatever exists that day** | Claude + Vyom (§4 Results interpreter row) | due 26 Aug 2026; depends on 1.3 + 1.5 (checklist 1.6) |
| 3 | Point-in-time gate backtest (Sharadar + Norgate/EODHD) — decision at month 2–3 | **Vyom** greenlights (spend + policy); Claude drafts the case | open; decision month 2–3 (checklist 4.3) |
| 4 | Golden-set construction — cycle 2 | **Vyom** hand-verifies answers; Claude drafts candidates | open; scaffold [`../calibration/`](../calibration/) (checklist 2.3) |
| 5 | Indian FA workbook — archived as reference logic | **Vyom** (archive) | archived read-only; its data-layout discipline informs the ledger schema, **nothing else carries over unexamined** |

## Change control

- Any change to this plan's gates or thresholds (bench ≥15 unlocking A-entries, the four-quarter weight freeze, backtest greenlight, connector spend) is a policy change: **versioned edit, Vyom alone — never mid-analysis, never from one outcome** (Constitution 13; §16).
- Every version change (model, prompt, skill, retrieval arrangement) reruns Loop 1 on the affected skills before that version researches anything live (§16). Ledger rows record `system_version`, `skill_versions`, `model_ids`, so outcomes stay attributable to the system that produced them.
- Until benchmark-adjusted ledger data exists (first test: **January 2027**), the system's edge is described as unproven (Constitution 12) — the build order builds infrastructure, not a track record.
