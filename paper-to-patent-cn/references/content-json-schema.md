# Content JSON Schema

Use this contract before calling `scripts/generate_final_patent_docx.py` or `scripts/audit_patent_content_json.py`.

## Required Fields

```json
{
  "title": "一种……方法",
  "abstract": ["说明书摘要正文"],
  "claims": [
    "一种……方法，其特征在于，包括：……。",
    "根据权利要求1所述的方法，其特征在于，……。"
  ],
  "description": {
    "technical_field": ["技术领域正文"],
    "background": ["背景技术正文"],
    "summary": ["发明内容中的技术问题和技术方案正文"],
    "benefits": ["发明内容中的有益效果正文"],
    "drawing_description": ["图1为……示意图。"],
    "embodiments": ["具体实施方式正文"]
  },
  "drawing_assets": [
    {"caption": "图1"},
    {"caption": "图2"}
  ],
  "gaps": []
}
```

`title`, `abstract`, `claims`, and `description` are required for a clean final document. The generator accepts strings or lists for paragraph fields, but lists are preferred because they preserve paragraph boundaries.

## Description Keys

- `technical_field` maps to `技术领域`.
- `background` maps to `背景技术`.
- `summary` maps to the main technical problem and technical solution under `发明内容`.
- `benefits` is appended under `发明内容` after `summary`; use it for source-supported technical effects.
- `drawing_description` maps to `附图说明`.
- `embodiments` maps to `具体实施方式`.

Do not use `invention_content` as the primary key unless a compatibility adapter converts it to `summary`; the final generator expects `summary`.

## Cover Fields

Optional `cover_fields` may override the default patent information page:

```json
{
  "cover_fields": {
    "专利名称": "一种……方法",
    "校内识别号": "Z",
    "专利类型": "国内专利",
    "专利类别": "发明专利",
    "申请人": "",
    "发明人": "",
    "第一发明人身份证号": "",
    "申报人": "",
    "申报人电话": "",
    "申报人邮箱": "",
    "联系人": "",
    "联系人电话": "",
    "联系人邮箱": ""
  }
}
```

If `cover_fields` is absent, the generator inserts these fields with defaults and blank personal-contact values.

## Drawing Fields

The current final Word format does not embed images. `drawing_assets` is used only to insert captions:

```json
[
  {"caption": "图1"},
  {"caption": "图2"}
]
```

Paths such as `png_path` and `svg_path` may be kept for separate optional drawing assets, but the default DOCX generator must not insert them. This avoids blank pages, oversized image placeholders, and accidental media in the Word package.

## Gap and Traceability Fields

Use these optional fields for review and reporting:

```json
{
  "source_fact_matrix": [
    {
      "patent_location": "权利要求1",
      "feature": "……",
      "source_basis": "论文第4页图2及方法部分",
      "status": "directly_disclosed"
    }
  ],
  "gaps": [
    "论文未提供……"
  ],
  "style_notes": [
    "已按示例 Word 格式生成；附图页仅保留图题。"
  ]
}
```

`source_fact_matrix` should be kept in the JSON or as a companion Markdown file. `gaps` must list every unresolved material gap if any placeholder remains in intermediate text.

## Required Preflight

Run:

```powershell
python scripts/audit_patent_content_json.py patent_content.json
```

Fix failures before DOCX generation. Warnings may remain only if they are also explained in the validation report.



