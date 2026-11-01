import string

from sqlalchemy.orm import Session

from models import Url

ALPHABET = string.digits + string.ascii_letters
OFFSET = 1_000_000


def encode_base62(number: int) -> str:
    if number == 0:
        return ALPHABET[0]

    chars = []
    while number:
        number, remainder = divmod(number, len(ALPHABET))
        chars.append(ALPHABET[remainder])

    return ''.join(reversed(chars))


def create_short_url(db: Session, original_url: str) -> Url:
    url = Url(original_url=original_url)
    db.add(url)
    db.flush()

    url.short_code = encode_base62(url.id + OFFSET)
    db.commit()
    db.refresh(url)

    return url
