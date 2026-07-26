import json
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.consumerfinance.gov/"
OUTPUT_FILE = Path("data/raw/cfpb_pages.json")

MAX_PAGES = 10

ALLOWED_PATH_KEYWORDS = (
    "/ask-cfpb/",
    "/consumer-tools/",
)


def is_valid_cfpb_url(url: str) -> bool:
    parsed_url = urlparse(url)

    if parsed_url.netloc != "www.consumerfinance.gov":
        return False

    return any(
        keyword in parsed_url.path
        for keyword in ALLOWED_PATH_KEYWORDS
    )


def extract_page(url: str) -> dict | None:
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": (
                    "Finance-RAG-Student-Project/1.0 "
                    "(educational use)"
                )
            },
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.get_text(strip=True) if soup.title else "Untitled"

        main_content = soup.find("main")

        if main_content is None:
            main_content = soup.body

        if main_content is None:
            return None

        text = main_content.get_text(
            separator=" ",
            strip=True,
        )

        text = " ".join(text.split())

        if len(text) < 100:
            return None

        links = []

        for anchor in soup.find_all("a", href=True):
            absolute_url = urljoin(url, anchor["href"])
            absolute_url = absolute_url.split("#")[0]

            if is_valid_cfpb_url(absolute_url):
                links.append(absolute_url)

        return {
            "url": url,
            "title": title,
            "text": text,
            "links": list(set(links)),
        }

    except requests.RequestException as error:
        print(f"Failed to fetch {url}: {error}")
        return None


def crawl_cfpb() -> list[dict]:
    start_urls = [
        "https://www.consumerfinance.gov/ask-cfpb/",
        "https://www.consumerfinance.gov/consumer-tools/",
    ]

    queue = start_urls.copy()
    visited = set()
    pages = []

    while queue and len(pages) < MAX_PAGES:
        current_url = queue.pop(0)

        if current_url in visited:
            continue

        visited.add(current_url)

        print(f"Crawling: {current_url}")

        page = extract_page(current_url)

        if page is None:
            continue

        pages.append(
            {
                "url": page["url"],
                "title": page["title"],
                "text": page["text"],
            }
        )

        for link in page["links"]:
            if link not in visited and link not in queue:
                queue.append(link)

    return pages


def save_pages(pages: list[dict]) -> None:
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            pages,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Saved {len(pages)} pages to {OUTPUT_FILE}")


if __name__ == "__main__":
    crawled_pages = crawl_cfpb()
    save_pages(crawled_pages)