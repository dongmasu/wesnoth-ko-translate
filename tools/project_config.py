"""Shared version and path configuration for the translation workspace."""

from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"
DEFAULT_VERSION = VERSION_FILE.read_text(encoding="utf-8").strip()
VERSION = os.environ.get("WESNOTH_VERSION", DEFAULT_VERSION)

PO_ROOT = ROOT / "po" / VERSION
WORK_ROOT = ROOT / "work" / VERSION
WORK_KO = WORK_ROOT / "ko"
GLOSSARY = WORK_ROOT / "glossary.tsv"


def versioned_path(root_name: str) -> Path:
    """Return a version directory below the repository root."""
    return ROOT / root_name / VERSION
