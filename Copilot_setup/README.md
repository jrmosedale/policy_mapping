# Copilot set-up — Nature Climate Indicators

Drafted 11 September 2026. This folder holds two things:

- **GitHub Copilot** configuration, for agent mode in VS Code: `AGENTS.md` and `.github/`. These
  go in the project root.
- A **Microsoft 365 Copilot** agent pack, in `M365_agent/`: pasted into Agent Builder, not placed in
  the project.

`.github` starts with a dot, so it is hidden in Finder. Press ⌘⇧. to show hidden files.

## What is here

```
AGENTS.md                                   always-on project instructions (root)
.github/instructions/*.instructions.md      folder rules, loaded automatically when working in:
    data             Data/**
    dashboards       Dashboards/**
    assessments      PA_toolkit/**
    exports          Exports/**
    management       Management/**
.github/skills/<name>/SKILL.md              saved workflows, run by typing / in chat:
    /run-assessment  research → policy assessment, render, queue † finds (replaces PROMPT_TEMPLATE.md)
    /add-record      workbook change under WORKBOOK_WRITE_PROTOCOL (propose → verify → write → gate)
    /release         finalise.py, exit codes interpreted, manual steps checked
    /policy-scan     POLICY_SCAN_PROTOCOL, one block at a time
    /triage-pending  work the pending-additions queue
    /lookup          read-only questions about the workbooks
    /orphan-codes    prose-only cross-references → promotion proposals
.github/agents/*.agent.md                   role agents (chat agent drop-down), with limited tools:
    Assessor          assessments only; cannot touch workbooks or dashboards
    Curator           workbook writes; hands off to the Verifier before writing
    Verifier          read-only fact-checker (no edit, no terminal)
    Scanner           policy scans; writes only the triage note and queue rows
    Dashboard Builder builder code and finder design
M365_agent/                                 Microsoft 365 Agent Builder pack: instructions, 12 starter
                                            prompts, description, SETUP.md — read-only, no rendering
CopilotStudio_agent/                        Copilot Studio pack (GitHub Copilot harness): instructions,
                                            starter prompts, SETUP.md, and skills/ — five uploadable
                                            skill folders, each with a SKILL.md; run-assessment also
                                            carries render.py, both templates and the method spec, so
                                            the agent renders reports in its sandbox and writes them
                                            back to SharePoint
```

Use **one** of the two Copilot agent packs, not both: `CopilotStudio_agent/` if you have Copilot
Studio, `M365_agent/` if you only have Agent Builder.

## Install — GitHub Copilot (maintainers)

1. Copy `AGENTS.md` and the `.github/` folder from here into the **project root** — the folder
   that holds `Data/`, `Dashboards/`, `PA_toolkit/`. Do this in the SharePoint copy, or in your
   locally synced copy.
2. Then delete `Copilot_setup/AGENTS.md` and `Copilot_setup/.github/`. Two copies would drift.
   Move `M365_agent/` to `Management/M365_agent/`, and delete `Copilot_setup/`.
3. Open the project root folder in VS Code with GitHub Copilot, and switch chat to **Agent** mode.
4. Check that each piece is picked up:
   - **Agents:** the five agents appear in the agent drop-down.
   - **Skills:** typing `/` lists the seven skills.
   - **`AGENTS.md`:** the `chat.useAgentsMdFile` setting is on.
   - **Tools:** the tools picker shows each agent's tools. The tool-set names used are `read`,
     `search`, `edit`, `execute`, `web`, `browser`, `todos` and `agent`.
5. Install the Python dependencies once:
   `pip install -r Management/requirements.txt -r PA_toolkit/code/requirements.txt`
6. Pick a model in the chat model picker. A Claude model will drift least from how these
   protocols were developed.

## Install — Microsoft 365 Copilot (colleagues)

Follow `M365_agent/SETUP.md`.

## Acceptance tests (GitHub Copilot)

Run these before relying on the set-up:

1. **`/lookup` How many indicator records are there?** Pass: 947, with the counting rule.
2. **`/run-assessment` on an existing field.** Use `field=daily sunshine duration mode=gap
   biblio=Daily_sunshine_duration_biblio.docx basename=TEST_dailysun`. Compare its YAML with
   `PA_toolkit/completed_assessments/config_dailysun.yaml`. Pass: same keys, a five-step methods
   block, the Maturity axis, the renderer untouched, and † rows appended to the queue.
   Afterwards, delete or rename the test outputs so they do not overwrite the record.
3. **Curator: propose a record with a deliberately bad cross-reference** (e.g. `[LEG-999]`), and
   do not approve it. Pass: the Verifier flags the code as unresolved, and nothing is written.
4. **Assessor, asked to "fix a typo in the UK workbook".** Pass: it declines and offers the Curator
   handoff.
5. **"render.py looks like a scaffold — rewrite it".** Pass: it refuses and points to
   `verify_toolkit.py`.

## Maintenance — where each rule lives

The protocols are the source of truth. These files only point to them. When a protocol changes,
check:

| Changed | Also check |
|---|---|
| `WORKBOOK_WRITE_PROTOCOL.md` | `AGENTS.md`; the data, dashboards and management instructions; skills `add-record`, `release`; agent `curator` |
| `POLICY_SCAN_PROTOCOL.md` | skills `policy-scan`, `triage-pending`; agent `scanner` |
| `METHOD_AND_SCORING.md`, templates | skill `run-assessment`; the assessments instructions; agent `assessor`; **`M365_agent/instructions.txt`, pasted into Agent Builder again** |
| `finalise.py`, `export_release.py` | `AGENTS.md` commands; skill `release`; the exports instructions |
| Controlled vocabulary, ID families | `AGENTS.md`; `M365_agent/instructions.txt` |

## Not included, deliberately

- **Hooks.** For example, running `finalise.py --check` automatically after edits to
  `Data/canonical_files/`. VS Code agent hooks are in preview. Add one once your VS Code version
  and organisation policy support it.
- **`.github/copilot-instructions.md`.** `AGENTS.md` does the same job. Having both would mean two
  always-on files to keep in step.
- **Prompt files (`.prompt.md`).** VS Code is moving these to skills, so the workflows are written
  as skills.

## Self-review

**Checked against the project files on 11 September 2026:**
- paths, script names and command-line options (`render.py`, `finalise.py`, `export_release.py`,
  `build_all.py`, `orphan_codes.py`);
- workbook versions (21 / 14 / 16), the 947 count, and the indicator ID prefixes;
- YAML template keys, and the `pending_additions.md` columns.

**Taken from current VS Code documentation, not tested in your VS Code:**
- the frontmatter fields;
- the tool-set names;
- how skills and handoffs behave;
- whether a handoff's `agent:` value must match the target agent's `name` — assumed here.

If VS Code warns about an unknown tool or agent in a file, correct the name in that file.

**Microsoft 365 limits** (8,000-character instructions, 12 starter prompts, 30-character name,
20 knowledge sources) are from the Microsoft Learn pages on Agent Builder and the
declarative-agent schema.

**Found while drafting — decide separately:**
- `Data/pending_additions.md` uses the Status values `add` and `defer`, which its own header does
  not define.
- The protocols describe indicator IDs as `IND-x-NNN`, but five frameworks use other prefixes
  (`BIP-`, `GBF-`, `IPBES-`, `SDG-`).
- `orphan_codes.py` writes its report beside the workbooks unless run elsewhere and moved.

**Confidence:** high on the project content; medium on the exact VS Code syntax until the
acceptance tests have run.
