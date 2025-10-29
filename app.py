"""Question 2 of TDS GA3."""

import asyncio
import os
import re

import openai
import wikipedia
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

load_dotenv()

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
async def home() -> JSONResponse:
    """Home page."""
    return JSONResponse({"api_key": os.getenv("OPENAI_API_KEY")})


class Statements(BaseModel):
    """Model for Statements."""

    sentences: list[str]


@app.get("/sentiment")
def get_page() -> str:
    """Placeholder function."""
    return "Sentiment Analysis"


async def get_sentiment(sentence: str) -> str:
    """Get the sentiment of a statement using an LLM."""
    async with openai.AsyncClient(
        api_key=os.getenv("OPENAI_API_KEY"), base_url="https://aipipe.org/openai/v1"
    ) as client:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a sentiment analysis assistant. "
                        "Respond with only one word: 'happy', 'sad', or 'neutral'."
                    ),
                },
                {"role": "user", "content": sentence},
            ],
            temperature=0.0,
        )

    sentiment = response.choices[0].message.content.strip().lower()
    return sentiment


@app.post("/sentiment")
async def analyze(payload: Statements) -> JSONResponse:
    """Analyze the sentiment of statements."""
    # Get sentiments
    sentiments = await asyncio.gather(
        *[
            asyncio.create_task(get_sentiment(sentence))
            for sentence in payload.sentences
        ]
    )

    print(sentiments)

    results = [
        {"sentence": sentence, "sentiment": sentiment}
        for (sentence, sentiment) in zip(payload.sentences, sentiments, strict=True)
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
