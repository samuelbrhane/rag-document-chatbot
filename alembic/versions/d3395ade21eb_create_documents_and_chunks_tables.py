"""create documents and chunks tables

Revision ID: d3395ade21eb
Revises: 
Create Date: 2026-11-15 10:28:04.120726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3395ade21eb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    op.execute("""
        CREATE TABLE documents (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL UNIQUE,
            uploaded_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
    """)

    op.execute("""
        CREATE TABLE chunks (
            id BIGSERIAL PRIMARY KEY,
            document_id INT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
            chunk_index INT NOT NULL,
            page INT,
            content TEXT NOT NULL,
            embedding VECTOR(1536) NOT NULL
        );
    """)

    op.execute("""
        CREATE INDEX chunks_embedding_idx
            ON chunks USING hnsw (embedding vector_cosine_ops);
    """)


def downgrade() -> None:
    op.execute("DROP TABLE chunks;")
    op.execute("DROP TABLE documents;")
