"""Парсинг групп ИЭФ со страницы miit.ru/timetable."""

import csv
from pathlib import Path
import re

INSTITUTE_CODE = "IEF"
HTML_PATH = Path(__file__).resolve().parents[1] / "_timetable.html"
OUT_PATH = (
    Path(__file__).resolve().parents[1] / "teams" / "data" / "ief_study_groups.csv"
)

COURSE_RE = re.compile(
    r'<span class="text-form__item-name">(\d+)\s*курс</span>',
)
LINK_RE = re.compile(
    r'<a href="/timetable/(\d+)"[^>]*>\s*([^<]+?)\s*</a>',
    re.DOTALL,
)
# Подписи dropdown-toggle без отдельной ссылки на группу
SKIP_NAMES = frozenset({"ЭПИ", "ЭБР", "ЭМПд", "ЭМЭ", "ЭСБ"})


def extract_block(html: str) -> str:
    start = html.find('<div id="ИЭФ"')
    if start == -1:
        raise ValueError("Блок ИЭФ не найден")
    end = html.find('<div id="ПИШ-"Академия-ВСМ""', start)
    if end == -1:
        end = html.find('id="ПИШ-"Академия-ВСМ"', start)
    if end == -1:
        raise ValueError("Конец блока ИЭФ не найден")
    return html[start:end]


def parse_groups(block: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    course_positions = [(m.start(), int(m.group(1))) for m in COURSE_RE.finditer(block)]
    if not course_positions:
        return rows

    for i, (pos, course) in enumerate(course_positions):
        next_pos = (
            course_positions[i + 1][0] if i + 1 < len(course_positions) else len(block)
        )
        section = block[pos:next_pos]
        for code, name in LINK_RE.findall(section):
            name = re.sub(r"\s+", " ", name).strip()
            if not name or name in SKIP_NAMES:
                continue
            rows.append(
                {
                    "Институт": INSTITUTE_CODE,
                    "Название группы": name,
                    "Курс": str(course),
                    "Код": code,
                    "Направление обучения": "",
                }
            )
    return rows


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    block = extract_block(html)
    rows = parse_groups(block)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "Институт",
                "Название группы",
                "Курс",
                "Код",
                "Направление обучения",
            ],
        )
        w.writeheader()
        w.writerows(rows)
    print(f"Записано {len(rows)} групп -> {OUT_PATH}")


if __name__ == "__main__":
    main()
