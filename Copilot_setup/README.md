# Copilot_setup — staging folder for the GitHub Copilot configuration

This folder holds the project's **GitHub Copilot** configuration (agent mode in VS Code) until it
is installed. GitHub Copilot is the AI environment chosen for managing this project on Met Office
systems; no other Copilot set-up is maintained.

**Installation, checks and acceptance tests are in the root `README.md`** ("Setting up GitHub
Copilot in VS Code"). Installing moves `AGENTS.md` and `.github/` to the repository root, after
which this folder is deleted. Do not keep both copies: they would drift.

`.github` starts with a dot, so it is hidden in Finder. Press ⌘⇧. to show hidden files.

## What is here

```
AGENTS.md                                   always-on project instructions (goes to the root)
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
```

Role separation is by **write scope** — no single agent can both research and write to a workbook.
Handoffs are declared in each agent's frontmatter with `send: false`, so the user confirms each one:
Assessor → Curator (triage new † finds), Curator → Verifier (verify a proposal), Scanner → Curator
(triage, then write).

## Not included, deliberately

- **Hooks.** For example, running `finalise.py --check` automatically after edits to
  `Data/canonical_files/`. VS Code agent hooks are in preview. Add one once your VS Code version
  and organisation policy support it.
- **`.github/copilot-instructions.md`.** `AGENTS.md` does the same job. Having both would mean two
  always-on files to keep in step.
- **Prompt files (`.prompt.md`).** VS Code is moving these to skills, so the workflows are written
  as skills.

Maintenance — which configuration file to re-check when a protocol or script changes — is in
`Management/PROJECT_HANDOVER_Nature_Climate_Indicators.md` §6.1, so that it survives the deletion of
this folder.

## Status and confidence

Drafted 11 September 2026; revised 6 October 2026 to remove the Microsoft 365 Agent Builder and
Copilot Studio packs (retired when GitHub Copilot was chosen) and to update record counts and the
removed `FRAMEWORK_CTX` references. **Not yet installed or tested.** The frontmatter fields,
tool-set names (`read`, `search`, `edit`, `execute`, `web`, `browser`, `todos`, `agent`) and
handoff behaviour are taken from VS Code documentation; whether a handoff's `agent:` value must match
the target agent's `name` is assumed. If VS Code warns about an unknown tool or agent in a file,
correct the name in that file. Confidence: high on project content, medium on VS Code syntax until
the acceptance tests have run.
