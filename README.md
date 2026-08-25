# Investment

A council-backed investment research CLI. One question goes to a cross-vendor
LLM council — every member analyzes it independently, peer-reviews the others
anonymously, and a chairman synthesizes — and the whole deliberation lands in
a markdown memo you keep.

> Research aid, not financial advice.

## How it relates to the conductor repo

The council itself lives in [vyomb1/conductor](https://github.com/vyomb1/conductor)
under `llm-council/` (the deliberation lab, a verbatim port of
[karpathy/llm-council](https://github.com/karpathy/llm-council)). This repo
**calls that service; it duplicates none of it.** All investment framing lives
in the brief this client sends — the council forwards one query verbatim to
every member, so Stage-1 independence is preserved: same brief to all.

## Setup

1. Start the council service from your conductor checkout:

   ```bash
   cd conductor/llm-council
   echo "OPENROUTER_API_KEY=sk-or-v1-..." > .env
   uv sync
   uv run python -m backend.main     # serves on http://localhost:8001
   ```

2. In this repo:

   ```bash
   uv sync
   ```

## Usage

```bash
uv run python -m investment "Should I overweight semiconductor equipment makers?"
uv run python -m investment "Is NVDA's moat durable through 2030?" --context-file notes.md
```

The chairman's synthesis prints to stdout and the full memo — synthesis,
council standings (anonymized peer rankings), and every member's analysis —
is written to `memos/<date>-<slug>.md`. Memos are committed: they are the
work product.

`COUNCIL_URL` overrides the service address (default `http://localhost:8001`).

## Tests

No network, council stubbed via `httpx.MockTransport`:

```bash
uv run python -m unittest discover -s tests -v
```
