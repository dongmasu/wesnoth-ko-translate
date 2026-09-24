from pathlib import Path
import csv
import re
import unittest

from tools.apply_manual_translation_batch import is_glossary_candidate
from tools.audit_glossary import parenthetical_is_source_component
from tools.merge_reference_translations import parse_field_values
from tools.normalize_contextual_translations import normalize_translation
from tools.normalize_korean_spacing import normalize_block
from tools.project_config import GLOSSARY, WORK_KO


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
        return list(reader.fieldnames or ()), list(reader)


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
        self.assertIn('msgstr "음악 담당"', about)
        self.assertIn('msgstr "음악"', preferences)

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

    def test_korean_spacing_normalization_does_not_touch_msgid_or_obsolete(self):
        active = 'msgid "Example"\nmsgstr "그렇게 할것이다"'
        normalized, count = normalize_block(active)
        self.assertEqual(count, 1)
        self.assertIn('msgid "Example"', normalized)
        self.assertIn('msgstr "그렇게 할 것이다"', normalized)

        obsolete = '#~ msgid "Example"\n#~ msgstr "그렇게 할것이다"'
        unchanged, count = normalize_block(obsolete)
        self.assertEqual(count, 0)
        self.assertEqual(unchanged, obsolete)

    def test_korean_typo_normalization_covers_unambiguous_typos(self):
        active = 'msgid "Example"\nmsgstr "절때 난장이가 쫒아가며 댓가를 치르고 부딛혀"\n'
        normalized, count = normalize_block(active)
        self.assertEqual(count, 5)
        self.assertIn(
            'msgstr "절대 난쟁이가 쫓아가며 대가를 치르고 부딪혀"',
            normalized,
        )

    def test_tarek_uses_the_korean_reference_spelling(self):
        _, rows = glossary_rows()
        tarek = next(row for row in rows if row["source_term"] == "Tarek")
        self.assertEqual(tarek["standard_korean"], "타렉(Tarek)")
        self.assertEqual(tarek["reference_japanese"], "Tarek")

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
            "Reeve Hoban": ("호반(Hoban) 행정관", "person_name"),
            "Vash-Gorn": ("바시-고른(Vash-Gorn)", "person_name"),
            "North Knalga": ("북부 크날가(Knalga)", "place_name"),
            "Chief Bir-brish": ("비르-브리시(Bir-brish) 족장", "person_name"),
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
            "Inky": "먹물(Inky)",
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
            "female^Inky": "암컷 먹물(Inky)",
            "teamname^Inky": "먹물(Inky)",
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
            "Dwarf Grenadier": "폭탄투척병 난쟁이",
            "Dwarf Hermit": "은둔자 난쟁이",
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
            r"^(?:Lady|Lord|Minister|Novice|Princess|Sir|Uncle)\b"
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
        external = {"Discord", "IRC", "Reddit", "SoF", "Steam", "WC", "WoCopedia"}
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
