#!/usr/bin/env python3
"""Normalize Korean proper-name pairing and compound-name placement."""

from __future__ import annotations

import argparse
import ast
import csv
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.project_config import GLOSSARY, WORK_KO


FIELDS = (
    "source_term",
    "standard_korean",
    "reference_japanese",
    "reference_chinese",
    "category",
    "forbidden_terms",
    "notes",
)

NON_NAME_WORDS = {
    "Abilities", "Academy", "Accuracy", "Achievements", "Action", "Actions",
    "Add", "Address", "Advanced", "Advancement", "Aftermath", "Afternoon",
    "Aged", "Alerts", "Alignment", "Ambush", "Announcements", "Any", "Areas",
    "Armory", "Art", "Artifacts", "Artwork", "Attack", "Attacking", "Attacks",
    "Author",
    "Authenticate", "Authors", "Auto-Save", "Back", "Backstab", "Bane",
    "Battery", "Bay", "Beacon", "Berserk", "Black", "Blue", "Brown",
    "Cache", "Calendar", "Campaign", "Campaigns", "Cancel", "Cargo", "Center",
    "Clean", "Clear", "Close", "Coal", "Coast", "Color", "Combat", "Commands",
    "Community", "Completed", "Confirm", "Connect", "Continue", "Controls",
    "Copy", "Core", "Create", "Credits", "Curse", "Cut", "Damage", "Dark",
    "Date", "Dawn", "Day-phase", "Death", "Decay", "Default", "Defaults",
    "Defeat", "Defense", "Defenses", "Delete", "Description", "Desire",
    "Desolation", "Despair", "Destiny", "Destruction", "Difficulty", "Dismiss",
    "Donate", "Done", "Download", "Downloads", "Dream", "Drought", "Dungeon",
    "Dusk", "Elemental", "ENLIGHTENED", "Enclave", "Encyclopedia", "Era", "Eras", "Error",
    "Escape", "Exit", "Experience", "Explore", "Faction", "Factions", "Fair",
    "Features", "Female", "Festival", "Field", "File", "Force", "Forums",
    "Generate", "Geography", "Glaciers", "Glade", "Gold", "Graphics",
    "Graveyard", "Harbor", "Healing", "Health", "Healthy", "Help", "Heroes",
    "Hideout", "Hits", "Image", "Income", "Info", "Independent", "Indoors",
    "Inland", "Inn", "Inspiring", "Introduction", "Island", "Items", "Join",
    "Kick", "Kills", "Language", "Last", "Layer", "Leadership", "Leave",
    "Libraries", "Library", "License", "Load", "Lobby", "Logging", "Login",
    "Losses", "Mainline", "Male", "Map", "Market", "Marksman", "Marsh",
    "Massacre", "Matchmaking", "Meadow", "Memory", "Menu", "Migrate", "Mine",
    "Mines", "Miscellaneous", "Morning", "Movement", "Moves", "Moving",
    "Multiplayer", "Mute", "Name", "Next", "No", "Nobody", "None", "Note",
    "Nothing", "OK", "Open", "Options", "Other", "Others", "Output", "Path",
    "Paths", "Places", "Play", "Players", "Playing", "Playlist", "Profile",
    "Programming", "Properties", "Quick", "Quit", "Race", "Random", "Range",
    "Recall", "Recalling", "Recalls", "Recruiting", "Recruits", "Red", "Redo",
    "Refuge", "Regenerate", "Regenerates", "Regeneration", "Reject", "Remove",
    "Research", "Reserved", "Reset", "Resistance", "Resistances", "Resize",
    "Response", "Rest", "Revert", "Rocks", "Route", "Ruin", "Schedule",
    "School", "Scenarios", "Screenshot", "Search", "Secret", "Select",
    "Settings", "Side", "Signal", "Site", "Skip", "Slow", "Sound", "South",
    "Speak", "Special", "Spider", "Start", "Statistics", "Status", "Stop",
    "Success", "Summer", "Support", "Surrender", "Survival", "Team", "Test",
    "Title", "Touch", "Tournament", "Tower", "Training", "Traits", "Translation",
    "Tree", "Triumph", "Turn", "Turns", "Undo", "Units", "Universities",
    "Upkeep", "Validate", "Version", "Victory", "Villages", "Wait", "Warning",
    "Waters", "Welcome", "White", "Wild", "Winter", "Yes", "You",
}

REFERENCE_NON_NAME_TOKENS = {
    "AI", "ADF", "API", "Battle", "Blue", "C", "Clean", "Dark", "Debug",
    "Default", "Dry", "Error", "Epic", "For", "Green", "GUI", "Help",
    "ID", "Info", "Invest", "Invalid", "King", "Lua", "Maintenance",
    "Map", "Music", "North", "OK", "Package", "RNG", "Run", "Sans",
    "Scenario", "South", "Text", "Theme", "Tools", "Type", "URL", "WML",
    "Warning", "West", "World", "a", "core", "file", "help", "i", "p",
    "the", "version", "vs", "wmlindent", "wmllint", "wmlscope",
    "wmlxgettext",
}

OVERRIDES = {
    "Avatar of Nova": "노바(Nova)의 화신",
    "2p — Ruphus Isle": "2p — 루퍼스(Ruphus) 섬",
    "2p — The Walls of Pyrennis": "2인 — 피레니스(Pyrennis)의 성벽",
    "2p — Tombs of Kesorak": "2인 — 케소락(Kesorak)의 무덤",
    "Minister Alanafel": "알라나펠(Alanafel) 장관",
    "Basilica of Li’sar": "리사르(Li’sar) 대성당",
    "Blackwater Port": "검은물(Blackwater) 항구",
    "Bones of Malin Keshar": "말린 케샤르(Malin Keshar)의 뼈",
    "Burin the Lost": "길잃은 부린(Burin)",
    "Flesh of Malin Keshar": "말린 케샤르(Malin Keshar)의 살점",
    "Ford of Alyas": "알리아스(Alyas)의 여울",
    "Ford of Tifranur": "티프라누르(Tifranur)의 여울",
    "Great River": "위대한 강",
    "Fang": "독니",
    "Diff": "차이점",
    "Far North": "극북",
    "Garard II": "가라르드(Garard) 2세",
    "Garard’s Hold": "가라르드(Garard)의 요새",
    "Great Chief Brurbar": "대족장 브루르바르(Brurbar)",
    "Howgarth III": "호우가르쓰(Howgarth) 3세",
    "Inky": "먹물(Inky)",
    "Kergai": "케르가(Kergai)",
    "Lord Bayar": "바야르(Bayar) 경",
    "Limit FPS": "FPS 제한",
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
    "Lich": "리치(Lich)",
    "Kingdom of Wesnoth": "웨스노스(Wesnoth) 왕국",
    "Karmarth Hills": "카르마쓰(Karmarth) 언덕",
    "Lady Jessene": "제세네(Jessene) 부인",
    "Lady Karae": "카라에(Karae) 여사",
    "Minion of Tairach": "타이라크(Tairach)의 졸개",
    "Lord Alric’s Palace": "알릭(Alric) 군주의 궁전",
    "Lord Asaeri": "아사에리(Asaeri) 군주",
    "Lord Gaelyc’s Citadel": "게일릭(Gaelyc) 군주의 요새",
    "Malin Keshar": "말린 케샤르(Malin Keshar)",
    "Mermaid Siren": "인어 세이렌(Siren)",
    "Merman Triton": "인어 트리톤(Triton)",
    "Masked Dwarf": "가면 쓴 난쟁이",
    "Naga": "나가(Naga)",
    "Northlands": "북부 지방",
    "Ogre": "오우거(Ogre)",
    "Minister Edren": "에드렌(Edren) 목사",
    "Minister Hylas": "힐라스(Hylas) 목사",
    "Minister Mefel": "메펠(Mefel) 목사",
    "Minister Romand": "로만드(Romand) 목사",
    "Neki the Brutal": "잔혹한 네키(Neki)",
    "Novice Dani": "초보자 다니(Dani)",
    "Novice Iona": "초보자 이오나(Iona)",
    "Novice Pior": "초보자 피오르(Pior)",
    "Port of Elensefar": "엘렌세파르(Elensefar) 항구",
    "Princess Mew": "메유(Mew) 공주",
    "Sir Cadaeus": "카다에우스(Cadaeus) 경",
    "Sir Efran": "에프란(Efran) 경",
    "Sir Gerrick": "게르릭(Gerrick) 경",
    "Sir Gwydion": "그위디온(Gwydion) 경",
    "Sir Ladoc": "라도크(Ladoc) 경",
    "Sir Ruddry": "루드리(Ruddry) 경",
    "Sir Seoraery": "세오레이리(Seoraery) 경",
    "Sir Efran’s Castle": "에프란(Efran) 경의 성",
    "Sir Seoraery’s Keep": "세오레이리(Seoraery) 경의 본영",
    "Soul of Malin Keshar": "말린 케샤르(Malin Keshar)의 영혼",
    "Telemon the Slayer": "살해자 텔레몬(Telemon)",
    "The Ford of Abez": "아베즈(Abez)의 여울",
    "The Isle of Alduin": "알두인(Alduin) 섬",
    "The Swamp of Esten": "에스텐(Esten)의 늪지대",
    "The Great River": "위대한 강",
    "Uncle Somf": "솜프(Somf) 삼촌",
    "Troll": "트롤(Troll)",
    "Wyrm": "웜(Wyrm)",
    "Ancient Lich": "고대의 리치(Lich)",
    "Ancient Ogre": "고대 오우거(Ogre)",
    "Cave Wyrmlet": "동굴 웜(Wyrm) 새끼",
    "Dread Lich": "공포의 리치(Lich)",
    "Eloh Cultists": "엘로(Eloh)의 광신도",
    "Fire Dragon": "불의 드래곤(Dragon)",
    "Flesh Golem": "육체 골렘(Golem)",
    "Great Ogre": "위대한 오우거(Ogre)",
    "Great Troll": "위대한 트롤(Troll)",
    "Naga Myrmidon": "나가 미르미돈(Myrmidon)",
    "Pirate Galleon": "해적 갤리언(Galleon)",
    "Red Wyrm": "붉은 웜(Wyrm)",
    "Red Wyrmlet": "붉은 웜(Wyrm) 새끼",
    "Storm Wisp": "폭풍 위습(Wisp)",
    "Wild Wyvern": "야생 와이번(Wyvern)",
    "Young Ogre": "어린 오우거(Ogre)",
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
    "Westin Guard": "웨스틴(Westin) 수비대",
    "WC2 Invest": "WC2 투자",
    "feature^Cocoa notifications back end": "Cocoa 알림 백엔드",
    "feature^D-Bus notifications back end": "D-Bus 알림 백엔드",
    "feature^Win32 notifications back end": "Win32 알림 백엔드",
    "female^Inky": "암컷 먹물(Inky)",
    "teamname^Inky": "먹물(Inky)",
    "Talking to Tyegëa": "티에게아(Tyegëa)와 대화",
    "Tyegëa": "티에게아(Tyegëa)",
    "Tyegëa and Priestesses": "티에게아(Tyegëa)와 여제사장들",
}

OVERRIDES.update(
    {
        "Abhai": "아브하이(Abhai)",
        "Abman": "압만(Abman)",
        "Affman": "아프만(Affman)",
        "Aleii": "알레이(Aleii)",
        "Artuman": "아르투만(Artuman)",
        "Beaky": "딱딱이(Beaky)",
        "Big Baby Dro": "큰 아기 드로(Dro)",
        "Bolwuldelman": "볼울델만(Bolwuldelman)",
        "Braga": "브라가(Braga)",
        "Cliffs of Thoria": "토리아(Thoria)의 절벽",
        "Council in Weldyn": "웰딘(Weldyn)에서의 평의회",
        "Cultists": "광신도",
        "Daellyn the Red": "적색의 댈린(Daellyn)",
        "Dark Sky Over Weldyn": "웰딘(Weldyn)에 드리운 암운",
        "Dwaba-Kukai": "드와바-쿠카이(Dwaba-Kukai)",
        "Eloh": "엘로(Eloh)",
        "Expected Battle Result (HP)": "예상 전투 결과(HP)",
        "Ford of Tifranur": "티프라누르(Tifranur)의 시내",
        "Galga": "갈가(Galga)",
        "Gnarl": "그나(Gnarl)",
        "Haaf-Garga": "하프-가르가(Haaf-Garga)",
        "Haliel-Maga": "할리엘-마가(Haliel-Maga)",
        "Hann": "한(Hann)",
        "Harman": "하르만(Harman)",
        "Heldaga": "헬다가(Heldaga)",
        "Hibro": "히브로(Hibro)",
        "Inalai": "이나라이(Inalai)",
        "Jarl": "자를(Jarl)",
        "Legend of Wesmere": "웨스미어(Wesmere)의 전설",
        "Love Theme": "사랑의 테마",
        "Na-alga": "나-알가(Na-alga)",
        "Nafga": "나프가(Nafga)",
        "Ordo": "오르도(Ordo)",
        "Orga": "오르가(Orga)",
        "Orofarnië": "오로파르니에(Orofarnië)",
        "Pillars of Thunedain": "투네다인(Thunedain)의 기둥",
        "Places to talk about Wesnoth": "웨스노스(Wesnoth)에 대해 이야기하는 곳",
        "Prince of Wesnoth": "웨스노스(Wesnoth)의 왕자",
        "Return to Parthyn": "파르틴(Parthyn)으로 귀환",
        "Return to Wesnoth": "웨스노스(Wesnoth)로 귀환",
        "Rukhos, Chosen of Death": "죽음이 선택한 루코스(Rukhos)",
        "Saving Inarix": "이나릭스(Inarix)를 구출",
        "Saving Parthyn": "파르틴(Parthyn)을 구출",
        "Southbay in Winter": "남만국(Southbay)의 겨울",
        "Sorrek, Chosen of Death": "죽음이 선택한 소렉(Sorrek)",
        "Statue of Lhun-dup": "룬둡(Lhun-dup)의 조각상",
        "Statue of Lo-bsang": "롭상(Lo-bsang)의 조각상",
        "Statue of Ri-nzen": "린젠(Ri-nzen)의 조각상",
        "Statue of Sulla": "술라(Sulla)의 조각상",
        "Statue of Ten-zin": "텐진(Ten-zin)의 조각상",
        "Tan-Gulo": "탄-굴(Tan-Gulo)",
        "The Court of Karrag": "카르라그(Karrag)의 궁중",
        "The Hammer of Thursagan": "투르사간(Thursagan)의 망치",
        "The Rise of Wesnoth": "웨스노스(Wesnoth)의 성립",
        "The Road to Weldyn": "웰딘(Weldyn)으로 가는 길",
        "The Swamp of Esten": "에스텐(Esten)의 늪지대",
        "The Swamps of Illuven": "일루벤(Illuven)의 늪지대",
        "Tinry the Red": "적색의 틴리(Tinry)",
        "To Elensefar": "엘렌세파르(Elensefar)로",
        "To Southbay": "남만국(Southbay)으로",
        "Toward Mountains of Haag": "하아그(Haag)의 산맥을 건너서",
        "Tyxrrn the Dauntless": "불굴의 틱스른(Tyxrrn)",
        "Urruga": "우르루가(Urruga)",
        "Welcome to Parthyn": "파르틴(Parthyn)에 오신 것을 환영합니다",
        "Xakae": "자카(Xakae)",
        "addons_of_type^MP campaigns": "MP 캠페인",
        "addons_of_type^MP eras": "MP 시대",
        "addons_of_type^MP factions": "MP 진영",
        "addons_of_type^MP map-packs": "MP 지도 모음",
        "addons_of_type^MP scenarios": "MP 시나리오",
    }
)

COMPOUND_SOURCE = re.compile(
    r"^(?:Lady|Lord|Minister|Novice|Princess|Sir|Uncle)\b"
    r"|\b(?:of|the)\b|[’']s\b"
)


def load_glossary(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def paired_sources(rows: list[dict[str, str]]) -> set[str]:
    sources = set()
    for row in rows:
        source = row["source_term"]
        sources.update(re.findall(r"\(([A-Za-z][^()]*)\)", row["standard_korean"]))
        if re.search(rf"\({re.escape(source)}\)$", row["standard_korean"]):
            sources.add(source)
    return sources


def normalize_value(value: str, sources: set[str]) -> str:
    for source in sorted(sources, key=len, reverse=True):
        value = value.replace(f" ({source})", f"({source})")
    return value


def normalize_compound_pairing(source: str, value: str) -> str:
    """Never attach a complete compound gettext key as a name gloss."""
    if COMPOUND_SOURCE.search(source) and value.endswith(f"({source})"):
        return value[: -len(f"({source})")].rstrip()
    return value


def paired_components(rows: list[dict[str, str]]) -> set[str]:
    components: set[str] = set()
    for row in rows:
        for match in re.finditer(r"\(([A-Za-z][^()]*)\)", row["standard_korean"]):
            if match.group(1) != row["source_term"]:
                components.add(match.group(1))
    return components


def should_remove_whole_pair(
    row: dict[str, str], preserved_components: set[str]
) -> bool:
    """Remove semantic whole-source glosses without consulting context."""
    source = row["source_term"]
    value = row["standard_korean"]
    if f"({source})" not in value or source in OVERRIDES:
        return False
    japanese = row["reference_japanese"].strip()
    chinese = row["reference_chinese"].strip()
    if source in preserved_components:
        return False
    if japanese == source or japanese.startswith(f"{source} "):
        return False
    # Both reference locales translate the source rather than preserving it.
    # This is a strong signal that the Korean value is semantic too.
    return japanese not in {"", "not found"} and chinese not in {"", "not found"} and japanese != source and chinese != source


def reference_name_tokens(row: dict[str, str]) -> list[str]:
    source_tokens = re.findall(r"[A-Za-z][A-Za-z0-9'’.-]*", row["source_term"])
    japanese = row["reference_japanese"]
    chinese = row["reference_chinese"]
    tokens = []
    for token in source_tokens:
        if token in REFERENCE_NON_NAME_TOKENS or token in NON_NAME_WORDS:
            continue
        pattern = rf"(?<![A-Za-z]){re.escape(token)}(?![A-Za-z])"
        if re.search(pattern, japanese) or re.search(pattern, chinese):
            tokens.append(token)
    return tokens


def korean_name_spans(value: str) -> list[tuple[str, str]]:
    spans = []
    pattern = re.compile(
        r"([가-힣]{2,})(의|은|는|이|가|을|를|에|로|와|과|도|만|에서|에게)?"
    )
    for match in pattern.finditer(value):
        base = match.group(1)
        if base not in {
            "초보자", "위대한", "고대의", "먼", "옛적의",
            "여성", "남성", "종족", "암컷", "수컷",
        }:
            spans.append((base, match.group(2) or ""))
    return spans


def infer_missing_reference_pair(row: dict[str, str]) -> str:
    """Add one high-confidence missing pair using preserved reference spelling."""
    value = row["standard_korean"]
    if "(" in value:
        return value
    names = reference_name_tokens(row)
    if len(names) != 1:
        return value
    source_name = names[0]
    spans = korean_name_spans(value)
    if not spans:
        return value
    japanese = row["reference_japanese"]
    position = japanese.find(source_name)
    at_end = position >= 0 and position + len(source_name) >= len(japanese) - 2
    if at_end:
        base, particle = spans[-1]
    else:
        base, particle = spans[0]
    return value.replace(
        f"{base}{particle}", f"{base}({source_name}){particle}", 1
    )


def normalize_single_named_pairing(source: str, value: str) -> str:
    """Normalize pairing from source/Korean text, never from context."""
    if re.search(r"\b(?:wmlindent|wmllint|wmlscope|wmlxgettext)\b", source):
        return re.sub(r"\((?:wmlindent|wmllint|wmlscope|wmlxgettext)\)", "", value)
    if source in NON_NAME_WORDS and value.endswith(f"({source})"):
        return value[: -len(f"({source})")].rstrip()
    return value


def normalize_unit_category(row: dict[str, str]) -> None:
    source = row["source_term"]
    if (
        source.startswith(("Dwarf ", "Merman ", "Troll "))
        and row["category"] not in {"faction", "terrain", "campaign_name"}
    ):
        row["category"] = "unit_name"
        if row["standard_korean"].endswith(f"({source})"):
            row["standard_korean"] = row["standard_korean"][
                : -len(f"({source})")
            ].rstrip()


def update_glossary(path: Path) -> int:
    rows = load_glossary(path)
    sources = paired_sources(rows)
    preserved_components = paired_components(rows)
    changed = 0
    for row in rows:
        source = row["source_term"]
        normalize_unit_category(row)
        if source in NON_NAME_WORDS:
            row["category"] = "term"
        original = row["standard_korean"]
        normalized = OVERRIDES.get(
            source,
            normalize_compound_pairing(source, normalize_value(original, sources)),
        )
        if re.match(r"^(여성|남성|종족|암컷|수컷)\([A-Za-z][^()]*\)", normalized):
            normalized = re.sub(
                r"^((?:여성|남성|종족|암컷|수컷))\(([A-Za-z][^()]*)\)",
                r"\1",
                normalized,
            ).lstrip()
        if should_remove_whole_pair(row, preserved_components):
            normalized = normalized.replace(f"({source})", "").strip()
        if normalized == original and source not in OVERRIDES:
            normalized = infer_missing_reference_pair(row)
        row["standard_korean"] = normalize_single_named_pairing(
            source, normalized
        )
        if row["standard_korean"] != original:
            changed += 1
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return changed


def parse_msgid(block: str) -> str:
    value = ""
    active = False
    for line in block.splitlines():
        if line.startswith("msgid "):
            value = ast.literal_eval(line[6:])
            active = True
        elif active and line.startswith('"'):
            value += ast.literal_eval(line)
        else:
            active = False
    return value


def quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def update_po(
    path: Path,
    translations: dict[str, str],
    sources: set[str],
) -> int:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    output = []
    for block in blocks:
        source = parse_msgid(block)
        target = translations.get(source)
        if target is None:
            continue_block = block
        else:
            target = OVERRIDES.get(
                source,
                normalize_compound_pairing(source, normalize_value(target, sources)),
            )
            target = normalize_single_named_pairing(source, target)
            if source.startswith(("Dwarf ", "Merman ", "Troll ")) and target.endswith(
                f"({source})"
            ):
                target = target[: -len(f"({source})")].rstrip()
            target = normalize_single_named_pairing(
                source, target
            )
            lines = block.splitlines()
            for index, line in enumerate(lines):
                if line.startswith("msgstr "):
                    if line != f"msgstr {quote(target)}":
                        lines[index:] = [f"msgstr {quote(target)}"]
                        changed += 1
                    break
            continue_block = "\n".join(lines)
        output.append(continue_block)
    path.write_text("\n\n".join(output), encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glossary", type=Path, default=GLOSSARY)
    parser.add_argument("--work-ko", type=Path, default=WORK_KO)
    args = parser.parse_args()

    rows = load_glossary(args.glossary)
    glossary_changed = update_glossary(args.glossary)
    rows = load_glossary(args.glossary)
    sources = paired_sources(rows)
    translations = {row["source_term"]: row["standard_korean"] for row in rows}
    po_changed = 0
    for path in sorted(args.work_ko.glob("*.po")):
        po_changed += update_po(path, translations, sources)
    print(f"glossary entries normalized: {glossary_changed}")
    print(f"PO entries normalized: {po_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
