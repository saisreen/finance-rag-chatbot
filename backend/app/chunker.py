import json
from pathlib import Path

INPUT_FILE = Path("data/processed/processed_pages.json")
OUTPUT_FILE = Path("data/chunks/chunks.json")

CHUNK_SIZE = 300


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE):
    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def create_chunks():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        pages = json.load(file)

    all_chunks = []

    chunk_id = 1

    for page in pages:

        chunks = split_into_chunks(page["text"])

        for chunk in chunks:
            all_chunks.append({
                "chunk_id": chunk_id,
                "url": page["url"],
                "title": page["title"],
                "text": chunk
            })

            chunk_id += 1

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(all_chunks, file, indent=2, ensure_ascii=False)

    print(f"Created {len(all_chunks)} chunks.")


if __name__ == "__main__":
    create_chunks()