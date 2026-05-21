"""Собрать fgos_specialitet_napravleniya.csv: level, code, name (без групп XX.00.00)."""

import csv
from html import unescape
from pathlib import Path
import re
from urllib.request import Request, urlopen

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
BASE = (
    "https://obrnadzor.gov.ru/gosudarstvennye-uslugi-i-funkczii/"
    "7701537808-gosfunction/acts_list2021/mandatory_requirements_2021/"
)
BAK_URL = BASE + "fgos_bakalavriat/"
SPE_URL = BASE + "fgos_specialitet/"


def parse_table_rows(html: str) -> list[tuple[str, str]]:
    return re.findall(
        r"<tr>\s*<td[^>]*>([^<]*)</td>\s*<td[^>]*>([^<]*)</td>",
        html,
        re.I,
    )


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def collect_codes(html: str, middle: str) -> dict[str, str]:
    """middle: '03' — бакалавриат, '05' — специалитет."""
    out: dict[str, str] = {}
    pat = re.compile(rf"^\d{{2}}\.{middle}\.\d{{2}}$")
    for code_raw, name_raw in parse_table_rows(html):
        code = unescape(code_raw).strip()
        name = unescape(name_raw).strip()
        if not pat.match(code):
            continue
        out[code] = name
    return out


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    bak = collect_codes(fetch(BAK_URL), "03")
    spe = collect_codes(fetch(SPE_URL), "05")

    rows: list[tuple[str, str, str]] = []
    for code in sorted(bak):
        rows.append(("бакалавриат", code, bak[code]))
    for code in sorted(spe):
        rows.append(("специалитет", code, spe[code]))

    out_path = root / "teams" / "data" / "fgos_specialitet_napravleniya.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["level", "code", "name"])
        w.writerows(rows)

    n = len(rows)
    print(f"Бакалавриат: {len(bak)}, специалитет: {len(spe)}, всего: {n} -> {out_path}")


if __name__ == "__main__":
    main()
