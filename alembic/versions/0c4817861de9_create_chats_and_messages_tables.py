"""create chats and messages tables

Revision ID: 0c4817861de9
Revises: d3395ade21eb
Create Date: 2026-11-15 13:40:24.408396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c4817861de9'
down_revision: Union[str, Sequence[str], None] = 'd3395ade21eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE chats (
            id SERIAL PRIMARY KEY,
            visitor_id TEXT NOT NULL,
            title TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
    """)

    op.execute("""
        CREATE INDEX chats_visitor_idx
            ON chats (visitor_id, updated_at DESC);
    """)

    op.execute("""
        CREATE TABLE messages (
            id BIGSERIAL PRIMARY KEY,
            chat_id INT NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
            role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
            content TEXT NOT NULL,
            rewritten_question TEXT,
            sources JSONB NOT NULL DEFAULT '[]',
            refused BOOLEAN NOT NULL DEFAULT false,
            refusal_reason TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
    """)

    op.execute("""
        CREATE INDEX messages_chat_idx
            ON messages (chat_id, id);
    """)


def downgrade() -> None:
    op.execute("DROP TABLE messages;")
    op.execute("DROP TABLE chats;")
