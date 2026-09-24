#!/usr/bin/env python3
"""Apply the first manual full-PO review batch."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.merge_reference_translations import (  # noqa: E402
    parse_field_values,
    replace_msgstr_fields,
)
from tools.project_config import WORK_KO  # noqa: E402


TRANSLATIONS = {
    "In this scenario you build up an economy": "이 시나리오에서는 경제를 발전시켜야 합니다.",
    "You know, you really ought to be more careful before handing over money to suspicious strangers like me. But, since I’m feeling nice at the moment, I think I will actually keep my word and offer you some protection.": "있잖아, 나처럼 수상한 낯선 사람에게 돈을 건네기 전에는 정말 더 조심해야 해. 하지만 지금은 기분이 좋으니 약속을 지키고 널 좀 보호해 주지.",
    "Stop stealing my villages!": "내 마을을 그만 빼앗아!",
    "I’ll be taking back that money that your men “borrowed” from me now, Garrath!": "이제 네 부하들이 내게서 “빌린” 돈을 되찾겠다, 가라쓰!",
    "Haunt": "지박령(Haunt)",
    "\n• <bold>text='Advancement'</bold>: When a unit <ref>dst='advancement' text='advances'</ref>, it will heal fully. This can happen as soon as your unit gains enough experience, whether it is your turn or not.": "\n• <bold>text='승급'</bold>: 유닛이 <ref>dst='승급' text='승급하면</ref> 완전히 회복됩니다. 자신의 턴인지와 관계없이 유닛이 충분한 경험치를 얻는 즉시 승급할 수 있습니다.",
    "Asheviere": "아셰비에레(Asheviere)",
    "And so the Dark Queen’s reign was ended. Li’sar, daughter of Garard II and Heir to the Throne of Wesnoth, was crowned Queen and Bearer of the Sceptre of Fire, which she would pass on to all her successors.": "이렇게 어둠의 여왕의 통치는 끝났습니다. 가라르드 2세의 딸이자 웨스노스의 왕위 계승자인 리사르는 여왕이자 화염의 홀을 지닌 자로 즉위했고, 그 홀을 모든 후계자에게 물려주게 됩니다.",
    "Revelation": "계시",
    "Modification": "수정",
    "“Don’t know why the Queen hired some stinkin’ orcs, we don’t need you here.” Yeah, well now they’re dead like a bunch of beasts.": "“여왕이 왜 저 더러운 오크들을 고용했는지 모르겠군. 여기에는 네놈들이 필요 없다.” 그래, 이제 그들은 짐승 떼처럼 죽어 버렸지.",
    "Baldras and Relana returned to their villages to find them destroyed, with any survivors borne away to unknown fates. It was a bitter doom, and as Wesnoth descended into chaos, they would live to see worse.": "발드라스와 렐라나는 마을로 돌아왔지만 마을은 파괴되어 있었고, 생존자들은 알 수 없는 운명으로 끌려간 뒤였습니다. 참혹한 운명이었습니다. 웨스노스가 혼란에 빠지면서 그들은 더욱 끔찍한 일을 목격하게 됩니다.",
    "Advancements": "승급",
    "Human Alliance": "인간 동맹",
    "As you finally defeat your last remaining foes, the dreary mists around the island seem to lift. The phantoms fade away, at last released from their eternal guardianship. You have finally cleansed the ancient shrine... for now.": "마침내 남은 적을 모두 물리치자 섬 주변을 뒤덮던 음울한 안개가 걷히는 듯합니다. 유령들은 영원한 수호의 의무에서 마침내 풀려나 사라집니다. 당신은 마침내 고대의 신전을 정화했습니다... 당분간은 말입니다.",
    "But still, Tallin, we will take losses, and for each one of us, there is no replacement — whereas for every monster we kill, it seems that two more come to take its place!": "하지만 탈린, 그래도 우리는 병력을 잃을 것이고 우리 중 한 명이 쓰러질 때마다 대신할 사람은 없소. 반면 우리가 괴물을 하나 죽일 때마다 두 마리가 그 자리를 차지하러 오는 것 같소!",
    "Be welcome to the Southern Tunnels, friends... or at least, what’s left o’ them.": "남부 터널에 온 것을 환영하오, 친구들... 아니, 적어도 그곳에 남은 것에 말이오.",
    "That is the problem lad, we ha’ been stranded in these tunnels for years now, almost completely cut off from sources of food or metals or tools. It ha’ been as much as we could do to survive. We’ll get more food again now that we can reach the surface, and tools aplenty there are in the stores where we couldna’ reach while the orcs and trolls held them. But metal will be scarce for a while yet; ore will have to be brought in for smelting, first.": "그게 문제라네, 젊은이. 우리는 몇 년째 이 터널에 갇혀 음식과 금속, 도구를 구할 곳에서 거의 완전히 단절되어 있었지. 살아남는 것만으로도 벅찼다네. 이제 지상에 닿을 수 있으니 식량을 다시 구할 수 있고, 오크와 트롤이 점거해 접근하지 못했던 창고에는 도구도 잔뜩 있을 걸세. 하지만 당분간 금속은 여전히 부족할 테니, 먼저 제련할 광석을 들여와야 하네.",
    "The Rod of Justice! What in the world is it doing all the way down here?": "정의의 지팡이다! 대체 이런 곳까지 어떻게 내려와 있는 거지?",
    "Aye. Word ha’ spread, and dwarves who had been living rough in the wilds for fear of the orcs have been coming to join us. Thanks to you, Tallin, Knalga is rising again!": "그렇소. 소문이 퍼져 오크를 피해 황야에서 힘겹게 살아가던 난쟁이들이 우리와 합류하러 오고 있소. 탈린, 모두 그대 덕분이오. 크날가가 다시 일어서고 있소!",
    "I know you’re impressive wi’ a pitchfork, and you are not half bad with a sword when you choose to use one. But there skills beyond swingin’ a weapon that a general must learn.": "당신이 쇠스랑을 잘 다루는 건 알고 있소. 검을 들기로 했을 때도 솜씨가 나쁘지 않더군. 하지만 장군이 배워야 할 것은 무기를 휘두르는 기술만이 아니오.",
    "Hey, we have had experiences with crazy mages ourselves. Believe me, they are dangerous! You will feel a lot better with some of them on your side.": "이봐요, 우리도 미친 마법사들을 겪어 봤소. 내 말을 믿어요. 그들은 위험하오! 그중 몇 명이라도 우리 편에 있으면 훨씬 마음이 놓일 거요.",
    "Come on, guys, it will be great! Those orcs will never know what hit them! Together we’ll rip them to shreds! If you are planning to retire after this, this is the perfect chance for you guys to go out with a bang! You guys will become legends! <i>“The two terrible mages, risen from the dead to devastate the orcish hordes!”</i>": "자, 여러분, 정말 멋질 거예요! 저 오크들은 무엇에 당했는지도 모를 겁니다! 함께 놈들을 갈가리 찢어 버리자고요! 이 일이 끝나면 은퇴할 생각이라면, 화려하게 마무리할 절호의 기회입니다! 여러분은 전설이 될 거예요! <i>“두 명의 무시무시한 마법사가 죽음에서 일어나 오크 무리를 쑥대밭으로 만들다!”</i>",
    "Gryphons and a picked force of human woodsmen were sent out that very night, and less than two days later managed to ambush an orcish messenger on the road out of Bitterhold. The messenger was carrying a ransom demand to the elves — for the sorceress was, in fact, a princess of the highest rank.": "그날 밤 바로 그리폰과 엄선한 인간 삼림병 부대가 파견되었고, 이틀도 지나지 않아 비터홀드에서 나가는 길의 오크 전령을 매복하는 데 성공했습니다. 전령은 엘프들에게 보낼 몸값 요구서를 가지고 있었습니다. 그 마법사는 사실 최고위 계급의 공주였기 때문입니다.",
    "There’s the fortress of Bitterhold. A grim and impressive pile indeed...": "저기 비터홀드 요새가 보이는군. 참으로 음침하면서도 위압적인 성채야...",
    "He is the one who led his people in revolt against the orcs armed with nothing but pitchforks.": "그는 쇠스랑만을 무기로 든 백성들을 이끌고 오크에게 맞서 반란을 일으킨 사람입니다.",
    "This is the famous and benevolent Princess Eryssa, in whose rescue we sacrificed many lives and <i>much</i> gold.": "이분은 유명하고 자애로운 에릿사 공주님입니다. 공주님을 구하기 위해 우리는 많은 목숨과 <i>막대한</i> 금화를 바쳤습니다.",
    "Resist until your people are ready to go (turn 12)": "당신의 백성이 떠날 준비를 마칠 때까지 저항하십시오(12번째 턴).",
    "You don’t control all villages on the north side of the river when turns run out": "턴이 다할 때 강 북쪽의 모든 마을을 장악하고 있지 않으면 패배합니다.",
    "Aye. Ye’ll recall that in repairing the western galleries we cleared a small cave-in hard by where Thursagan himself once had a workshop here, before he left to study in solitude in the further North.": "그렇소. 투르사간 본인이 한때 작업장을 두었던 곳 근처의 작은 붕괴를 치웠던 일을 기억할 거요. 서쪽 회랑을 수리하면서 말이지. 그가 더 먼 북쪽으로 떠나 홀로 연구하기 전의 일이오.",
    "Your great-nephew, my lord.": "영주님의 종손자입니다.",
    "A Witness functions as the eyes of the dwarves’ history, a deep lore that they never share with outsiders. The presence of a Witness inspires dwarvish warriors with the knowledge that their deeds (and their deaths) will not go unrecorded. They learn a fighting style deliberately unlike that of their fellows, one designed to turn the vaunted strength of the dwarves against itself. The person of a Witness is considered sacred, and Witnesses are often used as envoys between dwarvish clans.": "증인은 난쟁이 역사의 눈과 같은 존재로, 외부인과 절대 공유하지 않는 깊은 전승을 지킵니다. 증인이 있으면 난쟁이 전사들은 자신의 행동과 죽음이 기록으로 남으리라는 사실에 고무됩니다. 증인들은 동료들과 일부러 다른 전투 방식을 배우는데, 이는 난쟁이들이 자랑하는 힘을 난쟁이 자신에게 돌리는 방식입니다. 증인은 신성한 존재로 여겨지며, 증인들은 종종 난쟁이 부족 사이의 사절로 활동합니다.",
    "Agh! Who will guide you to victory now?": "아! 이제 누가 당신을 승리로 이끌겠습니까?",
    "There’s no way we can get all our people safely across the desert with outlaws harassing us. We must defeat them before we can continue.": "무법자들이 우리를 괴롭히는 상황에서는 우리 모두가 안전하게 사막을 건널 방법이 없습니다. 계속 나아가려면 먼저 그들을 물리쳐야 합니다.",
    "I deeply regret... I won’t be able to see that...": "정말 유감이야... 그 모습을 볼 수 없겠구나...",
    "And I shall avenge all those you have killed!": "네가 죽인 모든 이의 복수를 하겠다!",
    "The rest is silence...": "나머지는 침묵뿐이다...",
    "The real fighting? I thought that was what we were waist-deep in?": "진짜 싸움이라고? 지금까지 우리가 허리까지 빠져 있던 게 그게 아니었나?",
    "So you’ve come at last. Let it end, here and now!": "드디어 왔군. 이제 여기서 끝내자!",
    "Come on! I ain’t going anywhere for the rest of the day, and unless you can fight better than that, neither are you. Now get your sorry behinds up off the ground and do it all over again. You numbskulls aren’t getting the easy treatment on my watch, no sir!": "어서! 나는 오늘 남은 시간 동안 어디에도 가지 않을 테니, 너희가 그보다 잘 싸우지 못한다면 너희도 마찬가지다. 이제 얼른 땅에서 그 엉덩이들을 일으켜 다시 해 봐. 내가 지켜보는 동안 이 얼간이들에게 편의를 봐주는 일은 없어. 절대 안 돼!",
    "Sniff, who were those children? Why did they die, in the dark, so many years ago? May Eloh shine her eternal light upon their souls.": "훌쩍, 저 아이들은 누구였을까? 그토록 오래전 어둠 속에서 왜 죽어야 했을까? 엘로께서 그 영혼을 영원한 빛으로 비추시기를.",
    "Look, the western passage is already flooding! It must connect back somehow to the other tunnels.": "보세요, 서쪽 통로가 벌써 물에 잠기고 있어요! 어떻게든 다른 터널과 연결되어 있는 게 틀림없어요.",
    "You abandoned them, Kaleh, to eternal suffering and torment. And now you shall pay the price! You too shall watch the black waters consume those you love. Embrace the darkness, Kaleh, it is coming for you too.": "칼레흐, 네가 그들을 영원한 고통과 괴로움 속에 버렸다. 이제 그 대가를 치러라! 너 또한 검은 물이 네가 사랑하는 이들을 삼키는 모습을 보게 될 것이다. 어둠을 받아들여라, 칼레흐. 어둠은 너에게도 다가오고 있다.",
    "Kaleh, I am Eloh, bearer of the staff of Ishtar and slayer of the demon-god Zhangor. Submit to him or I shall abandon your people to suffering and death. Your bones will litter the sand dunes, and vultures shall pick at your flesh. I am a just god, Kaleh, but no more forgiving than the harsh desert sun.": "칼레흐, 나는 이슈타르의 지팡이를 든 자이자 악신 장고르를 쓰러뜨린 엘로다. 그에게 복종하지 않으면 네 백성을 고통과 죽음 속에 버리겠다. 네 뼈는 모래 언덕에 흩어지고 독수리들이 네 살을 쪼아 먹을 것이다. 나는 정의로운 신이지만, 혹독한 사막의 태양만큼이나 용서하지 않는 신이다.",
    "Look, the water is pouring out the side tunnel into the valley! That’s a lot of water: it’s even creating a small river. I sure wouldn’t want to be downstream of that deluge right now.": "보세요, 물이 측면 터널에서 계곡으로 쏟아지고 있어요! 엄청난 양이에요. 작은 강까지 만들어 내고 있네요. 지금 저 물줄기 하류에 있고 싶지는 않아요.",
    "$(16 - $turn_number) turns remain to free $number_merfolk_caged| merfolk": "인어 $number_merfolk_caged|명을 풀어주려면 $(16 - $turn_number)턴이 남았습니다.",
    "I am known as Melusand. I am what you might call a high priest among my people.": "나는 멜루산드라고 합니다. 당신들이 말하는 대사제에 해당하는 사람이지요.",
    "Perhaps I should start at the beginning, for that is a good place to start. Make yourselves comfortable, this may take a while. I want to tell you a tale, it is a story of the fall of what you refer to as ‘The Golden Age’.": "처음부터 시작하는 게 좋겠군요. 편히 앉으세요. 조금 오래 걸릴지도 모릅니다. 당신들이 ‘황금 시대’라고 부르는 시대가 몰락한 이야기를 들려드리고 싶습니다.",
    "I’ve saved his sorry ass all this way, I’m not going to let him go and let himself get killed now!": "내가 지금까지 그 녀석을 구해 왔는데, 이제 와서 죽게 내버려둘 수는 없어!",
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
