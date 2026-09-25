#!/usr/bin/env python3
"""Apply reviewed proper-name fixes to selected active PO messages."""

from __future__ import annotations

from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.merge_reference_translations import (  # noqa: E402
    parse_field_values,
    replace_msgstr_fields,
)
from tools.project_config import WORK_KO  # noqa: E402


EXACT_TRANSLATIONS = {
    "Deora—": "데오라—",
    "Alternate Wesnoth Server": "대체 웨스노스(Wesnoth) 서버",
    "Battle Princess": "전투 공주",
    "Barag Gór": "바락 고르(Barag Gór)",
    "Mal A’kai": "말 아카이(Mal A’kai)",
    "Mal Barath": "말 바라쓰(Mal Barath)",
    "Mal Maul": "말 마울(Mal Maul)",
    "Mal M’Brin": "말 므브린(Mal M’Brin)",
    "female^Mal Maul": "말 마울(Mal Maul)",
    "Mal Sevu": "말 세부(Mal Sevu)",
    "Mal Shiki": "말 쉬키(Mal Shiki)",
    "Muff Argulak": "머프 아르굴락(Muff Argulak)",
    "Muff Toras": "머프 토라스(Muff Toras)",
    "Naga Myrmidon": "나가 미르미돈(Myrmidon)",
    "Pidmer Gar": "피드메르 가르(Pidmer Gar)",
    "Urza Fastik": "우르자(Urza) 파스티크(Fastik)",
    "Bragdash Gar": "브라그다시 가르(Bragdash Gar)",
    "Chief Bir-brish": "족장 비르-브리시(Bir-brish)",
    "Contender Gorlack": "경쟁자 고를락(Gorlack)",
    "Contender Karron": "경쟁자 카르론(Karron)",
    "Chief Dra-Nak": "족장 드라-나크(Dra-Nak)",
    "Clan Whitefang": "하얀 송곳니 일족",
    "Drake Arbiter": "반룡 심판관",
    "Elvish Archer": "요정 궁수",
    "Footpad": "노상강도",
    "Necromancer": "강령술사",
    "Peasant Youth": "젊은 농부",
    "Quenoth Youth": "퀴노스(Quenoth) 젊은이",
    "White Mage": "백마법사",
    "Type": "유형",
    "female^Borderer": "국경의 주민",
    "female^Divine Avatar": "신의 아바타",
    "female^Divine Incarnation": "신의 화신",
    "female^Fighter": "투사",
    "female^Guard": "경비병",
    "female^Guardian": "지킴이",
    "female^Battle Princess": "전투 공주",
    "female^Drake Arbiter": "반룡 심판관",
    "female^Elvish Archer": "요정 궁수",
    "female^Footpad": "노상강도",
    "female^Necromancer": "강령술사",
    "female^Peasant Youth": "젊은 농부",
    "female^Quenoth Druid": "퀴노스(Quenoth) 자연술사",
    "female^Quenoth Mystic": "퀴노스(Quenoth) 신비주의자",
    "female^Quenoth Shaman": "퀴노스(Quenoth) 주술사",
    "female^Quenoth Shyde": "퀴노스(Quenoth) 샤이데",
    "female^Quenoth Sun Singer": "퀴노스(Quenoth) 태양의 가수",
    "female^Quenoth Sun Sylph": "퀴노스(Quenoth) 태양 실프",
    "female^Quenoth Youth": "퀴노스(Quenoth) 젊은이",
    "female^Senior Village Elder": "마을 원로",
    "female^Shadow Lord": "그림자 군주",
    "female^Shadow Mage": "그림자 마법사",
    "female^survivor": "생존자",
    "female^Watchwoman": "야경꾼",
    "female^Wesfolk Leader": "서부인(Wesfolk) 대장",
    "female^Wesfolk Outcast": "서부인(Wesfolk) 이단아",
    "female^White Mage": "백마법사",
    "female^feeding": "포식",
    "female^feral": "야생",
    "female^illuminates": "조명",
    "female^intelligent": "지능",
    "female^leadership": "지도력",
    "female^loyal": "충성스러운",
    "female^nightskirmish": "야간 전투",
    "female^poisoned": "중독됨",
    "race+female^Wolf": "늑대",
    "Gawffus the Dim": "어리숙한 가우푸스(Gawffus)",
    "Rawffus the Dim": "어리숙한 라우푸스(Rawffus)",
}

NAME_REPLACEMENTS = {
    "Syrsszk": "시르스즈크(Syrsszk)",
    "Rysssrylosszkk": "리스릴레로즈크(Rysssrylosszkk)",
    "Ruaskkolin": "라스코쿠린(Ruaskkolin)",
    "Chak’kso": "차크소(Chak’kso)",
}

UNIT_DESCRIPTION_REPLACEMENTS = {
    "Alavynne": "알라빈(Alavynne)",
}
BARAG_GOR_RE = re.compile(r"바락(?:\(Barag\))? 고르(?:\(Gór\))?(?:\(Barag Gór\))?")
DRA_NAK_REPLACEMENTS = {
    "족장(Dra-Nak) 드라-나크": "족장 드라-나크(Dra-Nak)",
    "드라-나크 족장(Dra-Nak)": "족장 드라-나크(Dra-Nak)",
    "오크 족장(Dra-Nak) 드라-나크": "오크 족장 드라-나크(Dra-Nak)",
}
NAME_COMPONENT_REPLACEMENTS = {
    "말(Mal) 바라쓰": "말 바라쓰(Mal Barath)",
    "말(Mal) 마울": "말 마울(Mal Maul)",
    "말(Mal) 므브린": "말 므브린(Mal M’Brin)",
    "말(Mal) 음브린": "말 므브린(Mal M’Brin)",
    "말(Mal) 세부": "말 세부(Mal Sevu)",
    "말(Mal) 쉬키": "말 쉬키(Mal Shiki)",
    "머프(Muff) 아르굴락": "머프 아르굴락(Muff Argulak)",
    "머프(Muff) 토라스": "머프 토라스(Muff Toras)",
    "나가(Naga) 미르미돈(Myrmidon)": "나가 미르미돈(Myrmidon)",
    "피드메르 가르(Gar)": "피드메르 가르(Pidmer Gar)",
    "우르자(Urza) 파스티크": "우르자(Urza) 파스티크(Fastik)",
    "브라그다시 가르(Gar)": "브라그다시 가르(Bragdash Gar)",
    "비르-브리시(Bir-brish) 족장": "족장 비르-브리시(Bir-brish)",
    "경쟁자(Gorlack) 고를락(Gorlack)": "경쟁자 고를락(Gorlack)",
    "경쟁자(Karron) 카르론(Karron)": "경쟁자 카르론(Karron)",
    "어리숙한(Gawffus) 가우푸스": "어리숙한 가우푸스(Gawffus)",
    "어리숙한(Rawffus) 라우푸스": "어리숙한 라우푸스(Rawffus)",
}
ALAVYNNE_RE = re.compile(r"알라빈(?!\(Alavynne\))")


def replace_unpaired_name_tokens(target: str) -> str:
    """Pair only bare name tokens; never rewrite text inside existing pairing."""
    for source, paired in NAME_REPLACEMENTS.items():
        korean = paired.split("(", 1)[0]
        nested = re.compile(
            rf"(?:{re.escape(korean)}\()+{re.escape(source)}(?:\))+"
        )
        target = nested.sub(paired, target)
        bare = re.compile(
            rf"(?<![A-Za-z0-9_])(?<!\(){re.escape(source)}"
            rf"(?![A-Za-z0-9_])(?!\))"
        )
        target = bare.sub(paired, target)
    return target


def update_file(path: Path) -> int:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    output: list[str] = []
    for block in blocks:
        values = parse_field_values(block)
        source = values.get("msgid", "")
        translation = values.get("msgstr")
        if not source or translation is None:
            output.append(block)
            continue

        target = EXACT_TRANSLATIONS.get(source, translation)
        if source.startswith("Xikkrisx of Syrsszk "):
            target = replace_unpaired_name_tokens(target)
        if source.startswith("Years of devotion may endow a priestess "):
            target = ALAVYNNE_RE.sub(
                UNIT_DESCRIPTION_REPLACEMENTS["Alavynne"],
                target,
            )
        if "Barag Gór" in source:
            target = BARAG_GOR_RE.sub("바락 고르(Barag Gór)", target)
        for old, new in NAME_COMPONENT_REPLACEMENTS.items():
            source_component = new.rsplit("(", 1)[-1].rstrip(")")
            target = re.sub(
                re.escape(old) + rf"(?!\({re.escape(source_component)}\))",
                new,
                target,
            )
        for old, new in DRA_NAK_REPLACEMENTS.items():
            target = target.replace(old, new)
        if target != translation:
            block = replace_msgstr_fields(block, {"msgstr": target})
            changed += 1
        output.append(block)

    if changed:
        path.write_text("\n\n".join(output), encoding="utf-8")
    return changed


def main() -> int:
    total = 0
    for path in sorted(WORK_KO.glob("*.po")):
        changed = update_file(path)
        if changed:
            print(f"{path.name}: {changed} message(s)")
            total += changed
    print(f"total: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
