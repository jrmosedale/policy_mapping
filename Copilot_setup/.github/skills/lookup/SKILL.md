---
name: lookup
description: Answer questions from the knowledge base — which UK or international policies, bodies, legislation or indicators relate to a topic; trace a record's governance chain; find climate-relevant indicators; count records correctly. Read-only. Use for any factual question about workbook content.
argument-hint: "<question, e.g. 'policies that could use soil moisture data' or 'governance chain for POL-012'>"
user-invocable: true
---
# Look up the knowledge base

Read-only. Never edit a workbook to answer a question.

## Sources

- The fastest route is `Exports/csv/`, one file per sheet. `Exports/csv/_manifest.csv` lists the
  sheets with their versions and record counts.
- If `Exports/` may be stale — check whether the workbook's `Changelog!B2` differs from the
  manifest's version — read `Data/canonical_files/*.xlsx` with openpyxl, `data_only=True`.
- Always state the workbook and version the answer comes from.

## Rules

- **Indicator records** need both `Record_ID` and `Indicator_Name`: 1,001 at v28 (1,005 is the known
  wrong answer). Quote the live count from `Exports/csv/_manifest.csv`.
- **Cross-references** are bracketed codes. Strip the brackets to join on `Record_ID` /
  `Framework_ID`. Typed link columns:

  | Column(s) | Link type |
  |---|---|
  | `Enabling_Legislation`, `Statutory_Role` | enabling |
  | `Lead_Department`, `Lead_Organisation`, `Lead_Body` | lead |
  | `Parent_Programme`, `Parent_Convention` | parent |
  | `Funded_By` | funding |
  | `Related_*`, `Affecting_Policies` | related |
  | `Intl_Links`, `UK_Links`, `UK_Ratification` | international |
  | `Indicator_Frameworks`, `Indirect_Policy_Links` | indicator |

- A code that appears only in narrative prose (`Key_Provisions`, `Scope_And_Commitments`,
  `Remit_And_Powers`, …) is a mention, not a typed link. Say which it is.
- **Climate relevance of indicators:** use `Climate_Score` (0–3), `Climate_Dependency` and
  `Climate_Rationale`. Apply the measured-quantity test: does what the indicator measures take a
  climate input?
- For a topic question, screen all rows, not just a keyword hit. Report what you searched and how
  many rows matched.
- Give Record IDs, names and the `Link` URL for each item. If the answer is "not held", say so, and
  offer to add it to `Data/pending_additions.md`.
- Point the user to the dashboards for exploration: `Dashboards/governance_diagram_v*.html` and
  `Dashboards/indicator_finder_v4.html`.
