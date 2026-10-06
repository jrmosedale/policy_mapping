# Legislation sheet — link audit

*6 October 2026. UK governance v27. Read-only: nothing below has been written except the POL-077 self-correction noted at the end.*

**Method.** For every record on the `Legislation` sheet (71), the `Link` was opened and the title and citation on the
page compared with the record's `Name` and `Year`. One page per record, through the fetch tool; legislation.gov.uk
rate-limited the run twice. Prompted by the LEG-034 finding: `check_links.py` validates codes, not whether a URL resolves
to the named instrument.

**Result.** 68 of 71 links checked. **3 open a different instrument** (plus LEG-034, fixed today), **1 points at a revoked
instrument**, **2 records are classed as legislation but are not legislation**, and **3 could not be checked**. The other
64 open the named instrument or document (LEG-044, LEG-008 and LEG-009 are discussed below).

## Wrong links — the URL opens a different instrument

| Record | Name held | Link opens | Proposed fix | Confidence |
|---|---|---|---|---|
| LEG-034 | *(was)* Environment (Scotland) Act 2023 | Bail and Release from Custody (Scotland) Act 2023 | **Done in v27** — repurposed to the UK Withdrawal from the EU (Continuity) (Scotland) Act 2021 | High |
| LEG-013 | Water (Special Measures) Act 2025 | **Arbitration Act 2025** (2025 c. 4) | Link → `https://www.legislation.gov.uk/ukpga/2025/5/contents` (the Act is **2025 c. 5**). `Status` reads "Royal Assent Jan 2025"; the date was not on the page, so confirm before changing it | High on the link |
| LEG-040 | Clean Air Act (Northern Ireland) 1964 | **Petroleum (Production) Act (Northern Ireland) 1964** | Repurpose to the **Clean Air (Northern Ireland) Order 1981** (SI 1981/158 (N.I. 4)), `https://www.legislation.gov.uk/nisi/1981/158/contents`, which is in force and covers what the record describes — dark smoke, grit and dust, chimney heights, smoke control areas, district councils — and carries transitional provisions and repeals relating to the 1964 Act. Year 1981; `General_Type` stays Primary Legislation (NI Orders in Council are primary). Keep the ID; inbound links from ORG-016 and LEG-062 remain valid | High on the replacement; medium on whether the 1964 Act is wholly repealed |
| LEG-047 | Water Framework Directive (retained UK law) | **Commission Regulation (EC) No 60/2000** on import values for fruit and vegetables (the `eur/` path is for regulations) | Link → `https://www.legislation.gov.uk/eudr/2000/60/contents` (Directive 2000/60/EC). Substantive point: directives were not themselves retained; the domestic law is the transposing regulations (Water Environment (Water Framework Directive) (England and Wales) Regulations 2017 and devolved equivalents). Consider reframing the record to those — not done | High |

## Points at a revoked instrument

| Record | Finding | Proposed action |
|---|---|---|
| LEG-044 Plant Health (England) Order 2015 | legislation.gov.uk marks it **revoked**; the page did not name the revoking instrument. `Status` reads "In force (as amended)" | Not fixable from this audit: identify the current GB plant-health regime (post-EU-exit regulations) before changing anything. `Status` vocabulary has no "Revoked" stem, so that is also a vocabulary decision. Inbound: ORG-020, POL-033, POL-034, POL-052, INT-L-023. **POL-077 (new in v27) no longer cites it** |

## Classed as legislation, but not legislation

| Record | Held as | What it is |
|---|---|---|
| LEG-008 Biodiversity Net Gain | Secondary Legislation, link to gov.uk guidance | A statutory scheme: Schedule 7A to the Town and Country Planning Act 1990, inserted by the Environment Act 2021, plus commencement and other regulations; mandatory from 12 Feb 2024. A scheme record, not an instrument |
| LEG-009 Environmental Principles Policy Statement | Secondary Legislation, link to gov.uk publication | A statutory policy statement under the Environment Act 2021 (published 12 May 2022; laid 31 Jan 2023; duty in force 1 Nov 2023). Not an SI — its own `Statutory_Enabling_Basis` says so |

Both sit on the Legislation sheet by long-standing choice and drive "enabling" edges in the diagram. Reclassifying them (to
`Policies & Activities`, or a new `General_Type` such as "Statutory scheme / statement") is a curation decision, not a
correction. Recommend leaving them and noting the distinction in each record — your call.

## Not checked

| Record | Reason |
|---|---|
| LEG-003 Carbon Budget Orders (1st–7th) | legislation.gov.uk refused the request (rate limit; the tool forbids a retry). The single link cannot represent seven Orders in any case |
| LEG-049 Government Trading Funds Act 1973 | Rate-limited, as above |
| LEG-021 Climate and Nature Bill | Link is to bills.parliament.uk, which is not among the approved fetch domains |

## Self-review

Verified: 64 title/citation matches and every finding in the tables above, each from the page itself on 6 October 2026.
Not verified: the three records under *Not checked*; LEG-013's Royal Assent date; what revoked LEG-044; whether the
Clean Air Act (NI) 1964 is wholly repealed. The audit compared titles only; it did not re-check years, status or
provisions, beyond the LEG-044 revocation that the page announced.

**One change made**: POL-077 (written today) cited [LEG-044] as enabling legislation; that link was removed in v27 before
release, leaving [LEG-043] Plant Health Act 1967. Recorded in the v27 Changelog entry.

## Applied — UK governance v28 (6 October 2026, approved by Jonathan)

[LEG-013] Link → 2025 c. 5; [LEG-047] Link → `eudr/2000/60`; [LEG-040] repurposed to the Clean Air (Northern Ireland)
Order 1981. The audit is now repeatable: `Data/code/check_legislation_links.py` runs as step 3 of 5 in `finalise.py`.
Before the fixes, run against the titles recorded here, it reported exactly the three mismatches above and the LEG-044
revocation; after them, 66 match and 0 mismatch. Its cache is seeded with the titles read in this audit (valid 30 days).

## Applied — UK governance v29 / international v18 (6 October 2026, approved by Jonathan)

LEG-008 (BNG) retired as a duplicate of [POL-065]; LEG-009 (EPPS) moved to Policies & Activities as [POL-111] (Strategy /
Framework, Statutory, enabling [LEG-004]); both IDs added to `RETIRED` in `check_links.py`. References repointed: POL-053
(enabling → related [POL-065]; prose), INT-L-022 `UK_Links` → [POL-111]. Links of every touched record re-opened: POL-065
(gov.uk, updated 14 Jul 2026 — NSIP date corrected to 2 Nov 2026, 0.2 ha exemption added), POL-053 (gov.uk, 30 Mar 2023),
POL-111 (gov.uk EPPS page; statutory basis corrected to ss.17–19 from legislation.gov.uk). INT-L-022's own link
(unece.org) not re-opened — outside the approved fetch domains. LEG-044 left unchanged by decision and queued as an
`investigate` row in `Data/pending_additions.md`.
