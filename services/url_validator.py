from urllib.parse import urlparse


VALID_DOMAINS = {
    "youtube.com",
    "www.youtube.com",
    "youtu.be",
    "www.youtu.be",
    "m.youtube.com"
}


def is_valid_youtube_url(url: str) -> bool:

    try:

        parsed = urlparse(url)

        return parsed.netloc.lower() in VALID_DOMAINS

    except Exception:

        return False