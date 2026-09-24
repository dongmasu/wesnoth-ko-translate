from ast import literal_eval
from collections import Counter
from pathlib import Path
import shutil
import re
import subprocess
import unittest

from tools.apply_manual_translation_batch import TRANSLATIONS, parse_msgstr
from tools.audit_po_structure import (
    PLACEHOLDER_RE,
    TAG_RE,
    mismatch,
    parse_messages,
)
from tools.audit_po_completion import audit_directory
from tools.project_config import DEFAULT_VERSION, PO_ROOT, VERSION, WORK_ROOT, WORK_KO


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_KO = ROOT / "References" / "20250322_wesnoth_한국어번역"
STRUCTURAL_REGRESSION_SOURCES = {
    "Engraved with a consecrated symbol, this amulet will bless both your "
    "<i><b>melee</b></i> and <i><b>ranged</b></i> attacks with <i><b>arcane</b></i> damage.",
    "The ‘deserter’ trait has caused $unit.name to flee back to your recall list.",
    "female^The ‘deserter’ trait has caused $unit.name to flee back to your recall list.",
}

FIELD_RE = re.compile(
    r"^(msgctxt|msgid_plural|msgid|msgstr(?:\[\d+\])?)\s+(.+?)(?:\r?\n)?$"
)


def po_files(directory):
    return {path.name for path in directory.glob("*.po")}


def po_keys(path):
    """Return gettext message keys without depending on a third-party parser."""
    keys = set()
    text = path.read_text(encoding="utf-8")

    for block in text.split("\n\n"):
        values = {}
        current = None
        for raw_line in block.splitlines():
            match = FIELD_RE.match(raw_line)
            if match:
                current = match.group(1)
                values[current] = literal_eval(match.group(2))
            elif current and raw_line.startswith('"'):
                values[current] += literal_eval(raw_line)
            else:
                current = None

        if "msgid" in values:
            keys.add(
                (
                    values.get("msgctxt", ""),
                    values["msgid"],
                    values.get("msgid_plural", ""),
                )
            )
    return keys


class TranslationLayoutTests(unittest.TestCase):
    def test_documented_rules_cover_structural_exceptions(self):
        project_rules = (ROOT / "PROJECT-AI.md").read_text(encoding="utf-8")
        work_rules = (ROOT / "work" / "README.md").read_text(encoding="utf-8")
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        combined = f"{project_rules}\n{work_rules}\n{root_readme}"

        for rule in (
            "placeholder",
            "실제 개행",
            "`^`",
            "복수형",
            "예외",
            "검토",
            "msgattrib",
            "obsolete",
            "msgid \"\"",
            "헤더",
            "용어집 판정 규칙",
            "forbidden_terms",
            "한글(English)",
            "멱등",
            "전체 PO 전수 검수",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, combined)

    def test_documented_context_prefix_rule_never_displays_prefixes(self):
        cases = (
            (ROOT / "PROJECT-AI.md", "번역문에 넣지"),
            (ROOT / "work" / "README.md", "번역문에 넣지"),
            (ROOT / "README.md", "do not display"),
        )
        for path, required_rule in cases:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn("female^", text)
                self.assertIn(required_rule, text)
                self.assertNotIn("preserve that marker", text)
                self.assertNotIn("여성^`, `남성^`으로 유지할 수", text)

    def test_structure_audit_detects_markup_loss(self):
        source = "<i><b>melee</b></i> and $unit.name"
        preserved = "<i><b>근접</b></i> 및 $unit.name"
        missing_markup = "근접 및 $unit.name"

        self.assertFalse(mismatch(source, preserved, TAG_RE))
        self.assertFalse(mismatch(source, preserved, PLACEHOLDER_RE))
        self.assertTrue(mismatch(source, missing_markup, TAG_RE))
        self.assertFalse(mismatch(source, missing_markup, PLACEHOLDER_RE))

    def test_placeholder_punctuation_is_not_part_of_name(self):
        source = "$version."
        translation = "$version."
        self.assertEqual(PLACEHOLDER_RE.findall(source), ["$version"])
        self.assertFalse(mismatch(source, translation, PLACEHOLDER_RE))

    def test_structure_audit_reads_plural_translations(self):
        path = ROOT / "tests" / "_plural_structure_fixture.po"
        path.write_text(
            'msgid "One <b>$name</b>"\n'
            'msgid_plural "Many <b>$name</b>"\n'
            'msgstr[0] "하나 <b>$name</b>"\n'
            'msgstr[1] "여럿 <b>$name</b>"\n',
            encoding="utf-8",
        )
        try:
            messages = parse_messages(path)
        finally:
            path.unlink()
        self.assertEqual(len(messages), 1)
        self.assertIn("msgstr[0]", messages[0])
        self.assertIn("msgstr[1]", messages[0])

    def test_manual_batch_preserves_markup_and_placeholders(self):
        tag_pattern = re.compile(r"</?[A-Za-z][^>]*>")
        placeholder_pattern = re.compile(
            r"%(?:\d+\$)?[+#-]?(?:\d+)?(?:\.\d+)?[A-Za-z]"
            r"|\$[A-Za-z_][A-Za-z0-9_.]*"
        )

        for path in sorted(WORK_KO.glob("*.po")):
            text = path.read_text(encoding="utf-8")
            for block in text.split("\n\n"):
                values = {}
                current = None
                for raw_line in block.splitlines():
                    match = FIELD_RE.match(raw_line)
                    if match:
                        current = match.group(1)
                        values[current] = literal_eval(match.group(2))
                    elif current and raw_line.startswith('"'):
                        values[current] += literal_eval(raw_line)
                    else:
                        current = None

                source = values.get("msgid")
                if source not in STRUCTURAL_REGRESSION_SOURCES:
                    continue
                with self.subTest(path=path.name, source=source):
                    translation = values.get("msgstr", "")
                    if translation != TRANSLATIONS[source]:
                        continue
                    self.assertEqual(
                        Counter(re.findall(tag_pattern, source)),
                        Counter(re.findall(tag_pattern, translation)),
                    )
                    self.assertEqual(
                        Counter(re.findall(placeholder_pattern, source)),
                        Counter(re.findall(placeholder_pattern, translation)),
                    )

    def test_manual_batch_reads_plural_msgstr_zero(self):
        block = 'msgid "Example"\nmsgid_plural "Examples"\nmsgstr[0] ""\n'
        self.assertEqual(parse_msgstr(block), "")

        translated = (
            'msgid "Example"\n'
            'msgid_plural "Examples"\n'
            'msgstr[0] "예시"\n'
        )
        self.assertEqual(parse_msgstr(translated), "예시")

    def test_expected_locale_directories_exist(self):
        for locale in ("ko", "ja", "zh_CN", "en_GB"):
            with self.subTest(locale=locale):
                self.assertTrue((PO_ROOT / locale).is_dir())

    def test_version_configuration_uses_root_default(self):
        self.assertEqual(DEFAULT_VERSION, "1.18.x")
        self.assertEqual(VERSION, DEFAULT_VERSION)
        self.assertEqual(PO_ROOT, ROOT / "po" / VERSION)
        self.assertEqual(WORK_ROOT, ROOT / "work" / VERSION)

    def test_mo_helpers_and_installation_docs_exist(self):
        for name in (
            "build_mo.sh",
            "build_mo.bat",
            "install_mo.sh",
            "install_mo.bat",
            "install_mo_macos_external.sh",
            "install_mo_macos_app.sh",
            "mark_korean_locale.sh",
            "mark_korean_locale.bat",
            "mark_korean_locale.ps1",
        ):
            with self.subTest(name=name):
                self.assertTrue((ROOT / "tools" / name).is_file())

        self.assertTrue((ROOT / "tools" / "audit_glossary.py").is_file())
        install_doc = (ROOT / "INSTALL.md").read_text(encoding="utf-8")
        for marker in (
            "tools/build_mo.sh",
            "tools\\build_mo.bat",
            "tools/install_mo.sh",
            "tools/install_mo_macos_external.sh",
            "tools/install_mo_macos_app.sh",
            "tools/mark_korean_locale.sh",
            "tools\\mark_korean_locale.bat",
            "tools/audit_and_pair_embedded_names.py",
            "tools\\install_mo.bat",
            "tools/audit_po_completion.py",
            "PO_LAST_MODIFIED_DATE",
            "LC_MESSAGES",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, install_doc)

    def test_work_files_follow_github_korean_file_set(self):
        self.assertTrue(REFERENCE_KO.is_dir())
        self.assertEqual(po_files(PO_ROOT / "ko"), po_files(WORK_KO))
        self.assertNotIn("wesnoth-tdg-ko.po", po_files(WORK_KO))

    def test_work_preserves_github_message_structure(self):
        for filename in sorted(po_files(WORK_KO)):
            with self.subTest(filename=filename):
                self.assertEqual(
                    po_keys(PO_ROOT / "ko" / filename),
                    po_keys(WORK_KO / filename),
                )

    def test_msgfmt_accepts_work_files(self):
        msgfmt = shutil.which("msgfmt")
        if msgfmt is None:
            self.skipTest("msgfmt is not installed")

        for path in sorted(WORK_KO.glob("*.po")):
            with self.subTest(path=path.name):
                result = subprocess.run(
                    [msgfmt, "--check", "--output-file=/dev/null", str(path)],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=f"{path} failed msgfmt check:\n{result.stderr}",
                )

    def test_work_has_no_active_untranslated_or_fuzzy_messages(self):
        for path, counts in audit_directory(WORK_KO).items():
            with self.subTest(path=path.name):
                self.assertEqual(counts.untranslated, 0)
                self.assertEqual(counts.fuzzy, 0)

    def test_completion_audit_runs_as_a_script(self):
        result = subprocess.run(
            [shutil.which("python3") or "python3", "tools/audit_po_completion.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("total", result.stdout)
        self.assertIn("untranslated=0", result.stdout)
        self.assertIn("fuzzy=0", result.stdout)

    def test_embedded_name_pairing_audit_is_clean_and_idempotent(self):
        result = subprocess.run(
            [
                shutil.which("python3") or "python3",
                "tools/audit_and_pair_embedded_names.py",
                "--check",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("messages=0 unresolved=0", result.stdout)


if __name__ == "__main__":
    unittest.main()
