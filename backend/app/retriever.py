import os

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


DB_PATH = "data/chroma"
COLLECTION_NAME = "finance_faq"
EMBEDDING_MODEL = "text-embedding-3-small"

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY is missing. Add it to backend/.env."
    )

openai_client = OpenAI(api_key=api_key)

chroma_client = chromadb.PersistentClient(path=DB_PATH)

collection = chroma_client.get_collection(
    name=COLLECTION_NAME
)


def create_query_embedding(question: str) -> list[float]:
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=question,
    )

    return response.data[0].embedding


def retrieve_relevant_chunks(
    question: str,
    top_k: int = 3,
) -> list[dict]:

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    question_embedding = create_query_embedding(
        question.strip()
    )

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    retrieved_chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # Reject unrelated questions
    RELEVANCE_THRESHOLD = 1.2

    if not distances or distances[0] > RELEVANCE_THRESHOLD:
        return []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        retrieved_chunks.append(
            {
                "text": document,
                "title": metadata.get("title", ""),
                "url": metadata.get("url", ""),
                "distance": distance,
            }
        )

    return retrieved_chunks


def print_results(results: list[dict]) -> None:

    if not results:
        print("\nNo relevant CFPB information found.")
        return

    for index, result in enumerate(results, start=1):
        print("\n" + "=" * 70)
        print(f"Result {index}")
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Distance: {result['distance']}")
        print(f"Text: {result['text'][:500]}...")


if __name__ == "__main__":

    test_question = "How do I cook pasta?"

    print(f"Question: {test_question}")

    matches = retrieve_relevant_chunks(
        question=test_question,
        top_k=3,
    )

    print_results(matches)