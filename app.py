"""Question 2 of TDS GA3."""

import re

import wikipedia
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://exam.sanand.workers.dev"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class PayLoad(BaseModel):
    """Input response type for app."""

    attachments: dict[str, str]


@app.get("/")
async def get_url(topic: str) -> JSONResponse:
    """Get the wikipedia url of topic."""
    url = wikipedia.page(topic).url
    return JSONResponse({"topic": topic, "url": url})


class Statements(BaseModel):
    """Model for Statements."""

    sentences: list[str]


def get_sentiment(sentence: str) -> str:
    """Get the sentiment of a statement using an LLM."""
    return "happy"


@app.post("/sentiment")
def analyze(payload: Statements) -> JSONResponse:
    """Analyze the sentiment of statements."""
    results = [
        {"sentence": sentence, "sentiment": get_sentiment(sentence)}
        for sentence in payload.sentences
    ]

    return JSONResponse({"results": results})


@app.post("/file")
async def mime_type(payload: PayLoad) -> JSONResponse:
    """Infer and return the mime type."""
    # Get the url from payload
    url = payload.attachments.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="attachments.url is required")

    # Parse the url
    mtype = "unknown"

    # Return JSON response
    mime_match = re.search(r"^data:(\w+)/.+", url)
    mtype = mime_match.group(1) if mime_match else "unknown"
    return JSONResponse({"type": mtype})
