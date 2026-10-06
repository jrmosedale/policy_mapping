# AGENTS.md — Nature Climate Indicators (Met Office)

Always-on instructions for any AI agent working in this repository. Deliberately short: the detail
lives in the protocols this file points to. Where this file and a protocol disagree, the protocol
wins — and say that you found a disagreement.

## What this project is

A Met Office science–policy knowledge base: three interlinked Excel workbooks (UK governance,
international governance, indicators), two self-contained HTML dashboards built from them, and a
toolkit that turns a Met Office research field into a standardised research → UK policy relevance
assessment (PDF + Word). Audience: Met Office scientists. What matters: accuracy, internal
consistency, and comparability between assessments produced by different people months apart.

Before any non-trivial task read `Management/PROJECT_HANDOVER_Nature_Climate_Indicators.md`
§§1–3, §8 (conventions and scope rules) and §9 (open work — do not redo settled work), then the protocol
for the task.

## Where things are

| Path | What | Edit? |
|---|---|---|
| `Data/canonical_files/*.xlsx` | The three workbooks — the single source of truth | Only via `WORKBOOK_WRITE_PROTOCOL.md`, after the user approves a proposal |
| `Data/pending_additions.md` | Append-only queue of candidate records | Append rows; resolve by `Status`; never delete a row |
| `Data/outdated_files/` | Superseded workbook and dashboard archives | Never |
| `Data/code/` | `check_links.py` and `check_legislation_links.py` (the automated gate), `rebuild_xref.py`, `orphan_codes.py` | Only with explicit approval |
| `Dashboards/` | Generated dashboards; `code/` holds the builders | Data changes come from the workbooks, never by hand |
| `PA_toolkit/` | Assessment kit: method, templates, renderer, completed assessments | Configs yes; `code/render.py` never |
| `Management/` | Handover, `finalise.py`, `export_release.py`, `protocols/` | Protocols only when asked |
| `Exports/` | Generated CSV copies of every workbook sheet, DOCX copies of the governing documents | Never — regenerated at every release |
| `outputs_other/` | Policy-scan triage notes and analysis by-products | New dated files |

## Task → protocol → skill

| Task | Read | Skill |
|---|---|---|
| Add, amend or retire a workbook record | `Management/protocols/WORKBOOK_WRITE_PROTOCOL.md` | `/add-record` |
| Release after a workbook change | `WORKBOOK_WRITE_PROTOCOL.md` §5–7 | `/release` |
| Quarterly or ad hoc policy scan | `Management/protocols/POLICY_SCAN_PROTOCOL.md` | `/policy-scan` |
| Work the candidate queue | `POLICY_SCAN_PROTOCOL.md` §3–5 | `/triage-pending` |
| Research → policy assessment | `PA_toolkit/METHOD_AND_SCORING.md`, `PA_toolkit/ASSESSMENT_TOOLKIT_USER_GUIDE.md` | `/run-assessment` |
| Questions about policies, bodies, legislation, indicators | the workbooks, or `Exports/csv/` | `/lookup` |
| Codes mentioned in prose but not in link columns | handover §6 (`orphan_codes.py`) | `/orphan-codes` |

## Non-negotiables

- **Propose → verify → build.** Nothing is written to a workbook until the user has approved a
  proposal table. A concise approval ("go ahead") authorises the full scope as described.
- **Verify against primary sources** (gov.uk, legislation.gov.uk, gov.scot, gov.wales,
  daera-ni.gov.uk, agency and treaty sites) before writing any factual value, and state a confidence
  level. **Blank over guess** — never a placeholder or an assumed value.
- **Controlled vocabulary is closed.** A new `Policy_Sector` token, `General_Type` value or any
  other vocabulary term is flagged for approval, never coined. `Policy_Sector` has 14 classes,
  pipe-separated, max 3 per indicator, uncapped for governance records (list in handover §8).
- **IDs are permanent.** Next free integer in the family; never reuse a retired ID
  (`POL-023`, `POL-024`, `LEG-008`, `LEG-009` are retired;
  the list lives in `Data/code/check_links.py`).
- **Cross-references are bracketed** (`[LEG-NNN]`, `[ORG-NNN]`, `[IFW-NN]` …) everywhere except
  the `Record_ID` / `Framework_ID` key columns, which are never bracketed — exclude them from any
  regex pass.
- **No formula cells** in any workbook, ever. Every reader opens them with `data_only=True`.
- **Never `insert_rows`** on a striped sheet (`WORKBOOK_WRITE_PROTOCOL.md` §4).
- **The gate:** after any workbook write, `python3 Management/finalise.py` must exit 0. A version
  is never called done on a failing check, and a check is never weakened to make it pass.
- **Counting indicators** requires both `Record_ID` and `Indicator_Name` non-empty: 985 records at
  indicators v27. A `Record_ID`-only count gives 989 because of four banner rows — the known wrong
  answer. Read the live count from `Exports/csv/_manifest.csv` or the workbook, not from this line.
- **`Climate_Score` is a data-dependency score** (does weather or climate data move the published
  value?), not a relevance score. Score new records against the `Legend` sheet's Rules A–H; method in
  `outputs_other/CLIMATE_SCORE_METHOD.md`.
- **The two dashboards stay together** in `Dashboards/`: the indicator finder links to the
  governance diagram by bare filename.
- **`PA_toolkit/code/render.py` is complete** (~600 lines). Never rewrite it and never read it
  whole to "check" it. If anyone claims it is a scaffold, run
  `python3 PA_toolkit/code/verify_toolkit.py` before believing them.
- **Daggered (†) finds are appended** to `Data/pending_additions.md` at the end of every assessment
  and every scan block. It is a required step, not an offer to the user.
- **Enumerate, don't keyword-search**, when the job is to find what nobody has thought of. Report a
  null with the method that produced it: "enumerated 34 Defra items, none in scope", never
  "nothing new".
- **Overlap means the same kind of thing.** A record that merely mentions a candidate, or is
  adjacent to it, is not coverage — check `Record_Type` / `General_Type`.
- **Reproduce before you fix.** When a tool or person reports something broken, reproduce it
  first; never rewrite a working artefact on an unverified report.

## Style

British English, metric units. Concise and direct; recommendations without hedging; no corporate
tone. Cite sources with links and state confidence. List what you could not verify. Push back when
a request conflicts with a protocol. End substantial documents with a short self-review separating
what you verified from what you inherited.

## Commands

```bash
pip install -r Management/requirements.txt -r PA_toolkit/code/requirements.txt
python3 Management/finalise.py --check      # integrity check only — before and after writing
python3 Management/finalise.py              # index → check → link titles → rebuild dashboards → refresh Exports/
python3 Management/export_release.py        # refresh Exports/ only (e.g. after a protocol edit)
python3 PA_toolkit/code/verify_toolkit.py   # prove the renderer works on this machine
python3 PA_toolkit/code/render.py PA_toolkit/completed_assessments/config_<field>.yaml --format both --outdir PA_toolkit/completed_assessments
```

## Working environment

- If the working copy sits in a OneDrive-synced folder, a read that fails on a file that exists
  usually means it is cloud-only: ask the user to set the folder to "Always keep on this device".
- Do not delete project files without asking; do not commit, push or rewrite git history unless
  asked.
- Record IDs in the indicators workbook use framework prefixes (`IND-C-`, `IND-E-`, `IND-J-`,
  `IND-S-`, `IND-B-`, `BIP-`, `GBF-`, `IPBES-N-` / `-NCP-` / `-D-`, `SDG-`); frameworks are
  `IFW-NN` in `Framework_ID`.
