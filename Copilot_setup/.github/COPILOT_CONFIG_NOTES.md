# GitHub Copilot configuration — notes

Reference notes for the project's GitHub Copilot configuration (agent mode in VS Code). Copilot
does not load this file; it is for the people maintaining the configuration. It travels with
`.github/` when the configuration is installed, so it stays beside the files it describes.

Installation, checks and acceptance tests are in the root `README.md` ("Setting up GitHub Copilot
in VS Code"). Which configuration file to re-check when a protocol or script changes is in
`Management/PROJECT_HANDOVER_Nature_Climate_Indicators.md` §6.1.

## What the configuration contains

| File | Role |
|---|---|
| `AGENTS.md` (repository root) | Always-on project instructions, loaded on every turn |
| `.github/instructions/*.instructions.md` | Folder rules, loaded automatically when working in `Data/`, `Dashboards/`, `PA_toolkit/`, `Exports/` or `Management/` |
| `.github/skills/<name>/SKILL.md` | Saved workflows, run by typing `/` in chat |
| `.github/agents/*.agent.md` | Role agents in the chat agent drop-down, each with limited tools |

**Skills**

| Skill | Does |
|---|---|
| `/run-assessment` | Research → policy assessment, render, queue † finds (replaces `PA_toolkit/PROMPT_TEMPLATE.md` inside Copilot) |
| `/add-record` | Workbook change under `WORKBOOK_WRITE_PROTOCOL.md`: propose → verify → write → gate |
| `/release` | Runs `finalise.py`, interprets exit codes, checks the manual steps |
| `/policy-scan` | `POLICY_SCAN_PROTOCOL.md`, one block at a time |
| `/triage-pending` | Works the pending-additions queue |
| `/lookup` | Read-only questions about the workbooks |
| `/orphan-codes` | Prose-only cross-references → promotion proposals |

**Agents**

| Agent | Scope |
|---|---|
| Assessor | Assessments only; cannot touch workbooks or dashboards |
| Curator | Workbook writes; hands off to the Verifier before writing |
| Verifier | Read-only fact-checker (no edit, no terminal) |
| Scanner | Policy scans; writes only the triage note and queue rows |
| Dashboard Builder | Builder code and finder design |

## Role separation and handoffs

Roles are separated by **write scope**: no single agent can both research and write to a workbook.
Handoffs are declared in each agent's frontmatter with `send: false`, so the user confirms each one:

- Assessor → Curator: triage new † finds
- Curator → Verifier: verify a proposal before writing
- Scanner → Curator: triage, then write

## Not included, deliberately

- **Hooks** — for example, running `finalise.py --check` automatically after edits to
  `Data/canonical_files/`. VS Code agent hooks are in preview; add one once the VS Code version
  and organisation policy support it.
- **`.github/copilot-instructions.md`** — `AGENTS.md` does the same job. Having both would mean
  two always-on files to keep in step.
- **Prompt files (`.prompt.md`)** — VS Code is moving these to skills, so the workflows are
  written as skills.

## Status and confidence

Drafted 11 September 2026; revised 6 October 2026 to remove the retired Microsoft 365 Agent
Builder and Copilot Studio packs; notes moved into `.github/` on 7 October 2026.
**Not yet installed or tested.** The frontmatter fields, tool-set names (`read`, `search`, `edit`,
`execute`, `web`, `browser`, `todos`, `agent`) and handoff behaviour are taken from VS Code
documentation; whether a handoff's `agent:` value must match the target agent's `name` is assumed.
If VS Code warns about an unknown tool or agent in a file, correct the name in that file and
update this section. Confidence: high on project content, medium on VS Code syntax until the
acceptance tests have run.
