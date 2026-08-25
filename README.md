# Investment OS v3.2

A research operating system for one investor. It widens the funnel, structures evidence, computes, and attacks theses — and **executes nothing**. Vyom writes every thesis, sets every size, and places every buy and sell by hand at the broker. There is no execution path in this system, by design.

- **Canonical spec:** [`spec/investment-os-v3.2-master-spec.md`](spec/investment-os-v3.2-master-spec.md) (v3.2.0, 25 Aug 2026)
- **How the system is built:** [`ARCHITECTURE.md`](ARCHITECTURE.md)
- **The 14 rules every agent runs under:** [`CONSTITUTION.md`](CONSTITUTION.md) — paste verbatim as the Claude Project instructions

## The loop in one paragraph

Streams (never Claude's memory) supply tickers into an inbox. `/triage` verifies the trigger, routes the name (earnings power → Playbook A/B; otherwise a specialist lens), and applies the trap filters — most names die here, logged with a reason. Survivors get an evidence pack (`/lock`), an underwrite in the fixed §8 order (price-implied expectations first, consensus only after your own read, variant thesis last), and two isolated red-team passes. Then the machine stops: Vyom writes the one-paragraph thesis and falsifiers in his own words — no paragraph, no position, not even a shadow one. The portfolio gate checks §9 caps, the logger writes the ledger row, and maintenance watches the falsifiers. Every surviving name is logged bought or not; results and calibration close the loop quarterly.

## Getting started (cycle 1 — Minimum Viable Loop)

Per [`runbooks/build-order.md`](runbooks/build-order.md):

1. Paste [`CONSTITUTION.md`](CONSTITUTION.md) into the Claude Project instruction block.
2. Create the inbox + ledger sheet from the column contracts in [`ledger/`](ledger/).
3. **Pre-register MOS in the ledger** — first mandatory action, flagged overdue in the spec. Draft awaiting sign-off: [`templates/mos-preregistration.md`](templates/mos-preregistration.md).
4. Backfill the July run as ledger rows 1–13 with 25-Aug marks ([`ledger/backfill-july/`](ledger/backfill-july/)).
5. Run `/results` on the WOR and WTC 26-Aug prints against their pre-registered falsifiers.
6. Run the MVL end to end: capture → triage → evidence lock → blind red team → **your** thesis → log.

## Map

| Directory | Contents |
| --- | --- |
| `.claude/skills/` | The 16 versioned skills (§14 registry): sweep, triage, lock, delta, underwrite-a/b/bio/exp/ss/dx/fin, redteam-blind/rebuttal, results, log, calibrate |
| `spec/` | The canonical master specification |
| `analysis/` | §6.3 lens method vocabularies shared across underwrite skills |
| `discovery/` | Lanes 1–3, the 8 Lane-2 channels, channel-scoring rules |
| `schemas/` | JSON Schemas: inbox row, triage verdict, evidence pack, ledger record |
| `templates/` | Thesis memo, evidence pack, red-team reports, results review, inbox capture, MOS pre-registration |
| `policy/` | Portfolio policy v1 (§9) · security model (§12) |
| `runbooks/` | Operating rhythm (8:6 roster, §13) · build order (§14) · maintenance |
| `calibration/` | Loop 1 golden-set scaffold · Loop 2 quarterly worksheets |
| `ledger/` | CSV column contracts, July backfill scaffold |
| `db/` | Supabase DDL (`leads`, `ledger`, `reviews`) with research-read-only / logger-insert-only role separation |

## Status

The system's edge is **unproven** until benchmark-adjusted ledger data exists — first test January 2027. Open items are owned, not hidden: see spec §"Open items".
