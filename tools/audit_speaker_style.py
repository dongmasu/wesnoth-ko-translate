#!/usr/bin/env python3
"""Report sentence-ending styles used by each PO message speaker.

This is a review aid, not an automatic translation decision. A speaker may
change register for a deliberate scene or quotation, so findings require
reading the English source and surrounding messages.
"""

from __future__ import annotations

import argparse
import ast
import re
from collections import Counter, defaultdict
from pathlib import Path


FIELD_RE = re.compile(r"^(msgid|msgstr)\s+(.+)$")
SPEAKER_RE = re.compile(r"^#\. \[message\]: speaker=([^\n]+)$", re.MULTILINE)


def field_value(block: str, field: str) -> str:
    match = re.search(rf"^{field}\s+(.+)$", block, re.MULTILINE)
    if not match:
        return ""
    value = ast.literal_eval(match.group(1))
    for line in block[match.end() :].splitlines():
        if not line.startswith('"'):
            break
        value += ast.literal_eval(line)
    return value


def ending_style(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).strip()
    text = re.sub(r"[\s.!?…\"”’]+$", "", text)
    if re.search(r"(?:습니다|ㅂ니다|습니까|십시오|세요|세요)$", text):
        return "formal"
    if re.search(r"(?:네|군|구나|걸세|하게|하오|소)$", text):
        return "archaic"
    if re.search(r"(?:해|야|지|거야|한다|다)$", text):
        return "plain"
    if re.search(r"(?:하라|해라|다오|가라|마라)$", text):
        return "imperative"
    return "other"


def audit(path: Path) -> dict[str, Counter[str]]:
    result: dict[str, Counter[str]] = defaultdict(Counter)
    for block in path.read_text(encoding="utf-8").split("\n\n"):
        speaker_match = SPEAKER_RE.search(block)
        if not speaker_match:
            continue
        msgid = field_value(block, "msgid")
        msgstr = field_value(block, "msgstr")
        if not msgid or not msgstr:
            continue
        result[speaker_match.group(1)][ending_style(msgstr)] += 1
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "po",
        type=Path,
        help="a PO file or a directory containing PO files",
    )
    args = parser.parse_args()

    paths = [args.po] if args.po.is_file() else sorted(args.po.glob("*.po"))
    for path in paths:
        for speaker, styles in sorted(audit(path).items()):
            strong_styles = {
                style: count
                for style, count in styles.items()
                if style != "other"
            }
            if len(strong_styles) <= 1:
                continue
            print(
                f"{path.name}\t{speaker}\t"
                + ", ".join(f"{style}={count}" for style, count in styles.items())
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
