# How to run this — plain instructions

You don't run this in normal Claude chat. You run it in **Claude Code**, pointed at this repository. A Claude Code session on this repo *is* the system's console: it auto-loads the Constitution and all 16 skills, and the skills appear as slash commands you type into the chat box.

## One-time setup (10 minutes)

1. **Open Claude Code on the web:** go to **claude.ai/code** in your browser and sign in. (This repo is already connected to your account — no install needed. The desktop app or terminal CLI work the same way if you prefer them later.)
2. **Start a session on this repo:** click **New session**, choose the **Investment** repository. That's it — the Constitution, the rules, and the slash commands load automatically.
3. **Fix the network policy** (so research can reach real filings): in the session's **environment settings**, set the network policy to allow at least `sec.gov`, `efts.sec.gov`, and `asx.com.au` — or choose the permissive/"trusted" policy. Without this, evidence lock is blocked and runs are capped at C3.
4. **Create the ledger sheet:** make a Google Sheet called anything you like, with two tabs:
   - **inbox** — row 1 = the header line from [`ledger/inbox.csv`](ledger/inbox.csv)
   - **ledger** — row 1 = the header line from [`ledger/ledger.csv`](ledger/ledger.csv)
   You are the logger (week one, per the spec): when a session hands you a validated ledger JSON block, you paste it as a new row. Never edit or delete old rows — corrections are new rows.

## Daily driving — what you actually type

Everything below is typed into the chat box of a Claude Code session on this repo.

| You want | Type | What happens |
| --- | --- | --- |
| Scan for new leads | `/sweep` | Scans the 8 discovery channels, gives you inbox rows |
| Check out a name (any source: sweep, a forum, your own eye) | `/triage UWMC` | 15-minute verify + route or kill, verdict JSON at the end |
| Go deeper on a routed name | `lock UWMC` | Builds the evidence pack from primary filings |
| Attack it | *(new session — see below)* `/redteam-blind` | Independent verdict + 3 ways you lose money |
| Full underwrite | `/underwrite-b UWMC` (or `-a`, or a lens) | The §8 valuation sequence |
| After you write your thesis | `/log` | Validated ledger row for you to paste into the sheet |
| An earnings print / event landed | `/results UWMC` | Scores the event against what you pre-registered |

Plain English works too — "triage UWMC", "sweep the channels", "what's on the inbox" — the session knows the system.

**The one special move — the blind red team.** Isolation is the point, so it can't run in the same session that did the research:

1. When `/lock` finishes it gives you the **evidence pack** as a block of text.
2. Open a **brand-new session** on this repo (New session — not a continuation).
3. Paste **only the pack** and type `/redteam-blind`. Don't say what you think of the name, don't mention how far along it is.
4. Bring the report back to your main session (or just read it). If it found a missed fact, the pack re-locks — that's the system working.

**Your part — the only thing the machine won't do:** the one-paragraph thesis and the falsifiers, in your own words ([`templates/thesis-memo.md`](templates/thesis-memo.md)). No paragraph → no position, not even a shadow one. Then `/log`, paste the row, done.

**Buying and selling:** entirely you, at your broker, by hand. The system never touches an order — it just makes sure that by the time you click buy, the name has survived triage, an evidence lock, a red team, and your own written falsifiers.

## A normal cycle, start to finish

1. `/sweep` → a few inbox rows
2. `/triage <ticker>` on whatever looks alive → most die here, that's the design
3. `lock <ticker>` on a survivor → evidence pack
4. New session → paste pack → `/redteam-blind`
5. Read both, write your thesis paragraph + falsifiers (or bin it — "can't write the paragraph" is a verdict)
6. `/log` → paste the row into your sheet
7. If you're actually buying: `/redteam-rebuttal` first (new session, pack + your thesis), then the §9 size checklist in [`policy/portfolio-policy-v1.md`](policy/portfolio-policy-v1.md), then place the order yourself

## What about normal Claude chat?

Usable as a fallback: make a claude.ai **Project**, paste [`CONSTITUTION.md`](CONSTITUTION.md) into its instructions, and work conversationally. You lose the slash commands, the schemas, and the validation — Claude Code on this repo is the real console. Phone capture on the go needs nothing at all: note "date, ticker, where you saw it, one line why" and feed it to `/triage` at your next session.
