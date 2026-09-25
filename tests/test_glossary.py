from pathlib import Path
import csv
import re
import unittest

from tools.apply_manual_translation_batch import is_glossary_candidate
from tools.audit_glossary import parenthetical_is_source_component
from tools.audit_gender_terms import lexical_pairs
from tools.merge_reference_translations import parse_field_values
from tools.normalize_contextual_translations import normalize_translation
from tools.normalize_korean_spacing import normalize_block
from tools.project_config import GLOSSARY, VERSION, WORK_KO


ROOT = Path(__file__).resolve().parents[1]

FIELDS = (
    "source_term",
    "standard_korean",
    "reference_japanese",
    "reference_chinese",
    "category",
    "forbidden_terms",
    "notes",
)
PO_FIELD = re.compile(r'^msgid "(.*)"$')
PO_STR = re.compile(r'^msgstr "(.*)"$')


def glossary_rows():
    with GLOSSARY.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = list(reader)
    for row in rows:
        for field in FIELDS:
            row[field] = row.get(field) or ""
    return list(reader.fieldnames or ()), rows


def exact_po_translations(path):
    translations = {}
    for block in path.read_text(encoding="utf-8").split("\n\n"):
        values = parse_field_values(block)
        if values.get("msgid") and "msgstr" in values:
            translations[values["msgid"]] = values["msgstr"]
    return translations


class GlossaryTests(unittest.TestCase):
    def test_glossary_schema_and_required_values(self):
        fieldnames, rows = glossary_rows()
        self.assertEqual(tuple(fieldnames), FIELDS)
        self.assertGreater(len(rows), 0)
        for row in rows:
            with self.subTest(row=row):
                self.assertTrue(row["source_term"])
                self.assertTrue(row["standard_korean"])

    def test_notes_are_not_generated_context_boilerplate(self):
        _, rows = glossary_rows()
        boilerplate = re.compile(
            r"^(?:대소문자를 구분하는 source_term 기준으로 유지; "
            r"category=[^;]+; PO locale 실제 표현을 대조|"
            r"PO locale 실제 표현과 고유명사 여부를 대조)$"
        )
        for row in rows:
            with self.subTest(source=row["source_term"]):
                self.assertFalse(boilerplate.fullmatch(row["notes"].strip()))

    def test_source_terms_are_exactly_unique(self):
        _, rows = glossary_rows()
        sources = [row["source_term"] for row in rows]
        self.assertEqual(len(sources), len(set(sources)))

    def test_forbidden_terms_are_not_the_standard_translation(self):
        _, rows = glossary_rows()
        for row in rows:
            standard = row["standard_korean"].strip()
            forbidden = {
                item.strip()
                for item in row["forbidden_terms"].split(";")
                if item.strip()
            }
            with self.subTest(source=row["source_term"]):
                self.assertNotIn(standard, forbidden)
                for alternative in forbidden:
                    self.assertNotRegex(
                        alternative,
                        r"(?:번역|검토|확인|TODO|FIXME)",
                    )

    def test_numeric_and_symbol_only_terms_are_excluded(self):
        _, rows = glossary_rows()
        for row in rows:
            source = row["source_term"]
            with self.subTest(source=source):
                self.assertIsNone(re.fullmatch(r"\s*\d+\s*", source))
                self.assertTrue(
                    re.search(r"\w", source)
                    or source in {"∞", "#"}
                )

    def test_glossary_terms_match_work_po(self):
        _, rows = glossary_rows()
        translations = {}
        for path in WORK_KO.glob("*.po"):
            translations.update(exact_po_translations(path))
        for row in rows:
            with self.subTest(source=row["source_term"]):
                if row["source_term"] in translations:
                    self.assertEqual(
                        translations[row["source_term"]],
                        row["standard_korean"],
                    )

    def test_great_river_variants_share_one_standard_translation(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        self.assertEqual(by_source["Great River"], "위대한 강")
        self.assertEqual(by_source["The Great River"], "위대한 강")

    def test_sorcerer_and_sorceress_preserve_gendered_korean_distinction(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        self.assertEqual(by_source["Sorcerer"], "마법사")
        self.assertEqual(by_source["Dark Sorcerer"], "흑마법사")
        self.assertEqual(by_source["Dark Sorceress"], "흑마녀")
        self.assertEqual(by_source["female^Elvish Sorceress"], "요정 마녀")

    def test_gender_context_does_not_invent_a_female_prefix(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        self.assertEqual(by_source["Elvish Archer"], "요정 궁수")
        self.assertEqual(by_source["female^Elvish Archer"], "요정 궁수")
        self.assertNotIn("여성", by_source["female^Elvish Archer"])

    def test_magic_terms_keep_the_project_mapping_explicit(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        self.assertEqual(by_source["Mage"], "마법사")
        self.assertEqual(by_source["Sorcerer"], "마법사")
        self.assertEqual(by_source["Wizard"], "마도사")

    def test_reviewed_core_ui_terms_are_natural_and_synchronized(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        expected = {
            "Install Dependencies": "의존성 설치",
            "Victory:": "승리 조건:",
            "Defeat:": "패배 조건:",
            "Plan Unit Advance": "유닛 승급 계획",
            "Force advancement planning": "승급 계획 강제",
            "No planned advancement": "승급 대상 미설정",
            "Plan Advancement": "승급 계획",
        }
        translations = {}
        for path in WORK_KO.glob("*.po"):
            translations.update(exact_po_translations(path))
        for source, korean in expected.items():
            with self.subTest(source=source):
                self.assertEqual(by_source[source], korean)
                self.assertEqual(translations[source], korean)

    def test_liminal_rules_description_is_not_mistranslated_as_diurnal(self):
        translations = {}
        for path in WORK_KO.glob("*.po"):
            translations.update(exact_po_translations(path))
        source = (
            "Liminal units fight best during the twilight times of day.\n\n"
            "Twilight: +25% Damage"
        )
        self.assertEqual(
            translations[source],
            "경계성 유닛은 황혼 시간대에 가장 잘 싸웁니다.\n\n"
            "황혼: 피해 +25%",
        )

    def test_magic_term_categories_do_not_use_unrelated_context_labels(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["category"] for row in rows}
        expected = {
            "Mage": "magic",
            "Mages": "magic",
            "Great Mage": "unit_name",
            "Mage Guard": "unit_name",
            "female^Mage": "magic",
            "female^Great Mage": "unit_name",
            "female^Mage of Light": "unit_name",
            "Red Wizards": "unit_role",
        }
        for source, category in expected.items():
            with self.subTest(source=source):
                self.assertEqual(by_source[source], category)

    def test_gender_audit_discovers_lexical_pairs_without_using_category(self):
        _, rows = glossary_rows()
        pairs = set(lexical_pairs(rows))
        self.assertIn(("Dark Sorcerer", "Dark Sorceress"), pairs)

    def test_gendered_lexical_terms_preserve_gender_meaning(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        expected = {
            "Ant Queen": "개미 여왕",
            "Dark Sorceress": "흑마녀",
            "Elvish Princess": "요정 공주",
            "Mother Gryphon": "엄마 그리폰(Gryphon)",
            "Sister Thera": "테라(Thera) 수녀",
            "female^Battle Princess": "전투 공주",
            "female^Frontier Baroness": "국경의 남작 부인",
            "female^Mermaid Priestess": "인어 여신관",
            "female^Vampire Lady": "뱀파이어 아가씨",
            "female^Watchwoman": "야경꾼",
        }
        for source, korean in expected.items():
            with self.subTest(source=source):
                self.assertEqual(by_source[source], korean)

    def test_gender_context_variants_match_base_unless_sex_is_identity(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        exceptions = {"female^Inky"}
        for source, korean in by_source.items():
            if not source.startswith(("female^", "male^", "race+female^")):
                continue
            base = source.split("^", 1)[1]
            if source in exceptions or base not in by_source:
                continue
            with self.subTest(source=source):
                self.assertEqual(korean, by_source[base])

        self.assertEqual(by_source["female^Inky"], "암컷 잉키(Inky)")

    def test_multiword_names_pair_only_transliterated_name_components(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        expected = {
            "Arcanclave": "아르칸클레이브(Arcanclave)",
            "Barag Gór": "바락 고르(Barag Gór)",
            "Bragdash Gar": "브라그다시 가르(Bragdash Gar)",
            "Chief Bir-brish": "족장 비르-브리시(Bir-brish)",
            "Chief Dra-Nak": "족장 드라-나크(Dra-Nak)",
            "Contender Gorlack": "경쟁자 고를락(Gorlack)",
            "Gawffus the Dim": "어리숙한 가우푸스(Gawffus)",
            "Kah Ruuk": "카 루크(Kah Ruuk)",
            "Lintanir": "린타니르(Lintanir)",
            "Mal Maul": "말 마울(Mal Maul)",
            "Mal M’Brin": "말 므브린(Mal M’Brin)",
            "Muff Argulak": "머프 아르굴락(Muff Argulak)",
            "Muff Toras": "머프 토라스(Muff Toras)",
            "Naga Myrmidon": "나가 미르미돈(Myrmidon)",
            "Pidmer Gar": "피드메르 가르(Pidmer Gar)",
            "Rawffus the Dim": "어리숙한 라우푸스(Rawffus)",
            "Urza Fastik": "우르자(Urza) 파스티크(Fastik)",
        }
        for source, standard in expected.items():
            with self.subTest(source=source):
                self.assertEqual(by_source[source], standard)
        self.assertNotIn("말(Mal) 아카이(A’kai)", by_source["Mal A’kai"])
        self.assertNotIn("말(Mal) 므브린", by_source["Mal M’Brin"])

    def test_embedded_name_audit_does_not_repair_components_of_a_paired_name(self):
        from tools.audit_and_pair_embedded_names import (
            NamePair,
            SOURCE_PATTERNS,
            SOURCE_TRANSLATION_PATTERNS,
            TRANSLATION_PATTERNS,
            process_file,
        )
        from tempfile import TemporaryDirectory

        pairs = [
            NamePair("Mal A’kai", "말 아카이", "person_name", "Mal A’kai"),
            NamePair("A’kai", "아카이", "person_name", "A’kai"),
        ]
        original_source_patterns = SOURCE_PATTERNS.copy()
        original_translation_patterns = TRANSLATION_PATTERNS.copy()
        original_source_translation_patterns = SOURCE_TRANSLATION_PATTERNS.copy()
        with TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "sample.po"
            path.write_text(
                'msgid "Mal A’kai"\nmsgstr "말 아카이(Mal A’kai)"\n',
                encoding="utf-8",
            )
            try:
                SOURCE_PATTERNS.clear()
                TRANSLATION_PATTERNS.clear()
                SOURCE_TRANSLATION_PATTERNS.clear()
                for pair in pairs:
                    SOURCE_PATTERNS[pair.source] = re.compile(
                        r"(?<![A-Za-z0-9-])"
                        + re.escape(pair.source)
                        + r"(?![A-Za-z0-9-])"
                    )
                    TRANSLATION_PATTERNS[(pair.korean, pair.source)] = re.compile(
                        re.escape(pair.korean)
                        + r"(?P<particle>(?:은|는|이|가|을|를|의|에|로|와|과|도|만|에서|에게|으로)?)"
                        + rf"(?!{re.escape(f'({pair.source})')})"
                        + r"(?!\()"
                    )
                    SOURCE_TRANSLATION_PATTERNS[pair.source] = re.compile(
                        r"(?<![A-Za-z0-9-(])"
                        + re.escape(pair.source)
                        + r"(?P<particle>(?:은|는|이|가|을|를|의|에|로|와|과|도|만|에서|에게|으로)?)"
                        + r"(?![A-Za-z0-9-])"
                    )
                messages, unresolved = process_file(path, pairs, apply=False)
            finally:
                SOURCE_PATTERNS.clear()
                SOURCE_PATTERNS.update(original_source_patterns)
                TRANSLATION_PATTERNS.clear()
                TRANSLATION_PATTERNS.update(original_translation_patterns)
                SOURCE_TRANSLATION_PATTERNS.clear()
                SOURCE_TRANSLATION_PATTERNS.update(
                    original_source_translation_patterns
                )
        self.assertEqual(messages, 0)
        self.assertEqual(unresolved, 0)

    def test_species_names_have_a_separate_context(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        for source in ("Drakes", "Dwarves", "Elves"):
            with self.subTest(source=source):
                self.assertEqual(by_source[source]["category"], "race_name")

    def test_categories_follow_display_meaning_not_automatic_po_markers(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["category"] for row in rows}
        self.assertEqual(by_source["Dwarf Ally"], "faction")
        self.assertEqual(by_source["Troll Encampment"], "terrain")
        self.assertEqual(by_source["Troll Encampment Keep"], "terrain")
        self.assertEqual(by_source["Troll Hole"], "campaign_name")

    def test_music_is_translated_by_po_context(self):
        about = None
        preferences = None
        for path in WORK_KO.glob("*.po"):
            for block in path.read_text(encoding="utf-8").split("\n\n"):
                if 'msgid "Music"' not in block:
                    continue
                if "[about]" in block:
                    about = block
                if "[column]" in block:
                    preferences = block
        self.assertIsNotNone(about)
        self.assertIsNotNone(preferences)
        self.assertIn('msgstr "음악"', about)
        self.assertIn('msgstr "음악"', preferences)

    def test_manual_core_terms_and_prose_are_reviewed(self):
        text = "\n".join(
            exact_po_translations(WORK_KO / "wesnoth-manual-ko.po").values()
        )
        for expected in (
            "《웨스노스(Wesnoth) 전투》는 판타지를 배경으로 하는 턴제 전략 게임입니다.",
            "강력한 군대를 만들고, 풋내기 신병을 차츰 노련한 베테랑으로 훈련하십시오.",
            "체력(HP)을 8씩 잃습니다.",
            "통제 권역을 형성하며",
            "통제 권역은 유닛이 도달할 수 있는 칸과 이동 경로에 영향을 줍니다.",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)
        for rejected in (
            "웨스노스(Wesnoth)의 전쟁은 판타지적",
            "저하할 수 없는 막강한 군대",
            "1 체력(HP)가 될 때까지",
            "통제 구역을 행사하며",
        ):
            with self.subTest(rejected=rejected):
                self.assertNotIn(rejected, text)

    def test_yes_no_use_response_words_not_presence_words(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        self.assertEqual(by_source["yes"]["standard_korean"], "예")
        self.assertEqual(by_source["no"]["standard_korean"], "아니오")
        self.assertEqual(by_source["yes"]["reference_japanese"], "はい")
        self.assertEqual(by_source["no"]["reference_japanese"], "いいえ")
        self.assertEqual(by_source["yes"]["reference_chinese"], "是")
        self.assertEqual(by_source["no"]["reference_chinese"], "否")

    def test_gettext_context_prefix_is_not_displayed(self):
        cases = (
            ("female^refreshed", "여성^회복됨", "회복됨"),
            ("race^Drakes", "종족^반룡들", "반룡들"),
            ("feature^Open", "기능^열기", "열기"),
        )
        for source, translation, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(
                    normalize_translation(source, translation),
                    expected,
                )

    def test_active_context_translations_do_not_start_with_a_prefix(self):
        prefix_pattern = re.compile(r"^[^\s^]+\^")
        for path in WORK_KO.glob("*.po"):
            for block in path.read_text(encoding="utf-8").split("\n\n"):
                values = parse_field_values(block)
                source = values.get("msgid", "")
                translation = values.get("msgstr", "")
                if "^" not in source or "\n" in source or not translation:
                    continue
                # Some source strings use ^ as syntax inside a literal command
                # name; that prefix is part of the command and must remain.
                if source.startswith("command_"):
                    continue
                with self.subTest(path=path.name, source=source):
                    self.assertIsNone(prefix_pattern.match(translation))

    def test_context_normalization_is_idempotent(self):
        cases = (
            ("female^refreshed", "여성^회복됨"),
            ("race^Drakes", "종족^반룡들"),
            ("feature^Open", "기능^열기"),
            ("female^refreshed", "회복됨"),
        )
        for source, translation in cases:
            with self.subTest(source=source, translation=translation):
                normalized = normalize_translation(source, translation)
                self.assertEqual(
                    normalize_translation(source, normalized),
                    normalized,
                )

    def test_korean_spacing_normalization_does_not_touch_msgid_and_normalizes_obsolete(self):
        active = 'msgid "Example"\nmsgstr "그렇게 할것이다"'
        normalized, count = normalize_block(active)
        self.assertEqual(count, 1)
        self.assertIn('msgid "Example"', normalized)
        self.assertIn('msgstr "그렇게 할 것이다"', normalized)

        normalized_again, count_again = normalize_block(normalized)
        self.assertEqual(count_again, 0)
        self.assertEqual(normalized_again, normalized)

        obsolete = '#~ msgid "Example"\n#~ msgstr "그렇게 할것이다"'
        normalized_obsolete, count = normalize_block(obsolete)
        self.assertEqual(count, 1)
        self.assertIn('#~ msgid "Example"', normalized_obsolete)
        self.assertIn('#~ msgstr "그렇게 할 것이다"', normalized_obsolete)

    def test_korean_typo_normalization_covers_unambiguous_typos(self):
        active = 'msgid "Example"\nmsgstr "절때 난장이가 쫒아가며 댓가를 치르고 부딛혀"\n'
        normalized, count = normalize_block(active)
        self.assertEqual(count, 5)
        self.assertIn(
            'msgstr "절대 난쟁이가 쫓아가며 대가를 치르고 부딪혀"',
            normalized,
        )

    def test_korean_spacing_normalization_covers_ordinal_spacing(self):
        active = 'msgid "Example"\nmsgstr "첫번째와 세번째 대상을 선택할 수 있다"\n'
        normalized, count = normalize_block(active)
        self.assertEqual(count, 2)
        self.assertIn(
            'msgstr "첫 번째와 세 번째 대상을 선택할 수 있다"',
            normalized,
        )

    def test_korean_spacing_normalization_covers_common_time_and_future_spacing(self):
        active = (
            'msgid "Example"\n'
            'msgstr "그때 도착할거다. 온것을 확인할때까지 수백년을 기다렸다."\n'
        )
        normalized, count = normalize_block(active)
        self.assertEqual(count, 4)
        self.assertIn(
            'msgstr "그때 도착할 거다. 온 것을 확인할 때까지 수백 년을 기다렸다."',
            normalized,
        )

    def test_korean_spacing_normalization_covers_reviewed_typos(self):
        active = (
            'msgid "Example"\n'
            'msgstr "다름 이름으로 빌견되지 않은 죽은자의 흔적이 '
            '치명타가 꽃히는것처럼 보였다."\n'
        )
        normalized, count = normalize_block(active)
        self.assertEqual(count, 4)
        self.assertIn(
            'msgstr "다른 이름으로 발견되지 않은 죽은 자의 흔적이 '
            '치명타가 꽂히는 것처럼 보였다."',
            normalized,
        )

    def test_korean_spacing_normalization_covers_reviewed_compound_spacing(self):
        active = (
            'msgid "Example"\n'
            'msgstr "살아있는 자가 좀더 기다리면 또다른 길이 있는건 아니다. '
            '몇군데의 북쪽지역을 평생동안 돌아다니며 자기자신을 지켰다."\n'
        )
        normalized, count = normalize_block(active)
        self.assertEqual(count, 8)
        self.assertIn(
            'msgstr "살아 있는 자가 좀 더 기다리면 또 다른 길이 있는 건 아니다. '
            '몇 군데의 북쪽 지역을 평생 동안 돌아다니며 자기 자신을 지켰다."',
            normalized,
        )

    def test_korean_spacing_normalization_covers_recent_review_candidates(self):
        active = (
            'msgid "Example"\n'
            'msgstr "걱정하지마. 돌아 가려했는데 알고있는 사람은 없었고, '
            '전투시에 보좌해준 이가 자랑스러워 하실 거에요. '
            '며칠 뒤 씻기는게 좋겠고, 다시는 안그럴께요."\n'
        )
        normalized, _ = normalize_block(active)
        self.assertIn(
            'msgstr "걱정하지 마. 돌아가려 했는데 알고 있는 사람은 없었고, '
            '전투 시에 보좌해 준 이가 자랑스러워하실 거예요. '
            '며칠 뒤 씻기는 게 좋겠고, 다시는 안 그럴게요."',
            normalized,
        )

        unit_name, _ = normalize_block(
            'msgid "Example"\nmsgstr "어린 오우거예요."\n'
        )
        self.assertIn('msgstr "어린 오우거예요."', unit_name)

        typo_block, _ = normalize_block(
            'msgid "Example"\n'
            'msgstr "기병를 태울만큼 알려줘야해요. 한 번도 속지마십시오."\n'
        )
        self.assertIn(
            'msgstr "기병을 태울 만큼 알려 줘야 해요. 한 번도 속지 마십시오."',
            typo_block,
        )

        additional_spacing, _ = normalize_block(
            'msgid "Example"\n'
            'msgstr "영주들에의해 붙잡혔고, 있는동안 원하는게 많았지만 '
            '두려워하지마. 포기하지마. 생각하지마."\n'
        )
        self.assertIn(
            'msgstr "영주들에 의해 붙잡혔고, 있는 동안 원하는 게 많았지만 '
            '두려워하지 마. 포기하지 마. 생각하지 마."',
            additional_spacing,
        )

        obsolete, _ = normalize_block(
            '#~ msgid "Example"\n'
            '#~ msgstr "옛날에는 한강을 건넜고, 원하는게 많았다."\n'
        )
        self.assertIn(
            '#~ msgstr "옛날에는 한강을 건넜고, 원하는 게 많았다."',
            obsolete,
        )

        generated_spacing, _ = normalize_block(
            '#~ msgid "Example"\n'
            '#~ msgstr "소집 가능한한 유닛과 이동 가능한한 영역을 확인하고 가능한한 오래 버티세요."\n'
        )
        self.assertIn(
            '#~ msgstr "소집 가능한 유닛과 이동 가능한 영역을 확인하고 가능한 한 오래 버티세요."',
            generated_spacing,
        )

        prose_spacing, _ = normalize_block(
            'msgid "Example"\n'
            'msgstr "걱정되는건 가본적이 없어서야. 동료들이 가담해준 뒤 싸워주고, '
            '대장인것을 알아야해. 남아있어야해."\n'
        )
        self.assertIn(
            'msgstr "걱정되는 건 가 본 적이 없어서야. 동료들이 가담해 준 뒤 싸워 주고, '
            '대장인 것을 알아야 해. 남아 있어야 해."',
            prose_spacing,
        )

        additional_review, _ = normalize_block(
            'msgid "Example"\n'
            'msgstr "달라지는건 없어. 모든게 끝이야. 보낸지 오래됐고 있을거야. '
            '안되네. 할테니 참여 할 생각이면 가까워지는것을 피하고 서있는것을 확인해."\n'
        )
        self.assertIn(
            'msgstr "달라지는 건 없어. 모든 게 끝이야. 보낸 지 오래됐고 있을 거야. '
            '안 되네. 할 테니 참여할 생각이면 가까워지는 것을 피하고 서 있는 것을 확인해."',
            additional_review,
        )

        recent_review, _ = normalize_block(
            'msgid "Example"\n'
            'msgstr "수백개의 요새들이곳곳에 생겼다. 그 건 닫힌후 내것이 됐다. '
            '어느정도 다가가지마라. 마법사놈을 놀린거라면 못봤고 안먹힐 것이다. '
            '볼줄 알며 도끼맛을 보여주고 만들어주겠다. 걸맞는 부족들간의 싸움붙이와 '
            '잠시후 왔다갔다."\n'
        )
        self.assertIn(
            'msgstr "수백 개의 요새들이 곳곳에 생겼다. 그건 닫힌 후 내 것이 됐다. '
            '어느 정도 다가가지 마라. 마법사 놈을 놀린 거라면 못 봤고 안 먹힐 것이다. '
            '볼 줄 알며 도끼 맛을 보여 주고 만들어 주겠다. 걸맞은 부족들 간의 싸움 붙이와 '
            '잠시 후 왔다 갔다."',
            recent_review,
        )

        dependent_noun_spacing, _ = normalize_block(
            'msgid "Example"\n'
            'msgstr "그럴거다. 죽을거야. 6일동안 버티고 잠시동안 쉬었다. 세월동안 기다렸다."\n'
        )
        self.assertIn(
            'msgstr "그럴 거다. 죽을 거야. 6일 동안 버티고 잠시 동안 쉬었다. '
            '세월 동안 기다렸다."',
            dependent_noun_spacing,
        )

    def test_tarek_uses_the_korean_reference_spelling(self):
        _, rows = glossary_rows()
        tarek = next(row for row in rows if row["source_term"] == "Tarek")
        self.assertEqual(tarek["standard_korean"], "타렉(Tarek)")
        self.assertEqual(tarek["reference_japanese"], "Tarek")

    def test_main_menu_uses_the_standard_ui_term(self):
        _, rows = glossary_rows()
        main_menu = next(
            row for row in rows if row["source_term"] == "Main Menu"
        )
        self.assertEqual(main_menu["standard_korean"], "메인 메뉴")
        for path in WORK_KO.glob("*.po"):
            self.assertNotIn("기본 차림표", path.read_text(encoding="utf-8"))

    def test_menu_terms_use_menu_not_old_korean_wording(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        self.assertEqual(by_source["Menu"], "메뉴")
        self.assertEqual(by_source["Time Schedule Menu"], "시간 일정 메뉴")
        for path in WORK_KO.glob("*.po"):
            self.assertNotIn("차림표", path.read_text(encoding="utf-8"))

    def test_wml_tool_commands_keep_command_names_and_share_the_same_korean_form(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        for command in ("wmlindent", "wmllint", "wmlscope", "wmlxgettext"):
            self.assertEqual(by_source[f"Run {command}"], f"{command} 실행")
        tools_po = (WORK_KO / "wesnoth-tools-ko.po").read_text(encoding="utf-8")
        self.assertNotIn("wmlxgettext를 실행", tools_po)

    def test_tools_gui_description_has_no_stray_backtick_or_awkward_locale_wording(self):
        tools_po = (WORK_KO / "wesnoth-tools-ko.po").read_text(encoding="utf-8")
        self.assertIn(
            "언어 코드는 POSIX 로케일 이름이어야 합니다.",
            tools_po,
        )
        self.assertNotIn(
            'msgstr "`지정된 언어로 GUI.pyw를 실행합니다.',
            tools_po,
        )

    def test_non_transliterated_labels_do_not_repeat_source_in_parentheses(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        expected = {
            "AToTB": "형제",
            "Base.x": "기준점 X",
            "Base.y": "기준점 Y",
            "Clan": "일족",
            "DM": "회고",
            "DW": "바다",
            "DiD": "DiD",
            "EI": "침동",
            "Garrison": "수비군",
            "HttT": "왕자",
            "LoW": "전설",
            "Northerners": "북부인",
            "NR": "부활",
            "SotA": "고대인",
            "SotBE": "검은눈",
            "THoT": "망치",
            "TRoW": "성립",
            "Treefolk": "나무 동포",
            "TSG": "남부",
            "UtBS": "태양",
            "WoF": "바람",
        }
        for source, standard in expected.items():
            with self.subTest(source=source):
                self.assertEqual(by_source[source], standard)

    def test_glossary_labels_are_applied_to_active_po_entries(self):
        expected = {
            "AToTB": "형제",
            "Base.x": "기준점 X",
            "Base.y": "기준점 Y",
            "Northerners": "북부인",
            "Treefolk": "나무 동포",
        }
        for path in WORK_KO.glob("*.po"):
            for block in path.read_text(encoding="utf-8").split("\n\n"):
                if any(line.startswith("#~") for line in block.splitlines()):
                    continue
                values = parse_field_values(block)
                source = values.get("msgid")
                if source in expected:
                    with self.subTest(path=path.name, source=source):
                        self.assertEqual(values.get("msgstr"), expected[source])

    def test_reviewed_two_brothers_names_use_canonical_spellings(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        self.assertEqual(by_source["Maghre"]["standard_korean"], "마그레(Maghre)")
        self.assertEqual(by_source["Arvith"]["standard_korean"], "아르비쓰(Arvith)")
        self.assertEqual(by_source["Baran"]["standard_korean"], "바란(Baran)")
        self.assertEqual(by_source["Toen Caric"]["standard_korean"], "토엔 카리크(Toen Caric)")
        self.assertEqual(by_source["Arvith"]["forbidden_terms"], "아르비트")

        text = (WORK_KO / "wesnoth-tb-ko.po").read_text(encoding="utf-8")
        self.assertNotIn("마그흐레", text)
        self.assertNotIn("아르비트", text)
        self.assertNotIn("토엔 캐릭", text)
        self.assertNotIn("바라네(Baran)", text)

    def test_mal_mbrin_uses_one_bilingual_compound_name(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        self.assertEqual(
            by_source["Mal M’Brin"]["standard_korean"],
            "말 므브린(Mal M’Brin)",
        )
        text = (WORK_KO / "wesnoth-tsg-ko.po").read_text(encoding="utf-8")
        self.assertIn("말 므브린(Mal M’Brin)을 처치하십시오", text)
        self.assertIn("말 므브린(Mal M’Brin)이라 불린다", text)
        self.assertNotIn("말(Mal) 므브린", text)
        self.assertNotIn("말(Mal) M’Brin", text)
        self.assertNotIn("말(Mal) 음브린", text)

    def test_hyphenless_mal_ravanal_uses_canonical_name(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        self.assertEqual(
            by_source["Mal Ravanal"],
            "말-라바날(Mal-Ravanal)",
        )
        text = (WORK_KO / "wesnoth-ei-ko.po").read_text(encoding="utf-8")
        self.assertIn("말-라바날(Mal-Ravanal)의 수도", text)
        self.assertNotIn("말(Mal) 라바날의 수도", text)

    def test_obsolete_queen_name_pairs_only_the_name_component(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        self.assertEqual(by_source["Xeila"]["standard_korean"], "제일라(Xeila)")
        text = (WORK_KO / "wesnoth-tsg-ko.po").read_text(encoding="utf-8")
        self.assertIn('#~ msgstr "제일라(Xeila) 여왕"', text)
        self.assertIn('#~ msgstr "제일라(Xeila) 여왕을 무찔러라"', text)
        self.assertNotIn("여왕 Xeila", text)

    def test_reviewed_two_brothers_dialogue_regressions(self):
        text = (WORK_KO / "wesnoth-tb-ko.po").read_text(encoding="utf-8")
        for expected in (
            "네가 불렀고, 나는 왔다. 그걸로 만족해라.",
            "반갑소, 형님. 돌아오셨소.",
            "잘했다, 제군들! 그런데 내 아우는 어떻게 된 거지?",
            "아르비쓰(Arvith)와 그의 부대는 실종된 아우를 찾아 북쪽으로 말을 달렸다.",
            "바란(Baran), 네 형을 믿지 못한 것이냐?",
            "금화 50개예요.",
            "그대가 알던 아우의 모습만 기억하게.",
            "그대가 너무 늦기를",
            "내 칼이 네놈 목에 닿아 있다.",
            "말에 올라라. 출발한다.",
            "씨족 없는 자 로타리크(Rotharik)의 일기",
            "흑마법사는 강력한 유닛입니다.",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

        for rejected in (
            "그쪽은 안전할지 몰라도 네놈 목은",
            "어쩼든",
            "비러먹을",
            "착마하라",
            "해야할 일",
            "네가 늦지 않기를",
            "어둠의 정령마법사",
            "무소속 로타릭",
        ):
            with self.subTest(rejected=rejected):
                self.assertNotIn(rejected, text)

    def test_south_guard_campaign_summary_preserves_plural_and_natural_prose(self):
        text = (WORK_KO / "wesnoth-tsg-ko.po").read_text(encoding="utf-8")
        self.assertIn("국경의 약탈당한 마을들을 조사하기 위해", text)
        self.assertNotIn("국경의 약탈당한 마을을 조사하기 위해", text)
        self.assertNotIn("불운한 싸움", text)

    def test_sorceress_is_feminine_not_plural_and_uses_witch_terms(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        self.assertEqual(by_source["Dark Sorcerer"]["standard_korean"], "흑마법사")
        self.assertEqual(by_source["Dark Sorceress"]["standard_korean"], "흑마녀")
        self.assertEqual(by_source["Sorcerer"]["standard_korean"], "마법사")
        self.assertEqual(
            by_source["female^Elvish Sorceress"]["standard_korean"], "요정 마녀"
        )

        for path in WORK_KO.glob("*.po"):
            for block in path.read_text(encoding="utf-8").split("\n\n"):
                if any(line.startswith("#~") for line in block.splitlines()):
                    continue
                values = parse_field_values(block)
                if values.get("msgid") == "Dark Sorcerer":
                    with self.subTest(path=path.name):
                        self.assertEqual(values.get("msgstr"), "흑마법사")
                if values.get("msgid") == "Dark Sorceress":
                    with self.subTest(path=path.name):
                        self.assertEqual(values.get("msgstr"), "흑마녀")
                if values.get("msgid") == "female^Elvish Sorceress":
                    with self.subTest(path=path.name):
                        self.assertEqual(values.get("msgstr"), "요정 마녀")
                if values.get("msgstr"):
                    with self.subTest(path=path.name, msgid=values.get("msgid", "")[:40]):
                        self.assertNotIn("흑마술사", values["msgstr"])
                        if "sorcerer" in values.get("msgid", "").lower():
                            self.assertNotIn("마술사", values["msgstr"])

    def test_sorcerer_descriptions_preserve_gender_and_meaning(self):
        text = (WORK_KO / "wesnoth-units-ko.po").read_text(encoding="utf-8")
        self.assertIn(
            "흑마법이 불러일으키는 공포는 이를 둘러싼 비밀과 흉흉한 소문 때문에",
            text,
        )
        self.assertIn(
            "흑마법이 불러일으키는 공포는 보통 사람들이 그것에 대해 아는 것이 거의 없다는",
            text,
        )
        self.assertIn(
            '주인"\n"인 그녀를 절대 의심하지 않는다.',
            text,
        )
        self.assertNotIn("무기력한 물체", text)
        self.assertNotIn("첫번째 성과는 빠르고 불편한 응용", text)
        self.assertNotIn("보이기만 하면, 알아내는 것은 시간문제", text)

    def test_sorceress_prose_uses_feminine_term_consistently(self):
        nr = (WORK_KO / "wesnoth-nr-ko.po").read_text(encoding="utf-8")
        sota = (WORK_KO / "wesnoth-sota-ko.po").read_text(encoding="utf-8")
        units = (WORK_KO / "wesnoth-units-ko.po").read_text(encoding="utf-8")
        units_block = next(
            block
            for block in units.split("\n\n")
            if parse_field_values(block).get("msgid") == "The dread inspired by black magic comes chiefly from how little is known about it by the common man. Dark sorceresses have begun to unlock the secrets of life and death, the latter of which is all too easy to inflict. This labor gives the first glimmerings of the connection between the soul and inert matter, and the first successful experiments in manipulating this bond. The terrible unknown that lurks beyond death is glimpsed, and will inevitably be fathomed.\n\nDespite any design they may have of using this to wrest their own immortality from nature’s grasp, the first results of their work have immediate, and unpleasant applications. The life they breathe into dead matter can create servants for them, servants which will work, but which will also kill, and will never question their mistress. These creations have a loyalty any tyrant would dream of, and it is tempting to those with even the merest desire for power."
        )
        dark_sorceress = parse_field_values(units_block)["msgstr"]

        self.assertIn("이 어린 마녀를 손에 넣으면", nr)
        self.assertIn("빌어먹을 마녀를 구하러", nr)
        self.assertNotIn("마법사들을 넘겨주면", nr)
        self.assertNotIn("여자 마법사를 구하러", nr)
        self.assertIn("그때 엘프 마녀를 만났다.", sota)
        self.assertNotIn("그때 엘프 마법사를 만났다.", sota)
        self.assertIn("거의 없다는 데서 비롯된다.", dark_sorceress)
        self.assertIn("죽음은 너무나 쉽게", dark_sorceress)
        self.assertNotIn("없다는데서 비롯된다", dark_sorceress)
        self.assertNotIn("죽음은너무나", dark_sorceress)

    def test_reviewed_game_terms_keep_context_specific_meanings(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        self.assertEqual(by_source["MP"]["standard_korean"], "이동력(MP)")
        self.assertEqual(
            by_source["addons_of_type^MP campaigns"]["standard_korean"],
            "멀티플레이 캠페인",
        )
        self.assertEqual(
            by_source["The Battle for Wesnoth"]["standard_korean"],
            "웨스노스(Wesnoth) 전투",
        )
        self.assertEqual(
            by_source["Battle For Wesnoth Help"]["standard_korean"],
            "웨스노스(Wesnoth) 전투 도움말",
        )
        self.assertEqual(by_source["Gweddry"]["standard_korean"], "그웨드리(Gweddry)")

        ei = (WORK_KO / "wesnoth-ei-ko.po").read_text(encoding="utf-8")
        self.assertNotIn("궤드리", ei)
        self.assertNotIn("다킨", ei)
        self.assertNotIn("오웨크", ei)
        self.assertIn("그웨드리(Gweddry), 다신(Dacyn), 오와에크(Owaec)", ei)

    def test_reviewed_ui_and_prose_spacing_is_clean(self):
        targets = (
            WORK_KO / "wesnoth-ko.po",
            WORK_KO / "wesnoth-dm-ko.po",
            WORK_KO / "wesnoth-dw-ko.po",
            WORK_KO / "wesnoth-help-ko.po",
        )
        text = "\n".join(
            block
            for path in targets
            for block in path.read_text(encoding="utf-8").split("\n\n")
            if not any(line.startswith("#~") for line in block.splitlines())
        )
        for rejected in (
            "게임 내 체팅",
            "이동가능한",
            "해야할",
            "할 수있는",
            "공격해야할",
        ):
            with self.subTest(rejected=rejected):
                self.assertNotIn(rejected, text)
        self.assertIn("크렐라누(Crelanu)의 서를 연구한 끝에", text)

    def test_recent_proofreading_batch_removes_clear_typos(self):
        def active_text(path):
            return "\n\n".join(
                block
                for block in path.read_text(encoding="utf-8").split("\n\n")
                if not any(line.startswith("#~") for line in block.splitlines())
            )

        editor = active_text(WORK_KO / "wesnoth-editor-ko.po")
        core = active_text(WORK_KO / "wesnoth-ko.po")
        two_brothers = active_text(WORK_KO / "wesnoth-tb-ko.po")
        burning_suns = active_text(WORK_KO / "wesnoth-utbs-ko.po")

        for expected in (
            "다음 지도가 수정되어 있으며",
            "디렉터리명이 포함되어 있어 설치할 수 없습니다.",
            "대화명 ‘$nick’는 예약되어 있어 플레이어가 사용할 수 없습니다.",
            "(초보자 수준, 시나리오 4개.)",
            "두 전투원 중 한쪽이 쓰러지거나 30회의 공격이 끝날 때까지",
            "물론 그대들이 그 지도를 봐도 이해하기 어려울 테니",
            "당신들에게 지상으로 가는 길을 안내하고 보호하는 것쯤은",
            "남아 있는 것은 두개골과 짐승 가죽",
            "경비도 삼엄할 겁니다",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, editor + core + two_brothers + burning_suns)

        for rejected in (
            "다음의 지도이 수정",
            "있어인스톨",
            "대화명 ‘$nick’ 는",
            "4 개 시나리오",
            "어느한쪽이 쓰러질때까지",
            "믈론 그대들이",
            "남아 있는것은",
            "지키지고 있을",
        ):
            with self.subTest(rejected=rejected):
                self.assertNotIn(rejected, editor + core + two_brothers + burning_suns)

    def test_latest_proofreading_batch_removes_repeated_spacing_errors(self):
        active_text = "\n\n".join(
            block
            for path in sorted(WORK_KO.glob("*.po"))
            for block in path.read_text(encoding="utf-8").split("\n\n")
            if not any(line.startswith("#~") for line in block.splitlines())
        )
        for rejected in (
            "있는것",
            "없는것",
            "인것",
            "였을때",
            "몇분",
            "깊은곳",
            "에서서",
            "뭉쳐야합니다",
            "해야하고",
        ):
            with self.subTest(rejected=rejected):
                self.assertNotIn(rejected, active_text)

    def test_reviewed_main_ui_descriptions_use_natural_korean(self):
        text = (WORK_KO / "wesnoth-ko.po").read_text(encoding="utf-8")
        for expected in (
            "편집기의 최근 파일 메뉴에 표시할 항목의 최대 개수",
            "게임 내에서 지원 중단 메시지 표시",
            "현재 해상도의 표준 크기를 기준으로 모든 텍스트 크기를 확대하거나 축소합니다.",
            "서버 연결 해제 시간 초과",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)
        for rejected in (
            "숫자의 최대치",
            "하게합니다",
            "부정적 메시지를 게임에서 표시",
            "서버가 시간 초과로 연결 해제되었습니다",
        ):
            with self.subTest(rejected=rejected):
                self.assertNotIn(rejected, text)

    def test_reviewed_dead_water_and_northern_rebirth_prose_is_clean(self):
        dw = (WORK_KO / "wesnoth-dw-ko.po").read_text(encoding="utf-8")
        nr = (WORK_KO / "wesnoth-nr-ko.po").read_text(encoding="utf-8")
        main = (WORK_KO / "wesnoth-ko.po").read_text(encoding="utf-8")
        low = (WORK_KO / "wesnoth-low-ko.po").read_text(encoding="utf-8")

        for expected in (
            "후회하게 될 거다",
            "거주민들은 그들을 별로 반기지 않는 듯했다",
            "저주받은 검은엄니 카즈그를 기습해 죽였소",
            "당신을 구출하러 온 대규모 요정 군대",
            "죽음의 문턱에 머뭅니다",
            "계약에는 우리의 명예가 걸려 있네",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, dw + nr + main + low)

        for rejected in (
            "네놈들감히",
            "희망이없는",
            "보호되고있습니다",
            "석방 할 수",
            "죽음의 문남아",
            "원치 않든간에",
        ):
            with self.subTest(rejected=rejected):
                self.assertNotIn(rejected, dw + nr + main + low)

    def test_reviewed_under_the_burning_suns_prose_preserves_meaning(self):
        text = (WORK_KO / "wesnoth-utbs-ko.po").read_text(encoding="utf-8")
        for expected in (
            "여기는 사막이 아니야",
            "평소처럼 수적 우위도 점하기 어렵지",
            "우리 추적자들은 그들을 한 명씩 또는 소규모 무리로 쫓아가 처치했다",
            "우리 요정 동족을 거의 알아차리지 못했다",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)
        for rejected in ("다시 한 번 주의했으면해", "싸우는것을", "진여에 접근", "그 떄문에"):
            with self.subTest(rejected=rejected):
                self.assertNotIn(rejected, text)

    def test_reviewed_northern_rebirth_and_dialogue_prose(self):
        nr = (WORK_KO / "wesnoth-nr-ko.po").read_text(encoding="utf-8")
        dw = (WORK_KO / "wesnoth-dw-ko.po").read_text(encoding="utf-8")
        utbs = (WORK_KO / "wesnoth-utbs-ko.po").read_text(encoding="utf-8")

        for expected in (
            "마주치는 오크, 트롤, 해골을 모조리 구워 버려서지.",
            "지상의 인간들이 몇 년 전 오크에게 노예가 되거나 죽었다고 생각했는데.",
            "자유를 지키기 위해 옛 동맹인 난쟁이들에게 도움과 장비를 구하러 왔습니다.",
            "우리 요새에 온 것을 환영하오.",
            "아직 놈들이 우리를 눈치채지 못한 듯하오.",
            "각자의 길을 갈 때가 되었다고 생각한 모양입니다.",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, nr)
        self.assertIn("네가 겉모습과 달리 용감하고 내 도움을 받을 자격이 있음을", dw)
        self.assertIn(
            "나와 내 백성을 위협하는 자들에게 나 자신을 넘기지는 않겠다.",
            utbs,
        )
        self.assertNotIn("원하신다면 저를 죽이십시오.", utbs)

    def test_reviewed_northern_rebirth_opening_keeps_meaning(self):
        text = (WORK_KO / "wesnoth-nr-ko.po").read_text(encoding="utf-8")
        for expected in (
            "이곳은 난쟁이 동굴 입구 중 하나구나.",
            "주인님께 알려야겠어.",
            "나는 이제 죽지만, 자유인으로 죽는다!",
            "별로 영리한 놈은 아니었지, 그렇지?",
            "새로 얻은 자유에 대한 사람들의 기쁨을 억누를 수 없었다.",
            "탈린(Tallin)만은 침통한 표정이었다.",
            "크날가(Knalga) 침공 때 죽은 난쟁이들이 이제 언데드가 되어",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)
        self.assertNotIn("입구중", text)
        self.assertNotIn("그렇게 대단한 놈도 아니구나", text)

    def test_reviewed_dead_water_opening_preserves_narrative_meaning(self):
        text = (WORK_KO / "wesnoth-dw-ko.po").read_text(encoding="utf-8")
        for expected in (
            "당신은 카이 크렐리스(Kai Krellis)입니다.",
            "(중급 난이도, 10개 시나리오.)",
            "인어 도시 조타(Jotha)가 있습니다.",
            "오크 다섯 명을 쓰러뜨렸습니다.",
            "실라나(Cylanna)는 그의 아버지의 친구였고",
            "죽음과 부패의 냄새가 납니다.",
            "이번이 지도자로서 치르는 첫 시험입니다.",
            "강령술사의 시체에서 솟아나",
            "스스로 리치가 된 위대한 인간 마법사",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)
        self.assertNotIn("죽은 시체", text)
        self.assertNotIn("현자 마법사", text)

    def test_reviewed_burning_suns_history_prose_uses_natural_mage_terms(self):
        text = (WORK_KO / "wesnoth-utbs-ko.po").read_text(encoding="utf-8")
        for expected in (
            "초대 왕의 젊은 후손이",
            "마법을 다루기 위해 여전히 열심히 수련하는 마법사들",
            "웨스노스(Wesnoth) 제국의 중심부가 완전히 파괴되었습니다.",
            "섬들이 줄지어 있습니다.",
            "배들이 교역품과 소식을 싣고 본토를 자주 오갔습니다.",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)
        self.assertNotIn("마술사들은 두 번째 산", text)
        self.assertNotIn("연이은의 섬들", text)
        self.assertNotIn("파괴 되버렸어요", text)

    def test_lisar_keeps_the_canonical_bilingual_spelling(self):
        path = WORK_KO / "wesnoth-httt-ko.po"
        text = path.read_text(encoding="utf-8")
        self.assertIn(
            'msgid "Death of Li’sar"\nmsgstr "리사르(Li’sar)의 죽음"',
            text,
        )
        self.assertNotIn('msgstr "Li\'sar의 죽음"', text)

    def test_reviewed_name_overrides_cover_truncated_and_long_prose_names(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        self.assertEqual(by_source["Deora—"]["standard_korean"], "데오라—")
        self.assertEqual(
            by_source["Mal A’kai"]["standard_korean"],
            "말 아카이(Mal A’kai)",
        )
        self.assertEqual(
            by_source["Ruaskkolin"]["standard_korean"],
            "라스코쿠린(Ruaskkolin)",
        )
        self.assertEqual(
            by_source["Alavynne"]["standard_korean"],
            "알라빈(Alavynne)",
        )

        tsg = (WORK_KO / "wesnoth-tsg-ko.po").read_text(encoding="utf-8")
        multiplayer = (
            WORK_KO / "wesnoth-multiplayer-ko.po"
        ).read_text(encoding="utf-8")
        self.assertIn('msgstr "데오라—"', tsg)
        self.assertIn('msgstr "말 아카이(Mal A’kai)"', tsg)
        self.assertNotIn('msgstr "말(Mal) 아카이(A’kai)"', tsg)
        for expected in (
            "시르스즈크(Syrsszk)",
            "리스릴레로즈크(Rysssrylosszkk)",
            "라스코쿠린(Ruaskkolin)",
            "차크소(Chak’kso)",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, multiplayer)

        units = (WORK_KO / "wesnoth-units-ko.po").read_text(encoding="utf-8")
        self.assertIn("알라빈(Alavynne)의 군사들에게", units)

    def test_name_override_pairing_is_idempotent_and_not_nested(self):
        from tools.apply_name_translation_overrides import (
            replace_unpaired_name_tokens,
        )

        source = (
            "시르스즈크(시르스즈크(시르스즈크(Syrsszk))) 출신의 "
            "시크리스(Xikkrisx)는 차크소(Chak’kso)를 만났다."
        )
        expected = (
            "시르스즈크(Syrsszk) 출신의 시크리스(Xikkrisx)는 "
            "차크소(Chak’kso)를 만났다."
        )
        once = replace_unpaired_name_tokens(source)
        twice = replace_unpaired_name_tokens(once)
        self.assertEqual(once, expected)
        self.assertEqual(twice, expected)

    def test_barag_gor_is_paired_in_all_active_contexts(self):
        for path in WORK_KO.glob("*.po"):
            for block in path.read_text(encoding="utf-8").split("\n\n"):
                if any(line.startswith("#~") for line in block.splitlines()):
                    continue
                values = parse_field_values(block)
                if "Barag Gór" not in values.get("msgid", ""):
                    continue
                with self.subTest(path=path.name, msgid=values["msgid"][:60]):
                    self.assertIn(
                        "바락 고르(Barag Gór)",
                        values.get("msgstr", ""),
                    )
                    self.assertNotIn(
                        "바락 고르(Barag Gór)(Barag Gór)",
                        values.get("msgstr", ""),
                    )

    def test_parser_error_messages_are_translated_without_changing_placeholders(self):
        source = "Found invalid closing tag [/$tag2] for tag [$tag1]"
        expected = "[$tag1] 태그에 잘못된 닫기 태그 [/$tag2]"

        path = WORK_KO / "wesnoth-ko.po"
        for block in path.read_text(encoding="utf-8").split("\n\n"):
            values = parse_field_values(block)
            if values.get("msgid") == source:
                self.assertEqual(values.get("msgstr"), expected)
                return
        self.fail(f"missing active msgid: {source}")

    def test_wesnoth_calendar_formats_are_consistent_and_translated(self):
        expected = {
            "$year BW": "웨스노스 건국 전 $year년",
            "$year YW": "웨스노스력 $year년",
            "$year BF": "웨스노스 몰락 전 $year년",
            "$year AF": "웨스노스 몰락 후 $year년",
        }
        text = (WORK_KO / "wesnoth-ko.po").read_text(encoding="utf-8")
        for source, translation in expected.items():
            with self.subTest(source=source):
                self.assertIn(f'msgid "{source}"\nmsgstr "{translation}"', text)

    def test_great_river_uses_the_canonical_name_in_active_translations(self):
        old_name = re.compile(
            r"(?<![가-힣])(한강|대하)(에서|으로|까지|보다|처럼|을|를|이|가|은|는|의|에|와|과|도|로|만)?"
            r"(?![가-힣])"
        )
        for path in WORK_KO.glob("*.po"):
            for block in path.read_text(encoding="utf-8").split("\n\n"):
                if any(line.startswith("#~") for line in block.splitlines()):
                    continue
                values = parse_field_values(block)
                if not re.search(
                    r"\bgreat river\b", values.get("msgid", ""), re.IGNORECASE
                ):
                    continue
                with self.subTest(path=path.name, msgid=values["msgid"][:60]):
                    self.assertIsNone(old_name.search(values.get("msgstr", "")))

    def test_great_river_normalization_does_not_change_word_substrings(self):
        from tools.normalize_great_river import normalize_translation

        text = "거대하다. 광대하여. 대하를 건넌다."
        self.assertEqual(
            normalize_translation(text),
            "거대하다. 광대하여. 위대한 강을 건넌다.",
        )
        self.assertEqual(
            normalize_translation(
                "위대한 강를 건너고, 위대한 강와 웰딘 강이 만난다."
            ),
            "위대한 강을 건너고, 위대한 강과 웰딘 강이 만난다.",
        )

    def test_known_name_normalization_does_not_replace_common_korean_words(self):
        from tools.normalize_known_name_spellings import update_po

        path = ROOT / "tests" / "_known_name_normalization_fixture.po"
        path.write_text(
            'msgid "I hope you do not."\n'
            'msgstr "그러지 않기를 바라네."\n\n'
            'msgid "Baran returned."\n'
            'msgstr "바라네(Baran)가 돌아왔다."\n\n'
            'msgid "Dacyn returned."\n'
            'msgstr "다친(Dacyn)이 돌아왔다."\n\n'
            'msgid "The wounded unit."\n'
            'msgstr "다친 유닛."\n',
            encoding="utf-8",
        )
        try:
            self.assertEqual(update_po(path), 2)
            text = path.read_text(encoding="utf-8")
        finally:
            path.unlink()

        self.assertIn('msgstr "그러지 않기를 바라네."', text)
        self.assertIn('msgstr "바란(Baran)가 돌아왔다."', text)
        self.assertIn('msgstr "다신(Dacyn)이 돌아왔다."', text)
        self.assertIn('msgstr "다친 유닛."', text)

    def test_toen_caric_uses_one_bilingual_place_name_spelling(self):
        _, rows = glossary_rows()
        toen_caric = next(
            row for row in rows if row["source_term"] == "Toen Caric"
        )
        self.assertEqual(
            toen_caric["standard_korean"],
            "토엔 카리크(Toen Caric)",
        )
        po = (WORK_KO / "wesnoth-tb-ko.po").read_text(encoding="utf-8")
        self.assertNotIn("토엔 캐릭", po)
        self.assertIn("토엔 카리크(Toen Caric)", po)
        self.assertNotIn('msgstr "Toen Caric', po)

    def test_newly_reviewed_proper_names_are_transliterated(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        expected = {
            "Managa’Gwin": "마나가 그윈(Managa’Gwin)",
            "Usadar Q’kai": "우사다르 쿠카이(Usadar Q’kai)",
            "WoCopedia": "WoC 백과사전",
        }
        for source, translation in expected.items():
            with self.subTest(source=source):
                self.assertEqual(by_source[source]["standard_korean"], translation)

    def test_named_entities_declared_by_po_ids_are_paired(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        expected = {
            "Mordak": "모르닥(Mordak)",
            "Morogor": "모로고르(Morogor)",
            "Mortic": "모르틱(Mortic)",
        }
        for source, translation in expected.items():
            with self.subTest(source=source):
                self.assertEqual(by_source[source]["standard_korean"], translation)

    def test_compound_name_pairing_keeps_titles_and_modifiers_outside_parentheses(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        expected = {
            "Ford of Alyas": ("알리아스(Alyas)의 여울", "place_name"),
            "Ford of Tifranur": ("티프라누르(Tifranur)의 여울", "place_name"),
            "Reeve Hoban": ("호반(Hoban) 행정관", "person_name"),
            "Vash-Gorn": ("바시-고른(Vash-Gorn)", "person_name"),
            "North Knalga": ("북부 크날가(Knalga)", "place_name"),
            "Chief Bir-brish": ("족장 비르-브리시(Bir-brish)", "person_name"),
            "Ur-Thorodor": ("우르-토로도르(Ur-Thorodor)", "person_name"),
        }
        for source, (translation, category) in expected.items():
            with self.subTest(source=source):
                self.assertEqual(by_source[source]["standard_korean"], translation)
                self.assertEqual(by_source[source]["category"], category)

    def test_single_token_proper_names_are_paired(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        self.assertEqual(by_source["Dolmannumbil"], "돌만눔빌(Dolmannumbil)")

    def test_parenthetical_audit_accepts_name_components(self):
        self.assertTrue(
            parenthetical_is_source_component("Garard", "Garard’s Hold")
        )
        self.assertTrue(
            parenthetical_is_source_component("Wyrm", "Cave Wyrmlet")
        )
        self.assertFalse(parenthetical_is_source_component("urgh", "Üurgh"))

    def test_common_words_are_not_paired_as_proper_names(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        self.assertEqual(by_source["Dream"], "꿈")
        self.assertEqual(by_source["Drought"], "가뭄")
        self.assertEqual(by_source["Diff"], "차이점")
        self.assertEqual(by_source["ENLIGHTENED"], "깨달음")
        self.assertEqual(by_source["Northlands"], "북부 지방")
        self.assertEqual(by_source["WC2 Invest"], "WC2 투자")
        self.assertEqual(by_source["Dream"], "꿈")
        self.assertEqual(
            next(row for row in rows if row["source_term"] == "Dream")["category"],
            "term",
        )

    def test_embedded_name_audit_pairs_raw_english_names(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        self.assertEqual(by_source["Deoran"], "데오란(Deoran)")
        self.assertEqual(
            by_source["Return to Kerlath"],
            "케를라스(Kerlath)로 귀환",
        )

    def test_embedded_name_candidate_audit_finds_unregistered_names(self):
        from tools.audit_and_pair_embedded_names import find_candidates

        path = ROOT / "tests" / ".tmp-name-candidate.po"
        path.write_text(
            'msgid "The village of Xandor is under attack."\n'
            'msgstr "Xandor 마을이 공격받고 있습니다."\n',
            encoding="utf-8",
        )
        try:
            candidates = find_candidates(path)
            self.assertEqual([candidate.source for candidate in candidates], ["Xandor"])
            self.assertFalse(candidates[0].obsolete)
        finally:
            path.unlink()

    def test_embedded_name_candidates_distinguish_obsolete_entries(self):
        from tools.audit_and_pair_embedded_names import find_candidates

        path = ROOT / "tests" / ".tmp-obsolete-name-candidate.po"
        path.write_text(
            '#~ msgid "Xandor"\n'
            '#~ msgstr "Xandor"\n',
            encoding="utf-8",
        )
        try:
            candidates = find_candidates(path)
            self.assertEqual([candidate.source for candidate in candidates], ["Xandor"])
            self.assertTrue(candidates[0].obsolete)
        finally:
            path.unlink()

    def test_embedded_name_candidate_audit_accepts_fixed_maghre(self):
        from tools.audit_and_pair_embedded_names import find_candidates, load_pairs

        pairs, conflicts = load_pairs(GLOSSARY)
        self.assertFalse(conflicts)
        candidates = find_candidates(
            ROOT / "work" / VERSION / "ko" / "wesnoth-tb-ko.po"
        )
        self.assertNotIn("Maghre", {candidate.source for candidate in candidates})

    def test_embedded_name_candidate_audit_ignores_bilingual_parentheses(self):
        from tools.audit_and_pair_embedded_names import find_candidates

        path = ROOT / "tests" / ".tmp-bilingual-name.po"
        path.write_text(
            'msgid "Barag Gór is ahead."\n'
            'msgstr "바락 고르(Barag Gór)가 앞에 있다."\n',
            encoding="utf-8",
        )
        try:
            self.assertEqual(find_candidates(path), [])
        finally:
            path.unlink()

    def test_embedded_name_audit_does_not_skip_long_prose_with_many_commas(self):
        from tools.audit_and_pair_embedded_names import find_candidates

        path = ROOT / "tests" / ".tmp-long-name-candidate.po"
        path.write_text(
            'msgid "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, '
            'P, Q, R, S, T, Xandor."\n'
            'msgstr "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, '
            'P, Q, R, S, T, Xandor."\n',
            encoding="utf-8",
        )
        try:
            candidates = find_candidates(path)
            self.assertEqual([candidate.source for candidate in candidates], ["Xandor"])
        finally:
            path.unlink()

    def test_compound_name_components_are_available_for_prose(self):
        from tools.audit_and_pair_embedded_names import load_pairs

        pairs, conflicts = load_pairs(GLOSSARY)
        self.assertFalse(conflicts)
        pair_map = {(pair.source, pair.korean) for pair in pairs}
        self.assertIn(("Darken", "다켄"), pair_map)
        self.assertIn(("Volk", "볼크"), pair_map)
        self.assertNotIn(("Minister", "에드렌"), pair_map)

    def test_whole_compound_name_is_paired_once(self):
        from tools.audit_and_pair_embedded_names import (
            SOURCE_PATTERNS,
            SOURCE_TRANSLATION_PATTERNS,
            TRANSLATION_PATTERNS,
            load_pairs,
            process_file,
        )

        pairs, conflicts = load_pairs(GLOSSARY)
        self.assertFalse(conflicts)
        path = ROOT / "tests" / ".tmp-mal-tath.po"
        original_source_patterns = SOURCE_PATTERNS.copy()
        original_translation_patterns = TRANSLATION_PATTERNS.copy()
        original_source_translation_patterns = SOURCE_TRANSLATION_PATTERNS.copy()
        path.write_text(
            'msgid "Mal Tath arrives."\n'
            'msgstr "말 타쓰가 도착했다."\n',
            encoding="utf-8",
        )
        try:
            SOURCE_PATTERNS.clear()
            TRANSLATION_PATTERNS.clear()
            SOURCE_TRANSLATION_PATTERNS.clear()
            for pair in pairs:
                SOURCE_PATTERNS[pair.source] = re.compile(
                    r"(?<![A-Za-z0-9-])"
                    + re.escape(pair.source)
                    + r"(?![A-Za-z0-9-])"
                )
                TRANSLATION_PATTERNS[(pair.korean, pair.source)] = re.compile(
                    re.escape(pair.korean)
                    + r"(?P<particle>(?:은|는|이|가|을|를|의|에|로|와|과|도|만|에서|에게|으로)?)"
                    + rf"(?!{re.escape(f'({pair.source})')})"
                    + r"(?!\()"
                )
                SOURCE_TRANSLATION_PATTERNS[pair.source] = re.compile(
                    r"(?<![A-Za-z0-9-(])"
                    + re.escape(pair.source)
                    + r"(?P<particle>(?:은|는|이|가|을|를|의|에|로|와|과|도|만|에서|에게|으로)?)"
                    + r"(?![A-Za-z0-9-])"
                )
            messages, unresolved = process_file(path, pairs, apply=True)
            self.assertEqual((messages, unresolved), (1, 0))
            self.assertIn(
                'msgstr "말 타쓰(Mal Tath)가 도착했다."',
                path.read_text(encoding="utf-8"),
            )
        finally:
            path.unlink()
            SOURCE_PATTERNS.clear()
            SOURCE_PATTERNS.update(original_source_patterns)
            TRANSLATION_PATTERNS.clear()
            TRANSLATION_PATTERNS.update(original_translation_patterns)
            SOURCE_TRANSLATION_PATTERNS.clear()
            SOURCE_TRANSLATION_PATTERNS.update(
                original_source_translation_patterns
            )

    def test_hyphenated_compound_name_keeps_the_korean_hyphen(self):
        from tools.audit_and_pair_embedded_names import load_pairs

        pairs, conflicts = load_pairs(GLOSSARY)
        self.assertFalse(conflicts)
        pair_map = {(pair.source, pair.korean) for pair in pairs}
        self.assertIn(("Mal-Ravanal", "말-라바날"), pair_map)

    def test_compound_unit_keeps_translated_race_name_unpaired(self):
        from tools.audit_and_pair_embedded_names import (
            configure_patterns,
            load_pairs,
            process_file,
        )

        path = ROOT / "tests" / ".tmp-naga-myrmidon.po"
        path.write_text(
            'msgid "Naga Myrmidon"\n'
            'msgstr "나가(Naga) 미르미돈"\n',
            encoding="utf-8",
        )
        try:
            pairs, conflicts = load_pairs(GLOSSARY)
            self.assertFalse(conflicts)
            configure_patterns(pairs)
            process_file(path, pairs, apply=True)
            self.assertEqual(
                path.read_text(encoding="utf-8"),
                'msgid "Naga Myrmidon"\n'
                'msgstr "나가 미르미돈(Myrmidon)"',
            )
        finally:
            path.unlink()

    def test_embedded_name_audit_skips_wml_name_generators(self):
        from tools.audit_and_pair_embedded_names import process_file

        sample = (
            'msgid ""\n'
            '"main={prefix}{suffix}\\n"\n'
            'msgstr ""\n'
            '"prefix=Ali|Ama\\n"\n'
        )
        path = ROOT / "tests" / ".tmp-name-generator.po"
        path.write_text(sample, encoding="utf-8")
        try:
            messages, unresolved = process_file(path, [], apply=False)
            self.assertEqual((messages, unresolved), (0, 0))
        finally:
            path.unlink()

    def test_embedded_name_audit_skips_generated_random_name_lists(self):
        from tools.audit_and_pair_embedded_names import find_candidates

        names = ",".join(
            [
                "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta",
                "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu",
                "Xi", "Omicron", "Pi", "Rho", "Sigma", "Tau", "Lollyra",
                "Upsilon", "Phi",
            ]
        )
        path = ROOT / "tests" / ".tmp-random-name-list.po"
        path.write_text(
            "#: data/campaigns/World_Conquest/lua/game_mechanics/random_names.lua:2\n"
            f'msgid "{names}"\n'
            f'msgstr "{names}"\n',
            encoding="utf-8",
        )
        try:
            self.assertEqual(find_candidates(path), [])
        finally:
            path.unlink()

    def test_embedded_name_audit_skips_core_generated_name_lists(self):
        from tools.audit_and_pair_embedded_names import find_candidates

        names = ",".join(
            [
                "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta",
                "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu",
                "Xi", "Omicron", "Pi", "Rho", "Sigma", "Tau", "Lollyra",
                "Upsilon", "Phi",
            ]
        )
        path = ROOT / "tests" / ".tmp-core-name-list.po"
        path.write_text(
            "#. Generator for male drake names\n"
            "#: data/core/macros/names.cfg:22\n"
            f'msgid "{names}"\n'
            f'msgstr "{names}"\n',
            encoding="utf-8",
        )
        try:
            self.assertEqual(find_candidates(path), [])
        finally:
            path.unlink()

    def test_embedded_name_audit_includes_obsolete_translations(self):
        from tools.audit_and_pair_embedded_names import process_file

        sample = (
            '#~ msgid "A young Knight, Deoran, served King Haldric."\n'
            '#~ msgstr "젊은 기사 Deoran은 Haldric 왕을 섬겼다."\n'
        )
        path = ROOT / "tests" / ".tmp-obsolete-name.po"
        path.write_text(sample, encoding="utf-8")
        try:
            messages, unresolved = process_file(path, [], apply=False)
            self.assertEqual((messages, unresolved), (0, 0))
        finally:
            path.unlink()

    def test_obsolete_name_pairing_preserves_obsolete_prefix(self):
        from tools.audit_and_pair_embedded_names import (
            NamePair,
            process_file,
            SOURCE_PATTERNS,
            TRANSLATION_PATTERNS,
            SOURCE_TRANSLATION_PATTERNS,
        )

        sample = (
            '#~ msgid "Deoran met Haldric."\n'
            '#~ msgstr "Deoran은 Haldric을 만났다."\n'
        )
        path = ROOT / "tests" / ".tmp-obsolete-name.po"
        path.write_text(sample, encoding="utf-8")
        pair_deoran = NamePair("Deoran", "데오란", "person_name", "Deoran")
        pair_hal = NamePair("Haldric", "할드릭", "person_name", "Haldric")
        SOURCE_PATTERNS.update(
            {
                "Deoran": re.compile(r"(?<![A-Za-z0-9-])Deoran(?![A-Za-z0-9-])"),
                "Haldric": re.compile(r"(?<![A-Za-z0-9-])Haldric(?![A-Za-z0-9-])"),
            }
        )
        TRANSLATION_PATTERNS.update(
            {
                ("데오란", "Deoran"): re.compile(r"데오란(?P<particle>(?:은|는)?)"),
                ("할드릭", "Haldric"): re.compile(r"할드릭(?P<particle>(?:을|를)?)"),
            }
        )
        SOURCE_TRANSLATION_PATTERNS.update(
            {
                "Deoran": re.compile(
                    r"(?<![A-Za-z0-9-(])Deoran(?P<particle>(?:은|는)?)"
                    r"(?![A-Za-z0-9-])"
                ),
                "Haldric": re.compile(
                    r"(?<![A-Za-z0-9-(])Haldric(?P<particle>(?:을|를)?)"
                    r"(?![A-Za-z0-9-])"
                ),
            }
        )
        try:
            messages, unresolved = process_file(
                path,
                [pair_deoran, pair_hal],
                apply=True,
            )
            self.assertEqual((messages, unresolved), (1, 0))
            result = path.read_text(encoding="utf-8")
            self.assertIn(
                '#~ msgstr "데오란(Deoran)은 할드릭(Haldric)을 만났다."',
                result,
            )
        finally:
            path.unlink()

    def test_obsolete_fuzzy_name_pairing_is_not_skipped(self):
        from tools.audit_and_pair_embedded_names import (
            NamePair,
            process_file,
            SOURCE_PATTERNS,
            TRANSLATION_PATTERNS,
            SOURCE_TRANSLATION_PATTERNS,
        )

        sample = (
            "#, fuzzy\n"
            '#~| msgid "Deoran met Haldric."\n'
            '#~ msgid "Deoran met Haldric."\n'
            '#~ msgstr "Deoran은 Haldric을 만났다."\n'
        )
        path = ROOT / "tests" / ".tmp-obsolete-fuzzy-name.po"
        path.write_text(sample, encoding="utf-8")
        pairs = [
            NamePair("Deoran", "데오란", "person_name", "Deoran"),
            NamePair("Haldric", "할드릭", "person_name", "Haldric"),
        ]
        SOURCE_PATTERNS.update(
            {
                "Deoran": re.compile(r"(?<![A-Za-z0-9-])Deoran(?![A-Za-z0-9-])"),
                "Haldric": re.compile(r"(?<![A-Za-z0-9-])Haldric(?![A-Za-z0-9-])"),
            }
        )
        TRANSLATION_PATTERNS.update(
            {
                ("데오란", "Deoran"): re.compile(r"데오란(?P<particle>(?:은|는)?)"),
                ("할드릭", "Haldric"): re.compile(r"할드릭(?P<particle>(?:을|를)?)"),
            }
        )
        SOURCE_TRANSLATION_PATTERNS.update(
            {
                "Deoran": re.compile(
                    r"(?<![A-Za-z0-9-(])Deoran(?P<particle>(?:은|는)?)"
                    r"(?![A-Za-z0-9-])"
                ),
                "Haldric": re.compile(
                    r"(?<![A-Za-z0-9-(])Haldric(?P<particle>(?:을|를)?)"
                    r"(?![A-Za-z0-9-])"
                ),
            }
        )
        try:
            messages, unresolved = process_file(path, pairs, apply=True)
            self.assertEqual((messages, unresolved), (1, 0))
            self.assertIn(
                '#~ msgstr "데오란(Deoran)은 할드릭(Haldric)을 만났다."',
                path.read_text(encoding="utf-8"),
            )
        finally:
            path.unlink()

    def test_zone_of_control_keeps_the_standard_acronym(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        self.assertEqual(
            by_source["Zone of Control"]["standard_korean"],
            "통제 권역(ZOC)",
        )
        self.assertIn("통제 권역", by_source["Zone of Control"]["forbidden_terms"])

    def test_single_token_faction_names_are_paired(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        self.assertEqual(by_source["Dulalas"], "둘라라스(Dulalas)")

    def test_name_pairing_keeps_particles_outside_parentheses(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        expected = {
            "Garard II": "가라르드(Garard) 2세",
            "Garard’s Hold": "가라르드(Garard)의 요새",
            "Great Chief Brurbar": "대족장 브루르바르(Brurbar)",
            "Gnarl": "그나(Gnarl)",
            "Howgarth III": "호우가르쓰(Howgarth) 3세",
            "Inky": "잉키(Inky)",
            "Kergai": "케르가(Kergai)",
            "Limit FPS": "FPS 제한",
            "Lord Bayar": "바야르(Bayar) 경",
            "Press ESC to skip": "ESC를 눌러 건너뛰기",
            "Rampant Graak": "화난 그라크(Graak)",
            "Rampant Grook": "화난 그루크(Grook)",
            "Rampant Gruak": "화난 그루아크(Gruak)",
            "Return to Kerlath": "케를라스(Kerlath)로 귀환",
            "Sir Alric": "알릭(Alric) 경",
            "Sir Daryn": "다린(Daryn) 경",
            "Sir Kaylan": "케일런(Kaylan) 경",
            "Sir Ruga": "루가(Ruga) 경",
            "The Princess of Wesnoth": "웨스노스(Wesnoth)의 공주",
            "Westin Guard": "웨스틴(Westin) 수비대",
            "feature^Cocoa notifications back end": "Cocoa 알림 백엔드",
            "feature^D-Bus notifications back end": "D-Bus 알림 백엔드",
            "feature^Win32 notifications back end": "Win32 알림 백엔드",
            "female^Inky": "암컷 잉키(Inky)",
            "teamname^Inky": "잉키(Inky)",
            "Talking to Tyegëa": "티에게아(Tyegëa)와 대화",
            "Tyegëa": "티에게아(Tyegëa)",
            "Tyegëa and Priestesses": "티에게아(Tyegëa)와 여제사장들",
        }
        for source, translation in expected.items():
            with self.subTest(source=source):
                self.assertEqual(by_source[source], translation)
                self.assertNotRegex(translation, r"\)[가-힣]*(?:이|가|은|는|을|를|에)$")

    def test_generic_dwarf_units_are_not_proper_names(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        for source, korean in {
            "Dwarf Grenadier": "난쟁이 폭탄투척병",
            "Dwarf Hermit": "난쟁이 은둔자",
        }.items():
            with self.subTest(source=source):
                self.assertEqual(by_source[source]["category"], "unit_name")
                self.assertEqual(by_source[source]["standard_korean"], korean)

    def test_compound_proper_names_pair_only_the_name_component(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        expected = {
            "Bones of Malin Keshar": "말린 케샤르(Malin Keshar)의 뼈",
            "Flesh of Malin Keshar": "말린 케샤르(Malin Keshar)의 살점",
            "Lady Dionli": "디온리(Dionli) 부인",
            "Lady Jessene": "제세네(Jessene) 부인",
            "Lady Karae": "카라에(Karae) 여사",
            "Lord Asaeri": "아사에리(Asaeri) 군주",
            "Minion of Tairach": "타이라크(Tairach)의 졸개",
            "Minister Alanafel": "알라나펠(Alanafel) 장관",
            "Minister Edren": "에드렌(Edren) 목사",
            "Minister Hylas": "힐라스(Hylas) 목사",
            "Minister Mefel": "메펠(Mefel) 목사",
            "Minister Romand": "로만드(Romand) 목사",
            "Neki the Brutal": "잔혹한 네키(Neki)",
            "Novice Dani": "초보자 다니(Dani)",
            "Novice Iona": "초보자 이오나(Iona)",
            "Novice Pior": "초보자 피오르(Pior)",
            "Princess Mew": "메유(Mew) 공주",
            "Soul of Malin Keshar": "말린 케샤르(Malin Keshar)의 영혼",
            "Telemon the Slayer": "살해자 텔레몬(Telemon)",
            "Uncle Somf": "솜프(Somf) 삼촌",
        }
        for source, translation in expected.items():
            with self.subTest(source=source):
                self.assertEqual(by_source[source], translation)

    def test_compound_keys_are_never_paired_as_a_whole(self):
        _, rows = glossary_rows()
        compound = re.compile(
            r"^(?:Lady|Lord|Minister|Novice|Princess|Sir|Uncle)\s+"
            r"|\b(?:of|the)\b|[’']s\b"
        )
        for row in rows:
            source = row["source_term"]
            if not compound.search(source):
                continue
            with self.subTest(source=source):
                self.assertNotIn(f"({source})", row["standard_korean"])

    def test_transliterated_unit_component_is_paired(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        self.assertEqual(by_source["Mermaid Siren"], "인어 세이렌(Siren)")
        self.assertEqual(by_source["Masked Dwarf"], "가면 쓴 난쟁이")
        self.assertEqual(by_source["Merman Triton"], "인어 트리톤(Triton)")
        self.assertEqual(by_source["Ancient Lich"], "고대의 리치(Lich)")
        self.assertEqual(by_source["Cave Wyrmlet"], "동굴 웜(Wyrm) 새끼")

    def test_lich_lord_pairs_only_the_person_name(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        self.assertEqual(
            by_source["Lich-Lord Jevyan"],
            "리치 군주 제비안(Jevyan)",
        )
        self.assertEqual(
            by_source["Lich-Lord Lenvan"],
            "리치 군주 렌반(Lenvan)",
        )

    def test_place_name_pairs_only_the_name_component(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row["standard_korean"] for row in rows}
        expected = {
            "Karmarth Hills": "카르마쓰(Karmarth) 언덕",
            "Brightleaf Wood": "빛나는 이파리(Brightleaf) 숲",
            "Clearwater Lake": "맑은물(Clearwater) 호수",
            "Estmark Hills": "샛자리(Estmark) 산맥",
            "Fort Brell": "브렐(Brell) 성채",
            "Fort Miryen": "미리엔(Miryen) 성채",
            "Gryphon Mountain": "그리폰(Gryphon) 산맥",
            "Heart Mountains": "하트(Heart) 산맥",
            "Lake Naga": "나가(Naga) 호수",
            "River Longlier": "롱리어(Longlier) 강",
            "River Telfar": "텔파르(Telfar) 강",
            "Southwind Wood": "마파람(Southwind) 숲",
            "Westwind Wood": "하늬바람(Westwind) 숲",
        }
        for source, translation in expected.items():
            with self.subTest(source=source):
                self.assertEqual(by_source[source], translation)

    def test_english_only_proper_names_are_transliterated_or_explicit_exceptions(self):
        _, rows = glossary_rows()
        external = {"Discord", "IRC", "Reddit", "SoF", "Steam", "WC"}
        contexts = {
            "person_name",
            "place_name",
            "unit_name",
            "faction",
            "race_name",
            "campaign_name",
            "proper_noun",
        }
        for row in rows:
            if row["category"] not in contexts:
                continue
            source = row["source_term"]
            with self.subTest(source=source):
                if source in external:
                    self.assertEqual(row["standard_korean"], source)
                elif row["standard_korean"] == source:
                    self.fail(f"internal proper name was left in English: {source}")

    def test_wml_tool_names_are_not_semantically_expanded(self):
        _, rows = glossary_rows()
        by_source = {row["source_term"]: row for row in rows}
        expected = {
            "wmlindent": "wmlindent",
            "wmllint": "wmllint",
            "wmlscope": "wmlscope",
            "wmlindent mode": "wmlindent 모드",
            "wmllint mode": "wmllint 모드",
            "wmlindent options": "wmlindent 옵션",
            "wmllint options": "wmllint 옵션",
            "wmlscope options": "wmlscope 옵션",
            "Run wmlindent": "wmlindent 실행",
            "Run wmllint": "wmllint 실행",
            "Run wmlscope": "wmlscope 실행",
        }
        for source, translation in expected.items():
            with self.subTest(source=source):
                self.assertIn(source, by_source)
                self.assertEqual(by_source[source]["standard_korean"], translation)
                self.assertNotIn("교정", by_source[source]["standard_korean"])

    def test_glossary_candidate_filter_excludes_dialogue(self):
        self.assertTrue(is_glossary_candidate("Run wmllint"))
        self.assertTrue(is_glossary_candidate("Find Gweddry, Dacyn and Owaec"))
        self.assertFalse(is_glossary_candidate("Come on! This way!"))
        self.assertFalse(is_glossary_candidate("AUTHOR"))
        self.assertFalse(is_glossary_candidate("Options for --multiplayer"))
        self.assertFalse(
            is_glossary_candidate("Battle for Wesnoth multiplayer network daemon")
        )
        self.assertFalse(
            is_glossary_candidate(
                "This is a long dialogue that should remain in the PO translation."
            )
        )

    def test_curated_term_rows_are_not_prose(self):
        _, rows = glossary_rows()
        for row in rows:
            if row["category"] != "term":
                continue
            source = row["source_term"]
            words = re.findall(r"\b[\w'-]+\b", source)
            with self.subTest(source=source):
                self.assertLessEqual(len(words), 6)
                self.assertFalse(re.search(r"[.!?]\s*$", source))
                self.assertNotRegex(source, r"[\n<%$]")

    def test_contextual_rows_use_display_translations_without_context_prefix(self):
        _, rows = glossary_rows()
        translations = {}
        for path in WORK_KO.glob("*.po"):
            translations.update(exact_po_translations(path))
        contextual = [row for row in rows if "^" in row["source_term"]]
        self.assertGreater(len(contextual), 0)
        for row in contextual:
            source = row["source_term"]
            context, display = source.split("^", 1)
            korean = row["standard_korean"]
            with self.subTest(source=source):
                self.assertTrue(context)
                self.assertTrue(display)
                if context in {"female", "male", "race"}:
                    if "^" in korean:
                        self.assertRegex(korean, r"^(?:여성|남성|종족)\^")
                else:
                    self.assertNotIn("^", korean)
                self.assertEqual(translations.get(source), korean)

    def test_contextual_keys_are_not_collapsed_by_display_text(self):
        _, rows = glossary_rows()
        contextual = [row for row in rows if "^" in row["source_term"]]
        for row in contextual:
            source = row["source_term"]
            _, display = source.split("^", 1)
            with self.subTest(source=source):
                self.assertEqual(source.split("^", 1)[1], display)
                self.assertTrue(row["standard_korean"])


if __name__ == "__main__":
    unittest.main()
