# Discovery Engine — Lanes & Channels

**Operating reference** · Stage: Discovery [S1A] · Actors: the engine + Vyom; Lane 2 runs via [/sweep](../.claude/skills/sweep/SKILL.md) (fast tier) · Spec: [`../spec/investment-os-v3.2-master-spec.md`](../spec/investment-os-v3.2-master-spec.md) v3.2.0 **§5** (normative), with §2, §8, §13. Where this file and the spec disagree, the spec wins and this file gets a versioned fix (§16).

## Why this engine exists (§5)

- **Cheapness is the output of mispricing, not the cause.** We hunt causes (§1): someone forced to sell regardless of value, informed money disagreeing with price, supply leaving an industry, a calendar effect. Every lane and channel below captures a *cause*.
- **LLM recall is popularity-weighted, so Claude never originates tickers from memory — streams supply names, Claude supplies reading speed.** A ticker without a stream behind it does not enter the system (Constitution 2).
- **No quotas.** Fewer names, or zero, is always an acceptable output of any lane, channel, or run (§2.5). A quiet cycle is data, not failure.
- **Every retrieval run declares one coverage class** before research begins (§2.1). All Lane-2 sweeps are **C2** unless run against an enumerated feed; dynamic, blocked, paywalled, or truncated sources downgrade the class; failed sources are logged, never substituted.

## One inbox

Everything — all three lanes — enters the **same inbox** with its tag.

**Schema (§5, verbatim):** `date, ticker, market, source_channel, coverage_class, one_line_mechanism, status`

**Ten seconds from a phone on site; capture and analysis are never the same activity.** One line, done — the mechanism field is a suspicion tag, not research.

Machine form: [`../schemas/inbox-row.schema.json`](../schemas/inbox-row.schema.json) · capture card: [`../templates/inbox-capture.md`](../templates/inbox-capture.md) · consumed by [/triage](../.claude/skills/triage/SKILL.md) on R&R day 1 at ≤15 min/name ([`../runbooks/operating-rhythm.md`](../runbooks/operating-rhythm.md)).

---

## Lane 1 — The Bench (Playbook-A supply)

**A-leads are manufactured in advance, not found weekly.**

- **Target:** 30–50 pre-underwritten global compounders, each with **pre-computed bear/base buy prices from §8** (the scenario bridge is the tranche-anchor layer; entry tranches anchor to bear/base scenario values).
- **Populate from:** high-ROIC screens ∩ Playbook-A pass · spin-off parents/children · founder-led names with heavy insider ownership · concentrated value-fund 13Fs and ASX substantial-holder notices.
- **Build rate:** ~5 names/cycle from cycle 3, one bench-building deep block per cycle ([`../runbooks/operating-rhythm.md`](../runbooks/operating-rhythm.md); [`../runbooks/build-order.md`](../runbooks/build-order.md) item 3.3). Each bench candidate runs the full pipeline to a logged, pre-underwritten state — bench names are shadow-book citizens like everything else.
- **Thereafter, Lane-1 discovery = price alerts.** A pre-set price hit becomes an inbox row tagged `lane1_bench_alert`; alert upkeep is Maintenance [S16] work ([`../runbooks/maintenance.md`](../runbooks/maintenance.md)).
- **No A-entries before ~15 bench names exist** (§5; unlock tracked at [`../runbooks/build-order.md`](../runbooks/build-order.md) item 4.1).
- The bench is what the §9 downturn deployment ladder deploys into at −15/−25/−35% — pre-set prices turn the strategy's hardest moment into clerical work ([`../policy/portfolio-policy-v1.md`](../policy/portfolio-policy-v1.md)).

## Lane 2 — Event scanner (Playbook-B and lens supply)

Channels, each tagged and C-class declared; run by [/sweep](../.claude/skills/sweep/SKILL.md) every cycle on R&R day 1 (channel 1 also quarterly + intra-quarter; channel 8 in season only). The table is §5 verbatim:

| # | Channel | Mechanism | Source | Cadence |
| --- | --- | --- | --- | --- |
| 1 | Index deletions | Trackers must sell at any price | S&P/ASX + S&P DJI rebalance announcements (3rd Fri Mar/Jun/Sep/Dec, ~2 wks notice); Market Index archive | Quarterly + intra-quarter |
| 2 | Insider clusters | Informed disagreement with price | EDGAR Form 4 MCP (US); Appendix 3Y via Market Index/EODHD (ASX) | Every cycle |
| 3 | Capital-cycle signals | Supply exit forces reversion | capex/D&A < 1, closures, bankruptcies, care-and-maintenance; Bigdata trigger phrases ("impairment", "strategic review", "covenant waiver", "capacity closure", "suspends dividend") | Every cycle |
| 4 | Multi-year lows ∩ survivability | Despair with a living balance sheet | Screen: within 15% of 3-yr low AND net debt/trough cash flow sane AND F-score ≥ 5 (EODHD) | Every cycle |
| 5 | Special situations | Forced/uneconomic sellers | Spin-offs, post-bankruptcy, delistings, rights overhangs; 8-K/ASX streams; VIC archive (free guest, 45-day delay) | Every cycle |
| 6 | Filing deltas | Language change predicts trouble; stabilisation on bombed-out names is a lead | [/delta](../.claude/skills/delta/SKILL.md) over watchlist + new-lows list | Every cycle |
| 7 | Activist/substantial holders | Size just declared your disagreement | 13D (US), 604 notices (ASX) | Every cycle |
| 8 | Tax-loss windows | Non-fundamental year-end selling | Worst performers with clean balance sheets; Dec (US), Jun (AU) | Seasonal |

### Operating notes per channel

Notes on lead quality only — verification, routing, and the §6.4 trap filters belong to /triage, and a false positive here is still a valid capture (the kill, with its reason, is data for channel scoring).

**1 — Index deletions.** *Good lead:* a confirmed deletion where tracker selling is large relative to the name's liquidity and the weakness dates from the announcement, not from the business. *False positives:* deletions driven by takeovers or delistings-by-acquisition (the price moved for a reason that isn't mispricing — a mechanical event, killed at Verify [S1B]); flow trivial vs ADV (tiny spread); capturing a deletion long after the forced flow has cleared.

**2 — Insider clusters.** **Signal ≠ thesis** (old S14's rule, intact): a cluster is informed disagreement with price — it earns an inbox row, never a conclusion. *Good lead:* multiple distinct insiders buying meaningful size, on-market, with their own cash, near lows. *False positives:* option exercises and vesting dressed as purchases; token confidence-signalling buys after a collapse; a single routine programmatic buyer counted as a "cluster".

**3 — Capital-cycle signals.** *Good lead:* evidence supply is actually leaving — capex/D&A < 1 across the industry, closures, care-and-maintenance, bankruptcies — attached to a name whose balance sheet can outlive the trough. *False positives:* the leverage mirage — the industry heals but this equity doesn't survive to see it (§6.4 trap 3); impairment/"strategic review" language on structural decline where volumes would not recover even if the macro did (melting ice cube, trap 2). The Bigdata trigger phrases are harvest keys, not verdicts.

**4 — Multi-year lows ∩ survivability.** *Good lead:* passes the conjunction verbatim — within 15% of the 3-yr low AND net debt/trough cash flow sane AND F-score ≥ 5 — with a nameable reason for the despair. *False positives:* value with no unlock — no mechanism, no clock, no alignment (trap 4; B names require a clock, "cheap and someday" is not a mechanism §6.2); names cheap against fading peak earnings (routes Peak → default pass).

**5 — Special situations.** *Good lead:* an identifiable seller who must sell for non-economic reasons — index funds handed a spin-off they can't hold, a rights overhang, post-bankruptcy paper landing on creditors — ideally with a checkable downside floor for the SS lens. *False positives:* "special situation" labels with no actual forced seller; mechanical events with tiny spread (Verify kill); VIC-archive ideas where the 45-day delay means the forced selling already cleared — the trigger must still be live at capture date.

**6 — Filing deltas.** *Good lead:* substantive language change — a new risk factor, covenant or going-concern wording, guidance-language retreat — or, on bombed-out names, **stabilisation language appearing** (the long side of this channel). *False positives:* boilerplate reshuffles, template and formatting churn, lawyer-driven rewording with no facts behind it. /delta's diff discipline, not headline coverage of the filing, is the source.

**7 — Activist/substantial holders.** *Good lead:* a fresh 13D (US) or 604 notice (ASX) from a concentrated, engaged holder — size just declared their disagreement. *False positives:* passive stakes and index funds crossing a disclosure threshold; brokers' aggregated relevant-interest notices; amendments restating a long-known position as if new.

**8 — Tax-loss windows.** Seasonal only — Dec (US), Jun (AU); outside the window the channel does not run. *Good lead:* the year's worst performers **with clean balance sheets**, where the selling is calendar-driven and reverses with the calendar. *False positives:* names down for fatal structural or balance-sheet reasons — the clean-balance-sheet screen exists precisely to exclude them; out-of-season captures mis-tagged to this channel.

## Lane 3 — Human flow

Forums, news, serendipity. **Rule: forums supply tickers, never theses.**

- **Sources:** VIC archive (free guest, 45-day delay) · MicroCapClub · Corner of Berkshire · Strawman · **HotCopper as rumour feed only.**
- Everything enters the same inbox, tagged `lane3_human`. Capture the ticker plus the *claimed mechanism* as a one-line suspicion tag; the poster's thesis stays in the forum. A Lane-3 row earns exactly what every row earns — ≤15 triage minutes — and its trigger is verified against primary sources at [S1B] like any other.
- A HotCopper rumour with no primary document behind it is a trigger to check, never a fact; if nothing checkable exists, NOT FOUND is the answer and the row dies at Verify with its reason logged.

## Channel scoring (§5)

Verbatim discipline:

> Every lead carries `source_channel`. Quarterly: leads → triage survival → shadow-book entries → 12-month result vs benchmark, per channel. **Weights may not change until four quarters of scored data exist (anti-overfit rule).** Then prune losers, feed winners.

Mechanics:

- The `source_channel` tag vocabulary is fixed in the schemas ([`../schemas/inbox-row.schema.json`](../schemas/inbox-row.schema.json)): `lane1_bench_alert`, `ch1_index_deletions` … `ch8_tax_loss`, `lane3_human`, `vyom_direct`. The tag travels from inbox row to every ledger record the name ever emits, which is what makes the funnel joinable per channel.
- **Kills count.** Every kill is logged with its reason (§4), so triage survival rates per channel are real numbers, not survivor lore.
- Computed quarterly as the channel-hit-rate section of Loop 2, on the first R&R after quarter-end ([/calibrate](../.claude/skills/calibrate/SKILL.md); §11, §13). The 12-month column uses the §10 benchmark conventions: S&P/ASX 300 accumulation (AU sleeve), S&P 500 total return + an energy/materials index (US sleeve), money-weighted.
- Until four quarters of scored data exist, **no reweighting, no pruning, no feeding** — however convinced one quarter makes you. After that, changes to channel weights are versioned edits by Vyom alone — never mid-analysis, never from one outcome (Constitution 13). What "prune" and "feed" mean in cadence or attention terms: set by Vyom via versioned edit.
