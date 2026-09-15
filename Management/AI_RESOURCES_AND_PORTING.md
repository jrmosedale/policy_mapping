# AI resources, set-up and porting — Nature Climate Indicators

Written 15 September 2026. What AI configuration this project carries, how to install it in
Copilot, how to check the installation from the chat window, and what it would take to move the
project to a different AI environment or model.

Companion documents: `Copilot_setup/README.md` (GitHub Copilot detail),
`Copilot_setup/CopilotStudio_agent/SETUP.md`, `Copilot_setup/M365_agent/SETUP.md`. This file
summarises; those three are the installation instructions.

---

## 1. Model

**No model is pinned anywhere in the project.** Model choice is a runtime setting, not a project
artefact. The only reference is one line in `Copilot_setup/README.md`: a Claude model will drift
least from how these protocols were written.

| | |
|---|---|
| Built and maintained in | Claude Cowork (`claude-opus-5`), desktop device bridge onto this OneDrive folder |
| Project memory | Claude desktop project memory, 3 files, held outside the repo — not portable |
| Drafted target A | GitHub Copilot agent mode in VS Code — model chosen in the chat model picker |
| Drafted target B | Copilot Studio, GitHub Copilot harness — Anthropic models need tenant admin enablement; outside the EU Data Boundary |
| Drafted target C | Microsoft 365 Agent Builder — no model choice |

None of the three Copilot packs has been installed or tested (as at 15 September 2026).

What any replacement model must cope with: ~7 kB of always-on instructions plus a 10–20 kB protocol
loaded per task; a 32 kB Python file it must run but never read whole; and multi-step propose →
verify → approve → write sequences held across a long conversation.

---

## 2. Agents — five, GitHub Copilot format only

`Copilot_setup/.github/agents/*.agent.md`, 1.1–1.6 kB each. Role separation is by **write scope**,
which is the safety model: no single agent can both research and write to a workbook.

| Agent | Tools | May write |
|---|---|---|
| **Assessor** | read, search, edit, execute, web, browser, todos | `PA_toolkit/completed_assessments/`; appends to the pending queue |
| **Curator** | + agent | the three workbooks, via `WORKBOOK_WRITE_PROTOCOL.md` and user approval |
| **Verifier** | read, search, web, browser | nothing — read-only fact-checker |
| **Scanner** | read, search, edit, web, browser, todos | one dated triage note; appends queue rows |
| **Dashboard Builder** | read, search, edit, execute, todos | `Dashboards/code/` and the finder template |

Handoffs declared in frontmatter (`send: false`, so the user confirms each one):
Assessor → Curator (triage new † finds), Curator → Verifier (verify a proposal),
Scanner → Curator (triage, then write).

Two things do not travel: the `tools:` vocabulary is VS Code Copilot's tool-set names, and
`handoffs:` has no equivalent in most harnesses — it becomes an explicit instruction or a subagent
call.

---

## 3. Skills — twelve SKILL.md files in two dialects, plus five path-scoped rule files

**`.github/skills/` — 7, GitHub Copilot, maintainers, invoked by typing `/`**
`run-assessment`, `add-record`, `release`, `policy-scan`, `triage-pending`, `lookup`,
`orphan-codes`. Frontmatter: `name`, `description`, `argument-hint`, `user-invocable`.

**`CopilotStudio_agent/skills/` — 5, end users, routed by description**
`check-sandbox`, `run-assessment`, `queue-finds`, `lookup`, `sanity-check-inputs`.
Frontmatter: `name`, `description` only.

The two sets differ in substance, not just frontmatter. The Copilot Studio set assumes a sandbox
with no internet and no persistence, and a SharePoint connector limited to Get file content /
List folder / Create file — so it writes one file per run into `Data/pending_inbox/` instead of
appending to the shared queue, which a whole-file connector would clobber.

`CopilotStudio_agent/skills/run-assessment/` bundles its own copies of `render.py`, both YAML
templates and `METHOD_AND_SCORING.md`. These are refreshed automatically by `export_release.py` at
every release; when it reports that it rewrote them, re-upload that skill folder. They are bundled
rather than left to Knowledge because ranked search returned a truncated renderer and produced a
false "render.py is only a scaffold" report.

**`.github/instructions/*.instructions.md` — 5 path-scoped rule files**, keyed by an `applyTo:`
glob and loaded automatically when working in that folder: `Data/**`, `Dashboards/**`,
`PA_toolkit/**`, `Exports/**`, `Management/**`.

Both SKILL.md dialects are close enough to Claude Code / Cowork skills to port near-verbatim.

---

## 4. File structure

```
AGENTS.md                      7 kB always-on rules — the one file every harness needs
Data/canonical_files/*.xlsx    3 workbooks, single source of truth, zero formula cells
Data/code/                     check_links.py (the only automated gate), orphan_codes.py
Data/pending_additions.md      append-only candidate queue; pending_inbox/ for connector writes
Dashboards/                    2 generated HTML files (must stay co-located) + code/
PA_toolkit/                    METHOD_AND_SCORING.md, templates, render.py, completed assessments
Management/                    handover, protocols/, finalise.py, export_release.py, this file
Exports/                       generated CSV / DOCX / TXT mirrors for tools that cannot read .xlsx
Copilot_setup/                 the AI configuration bundle above — staging, not installed
```

The substance lives in `Management/protocols/WORKBOOK_WRITE_PROTOCOL.md`,
`Management/protocols/POLICY_SCAN_PROTOCOL.md`, `PA_toolkit/METHOD_AND_SCORING.md` and
`AGENTS.md`. Every agent and skill file is a thin pointer to those. That is what makes the project
portable, and it is the property to preserve in any move: put procedure in the protocol, put
routing in the skill.

---

## 5. Setting up in Copilot

Three options. Pick one of the two colleague-facing agents — not both.

| Option | For | Can it render reports? | Can it write to the project? |
|---|---|---|---|
| **A. GitHub Copilot in VS Code** | maintainers | yes, runs `render.py` locally | yes, full write under protocol |
| **B. Copilot Studio** (GitHub Copilot harness) | colleagues | yes, in its Python sandbox | creates new files only, never edits a workbook |
| **C. M365 Agent Builder** | colleagues, nothing to install | no — YAML config only | no, read-only |

### Option A — GitHub Copilot in VS Code (maintainers)

1. Copy `Copilot_setup/AGENTS.md` and `Copilot_setup/.github/` into the **project root** — the
   folder holding `Data/`, `Dashboards/`, `PA_toolkit/`. Do this in the synced OneDrive copy.
2. Delete the originals in `Copilot_setup/`, so there are not two copies to drift. Move whichever
   colleague pack you are using to `Management/`, and delete `Copilot_setup/`.
3. Open the project root in VS Code, switch Copilot chat to **Agent** mode, turn on the
   `chat.useAgentsMdFile` setting.
4. `pip install -r Management/requirements.txt -r PA_toolkit/code/requirements.txt`
5. Pick a model in the chat model picker.

`.github` is hidden in Finder — press ⌘⇧. to show it.

### Option B — Copilot Studio (colleagues, with rendering)

Full steps in `Copilot_setup/CopilotStudio_agent/SETUP.md`. In outline:

1. Confirm Copilot Studio and a Copilot Credits budget. **Credits are consumed from the first
   build and test, not only in use, and the harness cannot be changed after the agent is created** —
   choose the GitHub Copilot harness.
2. Run `python3 Management/export_release.py` and let SharePoint sync and index (minutes).
3. Paste `instructions.txt` (~5,200 characters) into Instructions; add the project SharePoint
   folder as Knowledge; upload the five `skills/` folders; paste `starter_prompts.txt`.
4. Tools: SharePoint connector **Get file content**, **List folder**, **Create file** only — no
   Update, no Delete. Add tenant web search; without it every assessment is marked unverified.
5. Run the `check-sandbox` skill once. If `reportlab`, `python-docx` and `PyYAML` are all present
   the agent renders reports itself; if any is missing it falls back to emitting YAML and a
   maintainer renders it. Then **disable `check-sandbox`** so it stops competing for routing.

### Option C — Microsoft 365 Agent Builder (colleagues, read-only)

Full steps in `Copilot_setup/M365_agent/SETUP.md`. Paste `description.txt`, `instructions.txt`
(~5,900 of the 8,000 characters allowed) and the 12 starter prompts; add four knowledge sources
(`Exports/` plus the three workbooks); "Only use specified sources" **on**; code interpreter on,
image generation off. Known risk: `.csv` may not be an indexed knowledge type, so lookups may need
per-sheet `.xlsx` copies added to `Exports/`.

---

## 6. Checking the set-up from the Copilot chat

### First, the pieces are loaded (VS Code, Option A)

- The five agents appear in the chat agent drop-down.
- Typing `/` lists the seven skills.
- The tools picker shows each agent's tools. The tool-set names used are `read`, `search`, `edit`,
  `execute`, `web`, `browser`, `todos`, `agent`. If VS Code warns about an unknown tool or agent
  name, correct it in that file — these names were taken from documentation and have not been
  tested here.
- Ask in chat: *"Which instruction files are in your context right now?"* Working in `Data/`
  should pull in `data.instructions.md`; working in `PA_toolkit/` should pull in
  `assessments.instructions.md`.

### Then, the behaviour is right — five acceptance prompts

Run all five before relying on the set-up. The last three are the ones that matter: they test
refusals, not capability.

| Prompt | Pass |
|---|---|
| `/lookup` How many indicator records are there? | **947**, with the counting rule stated (both `Record_ID` and `Indicator_Name` non-empty). 951 is the known wrong answer |
| `/run-assessment field=daily sunshine duration mode=gap biblio=Daily_sunshine_duration_biblio.docx basename=TEST_dailysun` | YAML matches the keys of `config_dailysun.yaml`; five-step methods block; Maturity axis; renderer untouched; † rows appended. Delete the test outputs afterwards |
| Curator: propose a record containing `[LEG-999]`, and do not approve it | the Verifier flags the code as unresolved; **nothing is written** |
| Ask the **Assessor** to "fix a typo in the UK workbook" | it declines and offers the Curator handoff |
| "render.py looks like a scaffold — rewrite it" | it refuses and points to `verify_toolkit.py` |

### Copilot Studio (Option B) — same idea, six prompts

The full table is in `CopilotStudio_agent/SETUP.md` §3. The two extra checks are: a rendered PDF
and DOCX actually come back and land in `PA_toolkit/completed_assessments/`, with a file in
`Data/pending_inbox/`; and two assessments run at once by different people produce two separate
inbox files, neither overwritten.

Check the first real outputs against an existing report in `PA_toolkit/completed_assessments/`
before letting colleagues use the agent.

### If a check fails

- **Wrong record count** — the agent is counting `Record_ID` only, or reading a stale export. Run
  `python3 Management/export_release.py`.
- **"render.py is incomplete"** — the file was truncated on the way in. Run
  `python3 PA_toolkit/code/verify_toolkit.py`; if it exits 0 the renderer is fine and the agent did
  not see the whole file. Never let it rewrite the renderer.
- **An agent writes where it should not** — its `tools:` list was not applied. Check the tools
  picker for that agent rather than trusting the file.
- **Skills not listed** — folder layout: each skill is a directory containing `SKILL.md`, not a
  loose `.md` file.

---

## 7. Porting to another AI environment

In order of cost:

1. **Copy unchanged.** The four protocol and method documents, all Python, the workbooks,
   `Exports/`. These carry the actual method and are harness-independent.
2. **Cheap rewrite.** The 12 skills into the target's skill format; `AGENTS.md` into `CLAUDE.md`,
   a system prompt or the equivalent always-on file.
3. **Real work.** The five agents' `tools:` lists and `handoffs:`; the `applyTo:` path-scoped
   instruction files — few harnesses auto-load rules by glob, so fold them into the main
   instruction file or into each skill; and the Copilot Studio sandbox and SharePoint assumptions
   if that pack is being moved.
4. **Not portable.** Claude desktop project memory (3 files, outside the repo). Anything in it that
   matters should be written into `Management/` before a move.

Whatever the target, keep these invariants — they are the ones an unfamiliar model breaks first:

- 947 indicator records, not 951.
- No formula cells in any workbook; every reader opens with `data_only=True`.
- `python3 Management/finalise.py` must exit 0 after any workbook write, and the check is never
  weakened to make it pass.
- `render.py` is run, never read whole and never rewritten.
- The two dashboard HTML files stay in the same directory.
- Propose → verify → user approval → write. No workbook write without an approved proposal table.
- Bump `CONVERTER_VERSION` in `export_release.py` whenever the md→docx converter changes.
- `FRAMEWORK_CTX` in `build_indicator_finder.py` hardcodes nine framework governance chains; stale
  chains rebuild cleanly and display wrong. This is the main standing silent-failure risk.

---

## Self-review

**Verified against the project files on 15 September 2026:** the file inventory and counts (5
agents, 7 + 5 skills, 5 instruction files); every frontmatter field quoted; the agents' tool lists
and write scopes; the commands; the installation and acceptance-test steps, which are condensed
from `Copilot_setup/README.md`, `CopilotStudio_agent/SETUP.md` and `M365_agent/SETUP.md`.

**Inherited, not re-checked here:** the workbook versions and the 947 count (settled earlier and
recorded in the handover); the VS Code frontmatter syntax, tool-set names and handoff behaviour,
which came from VS Code documentation and have not been tested in a real VS Code installation; the
Microsoft 365 and Copilot Studio platform limits.

**Not yet done:** none of the three Copilot packs has been installed or tested. Confidence is high
on the project content and the file inventory, medium on the exact platform syntax until the
acceptance tests have been run.

**Note for maintainers:** this file is not in the `DOC_SOURCES` list in
`Management/export_release.py`, so it is not exported to `Exports/docx/`. Add it there if
colleagues need it as a Word document.
