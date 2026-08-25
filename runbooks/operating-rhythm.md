# Operating Rhythm — the 8:6 Roster

**Runbook** · Operator: **Vyom** · Spec: [`../spec/investment-os-v3.2-master-spec.md`](../spec/investment-os-v3.2-master-spec.md) v3.2.0 **§13** (normative), with §4, §5, §11 bindings. Where this file and the spec disagree, the spec wins and this file gets a versioned fix (§16).

> The roster is the budget, and the budget is a design input: the ≤15 min/name triage bound, the one-deep-block rule, and the kill rules all exist so a full research cycle fits inside 8 swing days × 15 min + 6 R&R days. When time is lost, the system drops to a **named degradation mode** (below) — it never cuts corners silently.

---

## The cycle at a glance

| Days | Mode | Time budget | Work | Forbidden |
| --- | --- | --- | --- | --- |
| Swing 1–8 | Capture | **15 min/day, phone only** | Read alerts; capture tickers to the inbox with tags | **Analysis of any kind on site** |
| R&R 1 | Intake | **~3h** | /sweep + Lane-3 adds + triage the inbox (**≤15 min/name**) | Deep work on any single name |
| R&R 2–5 | Deep work | **One block/day** | ONE of: an underwrite · a red-team + synthesis · bench-building (~5 candidates/cycle) | A second block; mixing blocks |
| R&R 6 (last) | Hygiene | — | Logging hygiene · falsifier checks · alerts set for the swing | Starting new research |
| + Quarterly (first R&R after quarter-end) | Calibration | — | Loop-2 calibration via [/calibrate](../.claude/skills/calibrate/SKILL.md) | — |

---

## On swing (8 days) — 15 min/day, phone only

Daily checklist:

- [ ] Read alerts: bench price alerts (Lane 1), falsifier/`next_check` alerts ([`maintenance.md`](maintenance.md)), channel feeds routed to the phone.
- [ ] Capture anything that deserves 15 minutes: **one inbox row, ten seconds, one line** per [`../templates/inbox-capture.md`](../templates/inbox-capture.md) — `date, ticker, market, source_channel, coverage_class, one_line_mechanism, status=new` ([`../schemas/inbox-row.schema.json`](../schemas/inbox-row.schema.json)).
- [ ] Stop at 15 minutes.

Rules:

- **No analysis on site** (§13). Capture and analysis are never the same activity (§5). If a second line is forming, stop — that is a deep block's job.
- Tickers come from the streams or from Vyom, never from model memory (Constitution 2); every row carries its `source_channel` tag and C-class.
- A fired bench alert (pre-set §8 buy price hit) still enters the inbox as `lane1_bench_alert`. The name is pre-underwritten and its prices pre-computed precisely so no on-site analysis is needed — and whether/when to act on it is Vyom's alone, at his broker, by hand. The system executes nothing.
- Fewer names, or zero, is always acceptable (§2.5). A quiet swing is a fine swing.

## R&R day 1 — intake (~3h)

- [ ] Run [/sweep](../.claude/skills/sweep/SKILL.md): all 8 Lane-2 channels ([`../discovery/channels.md`](../discovery/channels.md)), coverage class declared per channel run, failed sources logged never substituted.
- [ ] Add Lane-3 names gathered during the swing — **forums supply tickers, never theses** (§5); each row tagged `lane3_human`.
- [ ] Triage the inbox with [/triage](../.claude/skills/triage/SKILL.md): Verify [S1B] then Triage [S2] with the §6.4 trap filters, at **≤15 min/name — a hard bound**, not a target. A name that needs more than 15 minutes to justify itself hasn't.
- [ ] Log every verdict via [/log](../.claude/skills/log/SKILL.md) — kills **with reasons** (kills are data for channel scoring §5 and calibration §11). Unlogged = doesn't exist.
- [ ] Queue the survivors for days 2–5. Ordering the queue is scheduling, not analysis.

## R&R days 2–5 — ONE deep block per day

Pick exactly one block per day. Never two; never a hybrid.

| Block | Content | Stages / skills |
| --- | --- | --- |
| **An underwrite** | One queued name through Evidence lock and Underwrite, §8 ordering fixed: price-implied expectations (mechanical, first) → primary evidence → consensus snapshot (after your own read) → variant thesis | [/lock](../.claude/skills/lock/SKILL.md) + [/delta](../.claude/skills/delta/SKILL.md) [S3] → /underwrite-a·b·bio·exp·ss·dx·fin [S4] |
| **A red-team + synthesis** | Blind pass (fresh context, evidence pack only), then — cost-gated, names heading toward a real position — the rebuttal pass; then **Vyom writes the one-paragraph thesis and falsifiers, unaided**; portfolio gate; log | [/redteam-blind](../.claude/skills/redteam-blind/SKILL.md), [/redteam-rebuttal](../.claude/skills/redteam-rebuttal/SKILL.md) [S5] → Synthesis [S6/S9] → gate [U6] ([`../policy/portfolio-policy-v1.md`](../policy/portfolio-policy-v1.md)) → /log |
| **Bench-building** | ~5 candidates/cycle from cycle 3 — pre-underwrite Lane-1 compounders and pre-compute bear/base buy prices from §8 | [`../discovery/channels.md`](../discovery/channels.md) Lane 1 |

Rules:

- A block that **kills** its name is a full success — no quotas (§2.5), and every kill is logged with its reason.
- A name that can't finish inside its block parks cleanly at a stage boundary and waits. It does not bleed into the next day's block.
- A blind-pass discovery of a missed **fact** forces a return to evidence lock (§7) — that re-lock consumes the block; it is never squeezed in.
- Can't write the paragraph → **bench or bin** (§4 synthesis kill rule). Every survivor is logged **bought or not** (shadow-book rule, §10).

## Last R&R day — hygiene (day 6 on a full roster)

- [ ] **Logging hygiene:** every stage touched this cycle emitted its ledger record ([`../schemas/ledger-record.schema.json`](../schemas/ledger-record.schema.json)); kills carry reasons; survivors are logged bought or not; `system_version`, `skill_versions`, `model_ids` attached to every row. Nothing counts unless logged (Constitution 11).
- [ ] **Falsifier checks:** sweep the ledger for `next_check` dates and falsifier `check_date`s now due; anything already triggered opens the 7-day review clock **today** — see [`maintenance.md`](maintenance.md).
- [ ] **Alerts set for the swing:** an alert per falsifier observable whose `check_date` falls in the coming swing; every bench name's price alert live at its current pre-set prices; /results runs diaried for known events (earnings prints, readouts) in the window.
- [ ] Inbox status current: every row carries an accurate `status`; new captures since day 1 sit as `new` for next cycle's day 1 — they wait, they are not squeezed in.
- [ ] No open review is drifting toward its 7-day due date unresolved.

## Quarterly — first R&R after quarter-end

- [ ] Run **Loop-2 calibration** via [/calibrate](../.claude/skills/calibrate/SKILL.md) (§11): Brier scores on stated confidences (Vyom's and Claude's, **separately**); channel hit rates (§5 scoring: leads → triage survival → shadow-book entries → 12-month result vs benchmark, per channel); gate/threshold review; reason-match audit.
- [ ] Channel weights stay frozen until **four quarters of scored data exist** (§5 anti-overfit rule); after that, prune losers, feed winners — by versioned edit, Vyom alone (Constitution 13).
- First edge-claim test date: **January 2027** (§11). Until then the system's edge is described as unproven (Constitution 12).

---

## Degradation mode (§13, verbatim)

> **Degradation mode:** if a cycle's R&R is lost, run capture + falsifier monitoring only; nothing new enters the shadow book that cycle. The system pauses cleanly; it never cuts corners silently.

Operationally:

| Still runs | Stops |
| --- | --- |
| Swing-style capture (15 min/day, phone, inbox rows) | /sweep, triage, all deep blocks, bench-building |
| Falsifier monitoring and the 7-day review rule — **this never lapses** ([`maintenance.md`](maintenance.md)) | Any new shadow-book entry this cycle |

The inbox simply holds; the next full R&R resumes at day 1. A half-run pipeline stage, an untriaged "quick look", or an unlogged decision is exactly the silent corner-cutting this mode exists to prevent.

## Minimum Viable Loop (cycles 1–2 — mandatory before extras)

> **capture → triage → evidence lock → blind red team → your thesis → log** (§13, verbatim)

| MVL step | Stage | Actor / skill |
| --- | --- | --- |
| capture | Discovery [S1A] | inbox row, ten seconds ([`../templates/inbox-capture.md`](../templates/inbox-capture.md)) |
| triage | Verify [S1B] + Triage [S2] | [/triage](../.claude/skills/triage/SKILL.md), ≤15 min/name |
| evidence lock | Evidence lock [S3] | [/lock](../.claude/skills/lock/SKILL.md); Vyom verifies load-bearing facts |
| blind red team | Red team [S5], pass 1 | [/redteam-blind](../.claude/skills/redteam-blind/SKILL.md) — fresh context, pack only |
| **your thesis** | Synthesis [S6/S9] | **Vyom, unaided wording** — one paragraph + written falsifiers |
| log | Log | [/log](../.claude/skills/log/SKILL.md) via the sanctioned logger (week one: Vyom pasting the validated JSON himself, §10) |

Nothing beyond the MVL runs in cycles 1–2 — no rebuttal pass, no bench-building, no extras — until this loop runs clean end-to-end. What unlocks when is governed by [`build-order.md`](build-order.md).
