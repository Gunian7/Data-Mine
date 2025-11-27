import re
from typing import List

def clean_text(text: str) -> str:
    """Basic cleaning: remove extra whitespace and undesired characters."""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def chunk_iterable(seq, size: int):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]
