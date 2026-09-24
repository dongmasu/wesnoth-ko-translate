#!/usr/bin/env python3
"""Report active PO entries that are incomplete without counting obsolete data."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys

# Allow direct execution from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.merge_reference_translations import is_fuzzy, parse_field_values


@dataclass(frozen=True)
class CompletionCounts:
    messages: int = 0
    untranslated: int = 0
    fuzzy: int = 0

    def __add__(self, other: "CompletionCounts") -> "CompletionCounts":
        return CompletionCounts(
            messages=self.messages + other.messages,
            untranslated=self.untranslated + other.untranslated,
            fuzzy=self.fuzzy + other.fuzzy,
        )


def audit_file(path: Path) -> CompletionCounts:
    """Count active messages only; headers and obsolete blocks are excluded."""
    counts = CompletionCounts()
    for block in path.read_text(encoding="utf-8").split("\n\n"):
        values = parse_field_values(block)
        msgid = values.get("msgid")
        if not msgid:
            continue

        translations = {
            key: value
            for key, value in values.items()
            if key == "msgstr" or key.startswith("msgstr[")
        }
        counts = counts + CompletionCounts(
            messages=1,
            untranslated=int(
                not translations or any(not value for value in translations.values())
            ),
            fuzzy=int(is_fuzzy(block)),
        )
    return counts


def audit_directory(directory: Path) -> dict[Path, CompletionCounts]:
    return {path: audit_file(path) for path in sorted(directory.glob("*.po"))}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory",
        type=Path,
        nargs="?",
        default=Path("work/1.18.x/ko"),
    )
    args = parser.parse_args()

    total = CompletionCounts()
    for path, counts in audit_directory(args.directory).items():
        total += counts
        print(
            f"{path.name}\tmessages={counts.messages}\t"
            f"untranslated={counts.untranslated}\tfuzzy={counts.fuzzy}"
        )

    print(
        f"total\tmessages={total.messages}\t"
        f"untranslated={total.untranslated}\tfuzzy={total.fuzzy}"
    )
    return 1 if total.untranslated or total.fuzzy else 0


if __name__ == "__main__":
    raise SystemExit(main())
