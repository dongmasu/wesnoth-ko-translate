#!/usr/bin/env python3
"""Render version-aware project Markdown from docs/templates."""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "docs" / "templates"

TEMPLATES = {
    "README.md.in": ROOT / "README.md",
    "INSTALL.md.in": ROOT / "INSTALL.md",
    "PROJECT-AI.md.in": ROOT / "PROJECT-AI.md",
    "work-README.md.in": ROOT / "work" / "README.md",
}


def read_version() -> str:
    value = os.environ.get("WESNOTH_VERSION") or None
    if value is None:
        value = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+(?:\.\d+)?(?:[.-][0-9A-Za-z.-]+)?", value):
        raise ValueError(f"invalid Wesnoth version: {value!r}")
    return value


def major_minor(version: str) -> str:
    match = re.match(r"^(\d+\.\d+)", version)
    if match is None:
        raise ValueError(f"cannot derive major/minor version: {version!r}")
    return match.group(1)


def latest_po_date(version: str) -> str:
    candidates = sorted(
        (ROOT / "dist").glob(f"{version}-*/ko/PO_LAST_MODIFIED_DATE"),
        key=lambda path: path.parent.parent.name,
        reverse=True,
    )
    for path in candidates:
        value = path.read_text(encoding="utf-8").strip()
        timestamp_match = re.fullmatch(
            r"(\d{4})-(\d{2})-(\d{2}) \d{2}:\d{2}:\d{2}\+0900",
            value,
        )
        if timestamp_match:
            return "".join(timestamp_match.group(index) for index in (1, 2, 3))
        if re.fullmatch(r"\d{8}", value):
            return value
    return "<최종수정일>"


def render(
    template: str,
    version: str,
    po_date: str = "<최종수정일>",
) -> str:
    replacements = {
        "{{WESNOTH_VERSION}}": version,
        "{{WESNOTH_MAJOR_MINOR}}": major_minor(version),
        "{{PO_LAST_MODIFIED_DATE}}": po_date,
    }
    for token, value in replacements.items():
        template = template.replace(token, value)
    if "{{" in template or "}}" in template:
        raise ValueError("unresolved documentation template token")
    return template


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render version-aware Markdown documentation."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if generated documents differ from the working tree",
    )
    args = parser.parse_args()

    version = read_version()
    po_date = latest_po_date(version)
    changed: list[str] = []
    for template_name, output_path in TEMPLATES.items():
        template_path = TEMPLATE_DIR / template_name
        content = render(template_path.read_text(encoding="utf-8"), version, po_date)
        current = output_path.read_text(encoding="utf-8") if output_path.exists() else None
        if current != content:
            changed.append(str(output_path.relative_to(ROOT)))
            if not args.check:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(content, encoding="utf-8")

    if changed:
        if args.check:
            print("documentation is out of date:")
            for path in changed:
                print(f"  {path}")
            return 1
        print(f"rendered documentation for Wesnoth {version}")
        for path in changed:
            print(f"  {path}")
    else:
        print(f"documentation is up to date for Wesnoth {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
