import re
import time
from collections.abc import Iterable, Iterator

WORD_DELAY = 0.03  # seconds between words


def smooth_stream(chunks: Iterable[str], delay: float = WORD_DELAY) -> Iterator[str]:
    """Release streamed text one word at a time at a steady pace."""
    buffer = ""
    for chunk in chunks:
        buffer += chunk
        *complete, buffer = re.split(r"(\s+)", buffer)  # keep the last, possibly unfinished, word
        for piece in complete:
            yield piece
            if not piece.isspace():
                time.sleep(delay)
    if buffer:
        yield buffer