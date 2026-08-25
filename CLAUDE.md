# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

# Technical Notes for Investment

## What this is

A thin client + CLI over the LLM Council service. The council lives in
`vyomb1/conductor` under `llm-council/` (the deliberation lab); this repo
**calls it over HTTP and duplicates none of it**.

## Module map

- `investment/briefs.py` — `build_brief(question, context)`: the analyst
  framing (thesis / bull / bear / risks / what-would-change-my-mind /
  confidence). The brief IS the query the council sends verbatim to every
  member.
- `investment/council_client.py` — `deliberate(brief, transport)`: POST
  `/api/conversations`, then POST `.../message`; returns
  `{stage1, stage2, stage3, metadata}`. `COUNCIL_URL` overrides the base URL
  (default `http://localhost:8001`). `transport` exists for
  `httpx.MockTransport` in tests.
- `investment/__main__.py` — CLI; renders and writes
  `memos/<date>-<HHMM>-<slug>.md` (synthesis, standings table from
  `metadata.aggregate_rankings`, per-member appendix, disclaimer footer).

## The invariant to preserve

One run sends the council exactly **one brief**, identical for every member —
all investment framing lives client-side in that brief. That is what keeps
the council's Stage-1 independence intact from this side. Do not add
per-member prompts here, and do not re-frame Stage 2 (ranking criteria) or
Stage 3 (chairman memo format) from this repo: those need small upstream
hooks in the lab's `council.py` first (deliberate follow-up, not done).

## Conventions

- Memos are committed — they are the work product. Everything else generated
  (`.venv`, caches) is ignored.
- Tests are stdlib `unittest` + `httpx.MockTransport`, no network:
  `uv run python -m unittest discover -s tests -v`
- No web UI by design (v1); the council's own frontend shows raw stages.
- Every memo and CLI output carries the not-financial-advice disclaimer.
