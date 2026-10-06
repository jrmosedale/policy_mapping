# Proposal — approved queue candidates into UK governance v27

*6 October 2026. Handover §9 item 1. Nothing has been written to the canonical workbooks.*

Full proposal, every column of every record: `PROPOSAL_UK_v27.xlsx`. Record data: `proposal_data.py`.
Writer: `apply_proposal.py` (append-only, parity striping, Changelog bump; WORKBOOK_WRITE_PROTOCOL §4–5).

## What it does

| | Count | IDs |
|---|---|---|
| New Legislation | 4 | LEG-068 Natural Environment (Scotland) Act 2026 · LEG-069 Environment (PGBT) (Wales) Act 2026 · LEG-070 Building Act 1984 · LEG-071 NI Climate Commissioner Regulations 2025 |
| New Public Bodies | 4 | ORG-045 ESS · ORG-046 OEG Wales · ORG-047 UKHSA · ORG-048 Local Nature Partnerships (collective) |
| New Policies & Activities | 39 | POL-072 – POL-110 (13 Environment Act target delivery plans + overview = POL-083 – POL-096) |
| Edits | 8 UK + 1 intl | ORG-031 Statutory_Role; LEG-034 correction (6 cells); ORG-014 Statutory_Role; INT-L-007 UK_Links |
| Vocabulary | 1 | Policies & Activities `General_Type` + "Operational service / System" (approved 10 Sep) |

Versions: UK governance v26 → **v27**; international v16 → **v17** (reciprocal `UK_Links` for the two 30×30 records).
**Dry run** on copies: `rebuild_xref.py` then `check_links.py` — all six invariants pass; registry 1,139 → 1,186.

## Decisions needing your OK

1. **LEG-034 is wrong and should be repurposed.** It is named "Environment (Scotland) Act 2023", which does not exist; its link
   (`asp/2023/4`) resolves to the *Bail and Release from Custody (Scotland) Act 2023*. Its provisions — establishing
   Environmental Standards Scotland and the environmental principles — are those of the **UK Withdrawal from the European Union
   (Continuity) (Scotland) Act 2021** (2021 asp 4, Part 2). Proposed: repurpose the ID to that Act (precedent: ORG-036 in v23),
   keep its inbound links from LEG-004 and LEG-006, and drop it from NatureScot's `Statutory_Role` (ORG-014), since the
   Continuity Act does not establish or empower NatureScot. ESS (ORG-045) then takes `[LEG-034]` as its `Statutory_Role`.
   **How it got in:** not traceable — it predates the July 2026 changelog. It survived because `check_links.py` validates
   codes, not whether a URL resolves to the named instrument. Worth a one-off link-title audit of the Legislation sheet.
2. **UKHSA's sponsor, DHSC, is not held.** Proposed: `Lead_Department` written unbracketed ("Department of Health and Social
   Care (sponsor; not held as a record)"), so no diagram edge, rather than adding a DHSC record. Say if you want DHSC added.
3. **Three queued rows change form** (detail in the workbook's *Not written* sheet):
   - *Scottish Biodiversity Programme* → **reject**. No body or programme of that name in the current strategy or delivery
     plan; governance is a Strategic Biodiversity Council and a delivery board, now in POL-108's prose.
   - *JNCC evidence review on NI peatland* → **replaced by POL-106 NI Peatland Strategy to 2040.** One report fails the
     level-of-generality rule; the strategy it serves had no record. JNCC Report 828 is cited in its prose.
   - *CCC–ESS memorandum of understanding* → a sentence in ORG-045, not a record.
4. **NI Nature Recovery Strategy — not written.** Still a draft; the consultation closed in spring 2026 with no final
   strategy. Leave as `add` pending adoption.
5. **Legislative backlog rows** (Taxation (Energy and Vehicles) Act 2026, Finance Act 2026, English Devolution Act 2026,
   the 2026 Acts audit) — your D8 decision was to fold these into the backlog audit. Not in this batch.
6. **Two judgement calls on type**: 30by30 assessment guidance as *Guidance / Methodology* (queue left it to you vs
   *Standard / Code*); NSWWS recorded at service level, Extreme Heat warnings within it, not as a separate record.

## Queue facts corrected at source

| Item | Queue said | Source says |
|---|---|---|
| Environment Act target delivery plans | 13 plans, published 16 Jul 2026; 12 topics listed | 13 plans **first published 1 Dec 2025**, updated 16 Jul 2026; the missing topic is **wastewater** |
| Government Estate Nature Plan | 22 Jul 2026 | 26 Jun 2026 |
| National Framework for Water Resources 2025 | 27 Aug 2026 | Published 17 Jun 2025; 27 Aug 2026 is the update |
| Blue Belt Programme | (Defra implied) | Led by **FCDO**, delivered by Cefas and MMO |
| GGR review | 2026 review | Review Oct 2025 (Whitehead); government response 17 Jul 2026 |
| Water White Paper | "2026, confirm page" | *A new vision for water*, CP 1940, 20 Jan 2026 (correction 19 Feb 2026) |
| Nature security assessment | "Jan 2026, find gov.uk page" | gov.uk page confirmed, 20 Jan 2026, Defra |
| GGR scope (your 11 Sep question) | — | Response covers nature-based removals (woodland, peat, soil carbon) and biomass land use — so yes, clear habitat implications |

## Self-review

**Verified at source on 6 October 2026** (gov.uk, legislation.gov.uk, gov.scot, gov.wales, nature.scot, daera-ni.gov.uk,
environmentalstandards.scot, jncc.gov.uk, theccc.org.uk, metoffice.gov.uk, planthealthportal.defra.gov.uk): every title,
URL, publication/update date, lead body and the substance of every prose field, except as listed below.

**Inherited, not re-read**: NatEnv (Scotland) Act Royal Assent 12 Mar 2026 and NI Climate Commissioner Regulations dates
(both from earlier primary checks recorded in the queue); UKHSA operational date 1 Oct 2021; LNPs' origin in the 2011
White Paper; Scottish Biodiversity Strategy final publication Nov 2024 (page would not render; inferred from the
publication path) and its statutory basis in the 2004 Act s.2; the Schedule 17 forest-risk-commodity link; first-published
date of ten of the thirteen delivery plans (three opened, all 1 Dec 2025).

**Inferred links** (marked in `_conf`): Enabling_Legislation for the plant health contingency plans ([LEG-043], [LEG-044]) and
NFWR ([LEG-012]); soft links AWHP→NAP3 and Local Sites→NPPF.

Confidence: high overall; medium on POL-108's dates.
