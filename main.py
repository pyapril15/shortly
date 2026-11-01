import os

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import services
from database import get_db
from schemas import ShortenUrlResponse, ShortenUrlRequest

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

app = FastAPI(title="Shortly API", version="1.0.0")


def to_response(url: ShortenUrlResponse) -> ShortenUrlResponse:
    return ShortenUrlResponse(
        short_code=url.short_code,
        short_url=f"{BASE_URL}/{url.short_code}",
        original_url=url.original_url,
        click_count=url.click_count,
        created_at=url.created_at,
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/shorten", response_model=ShortenUrlResponse, status_code=201)
def shorten_url(body: ShortenUrlRequest, db: Session = Depends(get_db)):
    return to_response(services.create_short_url(db, str(body.url)))
