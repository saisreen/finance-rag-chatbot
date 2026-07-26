import json
import re
from pathlib import Path

INPUT_FILE = Path("data/raw/cfpb_pages.json")
OUTPUT_FILE = Path("data/processed/processed_pages.json")


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    remove_phrases = [
        "About us",
        "Legal disclaimer",
        "Page last modified",
    ]

    for phrase in remove_phrases:
        if phrase in text:
            text = text.split(phrase)[0]

    return text.strip()


def process_pages():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        pages = json.load(file)

    processed = []

    for page in pages:
        processed.append({
            "url": page["url"],
            "title": page["title"],
            "text": clean_text(page["text"])
        })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(processed, file, indent=2, ensure_ascii=False)

    print(f"Processed {len(processed)} pages.")


if __name__ == "__main__":
    process_pages()