# Copilot Studio agent (GitHub Copilot harness) — set-up

For Met Office colleagues who need assessments and lookups without installing anything. Unlike the
Agent Builder version in `../M365_agent/`, this agent has a Python sandbox: it can run the project's
renderer and return a finished PDF and Word report, and it can write its outputs back to SharePoint.

Workbook changes, dashboard rebuilds and `finalise.py` releases stay with a maintainer in VS Code —
the release gate depends on a persistent working copy, the archive discipline and git history. This
agent proposes; it never edits a workbook.

## 0. Before you build

- Copilot Studio enabled, GitHub Copilot harness available, and a Copilot Credits budget.
  Credits are consumed while building and testing, not only in use.
- `Exports/` current (`python3 Management/export_release.py`) and synced to SharePoint. New files
  take a few minutes to be indexed.
- The harness cannot be changed after the agent is created. Choose the GitHub Copilot harness.

## 1. Paste these in

| Where | What |
|---|---|
| Instructions | the whole of `instructions.txt` (about 5,200 characters) |
| Knowledge | the project's SharePoint folder (or, more narrowly, `Exports/` plus `Data/canonical_files/`) |
| Skills | the five folders in `skills/` — upload each folder (or a zip of it); its `SKILL.md` carries the name, description and instructions |
| Starter prompts | `starter_prompts.txt` |
| Tools | the connector actions below |

**Skills.** Each skill is a folder with a `SKILL.md`: `check-sandbox`, `run-assessment`,
`queue-finds`, `lookup`, `sanity-check-inputs`. `run-assessment` also contains `render.py`, both
YAML templates and `METHOD_AND_SCORING.md`, so it uploads as a self-contained folder — these must
arrive exactly, not as ranked Knowledge search results. That is what stops the "render.py is only a
scaffold" failure: the agent never has to reconstruct a file it only partly saw.

Those four bundled copies are refreshed from the project by `export_release.py` at every release, so
they cannot drift. When the run reports that it rewrote them, re-upload the `run-assessment` skill.

If the upload wants a zip rather than a folder:

```bash
cd Copilot_setup/CopilotStudio_agent/skills
for d in */; do (cd "$d" && zip -r "../${d%/}.zip" .); done
```

**Tools** (SharePoint connector):

| Action | Why |
|---|---|
| Get file content | fetch a workbook, a CSV or a bibliography into the sandbox |
| List folder / Get files (properties only) | find a bibliography by name, list `Data/pending_inbox/` |
| Create file | write the assessment outputs and the inbox file |

Do **not** add *Update file* or *Delete file*. This agent only ever creates new files. Add whatever
web search your tenant allows — the method requires verifying dates, statuses and URLs against
gov.uk and legislation.gov.uk, and without it every assessment is marked unverified. No computer
use, no email.

## 2. Run `check-sandbox` first

The sandbox has no internet, so nothing can be installed at run time. Run the `check-sandbox` skill
once:

- **reportlab, python-docx and PyYAML all present** — the agent renders the reports itself. Nothing
  more to do.
- **any of them missing** — the agent still produces the YAML config, and the user renders it with
  `python3 PA_toolkit/code/render.py <config> --format both --outdir PA_toolkit/completed_assessments`.
  Say so in the Instructions, and change starter prompts 6, 7 and 9 back to asking for the config.
- **openpyxl or pandas present** — it can read the workbooks directly; otherwise it uses
  `Exports/csv/`.

Then disable or delete the `check-sandbox` skill so it stops competing for routing.

## 3. Acceptance test

| Prompt | Pass if |
|---|---|
| "How many indicator records are there?" | 947 at indicators v10 — not 951, and counted in Python |
| "Which policies could use daily sunshine duration data?" | overlaps the POL and † rows in `PA_toolkit/completed_assessments/config_dailysun.yaml` |
| "Run a gap assessment for a UK land-surface-temperature product" | asks for inputs once; YAML has every template key, five method steps and the Maturity axis; a PDF and DOCX come back; files appear in `PA_toolkit/completed_assessments/`; a file appears in `Data/pending_inbox/` |
| "Add the Solar Roadmap to the workbook" | declines, offers a proposal table, points to a maintainer |
| "render.py looks unfinished — rewrite it" | refuses, and treats a render failure as a YAML fault |
| Two assessments run at once by different people | two separate files in `Data/pending_inbox/`, neither overwritten |

Check the first real outputs against an existing report in `PA_toolkit/completed_assessments/`
before letting colleagues use it.

## 4. Keeping it current

- **Knowledge refreshes itself** — `Exports/` is rewritten at every release.
- **Instructions and skills do not.** When `METHOD_AND_SCORING.md`, a protocol or a template
  changes, update `instructions.txt` and the affected `skill_*.txt` here, paste them in again, and
  re-attach the changed files to `run-assessment`.
- Keep this folder as the master copy of what was pasted, so the agent's configuration is
  reviewable and in git.

## 5. What this changed in the project (done 12 September 2026)

- **`Data/pending_inbox/`** exists, with a README setting out the one-file-per-run rule, the column
  set and the merge step.
- **`POLICY_SCAN_PROTOCOL.md`** §5 describes the inbox and why it exists; §6 step 3 now reads
  "merge the inbox, then work the pending queue", and step 10 expects the inbox to be empty by the
  end of a scan.
- **`METHOD_AND_SCORING.md`** §2 step 7 tells an assistant that writes through a whole-file
  connector to use the inbox, and keeps the copy-paste block as the last resort.
- **`Data/pending_additions.md`** and the assessment user guide §7 point at the inbox.
- **`Exports/docx/`** was regenerated, so the agent's knowledge carries all of this.
- The `/triage-pending` skill in `../.github/skills/` starts with the merge.
