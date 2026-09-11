# Prompt template — run a new Met Office field

Paste the prompt below into Claude (or another capable AI with code execution), and attach the files
you name in the INPUTS block: `METHOD_AND_SCORING.md`, `TEMPLATE_applied.yaml` or `TEMPLATE_gap.yaml`
(format example), the **bibliography**, the **governance workbook**, and — optionally — the
**indicators workbook**.

**Do not attach `render.py`.** The assistant's job ends at writing the YAML config; you run the
renderer yourself. Attaching it adds ~32 KB of code the assistant does not need, and invites the
failure described below — an assistant that truncates the file, concludes it is unimplemented, and
offers to rewrite it. (Earlier versions of this page did ask for it. They were wrong.)

Fill in everything in **angle brackets**. The two workbook names are now canonical and stable, so they no longer change between runs; only the bibliography, field, mode and output basename vary.

---

> **INPUTS** (use these exact attached files; do not guess which file is which):
> - Research field:        `<e.g. Microclimate modelling / Heat & health / Pollen & aeroallergens>`
> - Mode:                  `<applied | gap>`  (applied = existing MO research; gap = a product MO could build, evidenced by others' work)
> - Bibliography file:     `<e.g. Deborah-Hemming-Biblio.html>`  (applied: MO's own publications; gap: external reading list)
> - Governance workbook:   `uk_climate_nature_governance.xlsx` — sheet `Policies & Activities` (canonical name; stable across updates)
> - Indicators workbook:   `indicators_climate_nature.xlsx` (optional; omit to skip the indicators section; canonical name, stable across updates)
> - Flagship MO tool/URL:  `<e.g. https://www.metoffice.gov.uk/hadobs/biosecurity_uk_hist/>` (if any)
> - Output basename:       `<e.g. MO_microclimate_policy_relevance>`
>
> **Do not rewrite `render.py`.** It is a complete, working renderer (~600 lines, ~32 KB) with
> full `build_pdf` and `build_docx` implementations. Some assistants truncate large attachments
> silently, see only the first screenful, and report it as "a scaffold" with the rendering
> unimplemented. That is a reading artefact, not a fact about the file. If you believe it is
> incomplete, say so and stop rather than reconstructing it -- a rewritten renderer silently
> changes the layout and scoring presentation that make separate assessments comparable, which
> is the entire point of this kit. The human can confirm the file is intact in one command:
> `python3 PA_toolkit/code/verify_toolkit.py`.
>
> You are producing a "Met Office research -> UK policy relevance" assessment for the research field
> above. Follow `METHOD_AND_SCORING.md` exactly — same procedure, same two-axis scoring
> (Relevance 1–3 x Status Current/Opportunity), same document structure. Use `TEMPLATE_applied.yaml`
> only as the **format example**: produce a *new* YAML config with the same keys and this field's content.
>
> **Sources & web search.** The attached files are the primary inputs, but they are not complete.
> **If you have web access, search the internet to complement them** — do not rely on the files or your
> own memory alone. Use search to:
> - discover **policy activities, strategies, programmes and operational processes** relevant to the
>   field that are **not** in the governance workbook (add these as rows marked `†`);
> - confirm the **research->policy channel** (named partnerships, tools feeding a register/contingency
>   process, etc.) from primary sources (Met Office, Defra and its agencies, gov.uk), and date them;
> - **verify** every policy's current status, dates and URL against official sources
>   (gov.uk, legislation.gov.uk, agency portals), and inspect the flagship MO tool/URL directly.
> Prefer official/primary sources; record each source you use in the references.
> **If you do not have web access**, proceed from the attached files plus your own knowledge, render
> normally, and clearly flag every claim, date and URL you could not verify (list them at the end as
> "unverified — needs checking"), erring toward Status = Opportunity / lower confidence for anything
> not in the files.
>
> Steps ("the capability" = MO's existing research in applied mode, or the prospective product's
> outputs in gap mode):
> 1. Scope the capability for this field from `<Bibliography file>`; identify and characterise the
>    flagship tool/output (inspect `<Flagship MO tool/URL>` directly if given). In gap mode, the
>    bibliography is external evidence — define the prospective product's outputs instead (see the
>    gap-mode note below).
> 2. Establish the research→policy channel(s) per the "Sources & web search" note (in gap mode, this is
>    the evidence that the approach works elsewhere, plus MO/partner capability from MO/ESA pages).
> 3. From `<Governance workbook>` (`Policies & Activities`), assemble candidate policies: filter on the
>    relevant sector tags, then screen all records for a plausible dependency on the capability. Take
>    each policy's hyperlink from the `Link` column. Then add relevant activities found by search that
>    are absent from the workbook, marked `†`.
> 4. Score every candidate on both axes. Materiality → Relevance (row colour); the second axis →
>    Status (Current/Opportunity) in applied mode, or Maturity (Demonstrated/Emerging/Conceptual) in
>    gap mode. Set the axis in the config via `status_axis` (see the example files).
> 5. **If `<Indicators workbook>` is supplied, always run an indicator scan** (both modes): keyword-filter
>    it for the field, then keep only indicators whose *measured quantity* the capability could directly
>    inform (exclude indicators whose measured quantity takes no climate input, e.g. a GIS area). **Then
>    run a focused web scan** for authoritative indicators absent from the workbook (post-version
>    framework indicators, or operational/agency monitoring statistics not in any catalogued framework);
>    authoritative sources only, must genuinely not be in the workbook, must pass the same
>    measured-quantity test, mark `†` with source and note any overlap. Expect a small yield. List
>    ≤ ~6 in total with source framework and current policy application; populate `indicator_rows` plus
>    an `indicators_intro`, with `indicators` present in `section_order`. If no indicators workbook is
>    supplied, omit the section.
> 6. British English, metric units, no hedging. Where a link is inferred, mark it the lower second-axis
>    value (Opportunity / Conceptual) and say so.
>
> Output:
> - Write the completed config to `config_<field>.yaml` (same schema as the example; set
>   `meta.output_basename` = `<Output basename>`, `meta.title`, `meta.footer`, `labels`, `status_axis`,
>   key points, summary, policy_rows, indicator_rows, methods, gaps, references).
> - Run: `python render.py config_<field>.yaml --format both --outdir outputs_assessments`
> - Return the PDF and Word files.
> - **Append every `†` item to `Data/pending_additions.md`** — one row per daggered activity and per
>   daggered indicator, using that file's columns. **Append them; do not ask whether to.** This is a
>   required step, not an offer: it changes no workbook (the file is a candidate queue feeding the
>   quarterly policy scan, where each row is screened and approved before anything is written), and
>   capturing what you found must not depend on whether this particular user chooses to act on it.
>   If you cannot reach that file, emit the rows as a fenced copy-paste block clearly labelled for
>   pasting into `Data/pending_additions.md`. Do not let the finds evaporate.
> - Also list the `†` items in the chat reply so the user can see what was found, noting for each
>   whether the *measured quantity* takes a climate input, and any overlap with an existing record.
> - Also note in the chat: additional references/searches used, any candidates excluded and why,
>   confidence for the lower-maturity / Opportunity links, and any unverified items.
>
> Keep the methods block to the same five-step structure as the example so reports stay comparable.
>
> **If Mode = gap (prospective)**, adjust as follows (see `TEMPLATE_gap.yaml` and the
> "Two modes" section of `METHOD_AND_SCORING.md`):
> - Treat the bibliography as *external* evidence that the approach works elsewhere, not as MO's output.
>   Scope MO/partner capability from MO/ESA/agency pages instead.
> - In step 1, define the **prospective product** concretely (variables, resolution, cadence, coverage)
>   and what it adds beyond existing data.
> - Set the second axis to **Maturity** in the config:
>   `status_axis: {label: "Maturity", values: {Demonstrated: "0B5563", Emerging: "C9871B", Conceptual: "5A6B73"}}`
>   and score each row Demonstrated / Emerging / Conceptual (how proven the application is), not
>   Current / Opportunity.
> - Relabel `labels.summary` (e.g. "The evidence base for a prospective <X> product") and
>   `labels.references_primary` ("Evidence base (external literature)"); keep Relevance = materiality.

---

### Tips
- Authoring markup in any YAML text value: `**bold**`, `*italic*`, `[[label|https://url]]`.
- Two-policy row: use `parts:` with two `{label, url}` entries instead of `name`/`url`.
- Drop or reorder sections via `section_order` in the YAML — no code change.
- Restyle (colours/font) via the `theme` block — it drives both PDF and Word.
- The renderer needs no internet; only the **research step** above benefits from search.
- Mark activities absent from the governance workbook by setting their row `ref` to `†`.
