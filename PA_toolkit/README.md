# MO research → UK policy relevance — template kit

Produce a comparable, consistently formatted assessment of how a Met Office research field could
inform UK climate–nature policy, as **both** a styled PDF and an **editable Word** document, from a
single YAML config.

## What's in the kit

Start with `ASSESSMENT_TOOLKIT_USER_GUIDE.md` — this README is the field reference; the guide is the walkthrough.

| File | Purpose |
|---|---|
| `code/render.py` | The renderer. Reads a YAML config, writes PDF and/or DOCX. You rarely edit this. |
| `template_files/TEMPLATE_applied.yaml` | Worked example, **applied mode** (Plant Pest, Pathogen & Biosecurity). Copy and edit per field. |
| `template_files/TEMPLATE_gap.yaml` | Worked example, **gap / prospective mode** (a UK LST product MO could build). |
| `METHOD_AND_SCORING.md` | The fixed method and two-axis scoring, incl. the two modes. Keeps fields comparable. |
| `PROMPT_TEMPLATE.md` | Copy-paste prompt so Claude (or another AI) runs a new field and emits a config. |
| `code/requirements.txt` | Python dependencies — three packages, renderer only. |
| `code/verify_toolkit.py` | Proves the kit works on this machine: checks dependencies, confirms `render.py` is intact, renders both templates to PDF and DOCX in a temp directory. Run it first on any new machine. |

## Install (once)

```bash
pip install -r code/requirements.txt          # reportlab, python-docx, pyyaml
```

No Node, no internet needed to render. (Generating the *content* for a new field does need sources.)

## Run

```bash
python code/render.py template_files/TEMPLATE_applied.yaml --format both --outdir completed_assessments
# --format pdf | docx | both
```

Output names come from `meta.output_basename` in the YAML.

## Two question types (modes)

- **Applied** — where does/could *existing* MO research inform UK policy? Second axis = **Status**
  (Current / Opportunity). Example: `TEMPLATE_applied.yaml`.
- **Gap / prospective** — if MO *built* product X (evidenced by others' work elsewhere), what could UK
  policy do with it? Second axis = **Maturity** (Demonstrated / Emerging / Conceptual). Example:
  `TEMPLATE_gap.yaml`.

Switching mode is editing the YAML, not the code: change `labels.summary`, `labels.references_primary`
and the `status_axis` block (its `label` and `values` define the second-axis chip and colours).
`METHOD_AND_SCORING.md` defines both modes. The renderer is identical for both.

## Edit it yourself

Everything you'd normally ask for is in the YAML — no code changes:

- **Headings**: `labels:`
- **Section order / which sections appear**: `section_order:` (delete a line to drop a section)
- **Colours and Word font**: `theme:`
- **Title, subtitle, footer, output filename**: `meta:`
- **Scoring legend text**: `scoring.legend`
- **All content**: `key_points`, `summary`, `policy_rows`, `indicator_rows`, `methods`, `gaps`,
  `references_primary`, `references_other`

Authoring markup in any text value: `**bold**`, `*italic*`, `[[label|https://url]]`.
Policy rows: set `relevance:` 1–3 (drives row colour: 3 green / 2 amber / 1 grey) and
`status:` Current or Opportunity (drives the chip). For a two-policy row use `parts:` (two
`{label, url}` entries) instead of `name`/`url`.

## Run a new research field

1. Copy `template_files/TEMPLATE_applied.yaml` → `config_<field>.yaml`.
2. Either fill it in by hand, or use `PROMPT_TEMPLATE.md` to have an AI do the research and write it
   (attach this kit + the bibliography + the workbooks). In the prompt's **INPUTS block** you type the
   exact filenames you're attaching (they vary between runs) and the research field. Where the AI has
   web access, the prompt directs it to search to complement the files — finding policy activities not
   in the workbook and verifying dates/status/URLs — and to flag unverified items when offline.
3. `python render.py config_<field>.yaml --format both --outdir outputs`

## Share with another user

Send the whole `PA_toolkit/` folder (you can delete any rendered outputs). They need Python 3 and the renderer packages in
`requirements.txt`. With `PROMPT_TEMPLATE.md` + `METHOD_AND_SCORING.md` they can run their own
queries through Claude or another AI and get the same method, scoring and layout. The renderer is
self-contained and produces identical structure regardless of who runs it.

## Notes / limits

- PDF uses Helvetica (built into reportlab); Word uses `theme.font` (default Arial). They look near-identical.
- The renderer doesn't read the spreadsheets itself — policy hyperlinks are written into the YAML
  (taken from the workbook `Link` column during the research step). This keeps rendering offline and
  deterministic.
- `meta.prepared` and any "accessed" dates are free text — update them per run.
