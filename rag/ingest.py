from dataclasses import dataclass

from rag.chunker import chunk_pages
from rag.embedder import embed_texts
from rag.loader import load_file
from rag.store import save_document


@dataclass
class IngestResult:
    filename: str
    pages: int
    chunks: int


def ingest_file(filename: str, data: bytes) -> IngestResult:
    """Load, chunk, embed and save one file."""
    pages = load_file(filename, data)
    if not pages:
        raise ValueError(f"No text found in {filename}. It may be a scanned PDF.")

    chunks = chunk_pages(pages)
    vectors = embed_texts([chunk.content for chunk in chunks])
    save_document(filename, chunks, vectors)

    return IngestResult(filename=filename, pages=len(pages), chunks=len(chunks))