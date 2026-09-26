#!/usr/bin/env python3
"""Apply the next high-confidence Korean prose review batch."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.merge_reference_translations import parse_field_values, replace_msgstr_fields
from tools.project_config import WORK_KO


TRANSLATIONS = {
    "It would seem the enemy has built some underground mushroom mines nearby — it must be where the mainstay of their resources are produced. If we could destroy them our chances wouldn’t nearly be so slim.":
        "아무래도 적이 근처에 지하 버섯 광산을 지은 것 같군. 저곳이 적의 주요 자원이 생산되는 곳임이 분명하다. 우리가 광산을 파괴할 수 있다면 승산이 그렇게 희박하지는 않을 걸세.",
    "Delfador, your time as my apprentice is now almost over. You are a fully-trained mage and may choose your own path in life. I hope, however, that you will take my advice and enroll yourself in the service of King Garard. I have many contacts at the court and—":
        "델파도르(Delfador), 자네가 내 수련생으로 있던 시간도 이제 거의 끝났네. 이제 자네는 수련을 마친 마법사가 되었으니, 스스로 삶의 길을 선택할 수 있지. 하지만 내 조언을 받아들여 가라르드(Garard) 국왕을 섬기는 길을 택해 주면 좋겠네. 왕궁에 아는 이가 많아서—",
    "But you have not failed. The southlands have not yet fallen to the orcish army, and have you not learned more about the undead than any man alive? It is he who fears death above all things who deceives the spirits into believing they can live again, and blinds them to the peace and rest of their own domain.":
        "당신은 실패한 것이 아니에요. 남부는 아직 오크 군대에게 함락되지 않았고, 당신은 어떤 산 사람보다도 언데드에 대해 많이 알게 되지 않았나요? 영혼들이 다시 살아날 수 있다고 속이고, 자신들의 영역에서 평화와 안식을 누리지 못하도록 눈멀게 하는 자는 무엇보다도 죽음을 두려워하는 사람이지요.",
    "The elves have beaten us and they did not use da stone. Maybe they don’t have it? Great Chief will not like bad news!":
        "엘프족은 우릴 물리쳤고 그 돌도 사용하지 않았어. 어쩌면 저들에게 돌이 없는 걸까? 큰 족장님께서 나쁜 소식을 좋아하실 리 없겠군!",
    "That will be very difficult. We did that last time and they will no doubt be alert to that threat now. Anyway, it would be but a temporary solution. Soon another strong leader would come along, and we’d find oursel’ back in the same coil.":
        "그건 매우 어려울 것이오. 지난번에도 그렇게 했으니, 놈들은 이제 그 위협을 분명히 경계하고 있을 것이오. 게다가 그건 임시방편일 뿐이오. 머지않아 또 다른 강력한 지도자가 나타날 테고, 우리는 다시 같은 곤경에 빠지게 될 것이오.",
    "I propose that we go to Highbrook Pass and see how matters stand for ourselves. If the wizards are still alive, we might be able to persuade them to help us. What’s more, if Stalrag is still around we could use his help too.":
        "윗개울 고갯길로 가서 사정이 어떤지 직접 확인하자고 제안합니다. 마법사들이 아직 살아 있다면 우리를 돕도록 설득할 수 있을지도 모릅니다. 게다가 스탈라그(Stalrag)가 아직 근처에 있다면 그의 도움도 받을 수 있습니다.",
    "Remember, Ro’Arthian, we need willing allies rather than resentful lackeys that would turn on us at the first chance. If we rescue their princess, the elves may yet choose not to help us, but that is a risk we’ll have to take.":
        "기억해 두시오, 로아르티안. 우리는 첫 기회에 우리를 배신할 원한에 찬 앞잡이가 아니라, 기꺼이 함께할 동맹이 필요하오. 우리가 그들의 공주를 구출해도 요정들이 우리를 돕지 않기로 할 수 있소. 하지만 그 위험은 우리가 감수해야 하오.",
    "We have heard much of your intelligence and courage. The number of humans over the centuries who have earned the respect and admiration of the Northern Elves are extremely few, but let it be known that you are one of them.":
        "당신의 지혜와 용기는 익히 들었습니다. 수세기 동안 북부 요정들의 존경과 찬사를 얻은 인간은 극소수지만, 당신도 그들 중 한 명이라는 사실을 알아 두십시오.",
    "We have heard much of your intelligence and courage. The number of humans over the centuries who have earned the respect and admiration of the Northern Elves are extremely few, but you are one of them.":
        "당신의 지혜와 용기는 익히 들었습니다. 수세기 동안 북부 요정들의 존경과 찬사를 얻은 인간은 극소수지만, 당신은 그들 중 한 명입니다.",
    "I believe Thera and I can help you with that, Abhai. Have no worries, you shall soon be home.":
        "테라(Thera)와 나라면 그 일을 도울 수 있을 것 같아요, 아브하이(Abhai). 걱정하지 마세요. 곧 고향으로 돌아갈 수 있을 거예요.",
    "My eyes do not extend beyond the forest. You have indeed shown yourself a tree-friend, I would there were more I could do to help you.":
        "내 눈은 숲 너머까지 닿지 않는다. 너희는 진정 나무의 친구임을 보여 주었으니, 내가 더 도울 수 있는 일이 있다면 좋겠구나.",
    "Like I haven’t killed enough undead recently. Why can’t these creeps just stay dead?":
        "내가 요즘 언데드를 충분히 죽이지 않은 모양이네. 왜 이 섬뜩한 놈들은 그냥 죽은 채로 있지 못하는 거지?",
    "This is no natural passage, and the walls are too well carved and smooth to be made by orcs. I wouldn’t be surprised if this was once carved out by dwarves. I wonder if there are any still left in these mountains...":
        "이건 자연적으로 생긴 통로가 아니야. 벽이 너무 잘 다듬어지고 매끄러워서 오크가 만든 것 같지 않아. 한때 드워프들이 파낸 통로라고 해도 놀랍지 않겠어. 이 산맥에 아직 드워프들이 남아 있을까...",
    "In the center of this circle is a huge creature, with surging muscles and bloodshot eyes. I would think it was just a very big man, except for the fine stitches that cover its entire body. In fact it seems to be composed of many body parts all sewn together. It seems to be floating asleep in the center of the glowing magical circle. I could scratch out part of the circle and break it, but I have no idea what the consequences would be. I’m not sure I want something with that kind of strength attacking me.":
        "이 마법진 한가운데에는 솟구친 근육과 핏발 선 눈을 가진 거대한 생물이 있어요. 온몸을 덮은 가느다란 봉합선만 아니었다면 그저 아주 큰 사람이라고 생각했을 거예요. 실제로는 여러 신체 부위를 꿰매어 만든 것처럼 보입니다. 빛나는 마법진 한가운데에서 잠든 채 떠 있는 것 같아요. 마법진 일부를 긁어내 깨뜨릴 수는 있겠지만, 어떤 결과가 따를지는 전혀 모르겠어요. 저렇게 강한 존재가 나를 공격하게 만들고 싶은지는 잘 모르겠네요.",
    "Anyway you’ve really gotten us into a mess. The good news is that the outpost isn’t guarded as heavily as you might think. The garrison seems only half-manned. They obviously didn’t expect any serious attack to come from this direction.":
        "어쨌든 너 때문에 우리가 정말 곤란한 처지가 됐어. 다행히 전초 기지는 생각만큼 삼엄하게 지켜지고 있지 않아. 수비대도 정원의 절반 정도밖에 안 되는 것 같고. 이쪽에서 제대로 공격해 올 줄은 꿈에도 몰랐나 봐.",
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
