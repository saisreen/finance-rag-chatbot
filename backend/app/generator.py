import os

from dotenv import load_dotenv
from openai import OpenAI

from app.retriever import retrieve_relevant_chunks

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a helpful consumer banking assistant.

Answer ONLY using the provided context.

If the answer is not available in the context,
say:

"I couldn't find that information in the CFPB knowledge base."

Keep answers concise and easy to understand.
"""


def generate_answer(question: str):

    chunks = retrieve_relevant_chunks(
        question=question,
        top_k=3,
    )

    # No relevant CFPB content found
    if not chunks:
        return (
            "Sorry, I can only answer consumer finance questions using the CFPB knowledge base.",
            [],
            True,
        )

    context = ""

    for chunk in chunks:
        context += f"\n\nSource: {chunk['title']}\n"
        context += chunk["text"]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""
Context:

{context}

Question:

{question}
"""
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    return answer, chunks, False


if __name__ == "__main__":

    # Change this question to test different scenarios
    question = "What is APR?"

    answer, sources, refused = generate_answer(question)

    print("\nQuestion")
    print(question)

    print("\nAnswer")
    print(answer)

    print(f"\nRefused: {refused}")

    print("\nSources")

    if not sources:
        print("No sources")
    else:
        for source in sources:
            print(f"- {source['title']}")
            print(f"  {source['url']}")