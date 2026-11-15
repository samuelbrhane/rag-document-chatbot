from dataclasses import asdict, dataclass, field

from psycopg.types.json import Jsonb

from rag.answer import Source
from rag.store import get_connection

TITLE_LENGTH = 40


@dataclass
class ChatSummary:
    id: int
    title: str


@dataclass
class Message:
    role: str
    content: str
    rewritten_question: str | None = None
    sources: list[Source] = field(default_factory=list)
    refused: bool = False
    refusal_reason: str | None = None


def make_title(question: str) -> str:
    """Use the first question, shortened, as the chat title."""
    title = " ".join(question.split())
    return title if len(title) <= TITLE_LENGTH else title[: TITLE_LENGTH - 1].rstrip() + "…"


def create_chat(visitor_id: str, title: str) -> int:
    with get_connection() as conn:
        return conn.execute(
            "INSERT INTO chats (visitor_id, title) VALUES (%s, %s) RETURNING id",
            (visitor_id, title),
        ).fetchone()[0]


def list_chats(visitor_id: str) -> list[ChatSummary]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title FROM chats WHERE visitor_id = %s ORDER BY updated_at DESC",
            (visitor_id,),
        ).fetchall()
    return [ChatSummary(*row) for row in rows]


def rename_chat(chat_id: int, visitor_id: str, title: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE chats SET title = %s WHERE id = %s AND visitor_id = %s",
            (title, chat_id, visitor_id),
        )


def delete_chat(chat_id: int, visitor_id: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM chats WHERE id = %s AND visitor_id = %s",
            (chat_id, visitor_id),
        )


def add_message(chat_id: int, message: Message) -> None:
    """Save a message and move its chat to the top of the list."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO messages
                (chat_id, role, content, rewritten_question, sources, refused, refusal_reason)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                chat_id,
                message.role,
                message.content,
                message.rewritten_question,
                Jsonb([asdict(source) for source in message.sources]),
                message.refused,
                message.refusal_reason,
            ),
        )
        conn.execute("UPDATE chats SET updated_at = now() WHERE id = %s", (chat_id,))


def get_messages(chat_id: int, visitor_id: str) -> list[Message]:
    """Load a chat's messages in order, only if the chat belongs to this visitor."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT m.role, m.content, m.rewritten_question, m.sources, m.refused, m.refusal_reason
            FROM messages m
            JOIN chats c ON c.id = m.chat_id
            WHERE m.chat_id = %s AND c.visitor_id = %s
            ORDER BY m.id
            """,
            (chat_id, visitor_id),
        ).fetchall()

    return [
        Message(
            role=role,
            content=content,
            rewritten_question=rewritten,
            sources=[Source(**source) for source in sources],
            refused=refused,
            refusal_reason=reason,
        )
        for role, content, rewritten, sources, refused, reason in rows
    ]