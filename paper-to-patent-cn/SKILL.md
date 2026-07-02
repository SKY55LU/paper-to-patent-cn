---
name: paper-to-patent-cn
description: Generate Chinese invention patent applications directly from academic papers, PDFs, abstracts, or method notes, using the final CN patent structure and Word formatting established in this workflow. Use when Codex must produce source-faithful Chinese patent text, claims, specification sections, black-and-white patent drawings, DOCX/PDF deliverables, or match example Word patent formatting without an intermediate iterative draft.
---

# Paper to Chinese Patent

Use this skill to generate a Chinese invention patent application directly in the final patent structure and Word format. This is not an iterative "paper -> rough patent -> learn examples -> revise" workflow. Treat the mature example-aligned structure as the default output form from the beginning.

## Required Behavior

1. Work from disclosed source material only: paper PDF, manuscript text, abstract, figures, captions, method notes, experiment logs, or user-provided technical facts.
2. Do not invent undisclosed structures, parameter ranges, circuit details, process windows, performance numbers, or legal advantages.
3. Put missing but useful information in a separate gap report, not in the formal application body, unless the user explicitly authorizes assumptions.
4. Default to Simplified Chinese and Chinese invention patent style.
5. Generate deliverables in the final application structure: DOCX primary, PDF review copy when tooling is available, source JSON/content notes, drawing assets, and a short validation report.
6. Do not store user-provided papers, unpublished disclosures, generated patent drafts, API keys, tokens, local machine paths, or personal contact details inside the skill directory or any public release package.

## Direct Workflow

1. Identify inputs and output directory.
   - Source paper or notes.
   - Optional example Word/PDF only for format matching.
   - Optional original figures or generated line drawings.

2. Extract source facts.
   - Invention name candidate.
   - Technical field.
   - Prior-art problem from the paper introduction.
   - Core technical solution: structure, method, algorithm, control flow, material, device, or system.
   - Key parameters and ranges explicitly disclosed by the source.
   - Verified effects, simulations, experiments, and comparison baselines.
   - Figure content and captions.
   - Source anchors: page, section, figure/table number, or pasted-text location for each important technical fact when available.

3. Build the patent logic chain before drafting.
   - Distinguishing technical feature.
   - Technical problem solved.
   - Technical means.
   - Technical effect.
   - Embodiment support for every claim feature.
   - A source fact matrix mapping claim features, specification paragraphs, effects, and drawing captions back to the paper or user-provided material.

4. Draft the final document directly with this section order:
   - patent information page
   - `说   明   书   摘   要`
   - `摘    要   附   图`
   - `权  利  要  求  书`
   - `说   明   书`
   - invention title
   - `技术领域`
   - `背景技术`
   - `发明内容`
   - `附图说明`
   - `具体实施方式`
   - `说 明 书 附 图`

5. Write claims first enough to constrain the specification.
   - Normally draft 8-12 claims unless the technology is very narrow or the user requests otherwise.
   - Claim 1 should protect the broadest disclosed inventive concept.
   - Use dependent claims for implementation details, structural variants, parameter ranges, control logic, preparation steps, or use scenarios disclosed in the source.
   - Every dependent claim must cite a previous claim clearly.
   - Avoid vague terms such as "高效", "显著", "优异" unless tied to source-supported technical features.
   - Avoid uncertain claim words such as "大约", "可能", "例如", "比如", "优选", "可以", "不限于", "若干", and "基本".
   - Every claim must end with one Chinese full stop and should use commas or semicolons internally.

6. Write the specification to support the claims.
   - Background: describe similar prior-art limitations objectively.
   - Summary: state technical problem, technical solution, and beneficial effects.
   - Drawing description: one short sentence per drawing.
   - Embodiments: explain how claim features are implemented, with `参照图X` style where drawings exist.
   - Experimental/simulation results: include only source-supported values and conditions.

7. Prepare patent drawings.
   - Prefer black-and-white line drawings.
   - Do not put internal figure numbers or titles inside the drawing image if captions are handled in the document.
   - Keep drawings readable in grayscale.
   - Create schematic drawings when the paper figures are not suitable for patent drawings, while preserving source fidelity.
   - In the final Word document, do not embed drawing images by default; use captions only. Store optional drawing assets separately when they are useful for later manual insertion.

8. Apply the final Word format.
   - Use `references/final-word-format.md`.
   - If a user provides a new example Word file, inspect its DOCX XML before overriding the defaults.
   - Do not use publication-style paragraph numbers such as `[0001]` unless the user explicitly asks for them.
   - Treat formatting as a hard deliverable, not cosmetic cleanup.
   - Main headings, invention title, subheadings, body paragraphs, and claims must match the final Word draft format before delivery.
   - Add a patent information page before `说   明   书   摘   要`, using Songti 12 pt. Include at least: `专利名称：...`、`校内识别号：Z`、`专利类型：国内专利`、`专利类别：发明专利`、`申请人：`、`发明人：`、`第一发明人身份证号：`、`申报人：`、`申报人电话：`、`申报人邮箱：`、`联系人：`、`联系人电话：`、`联系人邮箱：`.
   - Because the patent information page precedes the abstract, insert a page break between the information page and `说   明   书   摘   要`; implement this as page-break-before on the `说   明   书   摘   要` heading paragraph.
   - Add page-break-before behavior to the remaining four main patent headings: `摘    要   附   图`、`权  利  要  求  书`、`说   明   书`、`说 明 书 附 图`. Do not place a page break between a heading and its own content.
   - Do not add page breaks before specification subheadings: `技术领域`、`背景技术`、`发明内容`、`附图说明`、`具体实施方式`.
   - Do not insert drawing images or blank image placeholders in `摘    要   附   图` or `说 明 书 附 图`. Only insert figure captions such as `图1`、`图2`; users will insert drawings manually.
   - When generating with Word COM or any stateful Word API, clear paragraph borders on every new paragraph before adding the bottom border to main headings. Word can otherwise inherit heading borders onto the invention title or subheadings.
   - Strip residual paragraph numbers such as `0001`, `0002`, `[0001]`, or `[0002]` from formal body text unless the user explicitly requests publication numbering.

9. Validate before delivery.
   - Run `scripts/audit_patent_content_json.py <patent_content.json>` before DOCX generation when structured JSON is available.
   - Extract DOCX text and check section order.
   - Check no `待补充`, mojibake, placeholder brackets, or internal drafting notes remain in the formal body.
   - Check claims are numbered and dependencies are valid.
   - Check the patent information page appears before `说   明   书   摘   要`, contains the required fields, and uses 12 pt Songti.
   - Check main headings have centered spaced text, 12 pt Songti, and a bottom border.
   - Check all five main headings have page-break-before behavior.
   - Check specification subheadings do not have page-break-before behavior.
   - Check the generated DOCX contains no embedded drawing media unless the user explicitly requests image insertion.
   - Check the invention title is 12 pt, centered, bold, and has no bottom border.
   - Check `技术领域`、`背景技术`、`发明内容`、`附图说明`、`具体实施方式` are 12 pt, left aligned, bold, and have no bottom border.
   - Check body paragraphs are 12 pt, first-line indented, and use about 22 pt line spacing.
   - Run `scripts/validate_final_word_format.py <docx>` when a DOCX is generated. If it reports failures, correct the DOCX and rerun validation before delivery.
   - Check PDF exists and is readable if PDF output is requested.
   - Keep a short validation report recording content audit status, DOCX format validation status, PDF conversion status, and any remaining material gaps.

## References

Read these before drafting or formatting:

- `references/patent-content-rules.md` for source fidelity, claim drafting, specification content, and gap handling.
- `references/final-word-format.md` for the final Word section structure and typography.
- `references/content-json-schema.md` for the structured JSON contract used by the generator and content audit.

## Optional Helper Script

The script `scripts/generate_final_patent_docx.py` converts a structured patent JSON file into a final-format DOCX and optional image-based PDF review copy. Prefer using it when the content has already been organized into JSON. Patch it rather than retyping large document-generation code.

The script `scripts/audit_patent_content_json.py` checks the structured patent JSON for required sections, claim dependencies, uncertain claim wording, bad tokens, drawing-caption consistency, and unresolved material gaps. Run it before DOCX generation when possible.

The script `scripts/validate_final_word_format.py` checks the generated DOCX XML for the final draft-format requirements. Use it after DOCX generation and before PDF export when possible; otherwise use the same XML checks manually.



