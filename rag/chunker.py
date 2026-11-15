from dataclasses import dataclass

from rag.config import CHUNK_OVERLAP, CHUNK_SIZE
from rag.loader import Page


@dataclass
class Chunk:
    content: str
    page: int | None
    index: int  # position of the chunk within its document


def chunk_pages(
    pages: list[Page],
    size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[Chunk]:
    """Split each page into overlapping chunks, keeping the page number."""
    chunks = []
    for page in pages:
        for piece in _split_text(page.text, size, overlap):
            chunks.append(Chunk(content=piece, page=page.page, index=len(chunks)))
    return chunks


def _split_text(text: str, size: int, overlap: int) -> list[str]:
    text = " ".join(text.split())  # collapse newlines and repeated spaces
    pieces = []
    start = 0

    while start < len(text):
        end = min(start + size, len(text))

        # end on a word boundary so words are not cut in half
        if end < len(text):
            space = text.rfind(" ", start, end)
            if space > start:
                end = space

        pieces.append(text[start:end].strip())
        if end >= len(text):
            break

        # step back by the overlap, always moving forward at least one character
        next_start = max(end - overlap, start + 1)

        # begin the next chunk at the start of a word
        space = text.find(" ", next_start, end)
        start = space + 1 if space != -1 else next_start

    return [p for p in pieces if p]