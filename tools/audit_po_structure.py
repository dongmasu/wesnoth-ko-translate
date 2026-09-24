#!/usr/bin/env python3
"""Report markup and placeholder differences between work PO messages."""

from __future__ import annotations

import argparse
import ast
import collections
import re
from pathlib import Path


FIELD_RE = re.compile(
    r"^(msgid_plural|msgid|msgstr(?:\[\d+\])?)\s+(.+)$"
)
TAG_RE = re.compile(
    r"</?(?:i|b|u|s|em|strong|small|big|span|ref|header|br)(?:\s[^>]*)?>"
)
PLACEHOLDER_RE = re.compile(
    r"%(?:\d+\$)?[+#-]?(?:\d+)?(?:\.\d+)?[A-Za-z]"
    r"|\$[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)*"
)


def parse_messages(path: Path) -> list[dict[str, str]]:
    messages = []
    for block in path.read_text(encoding="utf-8").split("\n\n"):
        values: dict[str, str] = {}
        current: str | None = None
        fuzzy = False
        for line in block.splitlines():
            if line.startswith("#,") and "fuzzy" in line:
                fuzzy = True
            match = FIELD_RE.match(line)
            if match:
                current = match.group(1)
                values[current] = ast.literal_eval(match.group(2))
            elif current and line.startswith('"'):
                values[current] += ast.literal_eval(line)
            else:
                current = None
        if (
            values.get("msgid")
            and any(key.startswith("msgstr") for key in values)
            and not fuzzy
        ):
            messages.append(values)
    return messages


def mismatch(source: str, translation: str, pattern: re.Pattern[str]) -> bool:
    return collections.Counter(pattern.findall(source)) != collections.Counter(
        pattern.findall(translation)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path, nargs="?", default=Path("work/1.18.x/ko"))
    args = parser.parse_args()

    tag_count = 0
    placeholder_count = 0
    for path in sorted(args.directory.glob("*.po")):
        for message in parse_messages(path):
            source_forms = [message["msgid"]]
            if message.get("msgid_plural"):
                source_forms.append(message["msgid_plural"])
            translations = sorted(
                (
                    int(key[7:-1]) if key != "msgstr" else 0,
                    value,
                )
                for key, value in message.items()
                if key == "msgstr" or key.startswith("msgstr[")
            )
            mismatches = [
                (
                    source_forms[min(index, len(source_forms) - 1)],
                    translation,
                )
                for index, translation in translations
            ]
            def matches_any_form(
                translation: str, pattern: re.Pattern[str]
            ) -> bool:
                return any(
                    not mismatch(source, translation, pattern)
                    for source in source_forms
                )

            tags_bad = any(
                not matches_any_form(translation, TAG_RE)
                for _, translation in mismatches
            )
            placeholders_bad = any(
                not matches_any_form(translation, PLACEHOLDER_RE)
                for _, translation in mismatches
            )
            if not tags_bad and not placeholders_bad:
                continue
            if tags_bad:
                tag_count += 1
            if placeholders_bad:
                placeholder_count += 1
            kinds = []
            if tags_bad:
                kinds.append("markup")
            if placeholders_bad:
                kinds.append("placeholder")
            print(f"{path.name}\t{','.join(kinds)}\t{mismatches[0][0]}")

    print(f"markup_mismatches={tag_count}")
    print(f"placeholder_mismatches={placeholder_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
