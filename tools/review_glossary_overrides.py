#!/usr/bin/env python3
"""Apply high-confidence glossary corrections consistently to work PO files."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


OVERRIDES = {
    "About the Game": "게임 정보",
    "Assign Local Time Schedule": "현지 시간 일정",
    "After the Fall": "몰락 이후",
    "Also kill Marg-Tonz": "Marg-Tonz도 처치하라",
    "Artwork and Graphics": "아트워크 및 그래픽",
    "Be more aggressive": "더 공격적으로 행동",
    "Be more defensive": "더 방어적으로 행동",
    "Be sure to explore": "반드시 탐험하세요",
    "Back to Turn ": "지정 턴으로 돌아가기",
    "Best Possible Enemy Moves": "적의 최선의 행동",
    "Build a Keep": "본영 건설",
    "Change Unit ID": "유닛 ID 변경",
    "Chat message aging": "채팅 메시지 만료",
    "Clear special orders": "특수 명령 초기화",
    "Clear the caves": "동굴을 정리하라",
    "Clear the Ground": "지면 정리",
    "Clearing the Mines": "광산 정리",
    "Complete the ritual": "의식을 완료하세요",
    "Confirm deleting saves": "저장 파일 삭제 확인",
    "Continue as before": "이전처럼 계속",
    "Current hex type": "현재 육각 타일 유형",
    "Damage Types and Resistance": "피해 유형 및 저항력",
    "Dependencies Installation Failed": "종속 항목 설치 실패",
    "Descending into Darkness": "어둠 속으로 내려가기",
    "Descent into Darkness": "어둠 속으로의 추락",
    "Desert Impassable Mountains": "사막의 통과 불가 산맥",
    "Destroy a fierce enemy": "사나운 적을 무찔러라",
    "Display animated terrain graphics": "애니메이션 지형 그래픽 표시",
    "Dwarf High Guard": "드워프 고위 경비대",
    "Dwarven Castle Keep": "드워프 성채 본영",
    "Error loading map": "지도 불러오기 오류",
    "Error loading mask": "마스크 불러오기 오류",
    "Fallen Lich Point": "몰락한 리치 곶",
    "File not found": "파일을 찾을 수 없습니다",
    "Finding Your Way": "길 찾기",
    "Ford of Alyas": "Alyas 여울",
    "Ford of Tifranur": "Tifranur 여울",
    "Get the Gold": "금화 획득",
    "Get yourself killed": "죽음을 자초하라",
    "Go Here Overlay": "여기로 이동 오버레이",
    "Great Chief Brurbar": "대족장 Brurbar",
    "Hex Line NW-SE": "북서-남동 육각형 선",
    "Invalid location id": "잘못된 위치 ID",
    "Keep Velon alive": "Velon을 생존시키기",
    "Latest Campaign Revision": "최신 캠페인 개정",
    "Load a saved game": "저장된 게임 불러오기",
    "Make definition list": "정의 목록 만들기",
    "Map loaded from scenario": "시나리오에서 불러온 지도",
    "Naga Sentinel": "나가 보초병",
    "No objectives available": "사용 가능한 목표 없음",
    "Oases heal and cure": "오아시스에서는 회복 및 치료 가능",
    "pause after current move": "현재 이동 후 일시정지",
    "Point of view": "시점",
    "Prose and Story Editing": "산문 및 이야기 편집",
    "Quit to Desktop": "바탕 화면으로 나가기",
    "Save Scenario As": "다른 이름으로 시나리오 저장",
    "Set Team Label": "팀 레이블 설정",
    "Show color cursors": "컬러 커서 표시",
    "Show deprecation messages in-game": "게임 내 사용 중단 예정 메시지 표시",
    "Server-side redirect loop": "서버 측 리디렉션 반복",
    "Start the map editor": "지도 편집기 시작",
    "The City Falls": "도시가 함락되다",
    "The Great Chamber": "대회의실",
    "The King is Dead": "왕이 죽었다",
    "The Knolls of Doldesh": "돌데시 언덕",
    "Three merfolk must survive": "인어족 3명이 생존해야 한다",
    "Time of Day": "시간대",
    "Cloaked Figure": "복면의 인물",
    "Delete Save": "저장 파일 삭제",
    "Herbalism": "약초학",
    "Lost Soul": "떠도는 영혼",
    "Mainline": "본편",
    "Ethereal Nightgaunt": "신비한 나이트건트",
    "nova": "신성",
    "Over the Northern Mountains": "북부 산맥 너머",
    "Regular Impassable Mountains": "일반 통과 불가 산맥",
    "refreshed": "회복됨",
    "Siege of Laurelmor": "로렐모르 포위전",
    "Show all lobby joins": "로비 입장 메시지 모두 표시",
    "Snowy Impassable Mountains": "눈 덮인 통과 불가 산맥",
    "Start Editor": "편집기 시작",
    "Still Another Wanderer": "또 다른 방랑자",
    "Steelclad": "강철갑옷",
    "Text file": "텍스트 파일",
    "Troll Flamecaster": "트롤 화염술사",
    "Turn dialog": "턴 대화 상자",
    "Undead Followers": "언데드 추종자들",
    "Variable not found": "변수를 찾을 수 없습니다",
    "wmlindent": "wmlindent",
    "wmlindent mode": "wmlindent 모드",
    "wmlindent options": "wmlindent 옵션",
    "wmllint": "wmllint",
    "wmllint mode": "wmllint 모드",
    "wmllint options": "wmllint 옵션",
    "wmlscope": "wmlscope",
    "wmlscope options": "wmlscope 옵션",
    "Turns run out": "턴이 모두 소진됨",
}


def update_glossary(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    changed = 0
    for row in rows:
        if row["source_term"] in OVERRIDES and row["standard_korean"] != OVERRIDES[row["source_term"]]:
            row["standard_korean"] = OVERRIDES[row["source_term"]]
            row["notes"] = "전체 용어집 재검토에서 직역·오역·오탈자를 수정"
            changed += 1
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return changed


def po_quote(value: str) -> str:
    return (
        '"'
        + value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\t", "\\t")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        + '"'
    )


def parse_msgid(block: str) -> str:
    import ast

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


def update_po(path: Path) -> int:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    output = []
    for block in blocks:
        source = parse_msgid(block)
        translation = OVERRIDES.get(source)
        if translation is None or re.search(r"^msgid_plural ", block, re.M):
            output.append(block)
            continue
        lines = block.splitlines()
        for index, line in enumerate(lines):
            if re.match(r"^msgstr(?:\[0\])? ", line):
                field = line.split(" ", 1)[0]
                lines[index:] = [f"{field} {po_quote(translation)}"]
                changed += 1
                break
        output.append("\n".join(lines))
    path.write_text("\n\n".join(output), encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glossary", type=Path, default=Path("work/1.18.x/glossary.tsv"))
    parser.add_argument("--work", type=Path, default=Path("work/1.18.x/ko"))
    args = parser.parse_args()

    print(f"glossary: {update_glossary(args.glossary)} entries updated")
    total = 0
    for path in sorted(args.work.glob("*.po")):
        count = update_po(path)
        if count:
            print(f"{path.name}: {count} entries updated")
            total += count
    print(f"po total: {total} entries updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
