import json
from pathlib import Path

import chromadb

INPUT_FILE = Path("data/embeddings/embedded_chunks.json")
DB_PATH = "data/chroma"

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(
    name="finance_faq"
)


def load_embeddings():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def store_embeddings():

    data = load_embeddings()

    print(f"Loading {len(data)} embeddings into ChromaDB...")

    for chunk in data:

        collection.add(
            ids=[str(chunk["chunk_id"])],
            embeddings=[chunk["embedding"]],
            documents=[chunk["text"]],
            metadatas=[{
                "url": chunk["url"],
                "title": chunk["title"]
            }]
        )

    print("Embeddings stored successfully!")


if __name__ == "__main__":
    store_embeddings()