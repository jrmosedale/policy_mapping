<!-- Section 1 of the response to the three-part diagram request. Prepared 2026-07-15. -->

## Do I still recommend promoting narrative codes into link columns (vs auto-inferring edges from prose)?

**Yes — unchanged.** Auto-converting every `[CODE]` found in prose into an edge would inject unvalidated, mistyped and often spurious links: a narrative field mentions a code for many reasons (contrast, history, "in scope of", "unlike"), and the direction/strength (hard vs soft, lead vs related) cannot be inferred from the fact of a mention. The workbook discipline deliberately excludes narrative from auto-edge extraction for exactly this reason. Curating each mention into the correct typed column keeps the graph validated, keeps `check_links.py` meaningful, and preserves the hard/soft distinction that carries the diagram's meaning.

The cross-check below **strengthens** that view: 20 of the 70 mentions are *already* in the diagram through a reciprocal typed link, so auto-inferring would have created 20 duplicate/again-directed edges for no gain. Promotion is selective; auto-inference is not.

### Method
Each `[CODE]` mention was checked against the actual edge set in `governance_diagram_v9.html` (either direction, any type). Mentions with an existing edge need no action. For the rest I assign the column it should go into and whether that yields a **hard** (solid: enabling/lead/parent) or **soft** (dashed: related/funding, or intl_soft) edge. "CHECK" / low-confidence rows are genuine judgement calls flagged for you.

# Orphan narrative codes — promotion analysis

Prepared for the governance diagram. Source: `outputs_other/orphan_narrative_codes.csv` (70 `[CODE]` mentions in narrative prose across 42 records). Cross-checked against the edges in `governance_diagram_v9.html`.

**Headline:** 20 of the 70 are *already shown* in the diagram via a reciprocal link (e.g. an ORG's remit names a POL, but the POL already carries `Lead_Organisation → that ORG`). 50 are genuinely absent. Of those 50, most are POL↔POL peer links that belong in `Related_Policy_Links` (soft); a handful are parent/child or funding (need a judgement call); and ~10 have **no suitable column in the current schema** and need either a prose-only decision or a new column.

## A. Already represented — no action needed (reciprocal links)

| Record (narrative) | Code | Already shown as |
|---|---|---|
| ORG-005 | POL-037 | POL-037→ORG-005 (lead) |
| ORG-005 | POL-038 | POL-038→ORG-005 (lead) |
| ORG-006 | POL-045 | POL-045→ORG-006 (lead) |
| ORG-009 | ORG-027 | ORG-027→ORG-009 (lead) |
| ORG-009 | ORG-026 | ORG-026→ORG-009 (lead) |
| ORG-032 | POL-042 | POL-042→ORG-032 (lead) |
| ORG-032 | POL-043 | POL-043→ORG-032 (lead) |
| ORG-032 | ORG-024 | ORG-024→ORG-032 (lead) |
| ORG-032 | ORG-023 | ORG-023→ORG-032 (lead) |
| ORG-033 | POL-046 | POL-046→ORG-033 (lead) |
| LEG-016 | POL-037 | POL-037→LEG-016 (enabling) |
| LEG-016 | POL-038 | POL-038→LEG-016 (enabling) |
| LEG-066 | POL-056 | POL-056→LEG-066 (enabling) |
| LEG-067 | POL-057 | POL-057→LEG-067 (enabling) |
| POL-040 | POL-011 | POL-011→POL-040 (funding) |
| POL-040 | POL-010 | POL-010→POL-040 (funding) |
| POL-053 | POL-030 | POL-030→POL-053 (parent) |
| POL-053 | POL-031 | POL-031→POL-053 (parent) |
| INT-O-024 | INT-P-033 | INT-P-033→INT-O-024 (lead) |
| INT-O-026 | INT-O-027 | INT-O-027→INT-O-026 (parent) |

## B. Missing from the diagram — recommended promotion

| Record | Code | → Column | Hard/soft | Conf. | Reciprocal? | Note |
|---|---|---|---|---|---|---|
| ORG-005 | POL-039 | — none available | n/a — SCHEMA GAP | flag |  | No ORG→POL / ORG→ORG(sibling) link column exists. Leave as prose, or add a new column (needs approval). |
| ORG-006 | POL-039 | — none available | n/a — SCHEMA GAP | flag |  | No ORG→POL / ORG→ORG(sibling) link column exists. Leave as prose, or add a new column (needs approval). |
| ORG-009 | ORG-028 | — none available | n/a — SCHEMA GAP | flag | yes | No ORG→POL / ORG→ORG(sibling) link column exists. Leave as prose, or add a new column (needs approval). |
| ORG-009 | ORG-029 | — none available | n/a — SCHEMA GAP | flag |  | No ORG→POL / ORG→ORG(sibling) link column exists. Leave as prose, or add a new column (needs approval). |
| ORG-011 | POL-039 | — none available | n/a — SCHEMA GAP | flag |  | No ORG→POL / ORG→ORG(sibling) link column exists. Leave as prose, or add a new column (needs approval). |
| ORG-022 | POL-039 | — none available | n/a — SCHEMA GAP | flag |  | No ORG→POL / ORG→ORG(sibling) link column exists. Leave as prose, or add a new column (needs approval). |
| ORG-025 | ORG-024 | — none available | n/a — SCHEMA GAP | flag |  | No ORG→POL / ORG→ORG(sibling) link column exists. Leave as prose, or add a new column (needs approval). |
| ORG-028 | ORG-009 | — none available | n/a — SCHEMA GAP | flag | yes | No ORG→POL / ORG→ORG(sibling) link column exists. Leave as prose, or add a new column (needs approval). |
| ORG-029 | ORG-027 | — none available | n/a — SCHEMA GAP | flag |  | No ORG→POL / ORG→ORG(sibling) link column exists. Leave as prose, or add a new column (needs approval). |
| ORG-033 | POL-004 | — none available | n/a — SCHEMA GAP | flag |  | No ORG→POL / ORG→ORG(sibling) link column exists. Leave as prose, or add a new column (needs approval). |
| POL-028 | POL-049 | Related_Policy_Links | soft · related | med | yes | Thematic/peer link. |
| POL-028 | INT-P-032 | Intl_Links (POL-028) + UK_Links (INT-P-032) | soft | med |  | IPCC SROCC is a non-treaty report → intl_soft. Reciprocal UK_Links needed on the intl record. |
| POL-037 | POL-038 | Related_Policy_Links | soft · related | med | yes | Thematic/peer link. |
| POL-038 | POL-037 | Related_Policy_Links | soft · related | med | yes | Thematic/peer link. |
| POL-040 | POL-030 | Funded_By or Related_Policy_Links | soft — CHECK | low |  | Does the Nature for Climate Fund fund WCC activity, or just relate to it? |
| POL-040 | POL-031 | Funded_By or Related_Policy_Links | soft — CHECK | low |  | As above for the Peatland Code. |
| POL-041 | POL-042 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-041 | POL-026 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-043 | POL-012 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-043 | POL-041 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-044 | POL-026 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-045 | POL-002 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-045 | POL-017 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-046 | POL-004 | Parent_Programme or Related_Policy_Links | hard/soft — CHECK | low |  | TDP delivers the transport component of the Net Zero Strategy; treat as parent (POL-046 child of POL-004) or merely related? |
| POL-047 | POL-015 | Parent_Programme (on POL-015) | hard · parent | med |  | BUS is a scheme delivered under the Heat & Buildings Strategy — child→parent. Add on the child (POL-015). |
| POL-049 | POL-028 | Related_Policy_Links | soft · related | med | yes | Thematic/peer link. |
| POL-050 | POL-009 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-053 | POL-038 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-055 | POL-013 | Parent_Programme or Related_Policy_Links | hard/soft — CHECK | low |  | EWCO sits within ELM; parent/child or related? |
| POL-055 | POL-030 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-055 | POL-011 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-056 | POL-013 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-057 | POL-013 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-057 | POL-056 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-058 | POL-001 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-059 | POL-009 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-059 | POL-050 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-059 | POL-028 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-060 | POL-022 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-061 | POL-054 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-061 | POL-062 | Related_Policy_Links | soft · related | med | yes | Thematic/peer link. |
| POL-062 | POL-054 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| POL-062 | POL-061 | Related_Policy_Links | soft · related | med | yes | Thematic/peer link. |
| POL-066 | POL-010 | Related_Policy_Links | soft · related | med |  | Thematic/peer link. |
| INT-O-015 | INT-O-025 | Intl_Links | soft · related | med | yes | Thematic intl↔intl link. |
| INT-O-024 | INT-O-025 | Lead_Body or Intl_Links | hard/soft — CHECK | low |  | IOC co-sponsors GOOS — a lead relationship (hard) rather than thematic (soft)? |
| INT-O-025 | INT-O-015 | Intl_Links | soft · related | med | yes | Thematic intl↔intl link. |
| INT-P-002 | INT-P-032 | Intl_Links | soft · related | med |  | Thematic intl↔intl link. |
| INT-P-011 | INT-P-033 | Intl_Links | soft · related | med | yes | Thematic intl↔intl link. |
| INT-P-033 | INT-P-011 | Intl_Links | soft · related | med | yes | Thematic intl↔intl link. |

## C. The schema gap (the ~10 "no column available" rows)

Ten mentions have **no home in the current schema** because the model only defines links from certain owner-sides:

- **ORG → POL** (e.g. Natural England / Environment Agency / Ofwat / DWI → POL-039 Independent Water Commission; DfT → POL-004 Net Zero Strategy). Public-body sheets have no "policies this body is affected by / contributes to" column. The POL side doesn't help here either, because the body is not the policy's *lead* — it is affected by or a contributor to it.
- **ORG → ORG (sibling / national analogue)** (Forestry Commission ↔ Scottish Forestry / Forestry and Land Scotland; Crown Estate Scotland → The Crown Estate). `Lead_Department` captures parent-department, not peer/analogue bodies across the four nations.

Two options, your call:

1. **Leave as prose (recommended default).** These are genuinely weaker "context" mentions, not governance edges; forcing them in risks over-connecting the graph. Cost: they never surface as links.
2. **Add one new controlled column** — e.g. `Related_Bodies` on Public Bodies (soft, undirected) and/or `Affecting_Policies` on Public Bodies — then promote them. This is a schema change and needs sign-off per `WORKBOOK_WRITE_PROTOCOL.md` (new column, controlled vocabulary, `check_links.py` update to recognise it).

My recommendation: **leave the ORG→POL "in scope of" mentions as prose**, but treat the **ORG↔ORG national-analogue** set as worth a `Related_Bodies` column if you want the four forestry/crown bodies visibly linked — that is a real, useful relationship a user would expect to see.

## D. Reciprocal pairs — add once, not twice

Several are reciprocal (both records name each other): POL-037↔POL-038, POL-057↔POL-056, POL-061↔POL-062, POL-028↔POL-049, INT-O-015↔INT-O-025, INT-P-011↔INT-P-033, plus the ORG↔ORG analogues. `Related_Policy_Links` / `Intl_Links` produce an **undirected** edge, so add the code on **one** record only (the checker's bidirectional rule applies to UK↔international, not to same-sheet related links). Adding both is harmless but redundant.

## Decisions I need from you before editing the workbook

1. The **CHECK** rows (parent-vs-related, funding-vs-related, lead-vs-related): POL-046→POL-004, POL-047→POL-015, POL-055→POL-013, POL-040→POL-030/031, INT-O-024→INT-O-025. I can research each against the source documents and propose a firm call, or you can decide.
2. The **schema-gap** question in §C: prose-only, or add `Related_Bodies` (and/or `Affecting_Policies`)?
3. Whether you want me to **make these edits** now (following the write protocol: propose table → verify → write → version/changelog → `check_links.py`) or just keep this as the plan.

*I have not edited any workbook — this is analysis and recommendation only.*
