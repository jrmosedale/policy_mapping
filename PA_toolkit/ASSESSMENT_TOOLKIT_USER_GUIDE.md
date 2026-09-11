# Policy assessment toolkit — user guide

**Draft, 1 September 2026.** A task-oriented how-to for producing a Met Office research → UK policy relevance assessment. It is the companion to `METHOD_AND_SCORING.md` (beside this file), which defines *why* the method is what it is; this guide covers *how to run it*.

Read this if you want to produce an assessment. Read `METHOD_AND_SCORING.md` if you want to change the method, or need to defend a score.

---

## 1. What you are producing

A short, styled report — **PDF and editable Word, from the same source** — answering one question about one Met Office research field:

> Where does, or could, this science inform UK climate–nature policy, and how material is it in each case?

Every assessment has the same structure, the same two-axis scoring and the same layout. That is the point: assessments of different fields, written months apart by different people, can be read side by side because none of the judgement structure was reinvented. Four exist so far — plant pest and biosecurity, daily sunshine duration, land surface temperature, ocean heatwaves — in `completed_assessments/`. Read one before you start; it is the fastest way to understand the shape of the output.

**How the work is actually done.** You do not write the report. You give an AI a fixed prompt, a fixed method document and a format example; it does the research and emits a YAML config; a script renders that config to PDF and Word. Your job is to choose the field and mode, supply the inputs, and then review what comes back. The method never varies between runs — only the content does.

---

## 2. What you need

Six files from `PA_toolkit/`, and nothing else from the project:

| File | Role |
|---|---|
| `code/render.py` | The renderer. You never edit it. |
| `code/requirements.txt` | Dependencies — three packages, renderer only. |
| `PROMPT_TEMPLATE.md` | The prompt you paste into the AI. |
| `METHOD_AND_SCORING.md` | The rules the AI must follow. Attached to the prompt; not read by the code. |
| `template_files/TEMPLATE_applied.yaml` **or** `template_files/TEMPLATE_gap.yaml` | A **format example** for the AI. Pick the one matching your mode. |
| `README.md` | The YAML field reference, for editing the config afterwards. |

Plus your own inputs:

- **A bibliography** for the field. In applied mode this is the Met Office researcher's own publication list; in gap mode it is external literature proving the approach works elsewhere. Any readable format — HTML, DOCX, CSV, Markdown. Existing examples are in `bibliographies/`.
- **`Data/canonical_files/uk_climate_nature_governance.xlsx`** — the source of policy candidates.
- **`Data/canonical_files/indicators_climate_nature.xlsx`** — optional; omit to skip the indicators section.
- **A flagship Met Office tool or dataset URL** for the field, if one exists.

Install once, then prove it works:

```bash
pip install -r code/requirements.txt
python3 code/verify_toolkit.py
```

`verify_toolkit.py` renders both templates to PDF and DOCX in a temporary directory and reports
what it found. Run it on any machine you port the kit to, **before** you run an assessment — it
turns "does this work here?" into a two-second answer.

The kit is self-contained. You can zip these six files and send them to a colleague with Python 3; they will get the same method, scoring and layout.

---

## 3. Choose your mode first

This is the only decision that changes the shape of the assessment, and it is easier to get right at the start than to correct later.

|  | **Applied** | **Gap / prospective** |
|---|---|---|
| The question | Where does or could *existing* MO research inform UK policy? | If MO *built* product X, what could UK policy do with it? |
| Bibliography is | MO's own publications | External literature — evidence the approach works elsewhere |
| Second axis | **Status**: Current / Opportunity | **Maturity**: Demonstrated / Emerging / Conceptual |
| Format example | `TEMPLATE_applied.yaml` | `TEMPLATE_gap.yaml` |

The rule of thumb: if the Met Office already produces the thing, it is applied. If the assessment is arguing that the Met Office *should* produce it, it is gap.

**Why the second axis changes.** In gap mode nothing can be "Current" — the product does not exist — so a realisation axis would be uniformly empty and tell you nothing. Maturity replaces it and discriminates between prospective applications by how proven they are elsewhere, which is a proxy for how near-term they are. The primary axis, Relevance, never changes.

---

## 4. Run it

**Step 1 — fill in the INPUTS block.** Open `PROMPT_TEMPLATE.md`. Everything in angle brackets is yours to complete: research field, mode, bibliography filename, flagship tool URL, output basename. The two workbook names are canonical and stable, so they no longer vary between runs.

**Step 2 — paste the prompt and attach the files.** Into Claude, or another AI with code execution. Attach exactly the files the INPUTS block names — the prompt tells the AI not to guess which file is which, so ambiguity here is the most common cause of a bad run.

**Step 3 — let it work, and expect it to search.** Where the AI has web access, the method *requires* it to search rather than rely on the attached files or its own knowledge: to find policy activities absent from the governance workbook, to confirm and date the research→policy channel from primary sources, to verify every status, date and URL against gov.uk / legislation.gov.uk / agency portals, to inspect the flagship tool directly, and to scan for authoritative indicators published since the workbook version. If the AI has **no** web access, the assessment is still valid but weaker, and it must list every unverified claim, date and URL at the end. Check that it did.

**Step 4 — render.**

```bash
python code/render.py config_<field>.yaml --format both --outdir completed_assessments
```

`--format` takes `pdf`, `docx` or `both`. Output filenames come from `meta.output_basename` in the YAML.

**Step 5 — review before you send.** See §6.

---

## 5. Reading the scores

Two axes, deliberately kept separate. Collapsing them into a single "confidence" or "relevance" number makes a high-value-but-unrealised link look weak, which is precisely the case this project most wants to surface.

**Relevance — materiality of MO science to the policy.** Drives the row colour.

- **3 High** (green) — a direct, often named, evidence input.
- **2 Medium** (amber) — informs a defined risk or evidence component.
- **1 Low** (grey) — indirect dependency.

**Status — realisation** (applied mode). Drives the chip.

- **Current** — MO science already informs the activity, and this is documented.
- **Opportunity** — a credible but not-yet-realised use.

**Maturity** (gap mode) — Demonstrated / Emerging / Conceptual, by how proven the application is elsewhere.

So a row can be `3 / Opportunity`: high materiality, not yet used. **That is the most interesting cell in the table**, and the reason the axes are separate — it is where the assessment is telling you something actionable rather than describing the status quo.

**The dagger (†)** marks an activity or indicator found by research but not held as a record in the workbooks. Daggers are proposals, not findings — see §7.

---

## 6. Review checklist

Before the report leaves your hands:

- **Every URL resolves**, and points at the current version of the instrument, not an archived one.
- **Every `Current` status is documented**, not inferred. An inferred link should be `Opportunity` (or `Conceptual`), and should say so.
- **British English, metric units, no hedging.** The renderer will not catch these.
- **The unverified list is empty, or you accept each item on it.** If the AI ran without web access, this list is the assessment's main weakness.
- **The indicator rows pass the measured-quantity test** — the capability could directly inform what the indicator *measures*, not merely the topic it sits under. An indicator measuring a GIS area takes no climate input however climate-adjacent its framework.
- **Open the DOCX.** The PDF and Word are generated independently; table layout problems show up in Word first.
- **The methods block still has its five-step structure.** It is what makes reports comparable; an AI will sometimes helpfully restructure it.

---

## 7. Afterwards — the daggers

`†` marks an activity or indicator the run found that the workbooks do not hold. These are
proposals, not findings, and they are **captured automatically**: the run appends each one as a row
to `Data/pending_additions.md`, the standing queue that the quarterly policy scan works through.

**This is not your decision to make, and that is deliberate.** The run used to *offer* to add them,
which meant a shared knowledge base stayed complete only if whoever happened to run the assessment
chose to act — and mostly they did not, so well-researched finds evaporated into old chat replies.
Appending changes no workbook and needs no sign-off; every row is still screened and approved at the
next scan (`Management/protocols/POLICY_SCAN_PROTOCOL.md` §5) before any record is written.

**What you should do:** read the daggered list in the chat reply and sanity-check it — you know the
field better than the assistant does. If something is plainly wrong, say so, and it can be marked
`rejected` in the queue with a reason rather than silently dropped.

**If you are working from a ported copy of `PA_toolkit/` alone**, the queue file will not be
reachable. The run must then hand you a copy-paste block instead. Paste it into
`Data/pending_additions.md` when you are next at the full project — it takes seconds, and it is the
only step in this workflow that depends on you remembering.

Anything eventually written to a workbook goes through
`Management/protocols/WORKBOOK_WRITE_PROTOCOL.md`: the target schema, its controlled vocabulary, its
ID conventions, no reused retired IDs, then `Management/finalise.py` before the version is finalised.

## 8. Editing the output yourself

Everything you would normally ask for is in the YAML. No code changes:

| Want to change | Edit |
|---|---|
| Headings | `labels:` |
| Which sections appear, and in what order | `section_order:` — delete a line to drop a section |
| Colours, Word font | `theme:` — drives both PDF and Word |
| Title, subtitle, footer, output filename | `meta:` |
| Scoring legend wording | `scoring.legend` |
| The second axis itself | `status_axis: {label, values}` |
| All content | `key_points`, `summary`, `policy_rows`, `indicator_rows`, `methods`, `gaps`, `references_primary`, `references_other` |

Authoring markup in any text value: `**bold**`, `*italic*`, `[[label|https://url]]`.

A two-policy row uses `parts:` with two `{label, url}` entries instead of `name`/`url`.

Re-render after editing. The renderer needs no internet and is deterministic — the same config always produces the same document.

---

## 9. Two classes of YAML — do not confuse them

- **Templates** — `TEMPLATE_applied.yaml` and `TEMPLATE_gap.yaml`, in `PA_toolkit/template_files/`. Structural exemplars, attached to the prompt as format examples. Never rendered as deliverables, never edited to hold real content.
- **Records** — `config_<field>.yaml`, in `PA_toolkit/completed_assessments/` beside their PDF and DOCX. The reproducible source of a specific assessment. Keep these: without the config, a rendered report cannot be updated, only rewritten.

Copy a template to start; save the result as a record.

---

## 10. If an assistant says `render.py` is incomplete

It is not. `render.py` is ~600 lines / ~32 KB with complete `build_pdf` (231 lines) and
`build_docx` (301 lines) implementations, no stubs, pure ASCII, and it renders both templates
to five-page PDFs and four-table Word documents. This has been verified by running it.

The claim comes from **silent truncation**: several AI assistants cap the size of an attached
file, read the first screenful, find `def build_pdf(cfg, out_path):` followed by its lazily
imported reportlab modules, and infer that the body is missing. Nothing warns you that the
rest of the file was never read.

**Do not accept an offer to rewrite it.** A regenerated renderer will produce documents that
look approximately right and differ in layout, colour mapping and table structure from the four
existing assessments — destroying the comparability that is the reason this kit exists, in a way
that is hard to notice until you put two reports side by side.

What to do instead:

1. Run `python3 code/verify_toolkit.py`. If it passes, the file is fine and the assistant is wrong.
2. Re-supply `render.py` — in chunks if the tool has a size cap, or paste only the function it
   claims is missing and ask it to confirm.
3. If it still insists, ignore it. The assistant never needs to read `render.py` to do its job:
   it writes a YAML config, and *you* run the renderer. `PROMPT_TEMPLATE.md` does not ask for
   `render.py` to be attached at all — only `METHOD_AND_SCORING.md`, a template YAML, the
   bibliography and the workbooks.

That last point is the durable fix: **`render.py` does not need to be attached to the prompt.**

## 11. Known limits

- The renderer does not read the workbooks. Policy hyperlinks are written into the YAML during the research step, taken from the workbook's `Link` column. This keeps rendering offline and deterministic, but means a link that changes in the workbook does not propagate to an already-rendered report.
- PDF uses Helvetica (built into reportlab); Word uses `theme.font`, default Arial. Near-identical, not identical.
- `meta.prepared` and any "accessed" dates are free text. Update them per run — nothing does it for you.
- The assessment reflects the workbook version current at the time of the run. It has no mechanism for noticing that the workbooks have since moved on.
