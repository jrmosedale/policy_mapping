---
name: Protocols and management
description: Rules for editing the handover, the protocols and the release scripts in Management/.
applyTo: "Management/**"
---
# Working in Management/

- The protocols in `Management/protocols/` are the source of truth for procedure. `AGENTS.md`, the
  skills in `.github/skills/`, the agents in `.github/agents/` and the instruction files only point
  to them. When a protocol changes, check those places for statements that are now wrong (the table
  in handover §6.1 lists which file to check for each protocol).
- **Documentation drift is a standing risk** (handover §10.3). Before a protocol states that a tool,
  check or convention exists, confirm it in the file store. Answer "clarify X" items by
  investigating the code or data, then record the finding as settled.
- Keep one handover document. Do not create parallel summaries that restate it; point to it
  instead.
- When a mistake is found, record the failure analysis in the artefact itself, not only the fix.
- `finalise.py` is the release gate: regenerate the Cross-Reference Index → integrity check →
  legislation link-title check → rebuild → export, each only if the previous step passed (exit codes
  1 / 2 / 3; 1 covers the index, the integrity check and the link check). It deliberately does not bump versions or archive — materiality is
  a human judgement. Do not add those steps.
- After editing any Markdown source that is exported, run `python3 Management/export_release.py`
  so that `Exports/docx/` matches.
