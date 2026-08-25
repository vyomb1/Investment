# Golden set — Loop 1 (model/system accuracy)

**Spec:** [§11 Loop 1, §14, §16](../../spec/investment-os-v3.2-master-spec.md) · **Run by:** [/calibrate](../../.claude/skills/calibrate/SKILL.md) · **Build timing: cycle 2** (spec §14; open item 4), with the Loop-1 baseline run in the same cycle.

The golden set answers one question after any change: *does the machine still read filings and dispose of cases correctly?* It has two parts: **25 filing-based questions** Vyom has hand-verified, and **8 historical process cases** with known correct dispositions.

## Cadence — when Loop 1 runs

- **On every version change** — model, prompt, skill, or retrieval arrangement (§11). **Not on every research run.**
- **Before the new version researches anything live** (§16 gate): any change bumps the version and Loop 1 reruns on affected skills first. An uncalibrated version doing live research is a §16 violation, not a shortcut.
- Clearing a version for live work is Vyom's call; the scorecard is his input, never the clearance itself.

**Answer-key holdout:** [`questions.csv`](questions.csv) (which carries `correct_answer`) and the case-disposition table below never enter the context of a skill under test. A graded run that saw its own key measures nothing; contamination voids the run.

---

## Part 1 — the 25 filing questions

Construction rules (all mandatory):

1. **Single right answer**, extractable from one specific filing. No judgment calls, no "roughly".
2. **Hand-verified by Vyom** against the filing itself before entry: `verified_by` and `verified_date` are required — a row without them is not in the set.
3. Categories per spec §11: **revenue, segment splits, covenant terms, share counts**.
4. **Across US and ASX filings** — both markets must be represented.
5. **Companies are chosen by Vyom from filings he verifies** — never proposed from Claude's memory (Constitution rule 2 binds the golden set too). Names already in the ledger or July workbook are natural candidates, since they entered through streams.

### Recommended category distribution

Recommendation only — the final composition is set by Vyom via versioned edit.

| Category | `category` value | Count | Construction note |
| --- | --- | --- | --- |
| Revenue | `revenue` | 7 | As-reported totals for a named fiscal period, reporting currency stated; "as reported, not restated" made explicit |
| Segment splits | `segment_split` | 6 | One segment's revenue share or figure per question, from the segment note |
| Covenant terms | `covenant_term` | 6 | Ratios/thresholds from credit agreements, debt notes, or facility disclosures |
| Share counts | `share_count` | 6 | Basic vs diluted named; as-of date named (cover vs weighted-average distinguished) |
| **Total** | | **25** | Recommended market mix ~13 US / 12 ASX (set by Vyom via versioned edit) |

### Example question formats — FORMAT EXAMPLES ONLY, NOT REAL ENTRIES

The three blocks below show the *shape* of a valid row. Companies, filings, and answers are placeholders. **None of these may be pasted into `questions.csv`** — real entries require Vyom's hand-verification against the actual filing. `questions.csv` stays header-only until his verified rows land.

**Format example 1 — revenue (US):**

| Field | Placeholder content |
| --- | --- |
| id | q01 |
| category | revenue |
| market | US |
| company | [COMPANY — Vyom selects] |
| filing_ref | FY20XX Form 10-K, filed YYYY-MM-DD, accession no. [XXXX] |
| question | What was total revenue for FY20XX as reported (not restated), in the reporting currency? |
| correct_answer | USD X,XXX.X million |
| tolerance | exact at the filing's stated precision |
| verified_by | vyom |
| verified_date | YYYY-MM-DD |

**Format example 2 — segment split (ASX):**

| Field | Placeholder content |
| --- | --- |
| id | q08 |
| category | segment_split |
| market | ASX |
| company | [COMPANY — Vyom selects] |
| filing_ref | FY20XX annual report, operating segments note [N] |
| question | What percentage of total revenue came from the [SEGMENT] segment in FY20XX? |
| correct_answer | XX.X% |
| tolerance | ±0.5pp (band set by Vyom via versioned edit) |
| verified_by | vyom |
| verified_date | YYYY-MM-DD |

**Format example 3 — covenant term (either market):**

| Field | Placeholder content |
| --- | --- |
| id | q14 |
| category | covenant_term |
| market | US |
| company | [COMPANY — Vyom selects] |
| filing_ref | Credit agreement exhibit to [FILING], dated YYYY-MM-DD |
| question | What is the maximum net leverage ratio permitted under the [FACILITY] financial covenant? |
| correct_answer | X.Xx net debt / EBITDA |
| tolerance | exact |
| verified_by | vyom |
| verified_date | YYYY-MM-DD |

Share-count questions follow the same pattern: name basic vs diluted, name the as-of date, tolerance exact.

---

## Part 2 — the 8 historical process cases

Known correct dispositions, per spec §11. Cases run through the pipeline skills operating normally (triage, trap filters, the relevant lens), with the disposition key held out of the context under test. Case packets contain only material as it existed at the original decision point — no look-ahead.

| # | Case | Known correct disposition | Spec anchor |
| --- | --- | --- | --- |
| 1 | ENGN | **Must kill on the May durability filing** | The ENGN rule: durability data over any-time response framings (§6.3 Bio lens); when fuller primary evidence defeats the framing, reverse and log why (§7) |
| 2 | KMX | **Trap — reject** | §6.4 trap filters fire |
| 3 | NKE seed | **Discard — no formal guide** | Verify/triage discipline |
| 4 | FULC | **Special-sit, downside floor** | §6.3 special situation / cash shell lens: floor = verifiable cash/asset backing vs economic cap |
| 5 | WTC | **Governance derating, watch** | Watch, not entry |
| 6 | LEN | **Quality, price fails** | Right business, wrong price — the §8 ordering must say so |
| 7 | GHY | **Title fact mandatory** | The GHY PEL rule: title/permit continuity is a *mandatory* fact (§6.3 Explorer lens) |
| 8 | One past personal trade | **Vyom to select** — case materials and correct disposition recorded here by Vyom via versioned edit | §11 |

A run passes a case only when it reaches the known disposition *for a defensible reason at the correct stage* — killing ENGN for an unrelated reason is not the ENGN kill.

---

## Scoring rules (spec §11)

- **Facts: exact-match/tolerance**, per each question's `tolerance` field. Tolerance bands are set by Vyom via versioned edit — never widened mid-run to rescue a score.
- **Refusals are counted separately from errors.** A NOT FOUND or refusal where the key holds an answer is a *refusal*, not an error; a wrong or invented number is an *error*. Both columns are reported side by side — the system must never learn that guessing beats declining (NOT FOUND is a good answer; an invented number is not, §2.2).
- **Per-skill scores recorded** — one score line per affected skill, so a regression is attributable to the skill that regressed.
- **Arithmetic runs in code**, formulas shown (Constitution rule 6).
- **Scorecard filed in this directory** (suggested name: `scorecard-YYYY-MM-DD-v<version>.md`, stating the exact version diff tested) and **logged via [/log](../../.claude/skills/log/SKILL.md)** with `system_version`, `skill_versions`, `model_ids` attached — an unlogged calibration run measured nothing (Constitution rule 11).

## Files

| File | Contents |
| --- | --- |
| [`questions.csv`](questions.csv) | Column contract for the 25 questions — **header row only** until Vyom's hand-verified entries land. No comment rows in the CSV; the format examples live in this README only. |
| `scorecard-*.md` | One per Loop-1 run (created from cycle 2 onward) |

## Constitution bindings

- **2** — golden-set companies come from Vyom, never from model memory.
- **3** — refusal vs error separation is the NOT FOUND rule made measurable.
- **6** — scoring arithmetic in code, formulas shown.
- **11** — every run logged with versions; unlogged runs measured nothing.
- **13** — the set, the tolerances, and the distribution change only by Vyom's versioned edit.
