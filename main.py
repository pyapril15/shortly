import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import services
from database import Base, engine, get_db
from schemas import ShortenUrlResponse, ShortenUrlRequest

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shortly API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/api/v1/stats/{code}", response_model=ShortenUrlResponse, status_code=200)
def stats(code: str, db: Session = Depends(get_db)):
    url = services.get_by_code(db, code)
    if not url:
        raise HTTPException(status_code=404, detail="Short link not found")
    return to_response(url)


@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    url = services.get_by_code(db, code)

    if not url:
        raise HTTPException(status_code=404, detail="Short link not found")

    services.register_click(db, url)
    return RedirectResponse(url=url.original_url, status_code=307)
