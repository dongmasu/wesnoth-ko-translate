#!/usr/bin/env python3
"""Fix unambiguous spacing errors in active Korean PO translations."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.project_config import WORK_KO


REPLACEMENTS = (
    (re.compile(r"다름 이름"), "다른 이름"),
    (re.compile(r"빌견되지"), "발견되지"),
    (re.compile(r"죽은자"), "죽은 자"),
    (re.compile(r"죽은자의"), "죽은 자의"),
    (re.compile(r"치명타가 꽃히는것"), "치명타가 꽂히는 것"),
    (re.compile(r"안통"), "안 통"),
    (re.compile(r"중인듯"), "중인 듯"),
    (re.compile(r"못믿"), "못 믿"),
    (re.compile(r"몇달"), "몇 달"),
    (re.compile(r"울려퍼"), "울려 퍼"),
    (re.compile(r"게을러질때"), "게을러질 때"),
    (re.compile(r"어릴적"), "어릴 적"),
    (re.compile(r"필요없"), "필요 없"),
    (re.compile(r"할것"), "할 것"),
    (re.compile(r"할거"), "할 거"),
    (re.compile(r"될것"), "될 것"),
    (re.compile(r"을것"), "을 것"),
    (re.compile(r"ㄹ것"), "ㄹ 것"),
    (re.compile(r"것같"), "것 같"),
    (re.compile(r"것에대해"), "것에 대해"),
    (re.compile(r"없어진건"), "없어진 건"),
    (re.compile(r"할수"), "할 수"),
    (re.compile(r"해야 겠"), "해야겠"),
    (re.compile(r"안됩니다"), "안 됩니다"),
    (re.compile(r"해야합니다"), "해야 합니다"),
    (re.compile(r"해야하고"), "해야 하고"),
    (re.compile(r"해야한다"), "해야 한다"),
    (re.compile(r"가고싶"), "가고 싶"),
    (re.compile(r"할수밖에"), "할 수밖에"),
    (re.compile(r"하는것"), "하는 것"),
    (re.compile(r"온것"), "온 것"),
    (re.compile(r"한것"), "한 것"),
    (re.compile(r"소집하는것"), "소집하는 것"),
    (re.compile(r"점령하는것"), "점령하는 것"),
    (re.compile(r"할수"), "할 수"),
    (re.compile(r"몇개"), "몇 개"),
    (re.compile(r"몇번"), "몇 번"),
    (re.compile(r"안되요"), "안 돼요"),
    (re.compile(r"안되나요"), "안 되나요"),
    (re.compile(r"안된다"), "안 된다"),
    (re.compile(r"안되면"), "안 되면"),
    (re.compile(r"안되오"), "안 되오"),
    (re.compile(r"안되고"), "안 되고"),
    (re.compile(r"안되는"), "안 되는"),
    (re.compile(r"안되었"), "안 되었"),
    (re.compile(r"안보"), "안 보"),
    (re.compile(r"것때문에"), "것 때문에"),
    (re.compile(r"것으로보니"), "것으로 보니"),
    (re.compile(r"되어있"), "되어 있"),
    (re.compile(r"보관 되어"), "보관되어"),
    (re.compile(r"돌아서서"), "돌아서"),
    (re.compile(r"쫒"), "쫓"),
    (re.compile(r"볼떄"), "볼 때"),
    (re.compile(r"그정도"), "그 정도"),
    (re.compile(r"저것좀"), "저것 좀"),
    (re.compile(r"돌로된"), "돌로 된"),
    (re.compile(r"몇개의"), "몇 개의"),
    (re.compile(r"수 많은"), "수많은"),
    (re.compile(r"이 모든게"), "이 모든 게"),
    (re.compile(r"무슨일"), "무슨 일"),
    (re.compile(r"어쩔수없"), "어쩔 수 없"),
    (re.compile(r"다시한번"), "다시 한 번"),
    (re.compile(r"이쪽편"), "이쪽 편"),
    (re.compile(r"가야해"), "가야 해"),
    (re.compile(r"해야해"), "해야 해"),
    (re.compile(r"정리를해야"), "정리를 해야"),
    (re.compile(r"절때"), "절대"),
    (re.compile(r"난장이"), "난쟁이"),
    (re.compile(r"쫒아"), "쫓아"),
    (re.compile(r"댓가"), "대가"),
    (re.compile(r"첫번째"), "첫 번째"),
    (re.compile(r"세번째"), "세 번째"),
    (re.compile(r"부딛혀"), "부딪혀"),
    (re.compile(r"가본적"), "가 본 적"),
    (re.compile(r"내옆"), "내 옆"),
    (re.compile(r"한마리"), "한 마리"),
    (re.compile(r"그터널"), "그 터널"),
    (re.compile(r"우리영토"), "우리 영토"),
    (re.compile(r"모든것"), "모든 것"),
    (re.compile(r"나의것"), "나의 것"),
    (re.compile(r"두번째"), "두 번째"),
    (re.compile(r"그이야기"), "그 이야기"),
    (re.compile(r"([가-힣])것이다"), r"\1 것이다"),
    (re.compile(r"([가-힣])것이야"), r"\1 것이야"),
    (re.compile(r"([가-힣])것같"), r"\1 것 같"),
    (re.compile(r"([가-힣])거야"), r"\1 거야"),
    (re.compile(r"([가-힣])겁니다"), r"\1 겁니다"),
    (re.compile(r"([가-힣])할수"), r"\1 할 수"),
    (re.compile(r"([가-힣])때문"), r"\1 때문"),
    (re.compile(r"수백년"), "수백 년"),
    (re.compile(r"수십년"), "수십 년"),
    (re.compile(r"수천년"), "수천 년"),
    (re.compile(r"할때"), "할 때"),
    (re.compile(r"있을때"), "있을 때"),
    (re.compile(r"끝장날때"), "끝장날 때"),
    (re.compile(r"몇 년후"), "몇 년 후"),
    (re.compile(r"([가-힣])들중"), r"\1들 중"),
    (re.compile(r"소집가능"), "소집 가능한"),
    (re.compile(r"이동가능범위"), "이동 가능한 범위"),
    (re.compile(r"이동가능"), "이동 가능한"),
    (re.compile(r"체팅"), "채팅"),
    (re.compile(r"해야할"), "해야 할"),
    (re.compile(r"할수있는"), "할 수 있는"),
    (re.compile(r"공격해야할"), "공격해야 할"),
    (re.compile(r"않는것"), "않는 것"),
    (re.compile(r"멀지않은"), "멀지 않은"),
    (re.compile(r"되어야한다"), "되어야 한다"),
    (re.compile(r"될거"), "될 거"),
    (re.compile(r"할거"), "할 거"),
    (re.compile(r"않는걸"), "않는 걸"),
    (re.compile(r"신경쓰"), "신경 쓰"),
    (re.compile(r"원치않"), "원치 않"),
    (re.compile(r"바랬"), "바랐"),
    (re.compile(r"희망이없"), "희망이 없"),
    (re.compile(r"보호되고있"), "보호되고 있"),
    (re.compile(r"두번쨰"), "두 번째"),
    (re.compile(r"안좋"), "안 좋"),
    (re.compile(r"몇가지"), "몇 가지"),
    (re.compile(r"더이상"), "더 이상"),
    (re.compile(r"두배"), "두 배"),
    (re.compile(r"잊지마"), "잊지 마"),
    (re.compile(r"있는거"), "있는 거"),
    (re.compile(r"서있는"), "서 있는"),
    (re.compile(r"있는것"), "있는 것"),
    (re.compile(r"없는것"), "없는 것"),
    (re.compile(r"인것"), "인 것"),
    (re.compile(r"였을때"), "였을 때"),
    (re.compile(r"몇분"), "몇 분"),
    (re.compile(r"깊은곳"), "깊은 곳"),
    (re.compile(r"에서서"), "에 서서"),
    (re.compile(r"뭉쳐야합니다"), "뭉쳐야 합니다"),
    (re.compile(r"아퍼져"), "아파져"),
    (re.compile(r"못헤요"), "못해요"),
    (re.compile(r"대 학원"), "대학원"),
    (re.compile(r"마리중"), "마리 중"),
    (re.compile(r"차례때"), "차례 때"),
    (re.compile(r"사로 잡"), "사로잡"),
    (re.compile(r"유지 하지"), "유지하지"),
    (re.compile(r"소집 할"), "소집할"),
    (re.compile(r"살아있는"), "살아 있는"),
    (re.compile(r"평생동안"), "평생 동안"),
    (re.compile(r"자기자신"), "자기 자신"),
    (re.compile(r"무릎꿇"), "무릎 꿇"),
    (re.compile(r"몇군데"), "몇 군데"),
    (re.compile(r"북쪽지역"), "북쪽 지역"),
    (re.compile(r"좀더"), "좀 더"),
    (re.compile(r"또다른"), "또 다른"),
    (re.compile(r"같은건"), "같은 건"),
    (re.compile(r"있는건"), "있는 건"),
    (re.compile(r"없는건"), "없는 건"),
    (re.compile(r"되는것"), "되는 것"),
    (re.compile(r"것같다"), "것 같다"),
    (re.compile(r"동작 하지"), "동작하지"),
    (re.compile(r"걱정하지마"), "걱정하지 마"),
    (re.compile(r"추적 할"), "추적할"),
    (re.compile(r"돌아 가"), "돌아가"),
    (re.compile(r"알고있는"), "알고 있는"),
    (re.compile(r"자랑스러워 하"), "자랑스러워하"),
    (re.compile(r"따르기만하는"), "따르기만 하는"),
    (re.compile(r"전투시에"), "전투 시에"),
    (re.compile(r"보좌해준"), "보좌해 준"),
    (re.compile(r"하는게"), "하는 게"),
    (re.compile(r"씻기는게"), "씻기는 게"),
    (re.compile(r"안그럴"), "안 그럴"),
    (re.compile(r"할께"), "할게"),
    (re.compile(r"거에요"), "거예요"),
    (re.compile(r"감사하고 ,"), "감사하고,"),
    (re.compile(r"몇일"), "며칠"),
    (re.compile(r"이 곳"), "이곳"),
    (re.compile(r"돌아가려했"), "돌아가려 했"),
    (re.compile(r"께요"), "게요"),
    (re.compile(r"([가-힣])거예요"), r"\1 거예요"),
    (re.compile(r"([가-힣])거다"), r"\1 거다"),
    (re.compile(r"([가-힣])거야"), r"\1 거야"),
    (re.compile(r"있을곳"), "있을 곳"),
    (re.compile(r"있는곳"), "있는 곳"),
    (re.compile(r"상징같은"), "상징 같은"),
    (re.compile(r"매우큰"), "매우 큰"),
    (re.compile(r"난것"), "난 것"),
    (re.compile(r"모우려고"), "모으려고"),
    (re.compile(r"오우 거예요"), "오우거예요"),
    (re.compile(r"알려줘야해요"), "알려 줘야 해요"),
    (re.compile(r"치안 판사 인"), "치안 판사인"),
    (re.compile(r"가치있는"), "가치 있는"),
    (re.compile(r"기병를"), "기병을"),
    (re.compile(r"태울만큼"), "태울 만큼"),
    (re.compile(r"잘만난 것"), "잘 만난 것"),
    (re.compile(r"속지마십시오"), "속지 마십시오"),
    (re.compile(r"한번도"), "한 번도"),
    (re.compile(r"살아있다는"), "살아 있다는"),
    (re.compile(r"지금즘이면"), "지금쯤이면"),
    (re.compile(r"하수도으로"), "하수도로"),
    (re.compile(r"소집 가능한한"), "소집 가능한"),
    (re.compile(r"이동 가능한한"), "이동 가능한"),
    (re.compile(r"가능한한 오래"), "가능한 한 오래"),
    (re.compile(r"([가-힣])에의해"), r"\1에 의해"),
    (re.compile(r"있는동안"), "있는 동안"),
    (re.compile(r"지난동안"), "지난 동안"),
    (re.compile(r"([가-힣])하지마"), r"\1하지 마"),
    (re.compile(r"하지마"), "하지 마"),
    (re.compile(r"가담해준"), "가담해 준"),
    (re.compile(r"싸워주"), "싸워 주"),
    (re.compile(r"보여주"), "보여 주"),
    (re.compile(r"떠나는게"), "떠나는 게"),
    (re.compile(r"대장인것"), "대장인 것"),
    (re.compile(r"걱정되는건"), "걱정되는 건"),
    (re.compile(r"가본적"), "가 본 적"),
    (re.compile(r"어야해"), "어야 해"),
    (re.compile(r"알아야해"), "알아야 해"),
    (re.compile(r"남아있어야"), "남아 있어야"),
    (re.compile(r"원하는게"), "원하는 게"),
    (re.compile(r"못하는게"), "못하는 게"),
    (re.compile(r"두려워하지마"), "두려워하지 마"),
    (re.compile(r"포기하지마"), "포기하지 마"),
    (re.compile(r"생각하지마"), "생각하지 마"),
    (re.compile(r"모다 두는것이"), "모아 두는 것이"),
    (re.compile(r"달라지는건"), "달라지는 건"),
    (re.compile(r"모든게"), "모든 게"),
    (re.compile(r"보낸지"), "보낸 지"),
    (re.compile(r"있을거"), "있을 거"),
    (re.compile(r"안되네"), "안 되네"),
    (re.compile(r"안되면"), "안 되면"),
    (re.compile(r"할테니"), "할 테니"),
    (re.compile(r"알테니"), "알 테니"),
    (re.compile(r"참여 할"), "참여할"),
    (re.compile(r"동작 할"), "동작할"),
    (re.compile(r"맡기고"), "맡기고"),
    (re.compile(r"바랄뿐"), "바랄 뿐"),
    (re.compile(r"가까워지는것"), "가까워지는 것"),
    (re.compile(r"서있는것"), "서 있는 것"),
    (re.compile(r"한번"), "한 번"),
    (re.compile(r"수백개의"), "수백 개의"),
    (re.compile(r"수십개의"), "수십 개의"),
    (re.compile(r"몇개의"), "몇 개의"),
    (re.compile(r"한개의"), "한 개의"),
    (re.compile(r"두개의"), "두 개의"),
    (re.compile(r"요새들이곳곳"), "요새들이 곳곳"),
    (re.compile(r"그 건"), "그건"),
    (re.compile(r"그말"), "그 말"),
    (re.compile(r"닫힌후"), "닫힌 후"),
    (re.compile(r"내것"), "내 것"),
    (re.compile(r"어느정도"), "어느 정도"),
    (re.compile(r"다가가지마"), "다가가지 마"),
    (re.compile(r"놀린거"), "놀린 거"),
    (re.compile(r"마법사놈"), "마법사 놈"),
    (re.compile(r"못봤"), "못 봤"),
    (re.compile(r"안먹힐"), "안 먹힐"),
    (re.compile(r"볼줄"), "볼 줄"),
    (re.compile(r"도끼맛"), "도끼 맛"),
    (re.compile(r"만들어주"), "만들어 주"),
    (re.compile(r"걸맞는"), "걸맞은"),
    (re.compile(r"부족들간"), "부족들 간"),
    (re.compile(r"목말라하는"), "목말라 하는"),
    (re.compile(r"이야기 할"), "이야기할"),
    (re.compile(r"잠시후"), "잠시 후"),
    (re.compile(r"싸움붙이"), "싸움 붙이"),
    (re.compile(r"왔다갔다"), "왔다 갔다"),
    (re.compile(r"몇 안 되는"), "몇 안 되는"),
    (re.compile(r"아무 것도"), "아무것도"),
    (re.compile(r"([0-9]+)일동안"), r"\1일 동안"),
    (re.compile(r"잠시동안"), "잠시 동안"),
    (re.compile(r"세월동안"), "세월 동안"),
)


def normalize_block(block: str) -> tuple[str, int]:
    if "msgid " not in block and "#~ msgid " not in block:
        return block, 0

    changed = 0
    output: list[str] = []
    in_translation = False
    for line in block.splitlines(keepends=True):
        if line.startswith("msgstr") or line.startswith("#~ msgstr"):
            in_translation = True
        elif (
            line.startswith("msgid")
            or line.startswith("msgctxt")
            or line.startswith("#~ msgid")
            or line.startswith("#~ msgctxt")
        ):
            in_translation = False

        if in_translation and (
            line.startswith('"') or line.startswith("msgstr")
            or line.startswith("#~ \"") or line.startswith("#~ msgstr")
        ):
            updated = line
            for pattern, replacement in REPLACEMENTS:
                updated, count = pattern.subn(replacement, updated)
                changed += count
            line = updated
        output.append(line)
    return "".join(output), changed


def normalize_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    blocks = text.split("\n\n")
    total = 0
    normalized = []
    for block in blocks:
        block, changed = normalize_block(block)
        total += changed
        normalized.append(block)
    if total:
        path.write_text("\n\n".join(normalized), encoding="utf-8")
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path, nargs="?", default=WORK_KO)
    args = parser.parse_args()
    total = 0
    for path in sorted(args.directory.glob("*.po")):
        changed = normalize_file(path)
        if changed:
            print(f"{path.name}: {changed}")
            total += changed
    print(f"total replacements: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
