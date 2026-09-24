#!/usr/bin/env python3
"""Fix unambiguous spacing errors in active Korean PO translations."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.project_config import WORK_KO


REPLACEMENTS = (
    (re.compile(r"할것"), "할 것"),
    (re.compile(r"될것"), "될 것"),
    (re.compile(r"을것"), "을 것"),
    (re.compile(r"ㄹ것"), "ㄹ 것"),
    (re.compile(r"것같"), "것 같"),
    (re.compile(r"것에대해"), "것에 대해"),
    (re.compile(r"없어진건"), "없어진 건"),
    (re.compile(r"할수"), "할 수"),
    (re.compile(r"해야겠"), "해야 겠"),
    (re.compile(r"안됩니다"), "안 됩니다"),
    (re.compile(r"해야합니다"), "해야 합니다"),
    (re.compile(r"해야한다"), "해야 한다"),
    (re.compile(r"가고싶"), "가고 싶"),
    (re.compile(r"할수밖에"), "할 수밖에"),
    (re.compile(r"절때"), "절대"),
    (re.compile(r"난장이"), "난쟁이"),
    (re.compile(r"쫒아"), "쫓아"),
    (re.compile(r"댓가"), "대가"),
    (re.compile(r"부딛혀"), "부딪혀"),
    (re.compile(r"가본적"), "가 본 적"),
    (re.compile(r"내옆"), "내 옆"),
    (re.compile(r"한마리"), "한 마리"),
    (re.compile(r"그터널"), "그 터널"),
    (re.compile(r"우리영토"), "우리 영토"),
    (re.compile(r"모든것"), "모든 것"),
    (re.compile(r"나의것"), "나의 것"),
    (re.compile(r"두번째"), "두 번째"),
    (re.compile(r"그이야기"), "그 이야기"),
)


def normalize_block(block: str) -> tuple[str, int]:
    if block.lstrip().startswith("#~") or "msgid " not in block:
        return block, 0

    changed = 0
    output: list[str] = []
    in_translation = False
    for line in block.splitlines(keepends=True):
        if line.startswith("msgstr"):
            in_translation = True
        elif line.startswith("msgid") or line.startswith("msgctxt"):
            in_translation = False

        if in_translation and (
            line.startswith('"') or line.startswith("msgstr")
        ):
            updated = line
            for pattern, replacement in REPLACEMENTS:
                updated, count = pattern.subn(replacement, updated)
                changed += count
            line = updated
        output.append(line)
    return "".join(output), changed


def normalize_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    blocks = text.split("\n\n")
    total = 0
    normalized = []
    for block in blocks:
        block, changed = normalize_block(block)
        total += changed
        normalized.append(block)
    if total:
        path.write_text("\n\n".join(normalized), encoding="utf-8")
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path, nargs="?", default=WORK_KO)
    args = parser.parse_args()
    total = 0
    for path in sorted(args.directory.glob("*.po")):
        changed = normalize_file(path)
        if changed:
            print(f"{path.name}: {changed}")
            total += changed
    print(f"total replacements: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
