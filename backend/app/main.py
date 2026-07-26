from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import ChatRequest, ChatResponse, Source
from app.generator import generate_answer

app = FastAPI(
    title="Finance RAG Chatbot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Finance RAG Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "UP"
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    answer, chunks, refused = generate_answer(request.question)

    sources = []
    seen_urls = set()

    for chunk in chunks:

        url = chunk["url"]

        if url and url not in seen_urls:

            seen_urls.add(url)

            sources.append(
                Source(
                    title=chunk["title"],
                    url=url
                )
            )

    return ChatResponse(
        answer=answer,
        sources=sources,
        refused=refused
    )