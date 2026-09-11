# Policy scan protocol

**Current methodology.** This document describes how a policy scan is run now; it is not a record of how it came to be. Scan history, findings and the reasoning behind past decisions live in the dated triage notes in `outputs_other/`.

The purpose of this protocol is to catch policies, frameworks, bodies, legislation and indicators published *after* the current canonical workbook versions, and to route them into the workbooks under the existing write discipline.

It exists because the knowledge base does not decay visibly. A workbook that is six months stale looks exactly like a workbook that is current: `check_links.py` still passes, the dashboards still build, every record still resolves. The only symptom is an absence — a policy that should be there and isn't. This protocol is the only thing that produces that symptom on purpose.

**Scope:** additions and retirements to the three canonical workbooks. It does not cover schema changes, dashboard rebuilds or assessment work; those follow `WORKBOOK_WRITE_PROTOCOL.md` and the assessment toolkit respectively.

---

## 1. Cadence

**Quarterly, run manually**, plus **ad hoc** whenever a major publication is trailed or lands.

Quarterly is the floor, not the target — it is fast enough that a scan is never more than three months of ground to cover, and slow enough that most scans find little. Ad hoc triggers matter more than the calendar.

The scan is deliberately **not** on an automated schedule today (§7.1), but §6 is written as a self-contained runbook so that it can be put on one later without rewriting the protocol. §8 says exactly what that would take.

**Ad hoc triggers**
- A new CCC Progress Report (adaptation or mitigation) or Carbon Budget advice.
- A JNCC UK Biodiversity Indicators refresh (annual, typically autumn).
- A new or revised Defra strategy, Environmental Improvement Plan revision, or EIF indicator release.
- A State of Nature report.
- A CBD COP or IPBES plenary outcome; an EEA indicator set update.
- Any Act receiving Royal Assent in scope, or a significant SI commencing.
- A machinery-of-government change creating, merging or abolishing a body in scope.

## 2. Watchlist

### 2.0 How to work it — enumerate first, search second

**This is the most important instruction in the protocol.**

Work each source by **enumerating what it actually published inside the window**, then screen that list. Do *not* start from keyword searches for publications you expect. A keyword-led scan returns only what the scanner already thought of, which is exactly inverted from the purpose of a scan: its whole job is to catch what nobody anticipated. Keyword search is a supplement for confirming details, never the method for finding candidates.

For gov.uk and its agencies, enumeration is a date-filtered query, not a guess:

```
https://www.gov.uk/api/search.json
  ?filter_organisations=department-for-environment-food-rural-affairs
  &filter_public_timestamp=from:YYYY-MM-DD,to:YYYY-MM-DD
  &count=100&order=-public_timestamp
  &fields=title,public_timestamp,link,content_store_document_type
```

Swap `filter_organisations` for each body below (`natural-england`, `environment-agency`, `joint-nature-conservation-committee`, `forestry-commission`, `marine-management-organisation`, `uk-health-security-agency`, `department-for-energy-security-and-net-zero`, …). The human-facing equivalent is `gov.uk/search/all` with `public_timestamp[from]` / `public_timestamp[to]`. legislation.gov.uk has `/new/all` with date filters; the devolved administrations and the CCC, OEP and international bodies publish dated listing pages — page through them rather than searching them.

**Use a browser, not a plain fetch.** The gov.uk search API works correctly *only* when the request is made by something that preserves the query string. A browser does; some fetch tools do not, and drop everything after the `?` — see the warning below. Loading the API URL in a browser pane and reading the page returns the filtered JSON directly.

Page through results with `start` (`&start=0`, `&start=100`, …) and narrow with `filter_content_store_document_type` (`policy_paper`, `guidance`, `statistics`, `detailed_guide`, …) to cut the screening load. Prefer several narrow queries over one large one: the output is read by a person or a model with finite attention, and a long undifferentiated list is where items get skimmed past.

**Atom feeds are a fallback, adequate only for low-volume publishers.** Every gov.uk organisation exposes one at `https://www.gov.uk/government/organisations/<slug>.atom` — a plain path with no query string, which matters because some fetch tools silently discard query parameters and return an unfiltered result set that *looks* like a successful search. A feed is a rolling window of the most recent items, not a date range, and **gov.uk feeds are capped at 20 entries with no pagination links**. For a department publishing several items a day that is roughly one day of output, so **the Atom feed cannot enumerate a quarter for a high-volume publisher.** It is serviceable for bodies that publish rarely (JNCC, the CCC, the OEP, MCCIP). Record how far back the feed actually reached, and treat anything earlier as un-enumerated.

**Verify that a filtered query was actually filtered.** If a search endpoint returns an implausible total (the whole corpus) or results unrelated to the filters, the filter was dropped. Treat that as enumeration failure, not as a null result. The tell is a total in the hundreds of thousands, or results about vehicle tax in an environment scan.

**Retrieval, not filtering, is the bottleneck — and it fails silently.** Filtering a feed or result set by timestamp is trivial. The risk is that the retrieval layer hands back *less than it fetched*: a summarising fetch tool reading a long document will quietly drop entries, and a truncated enumeration is indistinguishable from a complete one. The items it drops are exactly the unanticipated ones a scan exists to catch. Prefer structured JSON read through a browser, in slices small enough to be returned whole, over a large document passed through any summarising step.

If enumeration is unavailable for a source in a given run (blocked endpoint, dropped query parameters, no dated listing), **say so explicitly in the triage note against that source**. An un-enumerated source is an unscanned source, and the note must not imply otherwise.

### 2.0b Ministerial statements and debates — the highest-yield single source

**Scan Hansard and the written-statements service every time.** Ministerial statements exist to announce things, so a single statement routinely names a dozen publications, plans and funding commitments in one place — including documents that are hard to find by enumeration because they sit under an unexpected organisation, a Command Paper number, or a title nobody would have guessed.

**How to enumerate a window.** Written statements are date-filterable directly:

```
https://questions-statements.parliament.uk/written-statements?SearchTerm=&DateFrom=YYYY-MM-DD&DateTo=YYYY-MM-DD
```

Load it in a browser (a plain fetch drops the query string). Every result shows its **answering department**, so filter by eye rather than by URL — the department parameter is not reliably settable by hand; set it with the page's own *Show more options* control if you want it applied server-side. Expect a few hundred statements per quarter across all departments, paged 20 at a time; the relevant ones are identifiable from department plus title alone.

Statements from departments outside the usual watchlist still matter: planning, energy and housing statements routinely change instruments that bear on nature and climate.

- Hansard debates: `https://hansard.parliament.uk/commons/YYYY-MM-DD` and `/lords/YYYY-MM-DD`, plus the search interface.
- Useful recurring titles: *State of Climate and Nature*, and any statement naming a strategy, framework, roadmap, white paper, delivery plan or revision to an existing framework.

Read a relevant statement in full and extract **every named report, plan, framework, commitment and funding line**, then check each against the workbooks. Treat the statement as a pointer document, not as a record in itself — a statement is not a `POL`, but the things it names usually are.

**Departmental and devolved *policy pages* work the same way** and are the better route where a site's publication search cannot be date-filtered. `gov.scot/policies/<topic>/`, `gov.wales` and DAERA topic pages each summarise a nation's strategies, delivery plans, programmes and duties in one place, and name them explicitly. Where enumeration is blocked, enumerate the policy pages instead and treat every named instrument as a candidate.


Grouped by ID family, so a hit maps directly onto a workbook and sheet.

**UK legislation — `LEG`**
- legislation.gov.uk new-legislation feed (Public General Acts; UK SIs in scope).
- Devolved: Scottish Parliament, Senedd, Northern Ireland Assembly bill trackers.

**UK bodies — `ORG`**
- gov.uk organisations index (creations, mergers, abolitions, renames).
- Cabinet Office machinery-of-government announcements.

**UK policy and activities — `POL`**
- **Hansard and written ministerial statements (§2.0b)** — scan first; highest yield per minute spent.
- gov.uk publications feeds: Defra, DESNZ, DfT, MHCLG, DHSC, **HM Treasury** (carbon pricing, CBAM, fiscal instruments) and the **Cabinet Office** (national resilience) where climate–nature relevant. Atom: `gov.uk/government/organisations/<slug>.atom`.
- Instruments owned by finance, planning and transport departments are routinely in scope and are the ones a Defra-centred watchlist misses; statements (§2.0b) are the reliable way to catch them.
- Agency publication feeds: Natural England, Environment Agency, Marine Management Organisation, Forestry Commission, UKHSA (heat/health) — all on the gov.uk API.
- **JNCC (`jncc.gov.uk`) and Forest Research (`forestresearch.gov.uk`) publish on their own domains and are almost absent from gov.uk** — the API returns a handful of items for each. JNCC owns the UK Biodiversity Indicators, so this is the source most likely to change `IFW`/`IND` records and the one gov.uk enumeration cannot see. Enumerate their own news and publication listings directly.
- Devolved administrations: gov.scot, gov.wales, DAERA; NatureScot, SEPA, Natural Resources Wales.
  **Note: gov.scot's publication search ignores `topics` and `date` URL parameters** — a filtered request returns the whole corpus (50,000+ results), which is an enumeration failure, not a null. Use the topic policy pages (§2.0b) as pointer documents instead, and set filters through the site's own controls if a full enumeration is needed.
- Committee on Climate Change (CCC) and Office for Environmental Protection (OEP) publications.

**International — `INT-L`, `INT-O`, `INT-P`, `EU-L`**
- CBD (COP decisions, GBF monitoring framework revisions), IPBES, Ramsar, CMS, OSPAR, HELCOM.
- UNFCCC where it touches nature–climate indicators.
- EUR-Lex for EU instruments the UK has retained or that bear on the EEA indicator set.
- EEA indicator and briefing releases.

**Indicators and frameworks — `IND`, `IFW`**
- EIF (oifdata.defra.gov.uk), JNCC UKBI, CCC monitoring frameworks, ONS natural capital accounts, MCCIP report cards, UN SDG indicator revisions, BIP.

---

### 2.0c The title sweep — mandatory for every excluded document type

Screening the record-bearing document types (`policy_paper`, `research`, `document_collection`, `statutory_guidance`, `consultation_outcome`, `corporate_report`, `independent_report`, `transparency`) leaves a large remainder of operational material — on gov.uk, mostly `detailed_guide` and `guidance`. That remainder is **not** screened out; it gets a **title-only sweep**.

Fetch it with `fields=title` alone, read every title, and pull anything that names a fund, programme, scheme, framework, metric, plan, strategy, partnership or monitoring network. The cost is one query and a few minutes of reading; the risk it removes is a policy record misfiled under a routine type, which no other step would catch.

**A document type is never excluded outright — only downgraded from full screening to a title sweep.** Record in the triage note which types were swept by title and which were screened in full.

## 3. Screen

For each candidate, questions 1–4 in order; a "no" at any point stops the assessment and the item is logged as screened-out with the reason. Question 5 is asked once per scan, not per candidate.

1. **Does it introduce or retire a record?** A policy or activity (`POL`), a body (`ORG`), legislation (`LEG`), an international instrument (`INT-*`, `EU-L`), or an indicator/framework (`IND`, `IFW`). Commentary, consultations that have not concluded, and press notices are not records.
2. **Is it in scope?** Climate, biodiversity, ecosystem services or state of the environment, in a UK or UK-relevant international context.
3. **Is it an indicator candidate?** Official and national statistics, statistical data sets and agency monitoring outputs are `IND` candidates, not noise. Agency monitoring statistics that sit in no published framework are exactly what the assessment method hunts for, and they belong in the indicators workbook. Screen every statistics release on the same measured-quantity test as any other indicator, and check it against the existing framework sheets before proposing it — many will already be held under a framework's own indicator name rather than the statistic's title.

4. **Does it take a climate input?** For indicators specifically, this is the project's core relevance test: does the *measured quantity* depend on climate data, or could it? An indicator whose measured quantity takes no climate input (a GIS area, a count of designations) is catalogued if it belongs to a framework already tracked, but scores zero on climate relevance. The same measured-quantity test used in the assessment toolkit applies here — keep the two consistent.

5. **Has any catalogued framework been refreshed?** Check each `IFW` record in the indicators workbook against its publisher for a new release or revision in the window — EIF (Defra), CCC monitoring frameworks, JNCC UKBI, State of Nature, CBD GBF, BIP, IPBES, UN SDG, EEA. A framework refresh changes indicator records **wholesale** — adding, retiring and revising rows across a whole sheet — so it outranks any individual record find. It is also invisible to a normal enumeration, because the framework's landing page does not change even when its indicators do. Record the answer for every framework each scan, including "no refresh", so the next scanner knows what was checked rather than assumed.

Also screen for **retirements**, which are easier to miss than additions: a superseded strategy, a repealed Act, an abolished body, a framework indicator withdrawn at a refresh. A record that has been retired is marked, never deleted, and its ID is never reused.

---

## 4. Triage and record

Output of each scan is a single dated triage note, one row per candidate:

| Field | Content |
|---|---|
| Date found | Scan date |
| Source | URL, primary source only |
| Proposed family | `LEG` / `ORG` / `POL` / `INT-*` / `EU-L` / `IND` / `IFW` |
| Target sheet | The workbook and sheet it would land in |
| Action | Add / retire / amend / no action |
| Climate input | Yes / no / unclear (indicators only) |
| Overlap | Existing record it duplicates or relates to |
| Confidence | High / medium / low, with what is unverified |

Rules, carried over from the existing discipline and non-negotiable:

- **Propose, never silently add.** Every proposed addition is marked with a dagger (`†`) until approved.
- **Verify before writing.** Dates, status and URLs checked against primary sources — gov.uk, legislation.gov.uk, agency portals, the instrument's own text — not against secondary reporting or recollection.
- **Blank over guess.** An empty field is better than a presumptive one.
- **No silent controlled-vocabulary additions.** A candidate needing a new `Policy_Sector` token or `General_Type` value is flagged as a schema decision, not absorbed.
- **Never reuse a retired Record ID.**
- **Watch for the broken-chain pattern.** The most common false negative is a catalogue that holds the *organisation* and the *statute* but not the policy or scheme between them: the UK ETS Authority and the Energy Act are recorded while the Emissions Trading Scheme itself is not; the 30×30 Technical Working Group is recorded while the 30by30 commitment is not. A search on the missing record's name hits the body's record and reports coverage. **The test is internal consistency**: where a held record's own fields describe or point at something that has no record of its own, that is a defect in the workbook rather than a scope judgement, and it should be raised as a gap.
- **Do not infer a governance gap from an indicator alone.** It is tempting to treat "an `IND` exists but no `POL`/`LEG` does" as evidence of a missing record. It is not, on its own. The indicators workbook catalogues *frameworks' indicators*: a SAF blend-rate indicator exists because the CCC's monitoring framework tracks SAF, which is a fact about the CCC's framework, not about what the governance workbook should contain. The inference only holds where the indicator's `Policy_Goal` or `Indirect_Policy_Links` field **names** a policy or Act that has no record — the same orphan-reference problem `orphan_codes.py` detects for bracketed codes, but in prose. Otherwise the asymmetry is a **scope question** (does this domain belong in a climate–*nature* catalogue?) and should be queued as one, at medium confidence, not as a proven gap.
- **Ask whether a record should be per-nation.** UK-wide commitments are frequently delivered through four separate national instruments — 30by30 has an England delivery plan and a distinct Scottish commitment; biodiversity strategies, targets and delivery plans differ by nation. One record for a UK-wide *aspiration* will silently hide three missing national ones.
- **An overlap match must be the same *kind* of thing.** Searching the workbooks for a candidate's name will match records that merely *mention* it, or that are adjacent to it — a working group that developed a policy, a strategy that references a programme, a body that delivers it. None of those means the candidate is catalogued. Before recording an overlap, confirm the matched record's `Record_Type` and `General_Type` are what the candidate would be. A working group that developed a policy will match the policy's name and often link to its page, while the policy itself holds no record.
- **A null result must be reported with the method that produced it.** "Nothing found" is only useful if a reader can tell whether the source was enumerated or merely searched. Write "enumerated Defra publications 6 Jul – 2 Sep, 34 items, none in scope", not "no new Defra publications". An unfalsifiable null is worse than no entry, because it stops anyone looking again.

Approved items then go through `WORKBOOK_WRITE_PROTOCOL.md` (beside this file) in the normal way: propose → verify → link map → write → version bump and changelog → archive superseded → then **`python3 Management/finalise.py`**, which runs the integrity check and rebuilds both dashboards only if it passes.

---

## 5. The pending-additions queue

`Data/pending_additions.md` is a standing, append-only queue of proposed workbook records that have been *found* but not yet *written*. It is the mechanism by which discoveries made outside a scan reach the next scan.

**Why it exists.** Every assessment run with web access is instructed to find policy activities and indicators absent from the workbooks and mark them `†`. Those daggered items are a targeted, well-researched scan of one research field — better evidence than a quarterly sweep produces. Until now they were *offered* to the user at the end of a run and captured only if that individual chose to act. That made the completeness of a shared knowledge base depend on the disposition of whoever happened to run an assessment, and it lost the majority of what was found.

**The rule is now: assessment runs append to the queue. They do not offer.** Appending is not a change to the workbooks and needs no approval — the queue is a list of candidates, and everything in it still passes through the §3 screen and the §4 triage before any record is written. Nothing enters a workbook without sign-off; what has changed is that nothing is silently discarded before it gets there.

**Who writes to it**
- **Assessment runs** — every `†` activity and `†` indicator, appended at the end of the run. This is a step in `METHOD_AND_SCORING.md` §2 and in the prompt, not an option.
- **A quarterly scan** — anything found on the watchlist that is not actioned in the same sitting.
- **Anyone, at any time** — noticing a relevant publication is enough reason to add a row.

**Who reads it.** Step 3 of §6. Every scan starts by working the queue, because it is the highest-quality input available.

**Rows are never deleted.** A row is resolved by changing its `Status` to `added` (with the Record ID it became), `rejected` (with a reason), or `duplicate` (with the existing Record ID). Keeping rejected rows is the point: it stops the same candidate being re-proposed and re-argued every quarter.

**If the queue file is not reachable** — an assessment run on a ported copy of `PA_toolkit/` alone, for instance — the run must instead emit the rows as a fenced, copy-paste-ready block, explicitly labelled for pasting into `Data/pending_additions.md`. Silence is not an acceptable outcome.

**Also feeding the scan:** `Data/code/orphan_codes.py` identifies relationships already known but not yet promoted to typed columns. Different problem, same triage habit; run it as part of the post-scan write.

## 6. Procedure — the runbook

Self-contained by design: it names every input and output explicitly, so it can be handed to a person, an AI assistant, or (later) a scheduled task without alteration.

### 6.0 Work in blocks — one source group at a time, written up before the next

**A scan is never run as a single continuous pass.** It is run as a sequence of blocks, and **each block is written into the triage note and the queue before the next begins.**

The reason is quality, not convenience. A long unbroken pass degrades: attention thins across hundreds of titles, later sources get skimmed, and the skimming is invisible in the output — a source scanned carelessly and a source scanned well produce the same-looking line in a coverage table. That is the same silent-failure class as a dropped query string or a truncated feed, and it is the one the scanner introduces personally.

**The block sequence** (adjust the grouping, not the principle):

| Block | Sources |
|---|---|
| 1 | Ministerial statements and Hansard, all departments |
| 2 | Defra |
| 3 | Core nature agencies — Natural England, Environment Agency, Forestry Commission, MMO; JNCC and Forest Research on their own domains |
| 4 | Other departments — UKHSA, DESNZ, MHCLG, DfT, HM Treasury, Cabinet Office |
| 5 | legislation.gov.uk — Acts, then statutory instruments |
| 6 | Devolved — gov.scot, gov.wales, DAERA, NatureScot, SEPA, NRW |
| 7 | CCC and OEP |
| 8 | International — CBD, IPBES, Ramsar, CMS, OSPAR, HELCOM, UNFCCC, EUR-Lex, EEA |

**Rules for every block:**

- **Write before moving on.** Append the block's candidates to `Data/pending_additions.md` and its findings to the triage note *before* starting the next block. Findings held only in working memory are lost to a dropped connection, a session ending, or a context limit — and the queue exists precisely because discoveries that are not written down do not survive.
- **State coverage per block**, by document type and count: screened in full, title-swept, or not reached. A block is not complete until every type is one of those three.
- **Never mark a block complete to finish the scan.** Partial is an acceptable outcome; a partial block recorded as complete is not. If a block is abandoned, say what remains and why.
- **A block that finds nothing is still written up**, with the method used, per §4.
- **Stop when the work would degrade rather than when the list ends.** Reporting six blocks well and two not started is more useful than eight blocks skimmed, because the reader can act on the first and knows to distrust nothing.

Blocks may be run in separate sittings, days apart, by different people. The triage note's coverage table is the resumption point.

1. **Establish the window.** Note each canonical workbook's internal version (`Changelog!B2` in `Data/canonical_files/`). Find the most recent `outputs_other/policy_scan_*.md`; its date is the start of the window. If none exists, this is the first scan — use the oldest workbook's last-updated date.
2. **Read §7** — the operating settings govern how much to catalogue and how far to automate.
3. **Work the pending queue first** (§5). `Data/pending_additions.md`, every row with `Status: pending`. These are already-researched candidates and generally outrank anything the watchlist turns up.
4. **Scan ministerial statements first** (§2.0b) — date-filter the written-statements service and read every statement's department and title for the window, plus any Hansard debate a statement points to. Extract every named report, plan, framework and commitment. This step comes first because one statement typically names a dozen publications and tells you what to look for in step 5.
5. **Enumerate the watchlist in blocks** (§2.0, §6.0), one block at a time and writing up each before starting the next, for items published inside the window — *before* any keyword searching. Record, per source, how many items were enumerated and whether enumeration succeeded. Only then use targeted searches to fill in details or chase specific expected publications.
6. **Title-sweep the remainder** (§2.0c) — every document type not screened in full. Then **screen everything** per §3 — including retirements, which are easier to miss than additions. Record screened-out items and the reason; a documented "no" prevents the same candidate being reconsidered next quarter. When checking overlap against existing records, apply the same-kind-of-thing rule in §4.
7. **Write the triage note** (§4) to `outputs_other/policy_scan_YYYY-MM-DD.md`, appending each block as it completes rather than all at once at the end (§6.0). This file's existence is what defines the next scan's window, so write it even if the scan found nothing, and its coverage table is the resumption point if the scan is interrupted.
8. **Present for approval.** Nothing is written to a workbook until approved. Per §7.2 the assembly is assisted; the judgement and the write are not.
9. **Write approved items** via `WORKBOOK_WRITE_PROTOCOL.md`, then run `python3 Management/finalise.py` — it gates on `check_links.py` and rebuilds both dashboards only if the check passes.
10. **Resolve the queue.** Update the `Status` of every row you actioned: `added` (with its new Record ID), `rejected` (with a reason), or `duplicate` (with the existing ID). Rows never get deleted.

## 7. Operating settings

The parameters this protocol runs under. Change them deliberately; the reasoning is summarised so a future reader can tell a setting from an accident.

### 7.1 Cadence — manual quarterly, built to be schedulable

Quarterly, triggered by a person, plus the ad-hoc triggers in §1. §6 is a standalone runbook so a schedule can be added without touching this protocol (§8).

The weakness is that it depends on somebody remembering. The mitigations are the ad-hoc trigger list — in practice most scans are prompted by a publication landing rather than by the calendar — and the queue in §5, which keeps accumulating so a skipped scan delays work rather than losing it.

### 7.2 Assembly — assisted: AI drafts, human decides

An AI works the watchlist and the queue with web access, applies the §3 screen, and produces the §4 triage note as a draft. A person reviews, approves and writes. Roughly an hour per quarter rather than half a day.

Explicitly **not** automated: the write. The screen in §3 turns on whether an indicator's *measured quantity* takes a climate input — a judgement call this project has consistently kept human. Automating the write would also put unreviewed rows behind the `check_links.py` gate, which validates referential integrity but says nothing about whether a record *should* exist.

### 7.3 Triage threshold — tiered

Catalogue everything in scope; score climate relevance at entry; let the dashboards filter. This is what the workbooks already do — the indicator finder's climate-score filter exists so the catalogue can be broad and the *view* narrow. Cataloguing only climate-relevant records would hollow out the governance diagram, whose value is showing the full chain including the parts with no climate content.

### 7.4 Devolved administrations — in the standing watchlist

gov.scot, gov.wales, DAERA and their agencies are scanned every time, not on ad-hoc trigger only. They roughly triple the source count for a minority of records, and that cost is accepted: a UK-scope catalogue that scans England thoroughly and the devolved administrations opportunistically is misleading in a way no user could detect.

---

## 8. Adding a schedule later

Nothing in this protocol would change. The work is entirely in creating the scheduled task:

1. **Cron, in UTC.** `0 9 1 1,4,7,10 *` — 09:00 UTC on 1 January, April, July and October. That is 10:00 local during BST and 09:00 in winter; immaterial at this cadence, but it is why the field is not local time.
2. **The prompt must be standalone.** Each firing starts a fresh session with no memory of any previous scan or conversation. The prompt should say: read this protocol, execute §6 in order, write the triage note, propose nothing into the workbooks. §6 is written to be pasteable into exactly that instruction.
3. **State comes from the filesystem, not from memory.** The window start is the date on the newest `outputs_other/policy_scan_*.md`; the candidate list is the `pending` rows of `Data/pending_additions.md`. Both are the reason those two files must be written even when a scan finds nothing.
4. **Device binding must be declared at creation.** The task needs the local machine to read workbook versions and write the triage note; a binding cannot be added to an existing task afterwards. Web research runs in the cloud, where the network access is.
5. **Two practical traps.** A quarterly device-bound task only fires if the machine is awake with the desktop app running, and a missed firing is silent — so enable completion notifications and treat silence on the 1st as the alarm. And the feedback loop is three months long, so fire it manually once immediately to see what it actually produces before trusting the schedule.
