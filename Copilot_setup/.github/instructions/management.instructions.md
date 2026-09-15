---
name: Protocols and management
description: Rules for editing the handover, the protocols and the release scripts in Management/.
applyTo: "Management/**"
---
# Working in Management/

- The protocols in `Management/protocols/` are the source of truth for procedure. `AGENTS.md`, the
  skills in `.github/skills/` and the Microsoft 365 agent's instructions only point to them. When a
  protocol changes, check those three places for statements that are now wrong, and tell the user
  that the Microsoft 365 agent's instructions must be updated by hand in Agent Builder.
- **Protocol drift is a standing risk** (handover §4.3). Before a protocol states that a tool,
  check or convention exists, confirm it in the file store. Answer "clarify X" items by
  investigating the code or data, then record the finding as settled.
- Keep one handover document. Do not create parallel summaries that restate it; point to it
  instead.
- When a mistake is found, record the failure analysis in the artefact itself, not only the fix.
- `finalise.py` is the release gate: check → rebuild → export, each only if the previous step
  passed (exit codes 1 / 2 / 3). It deliberately does not bump versions or archive — materiality is
  a human judgement. Do not add those steps.
- After editing any Markdown source that is exported, run `python3 Management/export_release.py`
  so that `Exports/docx/` matches.
