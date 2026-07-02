# Final Word Format

This format reflects the final example-aligned Chinese patent application style used in the completed workflow.

## Section Order

Use this order in the generated DOCX:

1. Patent information page
2. `说   明   书   摘   要`
3. Abstract body
4. `摘    要   附   图`
5. Abstract drawing caption
6. `权  利  要  求  书`
7. Claims
8. `说   明   书`
9. Invention title
10. `技术领域`
11. `背景技术`
12. `发明内容`
13. `附图说明`
14. `具体实施方式`
15. `说 明 书 附 图`
16. Patent drawing captions

## Patent Information Page

Place a patent information page before `说   明   书   摘   要`.

Formatting:

- Songti Chinese font.
- 12 pt.
- Left aligned.
- No paragraph border.
- No first-line indent.
- The following `说   明   书   摘   要` heading must start on the next page.

Required fields:

- `专利名称：...`
- `校内识别号：Z`
- `专利类型：国内专利`
- `专利类别：发明专利`
- `申请人：`
- `发明人：`
- `第一发明人身份证号：`
- `申报人：`
- `申报人电话：`
- `申报人邮箱：`
- `联系人：`
- `联系人电话：`
- `联系人邮箱：`

## Main Section Headings

Main headings are:

- `说   明   书   摘   要`
- `摘    要   附   图`
- `权  利  要  求  书`
- `说   明   书`
- `说 明 书 附 图`

Formatting:

- Center aligned.
- Songti Chinese font, Times New Roman ASCII font.
- 12 pt.
- Not bold by default.
- Single bottom paragraph border across the text line.
- Fixed line spacing about 22 pt.
- Add modest spacing after the heading.
- These are the only paragraphs that should carry the bottom border.
- `说   明   书   摘   要` must have page-break-before behavior because the patent information page precedes it.
- `摘    要   附   图`, `权  利  要  求  书`, `说   明   书`, and `说 明 书 附 图` must have page-break-before behavior.
- Implement pagination as page-break-before on the heading paragraph when possible; do not insert the page break between a heading and its content.

## Invention Title

Formatting:

- Center aligned.
- Bold.
- 12 pt.
- Songti Chinese font.
- Use the exact invention name without an extra heading label.
- Must not have any paragraph border.

## Specification Subheadings

Subheadings are:

- `技术领域`
- `背景技术`
- `发明内容`
- `附图说明`
- `具体实施方式`

Formatting:

- Left aligned.
- Bold.
- 12 pt.
- Songti Chinese font.
- Fixed line spacing about 22 pt.
- Must not have any paragraph border.
- Must not have page-break-before behavior.

## Body Paragraphs

Formatting:

- 12 pt.
- Songti Chinese font and Times New Roman ASCII font.
- First-line indent about two Chinese characters.
- Fixed line spacing about 22 pt.
- Justified alignment is acceptable for body text.
- Do not use `[0001]`, `0001`, or CNIPA publication paragraph numbering unless explicitly requested.
- Strip residual paragraph numbers such as `0001`, `0002`, `[0001]`, `[0002]` before placing formal text in the final Word document.
- Do not use `一、二、三` numbering for the final Word section headings.

## Claims

Formatting:

- 12 pt body style.
- Claims are numbered `1.` through `N.`.
- Use hanging/first-line style only if it does not damage readability.
- Each claim is a complete sentence or semicolon-separated claim sentence ending with a Chinese full stop.

## Drawings

Formatting:

- Do not insert drawing images or reserve image placeholders by default.
- In `摘    要   附   图`, insert only the selected abstract drawing caption, normally `图1`.
- In `说 明 书 附 图`, insert only drawing captions such as `图1`, `图2`, `图3`.
- Users will insert the actual drawings manually.
- In structured JSON, `drawing_assets` should provide captions for this final Word layout. Image paths may be retained for separate assets, but the default DOCX must not package files under `word/media/`.

## DOCX XML Checks

When verifying the generated Word file:

- Main heading paragraphs should contain a bottom border element: `w:pBdr/w:bottom`.
- Only main heading paragraphs should contain the bottom border; the invention title, subheadings, claims, body paragraphs, and drawing captions should not inherit this border.
- The patent information page should appear before `说   明   书   摘   要`.
- All five main headings should contain page-break-before behavior, for example `w:pageBreakBefore` in DOCX XML.
- Specification subheadings should not contain `w:pageBreakBefore`.
- The generated DOCX should not contain embedded drawing media by default.
- Main heading, title, subheading, claim, and body run sizes should be 12 pt (`w:sz="24"`).
- Main heading paragraphs should be centered and not bold.
- Invention title should be centered, bold, and unbordered.
- Subheadings should be left aligned, bold, and unbordered.
- Body paragraphs should have first-line indentation and about 22 pt line spacing (`w:spacing w:line="440"`).
- Extracted text should preserve the exact heading strings above.

## Generation Sequence

When generating from JSON:

1. Run `scripts/audit_patent_content_json.py <patent_content.json>` and fix failures.
2. Generate DOCX with `scripts/generate_final_patent_docx.py`.
3. Run `scripts/validate_final_word_format.py <patent.docx>`.
4. Export PDF if requested and tooling is available.
5. Record content-audit, format-validation, and PDF status in the validation report.

## Word COM Warning

Microsoft Word can inherit paragraph borders from the previous paragraph. When creating a DOCX through Word COM or any stateful Word automation API, always clear top, left, bottom, and right paragraph borders before optionally applying the bottom border to a main heading. This avoids accidental horizontal lines under the invention title or subheadings.



