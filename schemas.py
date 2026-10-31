from datetime import datetime

from pydantic import BaseModel, HttpUrl


# url request
class ShortenUrlRequest(BaseModel):
    url: HttpUrl  # any http or https valid url


# response to url request
class ShortenUrlResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str
    click_count: int
    created_at: datetime
