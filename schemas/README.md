# schemas/ — wire formats for Investment OS v3.2

Every object that moves between pipeline stages is JSON, validated against one of the four schemas below (JSON Schema draft 2020-12, `additionalProperties: false`, every property described, spec sections cited in each `description`). Spec: [`spec/investment-os-v3.2-master-spec.md`](../spec/investment-os-v3.2-master-spec.md) (v3.2.0). Component map: [`ARCHITECTURE.md`](../ARCHITECTURE.md) §6.1.

## The four schemas

| Schema | Object | Spec | Produced by | Consumed by |
| --- | --- | --- | --- | --- |
| [`inbox-row.schema.json`](inbox-row.schema.json) | Inbox row | §5 | Discovery [S1A] capture — 10 s from a phone; Lane 1 alerts, Lane 2 channels 1–8, Lane 3 human flow | /triage |
| [`triage-verdict.schema.json`](triage-verdict.schema.json) | Triage verdict | §3, §4, §6.4 | /triage (Verify [S1B] + Triage [S2]: identity, trigger check, two-axis routing, trap filters) | Vyom skim → /lock, or the kill log; /log either way |
| [`evidence-pack.schema.json`](evidence-pack.schema.json) | Evidence pack | §2, §4, §7 | /lock (+ /delta) at Evidence lock [S3]; Vyom verifies load-bearing facts | Underwrite skills [S4], **blind red team (pack only)**, rebuttal red team, synthesis |
| [`ledger-record.schema.json`](ledger-record.schema.json) | Ledger record | §10 | Every stage, via /log | Logger → ledger; /results [S8]; /calibrate [S15] |

Notes that follow from the spec, enforced in the schemas themselves:

- **Evidence pack neutrality:** `pack_neutral` must be `true` — the pack feeds the blind red team (§7 Pass 1), which never sees the thesis or discovery transcript. CALC claims require a `formula`, EST claims a `sensitivity`, CONFLICT claims a `conflict_note` (§2.2). `NOT_FOUND` is a valid label and a good answer; failed sources are logged in `sources_failed`, never silently substituted (§2.3).
- **Triage verdicts:** any fired §6.4 trap, a false trigger, or `elevated_peak` on Axis 2 forces `verdict: "kill"` at the schema level; kills carry a `kill_reason` and are logged — kills are data for channel scoring (§5) and calibration (§11).
- **Ledger records:** the §10 field list verbatim, plus outcome columns (6/12/24/36-month marks vs benchmark, nullable until due, and `reason_match` — a right answer for the wrong reason scores as luck). `system_version`, `skill_versions`, `model_ids` are required on every row: nothing counts unless logged with versions attached (Constitution rule 11).

## Shared enums

Four enums appear in more than one schema. They are defined in each file's `$defs` and must stay **byte-identical** wherever they appear:

| Enum | Values |
| --- | --- |
| `coverage_class` | `C0`, `C1`, `C2`, `C3` (§2.1) |
| evidence `label` | `FACT`, `CALC`, `EST`, `INFERENCE`, `NOT_FOUND`, `CONFLICT` (§2.2) |
| `route` | `A`, `B`, `Peak`, `lens-bio`, `lens-exp`, `lens-ss`, `lens-dx`, `lens-fin`, `lens-resources`, `lens-tech` (§3, §6.3) |
| `source_channel` | `lane1_bench_alert`, `ch1_index_deletions` … `ch8_tax_loss`, `lane3_human`, `vyom_direct` (§5) |

**Enums change only by versioned edit** (spec §16; Constitution rule 13 — never mid-analysis, never from one outcome): bump the spec version, note it in the change log, update every schema that carries the enum in the same edit, and rerun Loop 1 on affected skills before the new version researches anything live. Vyom alone approves such edits (decision-rights table).

## Validation before the ledger

Validation runs **in code** — a schema check executed by /log, not an eyeball pass — before any ledger handoff. The flow (spec §10, §12):

1. A stage emits its JSON; /log validates it against the matching schema here.
2. Invalid JSON never reaches the logger. It goes back to the emitting stage; an unlogged record doesn't exist (Constitution rule 11).
3. Only the **separate insert-only logger** writes validated records to the ledger. It holds no web tools; research contexts hold read-only credentials and never possess the write key. Week-one sanctioned logger: Vyom pasting the validated JSON himself — same architecture, human as logger.

Nothing in these schemas describes an order, a broker, or an execution path. The system has none; Vyom places every buy and sell manually.
