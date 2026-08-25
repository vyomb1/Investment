# db/ — Storage layer & migration runbook

**Implements:** [`spec/investment-os-v3.2-master-spec.md`](../spec/investment-os-v3.2-master-spec.md) §10 (records, ledger, security separation), §12 (security rules), §14 (build order). Frame: [`ARCHITECTURE.md`](../ARCHITECTURE.md) §6. Binding policy: [`policy/security-model.md`](../policy/security-model.md), [`CONSTITUTION.md`](../CONSTITUTION.md) rules 9–11.

One migration lives here: [`001_init.sql`](001_init.sql) — Supabase/Postgres DDL for `leads`, `ledger`, `reviews` with the `research_ro` / `logger_writer` role separation. **This database stores research records only. It has no execution path; Vyom places every order by hand.**

---

## 1. Storage lifecycle (spec §10, §14)

| Phase | When | Store | Contract |
| --- | --- | --- | --- |
| 1 | Cycles 1–2 | **Google Sheet** (operational store) | CSV headers in [`ledger/`](../ledger/) — the headers **are** the column contract; the Sheet's columns must match them exactly |
| 2 | Cycles 4–6, once the schema stabilises | **Supabase** tables `leads`, `ledger`, `reviews` via `001_init.sql` | [`schemas/inbox-row.schema.json`](../schemas/inbox-row.schema.json) (leads), [`schemas/ledger-record.schema.json`](../schemas/ledger-record.schema.json) (ledger) — same contract, now in SQL |
| — | Always | The **July workbook** is a view/export layer (`july_workbook_export`), never the database | — |

Rules that hold in **both** phases:

- **Append-only.** No logged row is ever edited or deleted — corrections are new rows. This applies to the Sheet era too: strike nothing, overwrite nothing, add a superseding row.
- **Nothing counts unless logged**, with `system_version`, `skill_versions`, `model_ids` attached (Constitution 11). The Sheet carries these columns from day one.
- **Logger separation** (spec §10): research contexts read; only the logger writes; the logger receives only human-validated JSON. Week one the logger is Vyom pasting the validated record himself — **same architecture, human as logger.**
- Schema changes are versioned edits by Vyom (§16) and land as new numbered migrations (`002_*.sql`, …), never edits to `001_init.sql` after it has been applied.

The migration happens **once the schema stabilises** — i.e. after cycles 1–3 have exercised the record shape end-to-end. Do not migrate earlier; do not let the Sheet linger past the point where the bench and A-entries make append volume painful.

## 2. Applying `001_init.sql`

Run as the **database owner** — a credential that exists only on Vyom's own machine (see §3).

**Option A — Supabase SQL editor:** paste the whole file, run once. It is transactional (`BEGIN … COMMIT`) and role creation is idempotent.

**Option B — psql:**

```sh
psql "$SUPABASE_DB_URL" -f db/001_init.sql
```

**Option C — Supabase CLI migrations:** copy to `supabase/migrations/<timestamp>_init.sql` and `supabase db push`.

Then, still as owner, create the two **login** users and attach them to the group roles (passwords never appear in this repo or in any agent context):

```sql
CREATE ROLE research_agent LOGIN PASSWORD '<set in Vyom''s password manager>';
GRANT research_ro TO research_agent;

CREATE ROLE logger LOGIN PASSWORD '<set in Vyom''s password manager>';
GRANT logger_writer TO logger;
```

**Verify before handing out any credential.** Run the verification block at the bottom of [`001_init.sql`](001_init.sql). Expected: as `logger_writer`, INSERT succeeds and SELECT/UPDATE/DELETE all fail; as `research_ro`, SELECT succeeds and INSERT/UPDATE/DELETE all fail. If any expected failure succeeds, stop — the separation is broken; fix before proceeding.

## 3. Key handling — which context gets which key (spec §10, §12)

| Context | Credential | Can | Can never |
| --- | --- | --- | --- |
| Research contexts (Claude) | `research_agent` (member of `research_ro`) + read-only data connectors | SELECT on all tables and views | Write anything, anywhere. No ledger write, no execution tools, ever. |
| Logger context | `logger` (member of `logger_writer`); **no web tools, no analysis** | INSERT into `leads` / `ledger` / `reviews` | UPDATE, DELETE, or even SELECT. Corrections are new rows. |
| Red-team contexts | **None.** They receive the evidence pack as content, not a database connection | — | Touch the database at all. |
| Vyom's admin console (his machine only) | Owner credential + Supabase **service-role key** | Migrations, user creation, verification | Be pasted into any agent context. **Service-role keys never touch any agent** — the service role bypasses RLS by design, which is exactly why. |

**Week one — human logger.** Before Supabase exists (and as fallback afterwards), Vyom is the logger: `/log` validates the JSON against [`schemas/ledger-record.schema.json`](../schemas/ledger-record.schema.json) and hands it back; Vyom pastes it into the Sheet (later: runs the INSERT as `logger`). Same architecture, human as logger — the write path still passes through exactly one insert-only actor holding no web tools.

**Lethal-trifecta check (spec §12)** before granting anything new: no context may combine private data + untrusted content + external write ability. Research contexts hold untrusted content → no write. The logger holds write → no untrusted content (human-validated JSON only) and no web tools.

## 4. Backfill order

**Cycle 1, into the Sheet (spec §14):**

1. **Pre-register MOS in the ledger** — first mandatory action, already overdue (spec §14 cycle 1; open item 1; draft awaiting sign-off at [`templates/mos-preregistration.md`](../templates/mos-preregistration.md)).
2. **Backfill the July run as ledger rows 1–13, with 25-Aug marks** in `outcome_marks`. Each backfilled row carries its `system_version` / `skill_versions` / `model_ids` as best recorded for the July run; anything genuinely unrecoverable is logged as NOT FOUND, never reconstructed from memory.
3. Run `/results` on the WOR and WTC 26-Aug prints against their pre-registered falsifiers (85% cash conversion; ~3x leverage + FCF conversion) and log the resulting rows.

**At Supabase migration (cycles 4–6), replay the Sheet through the logger:**

1. Freeze the Sheet (no new rows land there once replay starts; if a cycle is mid-flight, wait for its logging-hygiene day).
2. Insert **July rows 1–13 first, with their 25-Aug marks**, in original row order.
3. Insert every subsequent Sheet row in logged order (append order preserved — insert order is the audit order).
4. Reconcile: row counts match; spot-check one row per stage against the Sheet; confirm `july_workbook_export` reproduces the workbook rows.
5. Mark the Sheet read-only and label it as archive. The July workbook is now the `july_workbook_export` view — a projection of the ledger, never a second database.

All replay inserts go through the logger credential (or Vyom-as-logger). Nothing about backfill relaxes the separation.

## 5. Benchmarks for outcome marks (spec §10)

Outcome marks at 6/12/24/36 months are scored **vs benchmark, money-weighted**:

| Sleeve | Benchmark |
| --- | --- |
| AU | S&P/ASX 300 **accumulation** (total-return) index |
| US | S&P 500 **total return** + an energy/materials index (which index: set by Vyom via versioned edit) |

`reason_match` is scored alongside the marks: did the position succeed/fail *for the pre-registered reason*? A right answer for the wrong reason scores as luck. First edge-claim test date: **January 2027** (6-month column on the July cohort) — until benchmark-adjusted ledger data exists, the system's edge is described as unproven (Constitution 12).

## 6. Objects created by `001_init.sql`

| Object | Kind | Purpose |
| --- | --- | --- |
| `leads` | table | Discovery inbox (spec §5): `date, ticker, market, source_channel, coverage_class, one_line_mechanism, status` |
| `ledger` | table | The one ledger (spec §10): scalar columns for queryable fields; JSONB for `key_evidence`, `falsifiers`, `skill_versions`, `model_ids`, `outcome_marks`; `reason_match` scalar |
| `reviews` | table | Falsifier/results reviews with the 7-day `due_at` rule; append-only open/resolve rows |
| `july_workbook_export` | view | The July workbook as an export layer over `ledger` (stub — refine the projection, never the tables) |
| `reviews_current` | view | Latest state per review thread; `resolved_at IS NULL` past `due_at` = overdue, nothing trades |
| `research_ro` | role | SELECT only, all tables and views — the only DB credential any research context may hold |
| `logger_writer` | role | INSERT only, three tables — no UPDATE/DELETE/SELECT; held only by the logger |

Row-level security is enabled on all three tables with policies mirroring the grants; no UPDATE or DELETE policy exists for anyone. `PUBLIC` (and Supabase `anon`/`authenticated`, where present) hold no privileges.
