---
name: lookup
description: Answers questions about what the knowledge base holds — which UK or international policies, bodies, legislation or indicators relate to a topic, what a record links to, which indicators take a climate input, and how many records there are. Use for any factual question about the workbooks.
---
# Look up the knowledge base

1. **Read-only.** Never write to a workbook.
2. Load the sheet you need into the sandbox. `Exports/csv/<workbook>/<Sheet_Name>.csv` is fastest;
   `Exports/csv/_manifest.csv` lists every sheet with its workbook version, row count and record
   count. Use the workbook itself (openpyxl, `data_only=True`) when you need cell detail the CSV
   lacks, or when the manifest's version differs from the workbook's `Changelog!B2` — say so if it
   does.
3. **Count in Python, never by eye, and never estimate.**
   - A row is an indicator only if `Record_ID` and `Indicator_Name` are both non-empty: 947 at
     indicators v16.
   - Say which workbook and version the answer came from.
4. For a topic question, screen every row rather than keyword hits alone, and say what you searched
   and how many rows matched.
5. **Governance chains:** strip the brackets from codes and follow them across sheets. Typed link
   columns are `Enabling_Legislation`, `Statutory_Role` (enabling); `Lead_Department`,
   `Lead_Organisation`, `Lead_Body` (lead); `Parent_Programme`, `Parent_Convention` (parent);
   `Funded_By` (funding); `Related_Legislation`, `Related_Policy_Links`, `Related_Bodies`,
   `Affecting_Policies` (related); `Intl_Links`, `UK_Links`, `UK_Ratification` (international);
   `Indicator_Frameworks`, `Indirect_Policy_Links` (indicator). A code found only in narrative prose
   is a mention, not a typed link — say which it is.
6. **Climate relevance:** `Climate_Score` (0–3), `Climate_Dependency`, `Climate_Rationale`, plus the
   measured-quantity test.
7. Give `Record_ID`, name and the `Link` URL for every item. If something is not held, say so and
   offer the `queue-finds` skill.
8. For exploring relationships, point the user to the dashboards in the project's `Dashboards`
   folder: the governance diagram and the indicator finder.
