-- ============================================================================
-- Investment OS v3.2 — db/001_init.sql
-- Postgres / Supabase DDL for the storage layer of spec §10.
--
-- Spec:        spec/investment-os-v3.2-master-spec.md (v3.2.0, 25 Aug 2026)
--              §10 records/ledger/security separation · §12 security rules ·
--              §14 build order (this migration lands at cycles 4–6, once the
--              schema has stabilised in the Google-Sheet era of cycles 1–2).
-- Contracts:   leads   mirrors schemas/inbox-row.schema.json   (spec §5 inbox)
--              ledger  mirrors schemas/ledger-record.schema.json (spec §10)
--              reviews implements the falsifier / results review discipline
--              (spec §4 Maintenance [S16] + Results interpreter [S8];
--               Constitution rule 9: triggered falsifier → logged review
--               within seven days, before any trade).
--              The CSV headers in ledger/ are the same column contract for the
--              Sheet era; this DDL is that contract in SQL.
--
-- ============================================================================
-- SECURITY MODEL — read this before touching anything (spec §10, §12).
--
--   The system has ZERO execution capability. There is no broker connector
--   and no order tool anywhere; Vyom places every buy and sell by hand.
--   This database is an audit trail and decision-support store, nothing more.
--
--   Two Postgres roles implement the logger separation of spec §10:
--
--     research_ro    SELECT only, on all three tables and the views.
--                    This is the ONLY database credential a research context
--                    may ever hold. Research contexts touch untrusted web
--                    content, so they get no write path of any kind
--                    (lethal-trifecta rule, §12: private data + untrusted
--                    content + write ability never share a context).
--
--     logger_writer  INSERT only, on leads / ledger / reviews.
--                    NO UPDATE. NO DELETE. NO SELECT. Corrections are new
--                    rows — history is never rewritten. The logger context
--                    holds ONLY this credential and NO web tools: it receives
--                    nothing but human-validated JSON (the /log skill
--                    validates against schemas/ before anything is inserted).
--                    Week-one sanctioned logger: Vyom pasting the validated
--                    record himself — same architecture, human as logger.
--
--   The Supabase service-role key (and the postgres owner credential)
--   BYPASSES row-level security by design. Therefore it NEVER touches any
--   agent — not the research contexts, not the logger, not anything (§10:
--   "service-role keys never touch any agent"). It lives only with Vyom,
--   on his own machine, for migrations and administration.
--
--   Enforcement is belt AND braces:
--     belt   — grants: each role is granted exactly its verb, nothing more,
--              and ALL privileges are revoked from PUBLIC (and from the
--              Supabase anon/authenticated roles, which Supabase default
--              privileges would otherwise silently grant).
--     braces — row-level security is ENABLED on every table with policies
--              that mirror the grants exactly: a SELECT policy for
--              research_ro, an INSERT policy for logger_writer, and NO
--              UPDATE or DELETE policy for anyone. Even a mistaken future
--              grant cannot make a row updatable or deletable while no such
--              policy exists.
--
--   RLS here enforces VERB separation, not row filtering: research_ro may
--   read every row (USING true), logger_writer may insert any schema-valid
--   row (WITH CHECK true). There are no per-row secrets in this system;
--   there is a hard wall between reading and writing.
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- 0. Roles (idempotent — CREATE ROLE has no IF NOT EXISTS)
--    Both are NOLOGIN group roles. Actual LOGIN users are created by Vyom,
--    from his own machine, and granted membership — see db/README.md.
-- ----------------------------------------------------------------------------
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'research_ro') THEN
    CREATE ROLE research_ro NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'logger_writer') THEN
    CREATE ROLE logger_writer NOLOGIN;
  END IF;
END
$$;

COMMENT ON ROLE research_ro IS
  'Spec §10/§12: read-only credential for research contexts. SELECT only, on leads/ledger/reviews and the export views. Research contexts hold no execution tools and no write path, ever.';
COMMENT ON ROLE logger_writer IS
  'Spec §10: the separate logger. INSERT only on leads/ledger/reviews — no UPDATE, no DELETE, no SELECT. Corrections are new rows. The logger context holds only this credential and no web tools; it receives only human-validated JSON. Week one: Vyom pasting the record himself — same architecture, human as logger.';

-- ----------------------------------------------------------------------------
-- 1. leads — the discovery inbox (spec §5; mirrors schemas/inbox-row.schema.json)
--    "Inbox schema: date, ticker, market, source_channel, coverage_class,
--     one_line_mechanism, status. Ten seconds from a phone on site; capture
--     and analysis are never the same activity."
--    Append-only: a lead's later life (verified, killed, routed) is recorded
--    as ledger rows, not by editing the lead.
-- ----------------------------------------------------------------------------
CREATE TABLE public.leads (
  id                  bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  logged_at           timestamptz NOT NULL DEFAULT now(),

  -- capture fields, verbatim from the spec §5 inbox schema -------------------
  date                date        NOT NULL,
  ticker              text        NOT NULL,
  market              text        NOT NULL,
  source_channel      text        NOT NULL,
  coverage_class      text        NOT NULL
                        CONSTRAINT leads_coverage_class_valid
                        CHECK (coverage_class IN ('C0', 'C1', 'C2', 'C3')),
  one_line_mechanism  text        NOT NULL,
  status              text        NOT NULL
);

COMMENT ON TABLE public.leads IS
  'Spec §5 discovery inbox (mirrors schemas/inbox-row.schema.json). One row per captured lead, source-tagged, C-class declared. Streams supply names — Claude never originates tickers from memory (§5, Constitution rule 2). Append-only; corrections are new rows.';
COMMENT ON COLUMN public.leads.id IS
  'Surrogate key. Insert order is the audit order.';
COMMENT ON COLUMN public.leads.logged_at IS
  'Insert timestamp (spec §10 discipline: nothing counts unless logged).';
COMMENT ON COLUMN public.leads.date IS
  'Capture date as written by the operator (spec §5 inbox schema).';
COMMENT ON COLUMN public.leads.ticker IS
  'Ticker as captured. Never model-originated: leads come from named streams or from Vyom (Constitution rule 2).';
COMMENT ON COLUMN public.leads.market IS
  'Listing market/exchange for the ticker (spec §5 inbox schema).';
COMMENT ON COLUMN public.leads.source_channel IS
  'Spec §5 channel tag (Lane 1 bench alert, Lane 2 channels 1–8, Lane 3 human flow). Feeds quarterly channel scoring; weights frozen until four quarters of scored data exist (§5 anti-overfit rule).';
COMMENT ON COLUMN public.leads.coverage_class IS
  'Spec §2.1: C0 user-supplied set · C1 enumerated universe · C2 bounded-source harvest · C3 open-web scout. Declared at capture; downgrades on blocked/dynamic/paywalled/truncated sources; never upgraded by more searching.';
COMMENT ON COLUMN public.leads.one_line_mechanism IS
  'Why this deserves 15 minutes — the suspected mispricing cause, one line (spec §5).';
COMMENT ON COLUMN public.leads.status IS
  'Inbox status; permitted values per schemas/inbox-row.schema.json. Kept as text — the schema layer, not the database, owns the vocabulary.';

-- ----------------------------------------------------------------------------
-- 2. ledger — the one ledger (spec §10; mirrors schemas/ledger-record.schema.json)
--    Merges the July Ledger and the shadow book. Every pipeline stage emits
--    exactly one JSON record; the /log skill validates it against the schema
--    and the logger inserts it. Unlogged = does not exist (Constitution 11).
--
--    Scalar columns for the queryable fields; JSONB for the structured ones.
--    Append-only: later outcome marks, corrections, and reversals (the ENGN
--    rule — the system changes its mind and logs why) arrive as NEW rows for
--    the same ticker/stage. The latest row is current; history is evidence.
-- ----------------------------------------------------------------------------
CREATE TABLE public.ledger (
  id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  logged_at       timestamptz NOT NULL DEFAULT now(),

  -- queryable scalars, verbatim fields from the spec §10 record --------------
  ticker          text    NOT NULL,
  date            date    NOT NULL,
  stage           text    NOT NULL,
  route           text    NOT NULL,
  verdict         text    NOT NULL,
  confidence      numeric NOT NULL
                    CONSTRAINT ledger_confidence_0_1
                    CHECK (confidence >= 0 AND confidence <= 1),
  size_or_shadow  text    NOT NULL,
  source_channel  text    NOT NULL,
  coverage_class  text    NOT NULL
                    CONSTRAINT ledger_coverage_class_valid
                    CHECK (coverage_class IN ('C0', 'C1', 'C2', 'C3')),
  system_version  text    NOT NULL,
  next_check      date,

  -- structured JSONB groups (shapes owned by schemas/ledger-record.schema.json)
  key_evidence    jsonb   NOT NULL
                    CONSTRAINT ledger_key_evidence_is_array
                    CHECK (jsonb_typeof(key_evidence) = 'array'),
  falsifiers      jsonb   NOT NULL
                    CONSTRAINT ledger_falsifiers_is_array
                    CHECK (jsonb_typeof(falsifiers) = 'array'),
  skill_versions  jsonb   NOT NULL,
  model_ids       jsonb   NOT NULL,

  -- outcome columns (spec §10: per position/shadow entry) --------------------
  outcome_marks   jsonb
                    CONSTRAINT ledger_outcome_marks_is_object
                    CHECK (outcome_marks IS NULL OR jsonb_typeof(outcome_marks) = 'object'),
  reason_match    boolean
);

COMMENT ON TABLE public.ledger IS
  'Spec §10: the one ledger (merges July Ledger + shadow book; mirrors schemas/ledger-record.schema.json). Every stage emits one record; every survivor is logged bought or not (shadow-book rule, target >= 20 scored decisions/year); every kill is logged with its reason. Append-only — corrections and later marks are new rows. Nothing counts unless logged with versions attached (Constitution 11).';
COMMENT ON COLUMN public.ledger.id IS
  'Surrogate key; insert order is the audit order. reviews.ledger_row points here.';
COMMENT ON COLUMN public.ledger.logged_at IS
  'Insert timestamp — when the logger persisted the record.';
COMMENT ON COLUMN public.ledger.ticker IS
  'Spec §10 record field. Identity confirmed upstream per Constitution rule 4.';
COMMENT ON COLUMN public.ledger.date IS
  'Spec §10 record field: the decision/record date stated in the JSON (distinct from logged_at).';
COMMENT ON COLUMN public.ledger.stage IS
  'Spec §4 pipeline stage that emitted the record (Discovery [S1A] … Calibrate [S15]); tokens per schemas/ledger-record.schema.json.';
COMMENT ON COLUMN public.ledger.route IS
  'Spec §3/§10: A / B / Peak / specialist lens. Lenses per §6.3; tokens per schemas/ledger-record.schema.json.';
COMMENT ON COLUMN public.ledger.verdict IS
  'Spec §10 record field: the stage outcome (e.g. route-or-kill at triage, held/failed at results).';
COMMENT ON COLUMN public.ledger.confidence IS
  'Spec §10: confidence in [0,1] as stated at logging time. Feeds Loop 2 Brier scoring (§11) — Vyom and Claude scored separately.';
COMMENT ON COLUMN public.ledger.size_or_shadow IS
  'Spec §10: real position size (set by Vyom alone, within §9 caps) or shadow-book marker. No position — real or shadow — exists without Vyom''s own thesis paragraph and written falsifiers (Constitution 8).';
COMMENT ON COLUMN public.ledger.source_channel IS
  'Spec §5 channel tag carried through from the lead; joins ledger outcomes back to channels for quarterly channel scoring.';
COMMENT ON COLUMN public.ledger.coverage_class IS
  'Spec §2.1 coverage class declared for the retrieval run behind this record.';
COMMENT ON COLUMN public.ledger.system_version IS
  'Spec §16: the spec version that produced this row, so outcome changes stay attributable to system changes.';
COMMENT ON COLUMN public.ledger.next_check IS
  'Spec §10 record field: next scheduled falsifier/maintenance check date. Drives the Maintenance stage [S16] alert sweep.';
COMMENT ON COLUMN public.ledger.key_evidence IS
  'Spec §10: array of {claim, label, source, as_of}. Labels per §2.2 (FACT/CALC/EST/INFERENCE/NOT FOUND/CONFLICT); every load-bearing number carries source + as-of date (§2.4).';
COMMENT ON COLUMN public.ledger.falsifiers IS
  'Spec §10: array of {observable, threshold, check_date}. Written and signed off by Vyom alone. A triggered falsifier forces a logged review within 7 days, before any trade (Constitution 9) — see reviews table.';
COMMENT ON COLUMN public.ledger.skill_versions IS
  'Spec §10/§16: versions of every skill that touched this record. Loop 1 reruns on any version change.';
COMMENT ON COLUMN public.ledger.model_ids IS
  'Spec §10/§16: model identifiers that produced this record, so outcomes are attributable across model changes.';
COMMENT ON COLUMN public.ledger.outcome_marks IS
  'Spec §10 outcome columns: mark at 6/12/24/36 months vs benchmark, keyed 6m/12m/24m/36m (canonical shape in schemas/ledger-record.schema.json). Benchmarks: S&P/ASX 300 accumulation (AU sleeve); S&P 500 total return + an energy/materials index (US sleeve); money-weighted. NULL until the first mark exists; later marks arrive as new rows (append-only).';
COMMENT ON COLUMN public.ledger.reason_match IS
  'Spec §10: did it succeed/fail FOR THE PRE-REGISTERED REASON? A right answer for the wrong reason scores as luck. NULL until resolved by /results.';

-- ----------------------------------------------------------------------------
-- 3. reviews — falsifier-triggered and results reviews
--    Spec §4 Maintenance [S16]: "Falsifier hit → review within 7 days, logged
--    before any trade." Spec §4 Results interpreter [S8]: did the event match
--    the pre-registered thesis? Constitution rule 9 binds the 7-day rule.
--
--    Append-only like everything else: a review is OPENED by one insert
--    (resolution NULL) and RESOLVED by a later insert for the same ledger_row
--    carrying resolution + resolved_at. The reviews_current view shows the
--    latest state of each review thread. The logger cannot update, so the
--    open row remains as permanent evidence of when the clock started.
-- ----------------------------------------------------------------------------
CREATE TABLE public.reviews (
  id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  ledger_row    bigint      NOT NULL REFERENCES public.ledger (id),
  trigger_type  text        NOT NULL
                  CONSTRAINT reviews_trigger_type_valid
                  CHECK (trigger_type IN ('falsifier', 'results')),
  opened_at     timestamptz NOT NULL DEFAULT now(),
  due_at        timestamptz NOT NULL DEFAULT (now() + interval '7 days'),
  resolution    text,
  resolved_at   timestamptz
);

COMMENT ON TABLE public.reviews IS
  'Falsifier-triggered and results reviews (spec §4 [S16]/[S8]; Constitution 9). Append-only: open with one insert (resolution NULL), resolve with a later insert for the same ledger_row. Hold/add/exit is decided by Vyom against pre-registered criteria, logged BEFORE any trade.';
COMMENT ON COLUMN public.reviews.ledger_row IS
  'The ledger row whose falsifiers or pre-registered thesis this review examines.';
COMMENT ON COLUMN public.reviews.trigger_type IS
  '''falsifier'' = a pre-registered falsifier observable crossed its threshold (Maintenance [S16]); ''results'' = event vs pre-registered thesis review (Results interpreter [S8], /results).';
COMMENT ON COLUMN public.reviews.opened_at IS
  'When the review clock started.';
COMMENT ON COLUMN public.reviews.due_at IS
  'The 7-day rule (spec §4, Constitution 9): defaults to opened_at + 7 days. Review is logged before any trade.';
COMMENT ON COLUMN public.reviews.resolution IS
  'Hold / add / exit vs pre-registered criteria, plus reasoning reference. NULL on the opening row; filled on the resolving insert. Decided by Vyom alone.';
COMMENT ON COLUMN public.reviews.resolved_at IS
  'When the resolving row was written. NULL on the opening row.';

-- ----------------------------------------------------------------------------
-- 4. Indexes — the queries the operating rhythm actually runs (spec §5, §13)
-- ----------------------------------------------------------------------------
CREATE INDEX idx_leads_ticker          ON public.leads  (ticker);
CREATE INDEX idx_leads_source_channel  ON public.leads  (source_channel);  -- channel scoring (§5)
CREATE INDEX idx_leads_status          ON public.leads  (status);          -- R&R day 1 inbox triage (§13)

CREATE INDEX idx_ledger_ticker         ON public.ledger (ticker);
CREATE INDEX idx_ledger_ticker_date    ON public.ledger (ticker, date);
CREATE INDEX idx_ledger_stage          ON public.ledger (stage);           -- pipeline funnel queries (§4)
CREATE INDEX idx_ledger_source_channel ON public.ledger (source_channel);  -- quarterly channel scoring (§5)
CREATE INDEX idx_ledger_next_check     ON public.ledger (next_check)
  WHERE next_check IS NOT NULL;                                            -- falsifier alert sweep [S16]

CREATE INDEX idx_reviews_ledger_row    ON public.reviews (ledger_row);
CREATE INDEX idx_reviews_open_due      ON public.reviews (due_at)
  WHERE resolved_at IS NULL;                                               -- overdue 7-day reviews

-- ----------------------------------------------------------------------------
-- 5. Views — the export layer
--    security_invoker = true (Postgres 15+ / current Supabase): the view runs
--    with the CALLER''s privileges, so research_ro grants and table RLS apply
--    through the view instead of being silently bypassed via the view owner.
-- ----------------------------------------------------------------------------

-- Spec §10/§14: "the July workbook … thereafter becomes a view/export layer,
-- not the database." This is that layer — a stub until the workbook columns
-- are frozen at migration time. It projects the ledger in workbook order and
-- flattens the four outcome marks; refine the projection (never the tables)
-- as the workbook evolves.
CREATE VIEW public.july_workbook_export
WITH (security_invoker = true) AS
SELECT
  l.id                     AS ledger_row,
  l.ticker,
  l.date,
  l.stage,
  l.route,
  l.verdict,
  l.confidence,
  l.size_or_shadow,
  l.source_channel,
  l.coverage_class,
  l.outcome_marks -> '6m'  AS mark_6m,
  l.outcome_marks -> '12m' AS mark_12m,
  l.outcome_marks -> '24m' AS mark_24m,
  l.outcome_marks -> '36m' AS mark_36m,
  l.reason_match,
  l.next_check,
  l.system_version,
  l.logged_at
FROM public.ledger l
ORDER BY l.id;

COMMENT ON VIEW public.july_workbook_export IS
  'Spec §10: the July workbook as a view/export layer over the ledger, not a database. Backfilled July rows 1–13 (25-Aug marks) appear here like every other row. Export stub — refine the projection when workbook columns freeze; the tables never bend to the workbook.';

-- Current state of each review thread under the append-only model: the most
-- recent insert per (ledger_row, trigger_type) wins. Open = resolved_at IS NULL.
CREATE VIEW public.reviews_current
WITH (security_invoker = true) AS
SELECT DISTINCT ON (r.ledger_row, r.trigger_type)
  r.id,
  r.ledger_row,
  r.trigger_type,
  r.opened_at,
  r.due_at,
  r.resolution,
  r.resolved_at
FROM public.reviews r
ORDER BY r.ledger_row, r.trigger_type, r.id DESC;

COMMENT ON VIEW public.reviews_current IS
  'Latest row per review thread (reviews is append-only; resolutions are new inserts). A row here with resolved_at IS NULL and due_at in the past is an OVERDUE 7-day review — nothing trades until it is logged (Constitution 9).';

-- ----------------------------------------------------------------------------
-- 6. Privileges — the belt.
--    Start from zero: revoke everything from PUBLIC, then grant each role
--    exactly its verb.
-- ----------------------------------------------------------------------------
REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON TABLE public.leads, public.ledger, public.reviews FROM PUBLIC;
REVOKE ALL ON TABLE public.july_workbook_export, public.reviews_current FROM PUBLIC;

-- Supabase projects ship ALTER DEFAULT PRIVILEGES that auto-grant table access
-- to anon / authenticated (API roles). Strip those grants explicitly wherever
-- the roles exist — no PostgREST/API surface reaches these tables. On plain
-- Postgres the roles are absent and this block is a no-op.
DO $$
DECLARE
  api_role text;
BEGIN
  FOREACH api_role IN ARRAY ARRAY['anon', 'authenticated'] LOOP
    IF EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = api_role) THEN
      EXECUTE format('REVOKE ALL ON TABLE public.leads, public.ledger, public.reviews FROM %I', api_role);
      EXECUTE format('REVOKE ALL ON TABLE public.july_workbook_export, public.reviews_current FROM %I', api_role);
    END IF;
  END LOOP;
END
$$;

-- Both roles may resolve names in the schema; nothing more at schema level.
GRANT USAGE ON SCHEMA public TO research_ro, logger_writer;

-- research_ro: SELECT only, on all three tables and both views (spec §10).
GRANT SELECT ON public.leads, public.ledger, public.reviews TO research_ro;
GRANT SELECT ON public.july_workbook_export, public.reviews_current TO research_ro;

-- logger_writer: INSERT only, on the three tables. Deliberately NO SELECT —
-- the logger cannot even read the ledger, only append to it. NO UPDATE and
-- NO DELETE — corrections are new rows (spec §10). Note: no RETURNING clause
-- in logger inserts; RETURNING would require SELECT privilege.
GRANT INSERT ON public.leads, public.ledger, public.reviews TO logger_writer;

-- Identity-column sequences are managed internally and normally need no
-- separate privilege; this is a belt-and-braces grant so inserts can never
-- fail on sequence ACLs. Sequence USAGE confers no read or write on any row.
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO logger_writer;

-- ----------------------------------------------------------------------------
-- 7. Row-level security — the braces.
--    Policies mirror the grants exactly. Because RLS is enabled and NO
--    UPDATE/DELETE policy exists on any table, updates and deletes are denied
--    for research_ro and logger_writer even if a grant were ever added by
--    mistake. RLS is not FORCEd so the table owner (the admin credential on
--    Vyom's machine, which never touches any agent) keeps a maintenance path;
--    the Supabase
--    service_role bypasses RLS by design — which is precisely why it never
--    touches any agent (spec §10).
-- ----------------------------------------------------------------------------
ALTER TABLE public.leads   ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ledger  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reviews ENABLE ROW LEVEL SECURITY;

-- leads
CREATE POLICY research_ro_select_leads   ON public.leads
  FOR SELECT TO research_ro   USING (true);
CREATE POLICY logger_writer_insert_leads ON public.leads
  FOR INSERT TO logger_writer WITH CHECK (true);

-- ledger
CREATE POLICY research_ro_select_ledger   ON public.ledger
  FOR SELECT TO research_ro   USING (true);
CREATE POLICY logger_writer_insert_ledger ON public.ledger
  FOR INSERT TO logger_writer WITH CHECK (true);

-- reviews
CREATE POLICY research_ro_select_reviews   ON public.reviews
  FOR SELECT TO research_ro   USING (true);
CREATE POLICY logger_writer_insert_reviews ON public.reviews
  FOR INSERT TO logger_writer WITH CHECK (true);

-- NO update policy. NO delete policy. On any table. Ever. Corrections are new
-- rows; history is never rewritten (spec §10).

COMMIT;

-- ============================================================================
-- Post-apply verification (run as owner; expected results in db/README.md):
--
--   SET ROLE logger_writer;
--   INSERT INTO public.leads (date, ticker, market, source_channel,
--     coverage_class, one_line_mechanism, status)
--   VALUES ('2026-08-25', 'TEST', 'ASX', 'lane3-human', 'C0',
--     'smoke test row', 'new');                          -- succeeds
--   SELECT count(*) FROM public.leads;                   -- ERROR: permission denied
--   UPDATE public.leads SET status = 'x';                -- ERROR: permission denied
--   DELETE FROM public.leads;                            -- ERROR: permission denied
--   RESET ROLE;
--
--   SET ROLE research_ro;
--   SELECT count(*) FROM public.leads;                   -- succeeds
--   INSERT INTO public.leads (date, ticker, market, source_channel,
--     coverage_class, one_line_mechanism, status)
--   VALUES ('2026-08-25', 'TEST', 'ASX', 'lane3-human', 'C0', 'x', 'new');
--                                                        -- ERROR: permission denied
--   RESET ROLE;
--
-- If any "ERROR" line above succeeds instead, STOP: the separation is broken.
-- Do not hand out any credential until every check passes.
-- ============================================================================
