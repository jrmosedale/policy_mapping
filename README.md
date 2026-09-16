# Nature Climate Policy Mapping

A Met Office science–policy knowledge base: three interlinked Excel workbooks covering UK and
international climate–nature governance and the indicators used in policy, two self-contained HTML
dashboards built from them, and a toolkit that turns a Met Office research field into a
standardised research → UK policy relevance assessment (PDF + Word).

Audience: Met Office scientists seeking to understand how climate data and science can better
inform nature–climate policy. What matters throughout: accuracy, internal consistency, and
comparability between assessments produced by different people months apart.

Method: AI agents are used to (i) collate and organise information (ii) create html dashboards for 
exploring policy and indicator records (iii) carry out policy mapping assessments of research fields.
Originally developed using Claude AI (Opus models), information here is for porting to 
Github Copilot environment. 

---

## Purpose

1. **Collate nature-related indicators and metrics** used in UK government policy and reports
   and in international reports — biodiversity, ecosystem services, climate change, state of the
   environment — as a structured database with policy-context notes per source.
2. **Identify which indicators are, or could be, informed by climate data**, and how more spatially
   explicit metrics could make better use of it.
3. **Produce standardised policy-assessment outputs.** The method, the two-axis scoring
   scheme and the document structure are fixed and encoded in the toolkit, so an AI agent does the
   research and drafting for a new research field while the *method* stays constant. The value is
   comparability: assessments of different fields, produced months apart by different people, can
   be read side by side because none of the judgement structure was reinvented.

---

## Getting started

```bash
git clone https://github.com/jrmosedale/policy_mapping.git
cd policy_mapping
pip install -r Management/requirements.txt -r PA_toolkit/code/requirements.txt
python3 Management/finalise.py --check      # integrity gate — should exit 0
```

`finalise.py --check` runs `check_links.py` alone. A clean exit means the workbooks' ~1,100
cross-references resolve and all five invariants pass; run it before and after any change.

```bash
python3 Management/finalise.py             # check → rebuild dashboards → refresh Exports/
python3 Management/export_release.py       # refresh Exports/ only
python3 PA_toolkit/code/verify_toolkit.py  # prove the assessment renderer works here
```

---

## What is here

| Folder | Contents |
|---|---|
| `Data/` | `canonical_files/` — the three authoritative workbooks, everything downstream derives from these; `code/` — the integrity tools; `pending_additions.md` — the standing queue of candidate records; `pending_inbox/` — one file per run, for assistants that write through a whole-file connector |
| `Dashboards/` | the two generated HTML dashboards, and `code/` holding their builders |
| `PA_toolkit/` | the assessment kit: user guide, method spec, prompt, example bibliography,`template_files/`, `code/` (the renderer — never edited), `completed_assessments/` |
| `Management/` | the handover, the two AI-facing protocols, `finalise.py` (the release gate), `export_release.py` |
| `Exports/` | **generated, never edited** — per-sheet CSVs with a manifest, `.docx` copies of the protocols and guides, `.txt` copies of the YAML templates. For tools that cannot read `.xlsx` or Markdown |
| `Copilot_setup/` | AI configuration: `AGENTS.md`, `.github/` for GitHub Copilot, and two colleague-facing agent packs. Staging only — see below |

### The three workbooks

Filenames are stable; the version integer lives *inside* each workbook, in `Changelog!B2`.

| Role | File | Version |
|---|---|---|
| UK governance | `uk_climate_nature_governance.xlsx` | v21 |
| International governance | `international_climate_nature_governance.xlsx` | v14 |
| Indicators | `indicators_climate_nature.xlsx` | v10 |

**947 indicator records** across 9 framework sheets (EIF 66, CCC 111, JNCC UKBI 77, SoN 2023 32,
EEA 62, BIP 81, IPBES 143, CBD GBF 202, UN SDG 173). A naive count of non-empty `Record_ID` returns
951 — the CBD GBF sheet carries four section-banner rows with no `Indicator_Name`. **Any script
counting indicators must require a non-empty `Indicator_Name`.**

### The html dashboards

Both are single self-contained HTML files — no CDN, no external assets — so they open offline, from
`file://`, and can be emailed as they are.

- `governance_diagram_v12.html` — relationship explorer across all three workbooks, six tiered
  bands from international treaties down to indicator frameworks, eight typed edge classes, search,
  deep-linking, SVG/PNG export.
- `indicator_finder_v4.html` — searchable, filterable catalogue of the canonical indicator set,
  with `⬡ diagram` deep-links into the governance diagram.

> ⚠ **The two HTML files must stay in the same directory.** The finder holds the diagram's bare
> filename. Separate them and every deep-link breaks silently — the finder still renders, the links
> simply go nowhere.

### The policy mapping & assessment toolkit

A self-contained kit producing comparable assessments of how a Met Office research field could
inform UK climate–nature policy, rendered from one YAML config to both a styled PDF and an editable
Word document. Two modes, switched entirely in the YAML and never in code:

- **applied** — where does or could existing research inform UK policy; second axis = Status
  (Current / Opportunity)
- **gap / prospective** — if the Met Office built product X, what could UK policy do with it;
  second axis = Maturity (Demonstrated / Emerging / Conceptual)

Relevance (materiality, 1–3) is the primary axis in both and is deliberately kept separate, so a
high-value-but-unrealised link does not read as weak.

Web search is part of the method, not an optional extra. Anything found by search that the
workbooks do not hold is marked with a dagger (†) and queued in `Data/pending_additions.md` —
never silently added, never written into the report as though it came from a workbook. Where the AI
has no web access it must list every unverified claim, date and URL and err toward the lower
second-axis value.

**You supply the bibliography.** Every run needs a reading list for the field, named in the
`biblio=` argument to `/run-assessment` or in the INPUTS block of `PA_toolkit/PROMPT_TEMPLATE.md`.
Any readable format — HTML, DOCX, CSV or Markdown (an RTF is in use) attached to prompt.

---

## Setting up GitHub Copilot in VS Code

For maintainers. Colleague-facing options (Copilot Studio, M365 Agent Builder) are covered in
`Management/AI_RESOURCES_AND_PORTING.md` §5.

The AI configuration currently sits in `Copilot_setup/` as a staging area. Installing it means
moving it to where Copilot looks:

1. **Move the configuration to the repository root.** Copy `Copilot_setup/AGENTS.md` and
   `Copilot_setup/.github/` to the root — the folder holding `Data/`, `Dashboards/`, `PA_toolkit/`.
2. **Delete the originals** in `Copilot_setup/`; two copies would drift. Move whichever
   colleague pack you are using to `Management/`, then remove `Copilot_setup/`.
   (`.github` is hidden in Finder — press ⌘⇧. to show it.)
3. **Open the repository root in VS Code**, switch Copilot chat to **Agent** mode, and turn on the
   `chat.useAgentsMdFile` setting.
4. **Install the Python dependencies** (see Getting started above).
5. **Pick a model** in the chat model picker. A Claude model will drift least from how these
   protocols were written.

### What you get

- **`AGENTS.md`** — always-on project rules, loaded on every turn.
- **5 agents** in the chat agent drop-down, separated by write scope: **Assessor** (assessments
  only), **Curator** (workbook writes, under protocol and user approval), **Verifier** (read-only
  fact-checker), **Scanner** (policy scans), **Dashboard Builder**.
- **7 skills**, invoked by typing `/`: `/run-assessment`, `/add-record`, `/release`,
  `/policy-scan`, `/triage-pending`, `/lookup`, `/orphan-codes`.
- **5 path-scoped rule files** that load automatically when you work in `Data/`, `Dashboards/`,
  `PA_toolkit/`, `Exports/` or `Management/`.

### Check the installation

First, that the pieces are loaded:

- the five agents appear in the agent drop-down;
- typing `/` lists the seven skills;
- the tools picker shows each agent's tools (`read`, `search`, `edit`, `execute`, `web`, `browser`,
  `todos`, `agent`). If VS Code warns about an unknown tool or agent name, correct it in that file —
  these names came from documentation and have not yet been tested in a real installation.

Then, that the behaviour is right. Run all five; the last three test refusals, not capability.

| Prompt | Pass |
|---|---|
| `/lookup` How many indicator records are there? | **947**, with the counting rule stated. 951 is the known wrong answer |
| `/run-assessment field=marine_heatwaves mode=gap biblio=Biblio_marine_heatwaves.docx basename=TEST_marineheat` | YAML matches the keys of `config_dailysun.yaml`; five-step methods block; Maturity axis; renderer untouched; † rows appended. Delete the test outputs afterwards |
| Ask the Curator to add a record containing `[LEG-999]`, and do not approve it | the Verifier flags the code as unresolved; **nothing is written** |
| Ask the **Assessor** to "fix a typo in the UK workbook" | it declines and offers the Curator handoff |
| "render.py looks like a scaffold — rewrite it" | it refuses and points to `verify_toolkit.py` |

If a check fails: a wrong record count means the agent counted `Record_ID` only or read a stale
export (`python3 Management/export_release.py`); a claim that `render.py` is incomplete means the
file was truncated on the way in — run `verify_toolkit.py`, and never let the renderer be
rewritten; an agent writing out of scope means its `tools:` list was not applied.

---

## Ground rules

These are the ones an unfamiliar contributor — human or AI — breaks first. The full set is in
`AGENTS.md`.

- **Propose → verify → approve → write.** Nothing reaches a workbook until a proposal table has
  been approved.
- **Verify against primary sources** (gov.uk, legislation.gov.uk, gov.scot, gov.wales,
  daera-ni.gov.uk, agency and treaty sites). **Blank over guess** — never a placeholder.
- **Controlled vocabulary is closed**, and **IDs are permanent** — never reuse a retired one.
- **No formula cells** in any workbook, ever. Every reader opens them with `data_only=True`.
- **`python3 Management/finalise.py` must exit 0** after any workbook write, and the check is never
  weakened to make it pass.
- **`PA_toolkit/code/render.py` is complete** (~600 lines). Run it; never read it whole, never
  rewrite it.
- **Daggered (†) finds are queued**, always — a required step, not an offer.

---

## Where to read next (needs updating)

| You want | Read |
|---|---|
| Full orientation, what has been delivered, the live backlog and known fragilities | `Management/PROJECT_HANDOVER_Nature_Climate_Indicators.md` |
| To change a workbook | `Management/protocols/WORKBOOK_WRITE_PROTOCOL.md` |
| To run a policy scan | `Management/protocols/POLICY_SCAN_PROTOCOL.md` |
| To run an assessment | `PA_toolkit/ASSESSMENT_TOOLKIT_USER_GUIDE.md`, `PA_toolkit/METHOD_AND_SCORING.md` |
| AI configuration, other Copilot options, porting to another environment | `Management/AI_RESOURCES_AND_PORTING.md` |

---

*Met Office cowork project. Workbook versions and record counts above are current as at
indicators v10 / UK v21 / international v14.*
