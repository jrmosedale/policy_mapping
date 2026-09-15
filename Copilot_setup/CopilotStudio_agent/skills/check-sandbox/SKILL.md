---
name: check-sandbox
description: Checks which Python libraries this agent's sandbox has, and whether the assessment renderer can run here. Use when asked to test the sandbox, check dependencies, or diagnose a failed render.
---
# Check the sandbox

Run once during set-up, then disable or delete this skill so it stops competing for routing.

1. In the sandbox, run Python that imports each of: `reportlab`, `docx` (python-docx), `yaml`
   (PyYAML), `openpyxl`, `pandas`. For each one, report the version or the exact import error.
2. Report the Python version, and whether a writable working directory is available.
3. Say plainly what this means:
   - **reportlab, docx and yaml all present** — the agent can render assessment reports itself with
     the `run-assessment` skill.
   - **any of those three missing** — the agent cannot render. It still produces the YAML config,
     and the user renders it with:
     `python3 PA_toolkit/code/render.py <config> --format both --outdir PA_toolkit/completed_assessments`
   - **openpyxl or pandas present** — the agent can read the workbooks directly; otherwise it uses
     the CSVs in `Exports/csv/`.
4. Do not attempt to install anything. The sandbox has no internet access.
