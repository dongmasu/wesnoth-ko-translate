#!/usr/bin/env python3
"""Apply the second manual full-PO review batch."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.merge_reference_translations import parse_field_values, replace_msgstr_fields  # noqa: E402
from tools.project_config import WORK_KO  # noqa: E402


TRANSLATIONS = {
    "Curse that girl! She’ll be the death of me. But still she doesn’t stand a chance without me. Kaleh is one thing, but Nym needs my protection. All right, I’m going in. The rest of you stand guard, if we don’t come out in half an hour then flee the island with the merfolk.": "저 저주받을 계집애! 저 애 때문에 내가 죽게 생겼군. 하지만 나 없이는 저 애도 어쩔 수 없어. 칼레흐는 그렇다 쳐도 님에게는 내 보호가 필요해. 좋아, 내가 들어가겠어. 너희는 나머지 모두 경계를 서. 30분 안에 우리가 나오지 않으면 인어들과 함께 섬을 떠나.",
    "So, the elf’s puny friends think they can save him. But you are too late. He is already mine!": "그래서 이 엘프의 보잘것없는 친구들이 그를 구할 수 있다고 생각하는군. 하지만 이미 늦었다. 그는 이미 내 것이다!",
    "Is that what you think? I shall prove you wrong. Look out upon your people and despair!": "그렇게 생각하나? 네가 틀렸다는 걸 보여주지. 네 백성을 바라보며 절망해라!",
    "I command you to stop this foolishness!": "이 어리석은 짓을 멈추라고 명령한다!",
    "What the heck? That central creature just hit me with some sort of slime. It hurts and I— I’m stuck!": "이런 젠장? 저 중앙의 생물이 무슨 슬라임 같은 걸로 나를 때렸어. 아프고, 난... 꼼짝할 수가 없어!",
    "Ow, I’m stuck!": "아야, 꼼짝할 수가 없어!",
    "Ugh. I’m covered in blood and guts, and this nasty blue stuff. I don’t know what in the nine hells we were fighting, but she doesn’t smell any better dead than she did alive.": "윽. 피와 내장, 이 지저분한 파란 물질까지 온몸에 뒤집어썼어. 대체 우리가 무슨 지옥 같은 것과 싸운 건지 모르겠지만, 저 여자는 살아 있을 때나 죽었을 때나 냄새가 나아지지 않았어.",
    "Although I believe that our battle in the black citadel was our finest hour, I am still haunted by Nym’s death in that dark place. And so every morning at sunrise I come out to the southeastern tip of the island and look out upon the waters, upon the world that we sacrificed so much to preserve. I remind myself what Zhul said, and they all believed, that despite all the death and fighting we saw in our journey, this world was a beautiful and good enough place that Nym was willing to sacrifice her life to save it. Looking out over the waters, and back upon the prosperity of my people, I tell myself it was worth it. But sometimes that seems a small consolation.": "검은 성채에서 벌인 전투가 우리의 최고의 순간이었다고 생각하지만, 아직도 그 어두운 곳에서 님의 죽음이 마음에 남아 있습니다. 그래서 매일 아침 해가 뜨면 섬 남동쪽 끝으로 나와 물결 너머, 우리가 큰 희생을 치르며 지켜 낸 세상을 바라봅니다. 줄이 했던 말과 우리 모두가 믿었던 것을 되새깁니다. 우리가 여정에서 수많은 죽음과 싸움을 보았지만, 이 세상은 님이 목숨을 바쳐 구할 만큼 아름답고 충분히 가치 있는 곳이었다는 것을요. 물을 바라보고 우리 백성의 번영을 돌아보며, 나는 그것이 그만한 가치가 있었다고 스스로에게 말합니다. 하지만 때로는 그것이 작은 위안에 불과해 보입니다.",
    "Although I believe that our battle in the black citadel was our finest hour, I am still haunted by Zhul’s death in that dark place. And so every morning at sunrise I come out to the southeastern tip of the island and look out upon the waters, upon the world that we sacrificed so much to preserve. I remind myself what Zhul said, and they all believed, that despite all the death and fighting we saw in our journey, this world was a beautiful and good enough place that Zhul was willing to sacrifice her life to save it. Looking out over the waters, and back upon the prosperity of my people, I tell myself it was worth it. But sometimes that seems a small consolation.": "검은 성채에서 벌인 전투가 우리의 최고의 순간이었다고 생각하지만, 아직도 그 어두운 곳에서 줄의 죽음이 마음에 남아 있습니다. 그래서 매일 아침 해가 뜨면 섬 남동쪽 끝으로 나와 물결 너머, 우리가 큰 희생을 치르며 지켜 낸 세상을 바라봅니다. 줄이 했던 말과 우리 모두가 믿었던 것을 되새깁니다. 우리가 여정에서 수많은 죽음과 싸움을 보았지만, 이 세상은 줄이 목숨을 바쳐 구할 만큼 아름답고 충분히 가치 있는 곳이었다는 것을요. 물을 바라보고 우리 백성의 번영을 돌아보며, 나는 그것이 그만한 가치가 있었다고 스스로에게 말합니다. 하지만 때로는 그것이 작은 위안에 불과해 보입니다.",
    "Although I believe that our battle in the black citadel was our finest hour, I am still haunted by the death of Grog in that dark place. And so every morning at sunrise I come out to the southeastern tip of the island and look out upon the waters, upon the world that we sacrificed so much to preserve. I remind myself what Zhul said, and they all believed, that despite all the death and fighting we saw in our journey, this world was a beautiful and good enough place that Grog was willing to sacrifice his life to save it. Looking out over the waters, and back upon the prosperity of my people, I tell myself it was worth it. But when I think of the desperate war that his people are probably still fighting underground, it seems a small consolation.": "검은 성채에서 벌인 전투가 우리의 최고의 순간이었다고 생각하지만, 아직도 그 어두운 곳에서 그로그의 죽음이 마음에 남아 있습니다. 그래서 매일 아침 해가 뜨면 섬 남동쪽 끝으로 나와 물결 너머, 우리가 큰 희생을 치르며 지켜 낸 세상을 바라봅니다. 줄이 했던 말과 우리 모두가 믿었던 것을 되새깁니다. 우리가 여정에서 수많은 죽음과 싸움을 보았지만, 이 세상은 그로그가 목숨을 바쳐 구할 만큼 아름답고 충분히 가치 있는 곳이었다는 것을요. 물을 바라보고 우리 백성의 번영을 돌아보며, 나는 그것이 그만한 가치가 있었다고 스스로에게 말합니다. 하지만 그의 백성이 지하에서 여전히 절박한 전쟁을 벌이고 있을 생각을 하면, 그것은 작은 위안에 불과해 보입니다.",
    "Although I believe that our battle in the black citadel was our finest hour, I am still haunted by the death of Nog in that dark place. And so every morning at sunrise I come out to the southeastern tip of the island and look out upon the waters, upon the world that we sacrificed so much to preserve. I remind myself what Zhul said, and they all believed, that despite all the death and fighting we saw in our journey, this world was a beautiful and good enough place that Nog was willing to sacrifice his life to save it. Looking out over the waters, and back upon the prosperity of my people, I tell myself it was worth it. But when I think of the desperate war that his people are probably still fighting underground, it seems a small consolation.": "검은 성채에서 벌인 전투가 우리의 최고의 순간이었다고 생각하지만, 아직도 그 어두운 곳에서 노그의 죽음이 마음에 남아 있습니다. 그래서 매일 아침 해가 뜨면 섬 남동쪽 끝으로 나와 물결 너머, 우리가 큰 희생을 치르며 지켜 낸 세상을 바라봅니다. 줄이 했던 말과 우리 모두가 믿었던 것을 되새깁니다. 우리가 여정에서 수많은 죽음과 싸움을 보았지만, 이 세상은 노그가 목숨을 바쳐 구할 만큼 아름답고 충분히 가치 있는 곳이었다는 것을요. 물을 바라보고 우리 백성의 번영을 돌아보며, 나는 그것이 그만한 가치가 있었다고 스스로에게 말합니다. 하지만 그의 백성이 지하에서 여전히 절박한 전쟁을 벌이고 있을 생각을 하면, 그것은 작은 위안에 불과해 보입니다.",
    "Although I believe that our battle in the black citadel was our finest hour, I am still haunted by the death of Rogrimir in that dark place. And so every morning at sunrise I come out to the southeastern tip of the island and look out upon the waters, upon the world that we sacrificed so much to preserve. I remind myself what Zhul said, and they all believed, that despite all the death and fighting we saw in our journey, this world was a beautiful and good enough place that Rogrimir was willing to sacrifice his life to save it. Looking out over the waters, and back upon the prosperity of my people, I tell myself it was worth it. But when I think of the desperate war that his people are probably still fighting underground, it seems a small consolation.": "검은 성채에서 벌인 전투가 우리의 최고의 순간이었다고 생각하지만, 아직도 그 어두운 곳에서 로그리미르의 죽음이 마음에 남아 있습니다. 그래서 매일 아침 해가 뜨면 섬 남동쪽 끝으로 나와 물결 너머, 우리가 큰 희생을 치르며 지켜 낸 세상을 바라봅니다. 줄이 했던 말과 우리 모두가 믿었던 것을 되새깁니다. 우리가 여정에서 수많은 죽음과 싸움을 보았지만, 이 세상은 로그리미르가 목숨을 바쳐 구할 만큼 아름답고 충분히 가치 있는 곳이었다는 것을요. 물을 바라보고 우리 백성의 번영을 돌아보며, 나는 그것이 그만한 가치가 있었다고 스스로에게 말합니다. 하지만 그의 백성이 지하에서 여전히 절박한 전쟁을 벌이고 있을 생각을 하면, 그것은 작은 위안에 불과해 보입니다.",
    "Although I believe that our battle in the black citadel was our finest hour, I am still haunted by the death of Jarl in that dark place. And so every morning at sunrise I come out to the southeastern tip of the island and look out upon the waters, upon the world that we sacrificed so much to preserve. I remind myself what Zhul said, and they all believed, that despite all the death and fighting we saw in our journey, this world was a beautiful and good enough place that Jarl was willing to sacrifice his life to save it. Looking out over the waters, and back upon the prosperity of my people, I tell myself it was worth it. But when I think of the desperate war that his people are probably still fighting underground, it seems a small consolation.": "검은 성채에서 벌인 전투가 우리의 최고의 순간이었다고 생각하지만, 아직도 그 어두운 곳에서 자를의 죽음이 마음에 남아 있습니다. 그래서 매일 아침 해가 뜨면 섬 남동쪽 끝으로 나와 물결 너머, 우리가 큰 희생을 치르며 지켜 낸 세상을 바라봅니다. 줄이 했던 말과 우리 모두가 믿었던 것을 되새깁니다. 우리가 여정에서 수많은 죽음과 싸움을 보았지만, 이 세상은 자를이 목숨을 바쳐 구할 만큼 아름답고 충분히 가치 있는 곳이었다는 것을요. 물을 바라보고 우리 백성의 번영을 돌아보며, 나는 그것이 그만한 가치가 있었다고 스스로에게 말합니다. 하지만 그의 백성이 지하에서 여전히 절박한 전쟁을 벌이고 있을 생각을 하면, 그것은 작은 위안에 불과해 보입니다.",
    "Although I believe that our battle in the black citadel was our finest hour, I am still haunted by my friends’ deaths in that dark place. And so every morning at sunrise I come out to the southeastern tip of the island and look out upon the waters, upon the world that we sacrificed so much to preserve. I remind myself what Zhul said, and they all believed, that despite all the death and fighting we saw in our journey, this world was a beautiful and good enough place that they were willing to sacrifice their lives to save it. Looking out over the waters, and back upon the prosperity of my people, I tell myself it was worth it. But I still miss each one of them horribly.": "검은 성채에서 벌인 전투가 우리의 최고의 순간이었다고 생각하지만, 아직도 그 어두운 곳에서 친구들이 죽은 일이 마음에 남아 있습니다. 그래서 매일 아침 해가 뜨면 섬 남동쪽 끝으로 나와 물결 너머, 우리가 큰 희생을 치르며 지켜 낸 세상을 바라봅니다. 줄이 했던 말과 우리 모두가 믿었던 것을 되새깁니다. 우리가 여정에서 수많은 죽음과 싸움을 보았지만, 이 세상은 친구들이 목숨을 바쳐 구할 만큼 아름답고 충분히 가치 있는 곳이었다는 것을요. 물을 바라보고 우리 백성의 번영을 돌아보며, 나는 그것이 그만한 가치가 있었다고 스스로에게 말합니다. 하지만 나는 아직도 친구들 한 명 한 명이 너무나 그립습니다.",
    "Long ago, during more prosperous times, elven warriors favored the use of swords as more elegant, versatile weapons compared to other melee armaments. However, in recent times, the dearth of supplies for smithing has reduced the availability of blade-crafting, necessitating the fashioning of cheaper, more easily repaired weaponry. To compensate for this diminishing in armament quality, the Quenoth have adopted a greater flexibility in their use. In the open sands, a fighter is trained to develop the acumen to split his attention between multiple enemies, be they brigand, wild creature, or undead.": "먼 옛날 번영하던 시절, 엘프 전사들은 다른 근접 무기보다 우아하고 다재다능한 검을 즐겨 사용했습니다. 하지만 최근에는 대장간 재료가 부족해 검날을 만들기 어려워졌고, 더 싸고 쉽게 수리할 수 있는 무기를 만들어야 했습니다. 무기의 질이 낮아진 것을 보완하기 위해 퀴노스는 무기를 더욱 유연하게 활용하는 법을 익혔습니다. 탁 트인 모래밭에서 싸움꾼은 산적이든 야생 생물이든 언데드든 여러 적에게 주의를 나누는 판단력을 기릅니다.",
    "When encountering wild taurochs, Quenoth hunters often observe the curious behavior of particularly stubborn beasts, who will brace their rugged bodies and absolutely refuse to budge when provoked. Though difficult to placate, these taurochs are sometimes selected by skilled riders for their exceptional resilience. Any warrior who finds their advance blocked by a Stalwart would undoubtedly be wise to seek another path, for trying to displace the beast would be akin to trying to fight a stone wall.": "야생 타우록을 만났을 때 퀴노스 사냥꾼들은 유난히 고집 센 짐승의 기묘한 행동을 종종 봅니다. 그런 타우록은 거친 몸을 단단히 버티고 서서 도발을 받아도 절대 움직이지 않습니다. 달래기 어려운 짐승이지만, 숙련된 기수들은 뛰어난 인내력 때문에 이런 타우록을 선택하기도 합니다. 강건한 타우록에게 진로가 막힌 전사는 다른 길을 찾는 것이 현명할 것입니다. 그 짐승을 밀어내려는 것은 돌벽과 싸우는 것과 다르지 않기 때문입니다.",
    "female^refreshed": "회복됨",
    "What lurked in the darkness? Who were the unbelievers that Eloh had so cryptically referred to? My heart beat loudly in my chest, everything seemed amplified down here. I felt a strong suspicion that this was not a place that my people were meant to be. I strode onwards grimly; considering everything we had gone through so far, Uria be damned if I was going to be frightened now.": "어둠 속에는 무엇이 숨어 있었을까? 엘로가 그토록 모호하게 말한 불신자들은 누구였을까? 심장이 가슴 속에서 크게 뛰었고, 이곳에서는 모든 감각이 증폭되는 듯했다. 나는 이곳이 우리 백성이 있어야 할 곳이 아니라는 강한 의심을 느꼈다. 지금까지 우리가 겪은 모든 일을 생각하면, 이제 와서 겁을 먹는다면 우리아에게 저주받을 일이다. 나는 굳은 표정으로 계속 걸어갔다.",
    "At first I thought that if we could just leave the desert, we could find a peaceful place away from all the bloodshed and death. But even underground the last remnants of the trolls and dwarves continue to fight a bloody struggle to the death. Is this what our world has become? And why did Eloh tell me to ‘kill the unbelievers’? If we had attacked both the dwarves and the trolls we would not have made it even this far. Everywhere I look I see remains of once great empires. If we destroyed the last of these peoples, what would be left around us but a howling emptiness?": "처음에는 사막만 벗어나면 유혈과 죽음에서 멀리 떨어진 평화로운 곳을 찾을 수 있을 거라 생각했다. 하지만 지하에서도 트롤과 드워프의 마지막 후손들은 죽을 때까지 피비린내 나는 싸움을 계속하고 있다. 우리 세상이 이렇게 변한 것인가? 그런데 엘로는 왜 나에게 ‘불신자들을 죽이라’고 했을까? 드워프와 트롤 양쪽을 모두 공격했다면 우리는 여기까지 오지도 못했을 것이다. 어디를 바라보아도 한때 위대했던 제국의 잔해가 보인다. 이 민족들의 마지막 남은 이들까지 우리가 없애 버린다면, 우리 주변에 남는 것은 울부짖는 공허뿐이지 않을까?",
    "Perilous that way is.\nA wide stretch of sea unexceptional flyers might cross with fortune from the Winds of Fate.\n\nThen only a cluster of shoals to rest them, which might be slid past unnoticed with perilous ease.": "그 길은 위험합니다.\n평범한 비행사라면 운명의 바람이 행운을 안겨 주어야 건널 수 있을 만큼 넓은 바다가 펼쳐져 있습니다.\n\n그 뒤에는 쉴 수 있는 작은 여울 무리만 있을 뿐입니다. 방심하면 위험할 정도로 쉽게 지나칠 수도 있는 곳이지요.",
    "Further east, another stretch of sea, nearly as wide.\n\nAt last, the Greatland, a land as vast as the ocean itself.\nLikewise mysterious.\n\nThe Spoken Memories tell us drakes once thrived there into the Time of Turmoil.\nWhen nigh all of them perished in an unknown calamity.": "더 동쪽에는 거의 그만큼 넓은 바다가 또 펼쳐져 있습니다.\n\n마침내 바다만큼 광활한 땅, 대지가 나타납니다.\n그곳 역시 신비롭습니다.\n\n구전된 기억에 따르면 반룡들은 대혼란의 시대까지 그곳에서 번성했습니다.\n그러다 알 수 없는 재앙으로 거의 모두가 죽고 말았습니다.",
    "Advantage is determined by adding the gold, the value of the drakes on the field, and five times the income; Right-click to see the current score": "우세도는 금화와 전장에 있는 반룡의 가치, 수입의 5배를 더해 결정됩니다. 현재 점수를 보려면 마우스 오른쪽 버튼을 클릭하세요.",
    "Even then, half among the flight were unready to last such a journey. Those yet too young. Those with wounds still mending. To Karron’s bewilderment, Gorlack gifted her these— a flight of her own to lead.": "그때도 비행단의 절반은 그런 여정을 견딜 준비가 되어 있지 않았습니다. 아직 너무 어린 이들이었고, 아직 상처를 회복 중인 이들이었습니다. 카르론이 어리둥절해하는 가운데, 고를락은 이들을 카르론에게 맡겼습니다. 카르론이 이끌 자신만의 비행단이었습니다.",
}


def apply_file(path: Path) -> int:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    output = []
    for block in blocks:
        values = parse_field_values(block)
        source = values.get("msgid", "")
        translation = TRANSLATIONS.get(source)
        if translation is None or "msgid_plural" in values:
            output.append(block)
            continue
        updated = replace_msgstr_fields(block, {"msgstr": translation})
        if updated != block:
            changed += 1
            block = updated
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
        count = apply_file(path)
        if count:
            print(f"{path.name}: {count} entries reviewed")
            total += count
    print(f"total: {total} entries reviewed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
