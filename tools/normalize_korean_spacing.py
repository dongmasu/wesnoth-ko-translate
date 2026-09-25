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
)


def normalize_block(block: str) -> tuple[str, int]:
    if block.lstrip().startswith("#~") or "msgid " not in block:
        return block, 0

    changed = 0
    output: list[str] = []
    in_translation = False
    for line in block.splitlines(keepends=True):
        if line.startswith("msgstr"):
            in_translation = True
        elif line.startswith("msgid") or line.startswith("msgctxt"):
            in_translation = False

        if in_translation and (
            line.startswith('"') or line.startswith("msgstr")
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
