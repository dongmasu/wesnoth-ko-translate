#!/usr/bin/env python3
"""Repair prose entries with lost paragraphs or review notes in msgstr."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.merge_reference_translations import parse_field_values, replace_msgstr_fields
from tools.project_config import WORK_KO


REPLACEMENTS = {
    "This 4p survival scenario allows you to construct buildings and terraform the land.":
        "이 4인용 생존 시나리오에서는 건물을 짓고 지형을 바꿀 수 있습니다.\n\n"
        "숙련자라면 시작 금화를 75로 낮추는 것이 좋습니다.",
    "You must survive until turn 25":
        "25번째 차례까지 살아남으십시오.",
    "The northern frontier town of Parthyn is annually raided":
        "북부 국경 마을인 파르틴(Parthyn)은 해마다 인근 오크 부족의 습격을 받습니다. "
        "추방된 마법사 말린 케샤르(Malin Keshar)는 그 과정에서 자신의 영혼을 희생하게 "
        "되더라도 어떤 수단을 써서라도 고향을 지키고 오크에게 복수하려 합니다.\n\n",
    "editor^<bold>text='How to Use'</bold>":
        "<bold>text='사용 방법'</bold>\n\n"
        "표식 화살표만으로는 그다지 유용하지 않지만, 절벽이나 협곡 유형의 지형을 "
        "사용하면 색칠한 영역을 제한할 수 있습니다.\n\n"
        "사용 예시는 다음과 같습니다.\n"
        "1. 편집기 팔레트에서 절벽(^Qhh)을 선택하고, 모든 칸이 초원인 빈 지도에서 "
        "한 칸 칠하기 도구로 큰 덩어리의 윤곽을 그립니다.\n"
        "2. 덩어리 안쪽의 타일에 높은 표식(^_mh) 화살표를 배치합니다(절벽 경계에는 "
        "배치하지 않습니다).\n"
        "3. 이제 덩어리 전체가 높아집니다. 표식이나 절벽 오버레이를 덮어쓰지 않는 한 "
        "필요한 다른 지형 오버레이를 추가할 수 있습니다.\n\n"
        "절벽 경계를 나타내는 그래픽은 기본 지형에 따라 결정됩니다.\n",
    "<ref>dst='..calendar' text='Calendar'</ref>":
        "<ref>dst='..calendar' text='달력'</ref>\n"
        "<ref>dst='..geography' text='지리'</ref>",
    "This section will list all the units you discover":
        "이 절에는 웨스노스(Wesnoth)의 세계를 탐험하며 발견한 모든 유닛이 표시됩니다. "
        "캠페인이나 멀티플레이어 시나리오에서 새로운 유닛을 발견하면 해당 종족의 "
        "하위 항목에 추가되며, 원할 때 언제든 그 페이지를 볼 수 있습니다. 유닛 "
        "페이지에는 일반 설명, 능력치, 공격, 저항력, 이동력과 방어력이 표시됩니다.\n\n",
    "A faction is a collection of units and leaders.":
        "진영은 유닛과 지도자로 구성됩니다. 멀티플레이어 게임에서는 진영이 각 진영에 "
        "배정됩니다.\n\n",
    "Some weapons have special features":
        "일부 무기에는 공격 효과를 높이는 특수 능력이 있습니다. 캠페인이나 멀티플레이어 "
        "시나리오에서 새로운 무기 특수 능력을 발견하면 이 목록에 추가되며, 원할 때 "
        "언제든 그 페이지를 볼 수 있습니다. 각 페이지에는 무기 특수 능력의 효과와 "
        "현재 발견한 유닛 중 해당 능력을 가진 유닛이 설명됩니다.\n\n",
    "\n\nGoblins are puny":
        "\n\n고블린은 작고 매우 허약해서 인간 어린이의 크기와 체격을 넘는 경우가 드뭅니다.\n\n"
        "고블린은 자신보다 큰 동족에게 평생 거의 노예처럼 부려지며 전투에서는 "
        "칼받이로 이용됩니다. 비극적인 운명에도 불구하고 고블린이 번성하는 것은 "
        "수가 매우 많기 때문이기도 하고, 오크들이 고블린에게 얼마나 의존하는지 "
        "잘 알고 있기 때문이기도 합니다. 고블린은 오크에게 필요한 육체노동의 대부분을 "
        "맡지만, 진짜 오크의 완력이 필요한 일만은 예외입니다. 오크들은 그런 일을 "
        "자신들의 힘을 과시하는 증거로 여기며 즐깁니다.",
    "Gryphons are broad, powerful beasts":
        "그리핀은 육지의 포식자와 맹금류 양쪽의 특징을 지닌 크고 강력한 짐승입니다. "
        "대담한 사람이 가끔 길들여 타기도 하지만, 그리핀은 특히 둥지 주변에서 "
        "영역 의식이 강하고 공격적입니다.\n\n"
        "그리핀이 그렇게 무거운 몸으로도 날 수 있는 원리는 수 세기 동안 논쟁의 "
        "대상이었지만, 그 기원만큼이나 여전히 수수께끼로 남아 있습니다.",
    "Domesticated horses come in many shapes":
        "길들인 말은 강력한 전쟁마부터 튼튼한 역마와 민첩한 목장 말까지 다양한 "
        "모양과 크기를 지닙니다. 많은 짐승보다 연약하지만, 빠르고 영리한 야생마는 "
        "야생에서 동족과 함께 번성할 수 있습니다.\n\n"
        "말은 많은 문명에서 중요한 존재였으므로 말을 중심으로 한 신화와 이야기가 "
        "많은 것도 놀라운 일이 아닙니다. 날개 달린 말, 인간과 말의 혼종, 유령 말이 "
        "문헌에 등장하지만, 그런 것을 실제로 보았다고 자신 있게 말할 수 있는 사람은 "
        "거의 없습니다.",
    "The add-on contains files or directories with case conflicts.":
        "이 부가 기능에는 대소문자만 다른 파일 또는 디렉터리가 포함되어 있습니다.\n\n"
        "같은 디렉터리의 이름은 대소문자만 달라서는 안 됩니다.",
    "One or more add-ons need to be installed":
        "이 게임에 참가하려면\n하나 이상의 부가 기능을 설치해야 합니다.",
    "This save is from a different version of the game":
        "이 저장 파일은 다른 버전($version_number|)의 게임에서 만들어졌으므로 이 "
        "버전에서는 작동하지 않을 수 있습니다.\n\n"
        "<b>경고:</b> 캠페인 중간에 저장한 파일은 특히 실패할 가능성이 높습니다. "
        "이전 버전을 사용하거나 캠페인을 다시 시작해야 합니다. 저장된 게임이 "
        "성공적으로 불러와지는 것처럼 보여도 게임 밸런스와 이야기 진행 같은 세부 "
        "요소에 영향을 받을 수 있으며, 난이도와 도전, <i>재미</i>가 사라질 수도 "
        "있습니다.\n\n"
        "예를 들어 초반 시나리오의 적 수가 줄어들도록 캠페인이 조정되었다면, "
        "후반 시나리오에서는 재소집 목록의 유닛이 그에 맞게 경험치를 덜 얻었을 "
        "것으로 예상할 수 있습니다.\n\n"
        "계속하시겠습니까?",
    "From the Annals of Alduin, 98 YW":
        "알두인의 연대기에서, 웨스노스력 98년\n\n"
        "지금으로부터 스물여덟 해 전인 웨스노스력 70년, 웨스노스 국왕과 엘렌세파르 "
        "영주는 인류의 안전을 강화하기 위해 무역 및 동맹 조약을 체결했습니다. "
        "이 조약을 실현하려면 웰딘과 엘렌세파르 사이에 안전한 길을 만들고, 문명화된 "
        "이 땅에서 온갖 적대적인 생물과 짐승을 몰아내야 했습니다. 단톤크에서 알드릴과 "
        "카르신을 세우면서 회색 숲을 따라 이어진 위험한 통로가 안전해졌고, 두 도시 "
        "사이의 길이 완성되었습니다. 이로써 이 동맹은 진정한 인간 연합이라 할 수 "
        "있게 되었습니다.",
    "15 III, 23 YW:":
        "웨스노스력 23년 3월 15일:\n\n"
        "내 박쥐 중 한 마리가 늙어서 죽은 모양이다. 그래서 대담하게도 그 시체를 "
        "되살리기로 했다. 정말로 되살아난 것을 보고 기뻤지만, 흥미로운 점은 따로 "
        "있었다. 박쥐가 처음 경련했을 때 마지막 생명력의 불꽃이 몸을 꿰뚫고 번쩍이는 "
        "것이 느껴졌다. 그것은 어떤 경로를 따라 흐르는 듯했다. 그로부터 한 가지 "
        "생각이 떠올랐다. 살아 있는 박쥐에게서 느낄 수 있는 것을 길잡이 삼아 정신으로 "
        "그 몸의 생명력 경로를 모두 찾아냈다. 그리고 <i>그 경로들을</i> 한꺼번에 "
        "되살리자 박쥐가 스스로 바닥에서 천천히 날개를 퍼덕이며 떠올랐다! (늙은 "
        "아이무카수르(Aimucasur)는 아마 모를 기술이다!) 더 좋은 점은 생명력 망을 "
        "흐르는 에너지가 스스로 유지되는 듯해서 계속 집중할 필요가 없었다는 것이다. "
        "이것이 비밀의 전부일까? 고대의 모든 군주가 죽은 <i>뒤에</i> 누군가에게 "
        "되살아난 것일까? 완전히 신뢰할 수 있는 다른 마법사가 필요하지만, 어쩌면 "
        "계약을 맺을 사람을 찾을 수 있을지도 모른다.",
    "The most hated living in my castle!":
        "내 성에 사는 자들 중 가장 증오하는 놈들이다! 나에게로 와라! 사막의 길 잃은 "
        "영혼들이여, 나에게로 와라! 이 오염을 정화하자!",
    "There’s too many of them for us to try":
        "둘을 모두 상대하기에는 수가 너무 많고, 게다가 이렇게 터널이 여러 갈래로 "
        "갈라져 있으면 어느 길로 가야 할지도 알 수 없어. 그들의 제안을 받아들이는 "
        "게 좋겠어. 한 진영과 동맹을 맺고 지상으로 돌아가는 길을 찾는 데 도움을 받자.",
    "Yeah, just like my old grandmam used":
        "그래, 우리 할머니가 예전에 말해 주던 것과 똑같군. 키가 작고 다부지며 턱수염이 "
        "길고, 갑오징어처럼 교활한 더러운 놈들이지. 놈들은 지하에 숨어 있다가 손에 "
        "넣을 수 있는 귀중품을 훔치러 올라와. 이건 놈들의 음모 중 일부임이 틀림없어. "
        "드워프들이 홍수를 일으킨 게 분명해!",
    "This attack is the third verse of the Song of Sun Ascension":
        "이 공격은 태양 승천의 노래의 세 번째 소절입니다. 이 유닛이 노래 소절 공격을 "
        "사용할 때마다 노래가 한 소절씩 진행됩니다.\n\n"
        "다음 차례에는 노래가 첫 번째 소절부터 다시 시작됩니다.\n\n"
        "이 노래를 사용하면 3차례 동안 조명 능력도 얻습니다.",
    "This attack is the third verse of the Song of Sun Ascension. After using it":
        "이 공격은 태양 승천의 노래의 세 번째 소절입니다. 이 공격을 사용하면 다음 "
        "차례에 첫 번째 소절을 사용할 수 있습니다. 또한 이 공격을 사용하면 3차례 "
        "동안 조명 능력을 얻습니다.",
    "A long, long time ago was the golden age among elves.":
        "아득한 옛날, 엘프에게는 황금시대가 있었습니다. 우리 민족은 눈에 보이는 곳까지 "
        "나무가 가득한 땅에서 자연과 조화를 이루며 살았습니다. 엘프와 인간·드워프 "
        "같은 다른 종족 사이에는 평화가 있었고, 사악한 생물들은 땅속 깊이 쫓겨났습니다. "
        "우리 민족은 아직 우리아(Uria)라는 불길한 이름을 알지 못했고, 우리의 힘은 "
        "하늘에 또 하나의 태양을 띄워 낮을 늘리고 어둠의 시간을 줄일 만큼 강했습니다. "
        "우리 민족은 이 긴 세월 동안 참으로 행복했지만, 그 행복은 영원하지 않았습니다.",
    "At scenarios 1 to 3, for each training level":
        "시나리오 1~3에서는 플레이어가 이미 보유한 각 훈련 단계마다 발견한 훈련자가 "
        "2~4% 확률로 고급 훈련자가 됩니다(2단계 제공).\n\n"
        "시나리오 4부터는 모든 훈련자가 항상 고급 훈련자가 되므로 이 기능은 의미가 "
        "없습니다.",
    "Speak, prey.\nYour kind fares beyond these isles.":
        "말하라, 먹잇감이여.\n너희 종족은 이 섬들 너머로 가고 있군.\n너희가 향하는 곳을 "
        "말해라.",
    "Further east, another stretch of sea":
        "더 동쪽으로 가면 또 다른 바다가 펼쳐져 있는데, 그 넓이는 앞의 바다와 거의 "
        "비슷하군.\n\n마침내 대지가 나타난다. 바다만큼 광활한 땅이지.\n마찬가지로 "
        "신비롭군.\n\n구전된 기억에 따르면 반룡들은 대혼란의 시대까지 그곳에서 "
        "번성했다고 한다.\n그때 알 수 없는 재앙으로 거의 모두 죽고 말았지.",
    "Today, my old mentor, it is I that teaches":
        "오늘은 내가 자네를 가르칠 차례일세, 오랜 스승이여.\n"
        "<i>자네</i>는 겸손에 대한 "
        "중요한 교훈을 배우게 될 걸세!",
    "It is given.\n\nTake wing!":
        "명령을 받들겠습니다.\n\n날아올라라!",
    "Excellent, we have them surrounded once more.":
        "훌륭하군. 다시 한 번 놈들을 포위했다. 이번에는 한 마리도 빠져나가지 못하게 "
        "하라. 국왕께서 놈들의 녹색 머리를 모두 망토 장식으로 삼으실 것이다.\n\n"
        "여기를 마치면 내륙 마을로 진격하여 알들을 짓밟아라. 이 작은 악마들은 더 이상 "
        "엘렌세(Elense) 요새에 문제를 일으키지 못할 것이다.",
    "Long ago, such maelstroms were strongholds":
        "오래전에는 그런 소용돌이 속에 고대의 적이 요새를 세웠지.\n지금도 그 안에 "
        "아주 사악한 것이 숨어 있을까 두렵군.\n그것과는 거리를 두는 편이 좋겠어.",
    "Gorlack, the clasher secrets may bear details":
        "고를락(Gorlack), 충돌하는 자들의 비밀에는 구전된 기억에도 없는 대지의 "
        "정보가 담겨 있을 수 있습니다.\n\n그 비밀에 귀 기울이지 않으면 어떻게 될지 "
        "두렵습니다—",
    "Speak no more of your fears!":
        "너의 두려움에 대해서는 더 이상 말하지 마라!\n\n"
        "우리는 수많은 시련을 이겨 냈다.\n수많은 적을 물리쳤지.\n"
        "그런데도 너는 아직 우리의 의지로 운명의 바람을 어떻게 바꾸는지 느끼지 "
        "못하는구나.",
    "... Gorlack, I grasp not your meaning.":
        "...고를락(Gorlack), 무슨 뜻인지 이해하지 못하겠어요.\n\n"
        "구전된 기억은 꾸준한 날개가 운명의 바람을 붙잡을 수 있다고 말하지만—",
    "When my diary is found, see that no one looks upon its pages—":
        "내 일기를 발견하거든 아무도 그 페이지를 보지 않게 해 줘—\n\n"
        "내 일기는 아주 사적인 것이란 말이야, 보넬(Vonel)!",
    "I shall keep that in mind.\nCarry on with your duty.":
        "명심하겠습니다.\n임무를 계속 수행하십시오.",
}


def repair_newline_count(source: str, translation: str) -> str:
    """Repair only literal newline-count drift after prose review."""
    while translation.startswith("\n") != source.startswith("\n"):
        if source.startswith("\n"):
            translation = "\n" + translation
        else:
            translation = translation[1:]
    while translation.endswith("\n") != source.endswith("\n"):
        if source.endswith("\n"):
            translation += "\n"
        else:
            translation = translation[:-1]
    difference = source.count("\n") - translation.count("\n")
    if difference > 0:
        for _ in range(difference):
            boundary = None
            for index, character in enumerate(translation):
                if character not in ".!?":
                    continue
                if index + 1 < len(translation) and translation[index + 1] == " ":
                    boundary = index + 1
                    break
            if boundary is None:
                break
            translation = (
                translation[:boundary] + "\n" + translation[boundary + 1 :]
            )
    elif difference < 0:
        if source.count("\n") == 0:
            return translation.replace("\n", " ")
        for _ in range(-difference):
            translation = translation.replace("\n\n", "\n", 1)
    return translation


def apply_file(path: Path) -> int:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    output: list[str] = []
    for block in blocks:
        if block.lstrip().startswith("#~"):
            output.append(block)
            continue
        values = parse_field_values(block)
        source = values.get("msgid", "")
        if not source:
            output.append(block)
            continue
        target = None
        for prefix in sorted(REPLACEMENTS, key=len, reverse=True):
            if source.startswith(prefix):
                target = REPLACEMENTS[prefix]
                break
        if "msgid_plural" in values:
            output.append(block)
            continue
        current = values.get("msgstr", "")
        if target is None:
            target = current
        target = repair_newline_count(source, target)
        if current != target:
            block = replace_msgstr_fields(block, {"msgstr": target})
            changed += 1
        output.append(block)
    if changed:
        path.write_text("\n\n".join(output), encoding="utf-8")
    return changed


def main() -> int:
    total = 0
    for path in sorted(WORK_KO.glob("*.po")):
        changed = apply_file(path)
        if changed:
            print(f"{path.name}: {changed} entries reviewed")
            total += changed
    print(f"total: {total} entries reviewed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
