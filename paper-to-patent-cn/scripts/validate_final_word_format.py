#!/usr/bin/env python3
# Copyright (c) 2026 LYJ. All rights reserved.
"""Validate final-format Chinese patent DOCX files against the skill rules."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W = NS["w"]

MAIN_HEADINGS = {
    "说   明   书   摘   要",
    "摘    要   附   图",
    "权  利  要  求  书",
    "说   明   书",
    "说 明 书 附 图",
}

SUBHEADINGS = {"技术领域", "背景技术", "发明内容", "附图说明", "具体实施方式"}
BAD_TOKENS = ["待补充", "TODO", "[0001]", "[0002]", "0001", "0002", "銆", "绛", "鍥"]
COVER_PREFIXES = [
    "专利名称：",
    "校内识别号：",
    "专利类型：",
    "专利类别：",
    "申请人：",
    "发明人：",
    "第一发明人身份证号：",
    "申报人：",
    "申报人电话：",
    "申报人邮箱：",
    "联系人：",
    "联系人电话：",
    "联系人邮箱：",
]


def w_attr(el: ET.Element | None, name: str) -> str:
    return "" if el is None else el.get(f"{{{W}}}{name}", "")


def paragraph_info(p: ET.Element) -> dict:
    text = "".join(t.text or "" for t in p.findall(".//w:t", NS)).strip()
    ppr = p.find("w:pPr", NS)
    jc = w_attr(ppr.find("w:jc", NS) if ppr is not None else None, "val")
    spacing = ppr.find("w:spacing", NS) if ppr is not None else None
    indent = ppr.find("w:ind", NS) if ppr is not None else None
    border = p.find(".//w:pBdr/w:bottom", NS) is not None
    page_break_before = p.find(".//w:pageBreakBefore", NS) is not None
    sizes: list[str] = []
    bold = False
    for run in p.findall("w:r", NS):
        rpr = run.find("w:rPr", NS)
        if rpr is None:
            continue
        size = rpr.find("w:sz", NS)
        if size is not None:
            sizes.append(w_attr(size, "val"))
        if rpr.find("w:b", NS) is not None:
            bold = True
    return {
        "text": text,
        "jc": jc,
        "line": w_attr(spacing, "line"),
        "first_line": w_attr(indent, "firstLine"),
        "border": border,
        "page_break_before": page_break_before,
        "sizes": sizes,
        "bold": bold,
    }


def all_12pt(info: dict) -> bool:
    return bool(info["sizes"]) and all(size == "24" for size in info["sizes"])


def validate(path: Path) -> list[str]:
    failures: list[str] = []
    with ZipFile(path) as package:
        root = ET.fromstring(package.read("word/document.xml"))
        media = [name for name in package.namelist() if name.startswith("word/media/")]
    infos = [paragraph_info(p) for p in root.findall(".//w:p", NS)]
    infos = [info for info in infos if info["text"]]
    text = "\n".join(info["text"] for info in infos)

    for token in BAD_TOKENS:
        if token in text:
            failures.append(f"bad token remains: {token}")

    texts = [info["text"] for info in infos]
    try:
        abstract_index = texts.index("说   明   书   摘   要")
    except ValueError:
        abstract_index = -1
    if abstract_index <= 0:
        failures.append("patent information page missing before abstract heading")
    else:
        cover_infos = infos[:abstract_index]
        cover_text = "\n".join(info["text"] for info in cover_infos)
        for prefix in COVER_PREFIXES:
            if prefix not in cover_text:
                failures.append(f"cover field missing: {prefix}")
        for info in cover_infos:
            if info["border"]:
                failures.append(f"cover line has paragraph border: {info['text'][:30]}")
            if info["page_break_before"]:
                failures.append(f"cover line should not have page-break-before: {info['text'][:30]}")
            if not all_12pt(info):
                failures.append(f"cover line not 12 pt: {info['text'][:30]}")

    seen_main = {info["text"] for info in infos if info["text"] in MAIN_HEADINGS}
    for heading in MAIN_HEADINGS - seen_main:
        failures.append(f"missing main heading: {heading}")

    for info in infos:
        current = info["text"]
        if current in MAIN_HEADINGS:
            if info["jc"] != "center":
                failures.append(f"main heading not centered: {current}")
            if not info["border"]:
                failures.append(f"main heading missing bottom border: {current}")
            if not info["page_break_before"]:
                failures.append(f"main heading missing page-break-before: {current}")
            if info["bold"]:
                failures.append(f"main heading should not be bold: {current}")
            if info["line"] != "440":
                failures.append(f"main heading line spacing is not 22 pt: {current}")
            if not all_12pt(info):
                failures.append(f"main heading not 12 pt: {current}")
        elif current in SUBHEADINGS:
            if info["jc"] not in {"left", ""}:
                failures.append(f"subheading not left aligned: {current}")
            if info["border"]:
                failures.append(f"subheading inherited bottom border: {current}")
            if info["page_break_before"]:
                failures.append(f"subheading should not have page-break-before: {current}")
            if not info["bold"]:
                failures.append(f"subheading not bold: {current}")
            if info["line"] != "440":
                failures.append(f"subheading line spacing is not 22 pt: {current}")
            if not all_12pt(info):
                failures.append(f"subheading not 12 pt: {current}")
        elif re.match(r"^\d+\.\s*(一种|根据)", current):
            if info["border"]:
                failures.append(f"claim inherited bottom border: {current[:30]}")
            if not all_12pt(info):
                failures.append(f"claim not 12 pt: {current[:30]}")

    title_candidates = [
        info for info in infos
        if info["text"] not in MAIN_HEADINGS
        and info["text"] not in SUBHEADINGS
        and "一种" in info["text"]
        and info["text"].endswith(("方法", "装置", "系统", "材料", "结构"))
        and info["jc"] == "center"
    ]
    if not title_candidates:
        failures.append("could not identify centered invention title")
    else:
        title = title_candidates[0]
        if title["border"]:
            failures.append("invention title inherited bottom border")
        if not title["bold"]:
            failures.append("invention title not bold")
        if not all_12pt(title):
            failures.append("invention title not 12 pt")

    body_checked = 0
    for info in infos:
        current = info["text"]
        if current in MAIN_HEADINGS or current in SUBHEADINGS:
            continue
        if any(current.startswith(prefix) for prefix in COVER_PREFIXES):
            continue
        if re.match(r"^\d+\.\s*(一种|根据)", current) or current.startswith("图"):
            continue
        if info["jc"] == "center":
            continue
        body_checked += 1
        if info["border"]:
            failures.append(f"body paragraph inherited bottom border: {current[:30]}")
        if info["line"] != "440":
            failures.append(f"body paragraph line spacing is not 22 pt: {current[:30]}")
        if info["first_line"] not in {"420", "419"}:
            failures.append(f"body paragraph missing first-line indent: {current[:30]}")
        if not all_12pt(info):
            failures.append(f"body paragraph not 12 pt: {current[:30]}")
        if body_checked >= 12:
            break

    if media:
        failures.append(f"embedded drawing media should be omitted by default: {len(media)} file(s)")

    return failures


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_final_word_format.py <patent.docx>")
    failures = validate(Path(sys.argv[1]))
    if failures:
        print("FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("OK: final Word patent format validated")


if __name__ == "__main__":
    main()



