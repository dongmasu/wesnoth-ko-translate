#!/usr/bin/env python3
"""Apply a high-confidence Korean prose review batch."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.merge_reference_translations import parse_field_values, replace_msgstr_fields
from tools.project_config import WORK_KO


TRANSLATIONS = {
    "I swear I saw somebody trapped in the spider’s web. Maybe we should rescue him?":
        "누군가 거미줄에 갇힌 걸 분명히 봤어요. 구해 주는 게 좋지 않을까요?",
    "You have won the game, but you may continue if you wish...":
        "게임에서 승리했습니다. 원한다면 계속할 수 있습니다...",
    "Mines can be built on hills or mountains. A peasant on a mine will automatically dig for gold at the start of your turn.":
        "광산은 언덕이나 산에 건설할 수 있습니다. 광산에 농부를 배치하면 턴 시작 시 자동으로 금을 캡니다.",
    "Villages can only be built on grassland. They provide income and healing as usual. Right-click on a peasant in a village and you can establish a university.":
        "마을은 초지에만 건설할 수 있습니다. 마을은 평소처럼 수입과 회복을 제공합니다. 마을의 농부를 오른쪽 클릭하면 대학을 세울 수 있습니다.",
    "$sm_player_name|, since the wisdom of my people exceeds yours I have instructed my scholars to aid you in your efforts to learn the science of mining.":
        "$sm_player_name|, 우리 백성의 지혜가 그대들보다 뛰어나기에, 내 학자들에게 그대들이 광업 기술을 배우는 일을 돕도록 지시했네.",
    "Malin Keshar was born ten years after the death of Haldric IV. He grew up in the northern border town of Parthyn, the second child and eldest son of the city’s baron. Every summer, by the time the mountainous paths and high passes shed their wintry gowns of snow, orcs descended from the northern hills to ravage the settlements at the frontier. Every year, Malin’s father led the townsfolk to repel the raids and force the orcs to retreat back to the north.":
        "말린 케샤르(Malin Keshar)는 할드릭(Haldric) 4세가 죽은 지 10년 뒤에 태어났다. 그는 북부 국경 도시 파르틴(Parthyn)에서 자랐으며, 그 도시 남작의 둘째 아이이자 장남이었다. 매년 여름, 산길과 높은 고갯길에서 겨울의 눈이 녹을 무렵이면 오크들이 북쪽 언덕에서 내려와 변경의 정착지를 약탈했다. 매년 말린의 아버지는 마을 사람들을 이끌고 습격을 막아 오크들을 북쪽으로 물러나게 했다.",
    "Elves?! What in the nine hells are elves doing down here?":
        "엘프라고?! 이런 지옥 같은 곳에서 대체 뭘 하고 있는 거야?",
    "Wait a minute. There’s a tiny outline of a door in the stone. But there’s no way to open it. All I see are what look like two tiny keyholes in the stone. Now I wonder where we might find the right keys?":
        "잠깐만. 돌에 작은 문 윤곽이 보여. 하지만 열 방법이 없어. 보이는 건 돌에 난 작은 열쇠 구멍 두 개 같은 것뿐이야. 이제 맞는 열쇠를 어디서 구할 수 있을지 궁금하군.",
    "The dwarf king was away cleaning up after the recent battle, and would not be back for several days. I happily spent what little time I had learning as much as I could about these strange people. I was very impressed by their craftsmanship; they made weapons and armor of a quality I had never seen before. We were also quite the curiosity to the dwarves; I have no idea when they had last seen an elf. While some seemed suspicious or frightened of us, the dwarves overall were very polite and met our every need. Finally the summons came to meet with the dwarven king...":
        "드워프 국왕은 최근 전투의 뒤처리를 위해 자리를 비워 며칠 동안 돌아오지 않을 예정이었다. 나는 얼마 남지 않은 시간을 이 낯선 종족에 대해 최대한 많이 배우며 즐겁게 보냈다. 나는 그들의 장인 정신에 깊은 인상을 받았다. 그들은 내가 지금까지 본 적 없는 품질의 무기와 갑옷을 만들었다. 우리도 드워프들에게 꽤 흥미로운 존재였을 것이다. 드워프들이 마지막으로 엘프를 본 게 언제였는지는 알 수 없었다. 몇몇은 우리를 의심하거나 두려워하는 듯했지만, 드워프들은 전반적으로 매우 예의 바르고 우리의 필요를 모두 충족해 주었다. 마침내 드워프 국왕을 만나라는 소환이 도착했다...",
}


def apply_file(path: Path) -> int:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    output: list[str] = []
    for block in blocks:
        values = parse_field_values(block)
        source = values.get("msgid", "")
        translation = TRANSLATIONS.get(source)
        if translation is None or "msgid_plural" in values:
            output.append(block)
            continue
        updated = replace_msgstr_fields(block, {"msgstr": translation})
        if updated != block:
            block = updated
            changed += 1
        output.append(block)
    if changed:
        path.write_text("\n\n".join(output), encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, default=WORK_KO)
    args = parser.parse_args()
    total = 0
    for path in sorted(args.work.glob("*.po")):
        changed = apply_file(path)
        if changed:
            print(f"{path.name}: {changed} entries reviewed")
            total += changed
    print(f"total: {total} entries reviewed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
