#!/usr/bin/env python3
"""Normalize internal proper names to Korean transliteration with source spelling."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.project_config import GLOSSARY


FIELDS = (
    "source_term",
    "standard_korean",
    "reference_japanese",
    "reference_chinese",
    "category",
    "forbidden_terms",
    "notes",
)

# These are internal Wesnoth names whose Korean value was still the English
# spelling. Brand names, protocols, and abbreviations are intentionally absent.
TRANSLITERATIONS = {
    "Agadla": "아가들라",
    "Aigaion": "아이가이온",
    "Aleron": "알레론",
    "Apalala": "아팔랄라",
    "Bellrok": "벨록",
    "Blum Duk": "블룸 둑",
    "Bramwythl": "브람위슬",
    "Bugg": "버그",
    "Cadry": "캐드리",
    "Chumet": "추멧",
    "Cicyn": "시신",
    "Cinry": "신리",
    "Dacayan": "다카얀",
    "Darglen": "다글렌",
    "Delurin": "델루린",
    "Dwaba-Kukai": "드와바-쿠카이",
    "Dwar-Ni": "드와르-니",
    "Earooa": "에라오아",
    "Eera": "에라",
    "Elbridge": "엘브리지",
    "Elcmar": "엘크마르",
    "Elrian": "엘리안",
    "Eltenmir": "엘텐미르",
    "Everlore": "에버로어",
    "Finde": "핀드",
    "Findlas": "핀들라스",
    "Galdrad": "갈드라드",
    "Galga": "갈가",
    "Gamlel": "감렐",
    "Gelgar": "겔가르",
    "Gerrick": "게릭",
    "Ginvan": "긴반",
    "Glasar": "글라사르",
    "Gnaba": "그나바",
    "Graak": "그라크",
    "Grek": "그렉",
    "Grook": "그룩",
    "Groth": "그로스",
    "Gruak": "그루악",
    "Gwaba": "과바",
    "Gwarloa": "그와를로아",
    "Gwimli": "귀믈리",
    "Gwoama": "그와마",
    "Haf-Mal": "하프-말",
    "Haldiel": "할디엘",
    "Heldaga": "헬다가",
    "Illan": "일란",
    "Inalai": "이나라이",
    "Jarek": "자렉",
    "Jarmal-Gorg": "자르말-고르그",
    "Jera Ilras": "제라 일라스",
    "Joran": "조란",
    "Josephus": "조세푸스",
    "Jul": "줄",
    "Kaba": "카바",
    "Kalba": "칼바",
    "Knafa-Tan": "크나파-탄",
    "Kojun Herolm": "코준 헤롤름",
    "Kramak": "크라막",
    "Kwaboo": "콰부",
    "Linderion": "린데리온",
    "Liryn": "리린",
    "Loflar": "로플라르",
    "Mabooa": "마부아",
    "Maelvas": "마엘바스",
    "Maga-Knafa": "마가-크나파",
    "Makees": "메이키스",
    "Mal Tera": "말 테라",
    "Mal-Akranbral": "말-아크란브랄",
    "Mal-Drakanal": "말-드라카날",
    "Mal-Kallat": "말-칼랏",
    "Mal-Katklagad": "말-카트클라가드",
    "Mal-Larakan": "말-라라칸",
    "Mal-Skraat": "말-스크라트",
    "Mal-Tar": "말-타르",
    "Mal-Xakralan": "말-자크랄란",
    "Mal-Xaskanat": "말-자스카낫",
    "Mal-un-Darak": "말-운-다라크",
    "Mal-un-Xadrux": "말-운-자드룩스",
    "Mal-un-Zanrad": "말-운-잔라드",
    "Malatus": "말라투스",
    "Meris": "메리스",
    "Mitche": "미치",
    "Mithalwe": "미탈웨",
    "Mokho Kimer": "모코 키메르",
    "Mokolo Qimur": "모콜로 키무르",
    "Moremirmu": "모레미르무",
    "Moreth": "모레스",
    "Mriram": "미리람",
    "Muff Jaanal": "머프 자날",
    "Muff Malal": "머프 말랄",
    "Myssh": "미시",
    "Na-alga": "나-알가",
    "Nafga": "나프가",
    "Nepba": "넵바",
    "Nethuns": "네툰스",
    "Nilaf": "닐라프",
    "Niodien": "니오디엔",
    "O O": "오 오",
    "Oceania": "오세아니아",
    "Orome": "오로메",
    "Owaec": "오와에크",
    "Parandra": "파란드라",
    "Rah Ihn Mar": "라 이흔 마르",
    "Rava-Krodaz": "라바-크로다즈",
    "Reglok": "레글록",
    "Rheban": "레반",
    "Rilhon": "릴혼",
    "Robryn": "로브린",
    "Seimus": "세이무스",
    "Selda-Mana": "셀다-마나",
    "Seran": "세란",
    "Simyr": "시미르",
    "Syryn": "시린",
    "Tarcyn": "타르신",
    "Terraent": "테라엔트",
    "Tindolean": "틴돌리언",
    "Tini": "티니",
    "Triram": "트리람",
    "Tarek": "타렉",
    "Tyborg": "타이보그",
    "Ufes": "유페스",
    "Uradredia": "우라드레디아",
    "Urug-Telfar": "우루그-텔파르",
    "Vardanos": "바르다노스",
    "Varrak-Klar": "바락-클라르",
    "Veocyn": "비오신",
    "Xakae": "자카에",
    "Xnamas": "크사마스",
    "Ylla": "일라",
    "Yran": "이란",
    "Yredd": "이레드",
}

EXTERNAL_IDENTIFIERS = {"Discord", "IRC", "Reddit", "SoF", "Steam", "WC", "WoCopedia"}


def update_glossary(path: Path) -> tuple[int, list[str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = list(reader)
        fieldnames = tuple(reader.fieldnames or ())

    changed: list[str] = []
    for row in rows:
        source = row["source_term"]
        if source not in TRANSLITERATIONS or source in EXTERNAL_IDENTIFIERS:
            continue
        if row["standard_korean"] == source or source == "Tarek":
            row["standard_korean"] = f"{TRANSLITERATIONS[source]} ({source})"
            row["notes"] = (
                "내부 고유명사: 한국어 음차와 원문을 항상 병기; "
                "중국어 음역과 기존 한국어 참고자료를 대조"
            )
            changed.append(source)

    if fieldnames != FIELDS:
        raise ValueError(f"unexpected glossary schema: {fieldnames}")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=fieldnames, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    return len(changed), changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--glossary", type=Path, default=GLOSSARY
    )
    args = parser.parse_args()
    count, changed = update_glossary(args.glossary)
    print(f"updated: {count}")
    print("\n".join(changed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
