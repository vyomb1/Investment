# Ledger — the column contract

**Spec:** [§10 records, ledger, security separation; §14 build order](../spec/investment-os-v3.2-master-spec.md) · **Schemas (source of truth):** [`schemas/ledger-record.schema.json`](../schemas/ledger-record.schema.json), [`schemas/inbox-row.schema.json`](../schemas/inbox-row.schema.json) · **Write path:** [/log](../.claude/skills/log/SKILL.md) → the separate insert-only logger.

**One ledger** — it merges the July Ledger and the shadow book (§10). Every pipeline stage emits one record into it.

## Storage lifecycle

1. **Cycles 1–2: the Google Sheet is the operational store.** The CSVs in this directory define its columns **exactly**: the header rows here are the contract — the sheet's tabs must carry these headers, in this order, and nothing else. Create the sheet by copying the headers verbatim (README getting-started step 2).
2. **The JSON schemas are the source of truth** for record shape and permitted values. The CSVs are the schemas flattened for a spreadsheet; where sheet and schema ever disagree, the schema wins and the sheet gets a versioned fix. Records are validated in code against the schema *before* the logger hand-off (`/log` step 2) — the sheet stores, it never validates.
3. **Cycles 4–6: Supabase supersedes the sheet** — tables `leads`, `ledger`, `reviews` per [`db/001_init.sql`](../db/001_init.sql), with logger separation (research contexts: read-only role; logger: insert-only role; service-role keys never touch any agent). The July workbook thereafter becomes a **view/export layer, not the database** (§10). These CSVs remain the column contract for any export.

## Files

| File | Contents |
| --- | --- |
| [`inbox.csv`](inbox.csv) | Inbox tab columns — the spec §5 inbox schema verbatim, per [`schemas/inbox-row.schema.json`](../schemas/inbox-row.schema.json) |
| [`ledger.csv`](ledger.csv) | Ledger tab columns — the §10 record flattened, plus outcome columns |
| [`backfill-july/`](backfill-july/) | Instructions for backfilling the July run as rows 1–13 with 25-Aug marks |

## Flattening rule — JSON fields → JSON strings in cells

The wire format is JSON (validated against the schema in code). The sheet stores **one row per record**; scalar fields map one-to-one to columns; any field that is a JSON object or array is serialised as a **compact JSON string in a single cell**, and its column takes a `_json` suffix:

| Schema field | CSV column | Cell content |
| --- | --- | --- |
| `key_evidence` | `key_evidence_json` | JSON array of `{claim, label, source, as_of}` |
| `falsifiers` | `falsifiers_json` | JSON array of `{observable, threshold, check_date}` |
| `skill_versions` | `skill_versions_json` | JSON object, e.g. `{"/triage":"1.0","/lock":"1.0"}` |
| `model_ids` | `model_ids_json` | JSON array of exact model identifiers |
| `outcome.mark_6m` … `outcome.mark_36m` | `mark_6m` … `mark_36m` | JSON object `{position_return, benchmark_return, benchmark_name, as_of}` per mark; **blank until the mark is due** |
| `outcome.reason_match` | `reason_match` | Enum value (`pending`, `matched`, `right_for_wrong_reason`, `failed_for_stated_reason`, `failed_for_other_reason`) |
| — | `benchmark` | The scoring benchmark assigned to this name **at logging time**, per §10: S&P/ASX 300 accumulation (AU sleeve); S&P 500 total return + an energy/materials index (US sleeve); money-weighted. Declared before outcomes exist, never chosen after; each mark's `benchmark_name` must equal this cell. |

Cells holding JSON are regenerated from the validated record — never hand-edited in place. A cell that cannot be filled truthfully is left blank / NOT FOUND; a plausible invented value is a contract violation (§2.2).

## Rules that bind every row

- **Unlogged = doesn't exist** (spec §4 Log stage; Constitution rule 11). Nothing counts unless logged with `system_version`, `skill_versions`, `model_ids` attached — a row without them is refused, because it would be unattributable and therefore unscoreable (§16).
- **Writes go through the separate logger only** (§10, §12). Research contexts hold read-only credentials and never possess the write key. Week one (cycles 1–2), the sanctioned logger is **Vyom pasting the validated JSON himself** — same architecture, human as logger.
- **Corrections are new rows.** The ledger is insert-only end to end: a correction is a fresh record superseding the old one; the original row stays as history. Never edit or delete a row — that permanence is what keeps calibration honest.
- **Shadow-book rule (§10):** every name surviving the full pipeline is logged with pre-registered predictions and confidence — **bought or not**. Target **≥20 scored decisions/year** — a logging-discipline target on survivors, not a quota on names (fewer names, or zero, is always acceptable, §2.5). No entry, real or shadow, without Vyom's own one-paragraph thesis and written falsifiers (Constitution rule 8).
- **Kills are logged with their reasons** — they are data for §5 channel scoring and §11 calibration.
- `source_channel` and `coverage_class` are carried through from the inbox row unchanged — they feed the quarterly per-channel funnel.
