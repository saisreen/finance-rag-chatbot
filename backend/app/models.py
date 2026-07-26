from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    title: str
    url: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    refused: bool