# paper-to-patent-cn

`paper-to-patent-cn` is a Codex skill for converting academic papers, PDFs, abstracts, and method notes into source-faithful Chinese invention patent application drafts.

It is designed for a specific final Word format established through local example alignment:

- patent information page;
- `说   明   书   摘   要`;
- `摘    要   附   图`;
- `权  利  要  求  书`;
- `说   明   书`;
- `说 明 书 附 图`;
- no embedded drawing images by default, only figure captions;
- content JSON audit before DOCX generation;
- DOCX XML validation after generation.

## Why This Exists

Turning a paper into a patent draft is not a translation task. A patent draft must identify the technical problem, technical solution, and technical effect, then express them as claims and a supporting specification without inventing undisclosed technical content.

This skill encodes a repeatable workflow for that conversion. It is intentionally conservative: missing paper details are recorded as material gaps instead of being fabricated.

## What It Does

- Extracts patentable technical facts from papers or structured notes.
- Builds a claim/specification logic chain.
- Produces a structured patent-content JSON file.
- Generates final-format DOCX and optional review PDF.
- Inserts figure captions only in drawing sections, leaving actual drawings for manual insertion.
- Validates the content JSON and generated DOCX.
- Reports unresolved material gaps.

## What It Does Not Do

- It does not provide legal advice or guarantee patentability, novelty, inventiveness, or grant.
- It does not invent missing structures, dimensions, circuit parameters, fabrication steps, datasets, or effects.
- It does not embed generated drawings in the final Word document by default.
- It does not store user papers or generated drafts inside the skill directory.

## Repository Layout

```text
paper-to-patent-cn-repo/
├── README.md
├── LICENSE
├── SECURITY.md
├── requirements.txt
├── .gitignore
└── paper-to-patent-cn/
    ├── SKILL.md
    ├── agents/
    ├── references/
    └── scripts/
```

The `paper-to-patent-cn/` directory is the Codex skill. The files at repository root are GitHub-facing project metadata.

## Installation

Copy the skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\paper-to-patent-cn "$env:USERPROFILE\.codex\skills\paper-to-patent-cn"
```

Install helper-script dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Basic Use

In Codex:

```text
Use $paper-to-patent-cn to convert this paper into a Chinese invention patent application DOCX/PDF.
```

For a structured JSON workflow:

```powershell
python .\paper-to-patent-cn\scripts\audit_patent_content_json.py .\patent_content.json
python .\paper-to-patent-cn\scripts\generate_final_patent_docx.py .\patent_content.json --output-dir .\outputs --pdf
python .\paper-to-patent-cn\scripts\validate_final_word_format.py .\outputs\patent_application.docx
```

## Content Contract

The generator expects a JSON object with:

- `title`;
- `abstract`;
- `claims`;
- `description.technical_field`;
- `description.background`;
- `description.summary`;
- `description.benefits`;
- `description.drawing_description`;
- `description.embodiments`;
- `drawing_assets` with captions such as `图1`, `图2`;
- optional `gaps` and `source_fact_matrix`.

See `paper-to-patent-cn/references/content-json-schema.md`.

## Quality Rules

The skill follows these hard rules:

- Preserve one invention name across abstract, claims, specification, and cover page.
- Claims must cite previous claims only.
- Claim wording should avoid uncertain terms such as `大约`, `可能`, `优选`, `可以`, `比如`, `不限于`, and unsupported generic `等`.
- Every technical feature should be traceable to the paper, user-provided notes, or the source fact matrix.
- Any unsupported but useful content belongs in `gaps`, not in the formal application body.
- The generated DOCX must contain no embedded image media unless the workflow is intentionally changed.

## Privacy and Disclosure Warning

Patent drafts often contain unpublished technical disclosure. Before committing or sharing, check that you are not publishing:

- original papers that are not meant to be public;
- unpublished invention disclosures;
- generated patent drafts containing confidential claims;
- PDFs, DOCX files, figures, screenshots, or extracted text;
- personal names, phone numbers, email addresses, ID numbers, local paths, API keys, tokens, or institution-specific templates.

Use the included `.gitignore` as a baseline, but review every commit manually.

## Dependencies

- `python-docx`: DOCX generation.
- `Pillow`: optional image-based PDF review copy.
- `pypdf`: optional PDF text extraction in external workflows.

Dependency licenses are not relicensed by this project. Review each dependency before redistribution in packaged software.

## Copyright and License

Copyright (c) 2026 LYJ. All rights reserved.

This repository is source-available for non-commercial personal, academic and research use only. Commercial use, paid services, redistribution in commercial products, and model-training or dataset use require prior written permission from LYJ. See `LICENSE`.

