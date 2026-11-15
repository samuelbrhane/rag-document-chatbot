from dataclasses import dataclass

from pgvector import Vector

from rag.config import TOP_K
from rag.embedder import embed_query
from rag.store import get_connection


@dataclass
class RetrievedChunk:
    filename: str
    page: int | None
    chunk_index: int
    content: str
    similarity: float  # 1.0 means identical meaning, near 0 means unrelated


def search(question: str, top_k: int = TOP_K) -> list[RetrievedChunk]:
    """Find the chunks whose meaning is closest to the question."""
    query_vector = Vector(embed_query(question))

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT d.filename, c.page, c.chunk_index, c.content,
                   1 - (c.embedding <=> %s) AS similarity
            FROM chunks c
            JOIN documents d ON d.id = c.document_id
            ORDER BY c.embedding <=> %s
            LIMIT %s
            """,
            (query_vector, query_vector, top_k),
        ).fetchall()

    return [RetrievedChunk(*row) for row in rows]