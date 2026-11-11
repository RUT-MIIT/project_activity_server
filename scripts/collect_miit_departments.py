"""Собирает структуру подразделений с https://www.miit.ru/depts в JSON.

Установка: python -m pip install playwright
Браузер: python -m playwright install chromium (или --browser msedge для Edge).
Запуск: python scripts/collect_miit_departments.py
"""

import argparse
from collections import defaultdict, deque
import json
from pathlib import Path
import re
import sys
from time import sleep
from urllib.parse import urljoin, urlsplit


CATALOG_URL = "https://www.miit.ru/depts"
HOSTS = {"miit.ru", "www.miit.ru", "rut-miit.ru", "www.rut-miit.ru"}
LINKS = 'a[href*="/depts/"]'
UNLINKED_PARENT = "В карточке указан родитель без ссылки на подразделение"

CATALOG_ROWS = r"""links => links.map(link => {
    let section = link.parentElement;
    while (section && !section.id) section = section.parentElement;
    return {
        url: link.href,
        label: link.textContent.replace(/\s+/g, ' ').trim(),
        section: section?.querySelector('h3')?.textContent.trim() ?? null,
    };
})"""

CARD_FIELDS = r"""label => {
    const normalize = text => text.replace(/\s+/g, ' ').trim();
    const row = label.parentElement;
    const fields = Array.from(row.parentElement.children);
    const parent = fields.find(field =>
        normalize(field.firstElementChild?.textContent ?? '') === 'Входит в состав'
    )?.children[1];
    return {
        name: normalize(label.nextElementSibling?.textContent ?? ''),
        parents: Array.from(parent?.querySelectorAll('a[href]') ?? [], link => link.href),
        parent_label: normalize(parent?.textContent ?? '') || null,
    };
}"""


def department_id(url: str) -> int | None:
    parsed = urlsplit(urljoin(CATALOG_URL, url))
    match = re.fullmatch(r"/depts/(\d+)/?", parsed.path)
    if parsed.scheme == "https" and parsed.hostname in HOSTS and match:
        return int(match[1])
    return None


def add_department(departments: dict, pending: deque, key: int) -> dict:
    if key not in departments:
        departments[key] = {
            "id": key,
            "url": f"{CATALOG_URL}/{key}",
            "name": None,
            "catalog_label": None,
            "sections": [],
            "parent_ids": [],
            "parent_label": None,
            "error": None,
        }
        pending.append(key)
    return departments[key]


def open_page(page, url: str) -> None:
    response = page.goto(url, wait_until="domcontentloaded")
    if response is None or not response.ok:
        status = response.status if response else "нет ответа"
        raise ValueError(f"{url}: {status}")


def resolve_text_parents(departments: dict) -> None:
    ids_by_name = defaultdict(set)
    for item in departments.values():
        for label in (item["name"], item["catalog_label"]):
            if label:
                ids_by_name[label.casefold()].add(item["id"])
                full_name, separator, _ = label.rpartition(", ")
                if separator:
                    ids_by_name[full_name.casefold()].add(item["id"])

    for item in departments.values():
        if item["error"] != UNLINKED_PARENT:
            continue
        matches = ids_by_name[item["parent_label"].casefold()] - {item["id"]}
        if len(matches) == 1:
            item["parent_ids"] = sorted(matches)
            item["error"] = None


def collect(page, delay: float, browser_error: type[Exception]) -> dict:
    open_page(page, CATALOG_URL)
    links = page.locator(LINKS)
    links.first.wait_for(state="attached")
    departments = {}
    pending = deque()
    for link in links.evaluate_all(CATALOG_ROWS):
        key = department_id(link["url"])
        if key is None or not link["label"]:
            continue
        item = add_department(departments, pending, key)
        item["catalog_label"] = item["catalog_label"] or link["label"]
        section = link["section"]
        if section and section not in item["sections"]:
            item["sections"].append(section)
    if not pending:
        raise ValueError("В каталоге не найдено ссылок на карточки подразделений")

    while pending:
        key = pending.popleft()
        item = departments[key]
        sleep(delay)
        try:
            open_page(page, item["url"])
            if department_id(page.url) != key:
                raise ValueError(f"Неожиданное перенаправление на {page.url}")
            card = page.get_by_text("Наименование", exact=True).first.evaluate(CARD_FIELDS)
            if not card["name"]:
                raise ValueError("Карточка не содержит наименование")
            item["name"] = card["name"]
            item["parent_label"] = card["parent_label"]
            for url in card["parents"]:
                parent = department_id(url)
                if parent is not None and parent != key and parent not in item["parent_ids"]:
                    item["parent_ids"].append(parent)
                    add_department(departments, pending, parent)
            if item["parent_label"] and not item["parent_ids"]:
                item["error"] = UNLINKED_PARENT
        except (browser_error, ValueError) as exc:
            item["error"] = str(exc).splitlines()[0]
    resolve_text_parents(departments)
    for item in departments.values():
        if item["error"]:
            print(f"{item['url']}: {item['error']}", file=sys.stderr)
    return departments


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/miit_departments.json"))
    parser.add_argument("--browser", choices=("chromium", "msedge", "chrome"), default="chromium")
    parser.add_argument("--delay", type=float, default=0.35, help="Пауза между карточками, секунды")
    args = parser.parse_args()
    if not 0 <= args.delay < float("inf"):
        parser.error("--delay должен быть конечным неотрицательным числом")

    try:
        from playwright.sync_api import Error, sync_playwright
    except ImportError:
        parser.exit(1, "Установите Playwright: python -m pip install playwright\n")

    try:
        with sync_playwright() as playwright:
            channel = None if args.browser == "chromium" else args.browser
            browser = playwright.chromium.launch(channel=channel)
            try:
                page = browser.new_page()
                page.set_default_timeout(15000)
                departments = collect(page, args.delay, Error)
            finally:
                browser.close()
    except (Error, ValueError) as exc:
        parser.exit(1, f"Не удалось собрать каталог: {exc}\n")

    failed = sum(item["error"] is not None for item in departments.values())
    output = args.output
    if failed:
        output = output.with_stem(f"{output.stem}.partial")
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": CATALOG_URL,
        "departments": sorted(departments.values(), key=lambda item: item["id"]),
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Карточек: {len(departments)}, ошибок: {failed}. Файл: {output}")
    return int(bool(failed))


if __name__ == "__main__":
    sys.exit(main())
