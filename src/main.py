import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PEP_URL
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, "whatsnew/")
    response = get_response(session, whats_new_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features="lxml")
    main_div = find_tag(soup, "section", attrs={"id": "what-s-new-in-python"})
    div_with_ul = find_tag(main_div, "div", attrs={"class": "toctree-wrapper"})
    sections_by_python = div_with_ul.find_all(
        'li',
        attrs={'class': 'toctree-l1'}
    )
    results = [("Ссылка на статью", "Заголовок", "Редактор, Автор")]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find("a")
        href = version_a_tag["href"]
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features="lxml")
        h1 = find_tag(soup, "h1")
        dl = find_tag(soup, "dl")
        dl_text = dl.text.replace("\n", " ")
        results.append((version_link, h1.text, dl_text))
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, "lxml")
    sidebar = find_tag(soup, "div", {"class": "sphinxsidebarwrapper"})
    ul_tags = sidebar.find_all("ul")
    for ul in ul_tags:
        if "All versions" in ul.text:
            a_tags = ul.find_all("a")
            break
    else:
        raise Exception("Не найден список c версиями Python")
    results = [("Ссылка на документацию", "Версия", "Статус")]
    pattern = r"Python (?P<version>\d\.\d+) \((?P<status>.*)\)"
    for a_tag in a_tags:
        link = a_tag["href"]
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ""
        results.append((link, version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, "download.html")
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features="lxml")
    main_tag = find_tag(soup, "div", {"role": "main"})
    table_tag = find_tag(main_tag, "table", {"class": "docutils"})
    pdf_a4_tag = find_tag(
        table_tag,
        'a',
        {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag["href"]
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split("/")[-1]
    downloads_dir = BASE_DIR / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, "wb") as file:
        file.write(response.content)
    logging.info(f"Архив был загружен и сохранён: {archive_path}")


def pep(session):
    response = get_response(session, PEP_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features="lxml")
    section_all_pep = find_tag(
        soup, 
        "section", 
        attrs={"id": "numerical-index"}
    )
    all_rows_tr = section_all_pep.find_all("tr")
    results = [("Статус", "Количество")]
    all_status = defaultdict(int)
    total = 0
    for tr in tqdm(all_rows_tr):
        version_td_tag = tr.find("td")
        type_and_status = version_td_tag.text[1:]
        version_td_tag_next = version_td_tag.find_next_sibling("td")
        version_a_tag = find_tag(version_td_tag_next, "a")
        version_link = urljoin(PEP_URL, version_a_tag["href"])
        response = session.get(version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features="lxml")
        version_dl_tag = find_tag(soup, "dl")
        version_dt_tag = version_dl_tag.find_all("dt")
        for dt in version_dt_tag:
            if dt.text == "Status:":
                status = dt.find_next_sibling("dd").text
        expected_status = EXPECTED_STATUS[type_and_status]
        if status not in expected_status:
            logging.info(
                f"""
                f'Несовпадающие статусы:: {version_link}
                f'Статус в карточке: {status}
                f'Ожидаемые статусы: {expected_status}"""
            )
        all_status[status] += 1
        total += 1
    results.extend(all_status.items())
    results.append(("Total", total))
    return results


MODE_TO_FUNCTION = {
    "whats-new": whats_new,
    "latest-versions": latest_versions,
    "download": download,
    "pep": pep,
}


def main():
    configure_logging()
    logging.info("Парсер запущен!")
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f"Аргументы командной строки: {args}")
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
