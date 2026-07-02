# Patent Content Rules

## Source Fidelity

The patent must be traceable to the source paper or user-provided facts.

Allowed:

- Rewriting disclosed technical content in patent language.
- Generalizing disclosed embodiments when the generalization is technically supported.
- Converting research figures into patent-style schematics.
- Stating technical effects that are demonstrated or logically implied by disclosed mechanisms.

Not allowed without user confirmation:

- New components, materials, algorithms, fabrication steps, voltages, dimensions, thresholds, or ranges.
- New experiments, benchmark results, application scenarios, or comparison data.
- Legal claims of superiority that are not grounded in source evidence.
- Hidden assumptions inserted into the formal claims or specification.

Before drafting, build a compact source fact matrix. It should record:

- Claim feature or specification statement.
- Source basis: page, section, figure/table number, caption, pasted text, or user-provided note.
- Patent location where the fact is used.
- Fidelity status: directly disclosed, technically supported generalization, or missing/needs confirmation.

If a feature cannot be traced to source material, either remove it from the formal application or move it to the gap report.

## Gap Handling

If important information is missing, create a separate gap report with:

- Missing item.
- Why it matters for patent support.
- Whether it affects claims, embodiments, drawings, or enablement.
- Suggested source or experiment needed.

Do not leave `待补充` or bracketed drafting notes inside the formal application.

In direct generation, placeholders may be used only in intermediate content files. The final DOCX should be clean unless the user explicitly asks to keep material-gap placeholders visible.

## Claim Drafting

The claims define the protection scope. Every claim feature must be supported by the specification.

Recommended structure:

- Claim 1: broad independent claim for the core structure, method, device, system, or material.
- Claims 2-6: dependent claims for structural details, parameter ranges, control rules, preparation steps, or algorithmic operations.
- Claims 7-10: dependent claims for embodiments, optimization, application scenarios, or testing configuration.
- Optional second independent claim: method, system, device, or use claim when the paper discloses a second statutory category clearly.

Quality checks:

- Claim dependencies are valid.
- Claims do not depend on later claims.
- Claim 1 is broad but enabled.
- Dependent claims narrow the scope rather than repeating Claim 1.
- Relative terms are anchored to structural or operational features.
- Each claim ends with exactly one Chinese full stop.
- Use semicolons or commas inside claims instead of multiple sentence-ending periods.
- Do not use uncertain words in claims: `等`, `大约`, `可能`, `也许`, `例如`, `比如`, `优选`, `可以`, `不限于`, `某些`, `若干`, `某种程度上`, `基本`.
- A dependent claim must cite an earlier claim that actually contains the referenced feature.
- Multi-dependent claims should not depend on another multi-dependent claim unless the user specifically requires that drafting style.

## Specification Drafting

Use a patent register: precise, concrete, and implementation-oriented.

Technical field:

- One short paragraph identifying the technical domain.

Background:

- Describe existing technology and objective limitations.
- Avoid attacking prior art emotionally.
- If similar patents or example patents are available, use their style to frame the problem, but do not copy text.

Summary:

- State the technical problem.
- State the technical solution in claim-consistent language.
- State beneficial effects tied to mechanism and disclosed evidence.

Drawing description:

- One sentence per drawing.
- Keep descriptions factual and short.

Embodiments:

- Explain each core claim feature in enough detail to support implementation.
- Use source parameters and source performance results.
- Use `在一种实施方式中` and `参照图X` patterns where appropriate.
- Keep alternative embodiments separate from required features.
- For each important step or module, state what it is, what problem it addresses, how it operates, and what output or technical effect it produces.
- Ensure every independent-claim feature appears in `具体实施方式`; dependent-claim details should also have embodiment support.
- Keep terms consistent across abstract, claims, specification, drawing descriptions, and drawing captions.

## Drawing Rules

Patent drawings should clarify the technical solution rather than reproduce publication-style figures blindly.

Use:

- Device/system block diagrams.
- Structural schematics.
- Flowcharts.
- Equivalent circuit or module diagrams.
- Performance curves only when they support technical effect and are readable in black and white.

Avoid:

- Dense color heatmaps as the only figure.
- Decorative backgrounds.
- Publication panel labels that do not help patent interpretation.
- Cropped figures with unreadable labels.

Current final Word policy:

- Do not embed drawing images or blank placeholders by default.
- Use only captions such as `图1` in `摘要附图` and `图1`、`图2` in `说明书附图`.
- Keep any generated SVG/PNG drawings as separate optional assets for manual insertion.
- Captions and drawing descriptions must correspond to source-supported steps, modules, or structures; do not introduce generic flowchart nodes.

When optional drawing assets are generated, they must be source-faithful black-and-white line drawings with no internal figure numbers, titles, watermarks, decorative effects, unrelated modules, or excessive blank margins.

## Content Audit

Before creating the final DOCX:

- Check the invention name is identical across abstract, claims, specification, cover page, and file names.
- Check the difference point, technical problem, technical solution, and technical effect form a coherent chain.
- Check each claim feature is supported by the specification and by the source fact matrix.
- Check experimental conclusions are not overstated as universal effects.
- Check background problems are present in, or logically tied to, the source paper.
- Check drawing descriptions match the claim steps/modules and do not add unsupported elements.
- Run `scripts/audit_patent_content_json.py <patent_content.json>` when structured JSON exists.

## Delivery Report

The final response should summarize:

- Output DOCX/PDF paths.
- Source files used.
- Number of claims.
- Drawing captions included and optional drawing assets generated, if any.
- Known gaps or assumptions.
- Validation performed and any failures.



