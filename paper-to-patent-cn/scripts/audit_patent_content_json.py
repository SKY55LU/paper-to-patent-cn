#!/usr/bin/env python3
# Copyright (c) 2026 LYJ. All rights reserved.
"""Audit structured Chinese patent content before final DOCX generation."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable, Mapping, Sequence

REQUIRED_DESCRIPTION_KEYS = [
    "technical_field",
    "background",
    "summary",
    "drawing_description",
    "embodiments",
]

BAD_TOKENS = [
    "TODO",
    "待完善",
    "待确认",
    "[0001]",
    "[0002]",
    "0001",
    "0002",
    "銆",
    "绛",
    "鍥",
]

UNCERTAIN_CLAIM_WORDS = [
    "大约",
    "可能",
    "也许",
    "例如",
    "比如",
    "优选",
    "可以",
    "不限于",
    "某些",
    "若干",
    "某种程度上",
    "基本",
]

UNCERTAIN_CLAIM_PATTERNS = [
    (re.compile(r"(?<!等)等(?=[、，；。\s])"), "等"),
]


def as_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [part.strip() for part in re.split(r"\n+", value) if part.strip()]
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return [str(part).strip() for part in value if str(part).strip()]
    return [str(value).strip()]


def walk_text(value: object) -> Iterable[str]:
    if value is None:
        return
    if isinstance(value, str):
        yield value
        return
    if isinstance(value, Mapping):
        for child in value.values():
            yield from walk_text(child)
        return
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        for child in value:
            yield from walk_text(child)
        return
    yield str(value)


def normalize_claim(claim: str) -> str:
    claim = claim.strip()
    claim = re.sub(r"^\s*\d+[\.、]\s*", "", claim)
    return claim


def audit(data: Mapping[str, object]) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []

    title = str(data.get("title") or data.get("invention_name") or "").strip()
    if not title:
        failures.append("missing title/invention_name")

    abstract = as_list(data.get("abstract"))
    if not abstract:
        failures.append("missing abstract")

    claims = [normalize_claim(claim) for claim in as_list(data.get("claims"))]
    if not claims:
        failures.append("missing claims")
    elif len(claims) < 6 or len(claims) > 12:
        warnings.append(f"claim count is outside the normal 6-12 range: {len(claims)}")

    if claims and claims[0].startswith("根据权利要求"):
        failures.append("claim 1 must be an independent claim")

    for index, claim in enumerate(claims, 1):
        if not claim.endswith("。"):
            failures.append(f"claim {index} does not end with a Chinese full stop")
        if claim.count("。") > 1:
            failures.append(f"claim {index} contains more than one Chinese full stop")
        for word in UNCERTAIN_CLAIM_WORDS:
            if word in claim:
                failures.append(f"claim {index} contains uncertain wording: {word}")
        for pattern, label in UNCERTAIN_CLAIM_PATTERNS:
            if pattern.search(claim):
                failures.append(f"claim {index} contains uncertain wording: {label}")
        for ref in re.findall(r"权利要求\s*(\d+)", claim):
            ref_num = int(ref)
            if ref_num >= index:
                failures.append(f"claim {index} depends on non-previous claim {ref_num}")

    description = data.get("description")
    if not isinstance(description, Mapping):
        failures.append("description must be an object")
        description = {}
    for key in REQUIRED_DESCRIPTION_KEYS:
        if not as_list(description.get(key)):
            failures.append(f"missing description.{key}")

    drawing_descriptions = as_list(description.get("drawing_description"))
    drawing_assets = data.get("drawing_assets") or data.get("drawings") or []
    drawing_captions: list[str] = []
    if isinstance(drawing_assets, Sequence) and not isinstance(drawing_assets, (str, bytes, bytearray)):
        for item in drawing_assets:
            if isinstance(item, Mapping):
                caption = str(item.get("caption") or item.get("title") or "").strip()
            else:
                caption = str(item).strip()
            if caption:
                drawing_captions.append(caption)
    if drawing_descriptions and not drawing_captions:
        warnings.append("drawing descriptions exist but no drawing captions/assets were provided")

    text_blob = "\n".join(walk_text(data))
    for token in BAD_TOKENS:
        if token in text_blob:
            failures.append(f"bad token remains in content JSON: {token}")
    if "【待补充" in text_blob:
        warnings.append("content JSON contains explicit material gaps; list them in the gap report")

    gaps = as_list(data.get("gaps"))
    if "【待补充" in text_blob and not gaps:
        failures.append("placeholders exist but gaps list is missing")

    return failures, warnings


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: audit_patent_content_json.py <patent_content.json>")
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, Mapping):
        raise SystemExit("Patent content JSON must be an object.")
    failures, warnings = audit(data)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if failures:
        print("FAILED")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("OK: patent content JSON audit passed")


if __name__ == "__main__":
    main()



