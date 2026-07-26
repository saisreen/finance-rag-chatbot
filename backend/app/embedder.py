import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

INPUT_FILE = Path("data/chunks/chunks.json")
OUTPUT_FILE = Path("data/embeddings/embedded_chunks.json")

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_embeddings():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embedded_chunks = []

    print(f"Generating embeddings for {len(chunks)} chunks...")

    for chunk in chunks:

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk["text"]
        )

        embedded_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "url": chunk["url"],
            "title": chunk["title"],
            "text": chunk["text"],
            "embedding": response.data[0].embedding
        })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(embedded_chunks, f)

    print("Embeddings generated successfully!")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    create_embeddings()