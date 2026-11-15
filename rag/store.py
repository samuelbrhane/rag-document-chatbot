import psycopg
from pgvector import Vector
from pgvector.psycopg import register_vector

from rag.chunker import Chunk
from rag.config import DATABASE_URL


def get_connection() -> psycopg.Connection:
    conn = psycopg.connect(DATABASE_URL)
    register_vector(conn)
    return conn


def save_document(filename: str, chunks: list[Chunk], vectors: list[list[float]]) -> int:
    """Save a document and its chunks. Replaces any earlier version with the same filename."""
    rows = []
    for chunk, vector in zip(chunks, vectors, strict=True):
        content = chunk.content.replace("\x00", "")
        rows.append((chunk.index, chunk.page, content, Vector(vector)))

    with get_connection() as conn:
        conn.execute("DELETE FROM documents WHERE filename = %s", (filename,))
        document_id = conn.execute(
            "INSERT INTO documents (filename) VALUES (%s) RETURNING id",
            (filename,),
        ).fetchone()[0]

        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO chunks (document_id, chunk_index, page, content, embedding)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [(document_id, *row) for row in rows],
            )

    return document_id


def delete_document(filename: str) -> None:
    """Delete a document and, through the cascade, all its chunks."""
    with get_connection() as conn:
        conn.execute("DELETE FROM documents WHERE filename = %s", (filename,))


def list_documents() -> list[tuple[str, int]]:
    """Return each stored document's filename and number of chunks, newest first."""
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT d.filename, COUNT(c.id)
            FROM documents d
            LEFT JOIN chunks c ON c.document_id = d.id
            GROUP BY d.id
            ORDER BY d.uploaded_at DESC
            """
        ).fetchall()