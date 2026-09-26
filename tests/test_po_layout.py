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
    newline_mismatch,
    parse_messages,
)
from tools.audit_po_completion import audit_directory
from tools.audit_locale_comparison import active_entries
from tools.audit_speaker_style import ending_style
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
    def test_active_translations_have_no_review_markers(self):
        markers = (
            "번역확인",
            "번역확인필요",
            "FIXME",
            "검토 필요",
        )
        for path in sorted(WORK_KO.glob("*.po")):
            for block in path.read_text(encoding="utf-8").split("\n\n"):
                if any(line.startswith("#~") for line in block.splitlines()):
                    continue
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

                translations = [
                    value
                    for field, value in values.items()
                    if field == "msgstr" or field.startswith("msgstr[")
                ]
                for translation in translations:
                    for marker in markers:
                        with self.subTest(path=path.name, marker=marker):
                            self.assertNotIn(marker, translation)

    def test_locale_comparison_uses_matching_active_keys(self):
        work = active_entries(WORK_KO)
        english = active_entries(PO_ROOT / "en_GB")
        japanese = active_entries(PO_ROOT / "ja")
        chinese = active_entries(PO_ROOT / "zh_CN")
        self.assertEqual(set(work), set(english))
        self.assertEqual(set(work), set(japanese))
        self.assertEqual(set(work), set(chinese))

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
            "검수자",
            "수정자",
            "검증자",
            "배포자",
            "flowchart TD",
            "검수 보고서",
            "단계별 권한과 산출물",
            "불변의 진실",
            "실제 PO 문맥",
            "용어집 오류",
            "영향 범위",
            "자동 재적용하지",
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

    def test_structure_audit_detects_newline_loss_and_trailing_drift(self):
        self.assertFalse(newline_mismatch("첫 문단\n\n둘째 문단", "첫 문단\n\n둘째 문단"))
        self.assertTrue(newline_mismatch("첫 문단\n\n둘째 문단", "첫 문단 둘째 문단"))
        self.assertTrue(newline_mismatch("문장\n", "문장"))
        self.assertTrue(newline_mismatch("\n문장", "문장"))

    def test_placeholder_punctuation_is_not_part_of_name(self):
        source = "$version."
        translation = "$version."
        self.assertEqual(PLACEHOLDER_RE.findall(source), ["$version"])
        self.assertFalse(mismatch(source, translation, PLACEHOLDER_RE))

    def test_speaker_style_audit_classifies_common_korean_endings(self):
        self.assertEqual(ending_style("문을 여십시오."), "formal")
        self.assertEqual(ending_style("그렇군."), "archaic")
        self.assertEqual(ending_style("어서 가라!"), "imperative")
        self.assertEqual(ending_style("이제 끝났다."), "plain")

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

    def test_curated_glossary_is_the_only_glossary_artifact(self):
        self.assertTrue((WORK_ROOT / "glossary.tsv").is_file())
        for name in (
            "glossary-candidates.tsv",
            "glossary-inventory.tsv",
            "glossary-untranslated.tsv",
        ):
            with self.subTest(name=name):
                self.assertFalse((WORK_ROOT / name).exists())
        for name in (
            "extract_glossary_candidates.py",
            "promote_glossary_candidates.py",
        ):
            with self.subTest(name=name):
                self.assertFalse((ROOT / "tools" / name).exists())

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
        self.assertTrue(
            (ROOT / "tools" / "normalize_glossary_labels.py").is_file()
        )
        self.assertTrue(
            (ROOT / "tools" / "normalize_known_name_spellings.py").is_file()
        )
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

    def test_full_review_policy_distinguishes_format_audits_from_prose_review(self):
        work_readme = (ROOT / "work" / "README.md").read_text(encoding="utf-8")
        for marker in (
            "자동 감사가 통과해도 의미, 문체",
            "같은 화자가 말하는 대사는",
            "audit_speaker_style.py",
            "수동 검수 대상",
            "음차는 철자 대 철자 치환이 아니라",
            "Arvith=아르비쓰",
            "Mal Tath=말 타쓰",
            "발음 예외",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, work_readme)

    def test_dist_snapshots_include_last_modified_date_and_ignore_only_backups(self):
        build_script = (ROOT / "tools" / "build_mo.sh").read_text(encoding="utf-8")
        build_batch = (ROOT / "tools" / "build_mo.bat").read_text(encoding="utf-8")
        install_script = (ROOT / "tools" / "install_mo.sh").read_text(encoding="utf-8")
        install_batch = (ROOT / "tools" / "install_mo.bat").read_text(encoding="utf-8")
        locale_script = (ROOT / "tools" / "mark_korean_locale.sh").read_text(
            encoding="utf-8"
        )
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        install_doc = (ROOT / "INSTALL.md").read_text(encoding="utf-8")

        self.assertIn('DIST_DIR="$ROOT/dist/$VERSION-$po_date"', build_script)
        self.assertIn("po_timestamp", build_script)
        self.assertIn("YYYY-MM-DD HH:MM:SS+0900", build_script)
        self.assertIn("PO_TIMESTAMP", build_batch)
        self.assertIn('SOURCE_DIR=${2:-"$ROOT/dist/$VERSION-$po_date/ko/LC_MESSAGES"}', install_script)
        self.assertIn("po_timestamp", install_script)
        self.assertIn("PO_TIMESTAMP", install_batch)
        self.assertIn("PO_TIMESTAMP", locale_script)
        work_readme = (ROOT / "work" / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("MO 생성 날짜", work_readme)
        self.assertIn("PO 중 가장 최근의 최종 수정 시각", work_readme)
        self.assertNotIn("LC_MESSAGES.backup", gitignore)
        self.assertNotIn("\ndist/\n", gitignore)
        self.assertIn('rm -f "$mo"', install_script)
        self.assertIn('del /q "%TARGET_DIR%\\*.mo"', install_batch)
        self.assertIn("dist/<버전>-<최종수정일>/ko/LC_MESSAGES/", install_doc)
        self.assertIn("Versioned `dist/<version>-<last-modified-date>/`", install_doc)
        self.assertNotIn("<작업일>", install_doc)
        self.assertNotIn("<작업날짜>", install_doc)
        self.assertNotIn("<work-date>", install_doc)
        self.assertIn("rebuild from", install_doc)
        self.assertIn("동기화", install_doc)
        self.assertIn("`data/`와\n`translations/`는 ZIP 최상위의 형제", install_doc)
        self.assertIn("data/languages/ko_KR.cfg", install_doc)
        self.assertIn("translations/ko/LC_MESSAGES/", install_doc)
        self.assertIn("translations/`를 `data/` 아래에", install_doc)

    def test_documentation_uses_last_modified_date_term_consistently(self):
        documentation_files = [
            ROOT / "README.md",
            ROOT / "INSTALL.md",
            ROOT / "PROJECT-AI.md",
            ROOT / "work" / "README.md",
            ROOT / "work" / VERSION / "README.md",
            ROOT / "docs" / "templates" / "README.md.in",
            ROOT / "docs" / "templates" / "INSTALL.md.in",
            ROOT / "docs" / "templates" / "PROJECT-AI.md.in",
            ROOT / "docs" / "templates" / "work-README.md.in",
        ]
        legacy_terms = ("<작업일>", "<작업날짜>", "<work-date>")
        for path in documentation_files:
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                for term in legacy_terms:
                    self.assertNotIn(term, content)
                if path.suffix == ".md":
                    self.assertIn("<최종수정일>", content)

    def test_locale_marker_sets_complete_translation_percentage(self):
        shell_script = (ROOT / "tools" / "mark_korean_locale.sh").read_text(
            encoding="utf-8"
        )
        powershell_script = (ROOT / "tools" / "mark_korean_locale.ps1").read_text(
            encoding="utf-8"
        )
        self.assertIn('sub(/percent[[:space:]]*=[[:space:]]*[0-9]+/, "percent=100")', shell_script)
        self.assertIn("$updated = $updated -replace 'percent\\s*=\\s*\\d+', 'percent=100'", powershell_script)
        self.assertIn('sort_name = "Hangugeo"', shell_script)
        self.assertIn('sort_name\\s*=\\s*"Hangugeo"', powershell_script)
        self.assertNotIn('sub(/sort_name = "[^"]*"/', shell_script)
        self.assertNotIn("$updated = $updated -replace 'sort_name", powershell_script)
        self.assertIn('sort_name = "Hangugeo"', (ROOT / "work" / VERSION / "ko_KR.cfg").read_text(encoding="utf-8"))
        self.assertIn("percent=100", (ROOT / "INSTALL.md").read_text(encoding="utf-8"))

    def test_readme_documents_mo_only_release_asset(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("MO만 필요한 사용자를 위한 다운로드", readme)
        self.assertIn(
            "wesnoth-ko-translate-1.18.x-20260926.zip",
            readme,
        )
        self.assertIn(
            "releases/download/wesnoth-ko-translate-1.18.x-20260926/"
            "wesnoth-ko-translate-1.18.x-20260926.zip",
            readme,
        )
        self.assertIn("Release asset이 게시된 뒤에는", readme)
        self.assertIn("마지막 PO 수정 시각", readme)

    def test_completion_tag_uses_version_and_last_po_modified_date(self):
        documents = (
            ROOT / "README.md",
            ROOT / "PROJECT-AI.md",
            ROOT / "INSTALL.md",
            ROOT / "work" / VERSION / "README.md",
        )
        old_tag = f"wesnoth-{VERSION}-ko.1"
        new_tag = f"wesnoth-ko-translate-{VERSION}-"

        for path in documents:
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn(new_tag, content)
                self.assertNotIn(old_tag, content)

        install_doc = (ROOT / "INSTALL.md").read_text(encoding="utf-8")
        self.assertIn("KST/JST", install_doc)
        self.assertIn("PO_LAST_MODIFIED_DATE", install_doc)
        self.assertIn(
            'TAG="wesnoth-ko-translate-${VERSION}-${LAST_MODIFIED_DATE}"',
            install_doc,
        )
        self.assertIn("YYYY-MM-DD HH:MM:SS+0900", install_doc)
        self.assertIn("PO_TIMESTAMP=", install_doc)

        metadata = (
            ROOT / "dist" / "1.18.x-20260926" / "ko" / "PO_LAST_MODIFIED_DATE"
        ).read_text(encoding="utf-8").strip()
        self.assertRegex(
            metadata,
            r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+0900$",
        )

    def test_docs_workflow_only_publishes_from_main(self):
        workflow = (ROOT / ".github" / "workflows" / "docs.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("branches:\n      - main", workflow)
        self.assertIn("git push origin HEAD:main", workflow)
        self.assertNotIn("\n          git push\n", workflow)

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
                self.assertNotIn(
                    "warning:",
                    result.stderr,
                    msg=f"{path} has msgfmt header warnings:\n{result.stderr}",
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
        # A nonzero message count means pairable name candidates were found;
        # unresolved=0 is the invariant that matters for this audit.
        self.assertIn("unresolved=0", result.stdout)

    def test_name_candidate_audit_reports_active_and_obsolete_counts(self):
        result = subprocess.run(
            [
                shutil.which("python3") or "python3",
                "tools/audit_and_pair_embedded_names.py",
                "--candidates",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertRegex(result.stdout, r"active_candidates=\d+")
        self.assertRegex(result.stdout, r"obsolete_candidates=\d+")

    def test_shared_ui_review_batch_is_applied(self):
        batch = ROOT / "tools" / "apply_review_batch_08.py"
        self.assertTrue(batch.is_file())
        checks = {
            "wesnoth-editor-ko.po": (
                'msgid "Time Schedule Menu"',
                'msgstr "시간 일정 메뉴"',
            ),
            "wesnoth-ko.po": (
                'msgid "No description available."',
                'msgstr "설명이 없습니다."',
            ),
            "wesnoth-lib-ko.po": (
                'msgid "Clipboard support not found, contact your packager"',
                'msgstr "클립보드 지원을 찾을 수 없습니다. 패키지 관리자에게 문의하세요"',
            ),
        }
        for filename, markers in checks.items():
            content = (WORK_KO / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                for marker in markers:
                    self.assertIn(marker, content)


if __name__ == "__main__":
    unittest.main()
