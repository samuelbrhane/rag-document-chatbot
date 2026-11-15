from openai import OpenAI

from rag.config import CHAT_MODEL

_client = OpenAI()

HISTORY_MESSAGES = 6  # how many recent messages the rewriter looks at

REWRITE_PROMPT = """You rewrite follow-up questions so they can be understood on their own.

Given a conversation and the user's latest question, return the latest question rewritten
as a complete, standalone question. Replace words like "it", "that" or "those" with what
they refer to in the conversation.

If the latest question is already standalone, return it unchanged.
Return only the question, with no explanation."""


def rewrite_question(question: str, history: list[tuple[str, str]]) -> str:
    """Turn a follow-up into a standalone question using recent chat history."""
    if not history:
        return question

    recent = history[-HISTORY_MESSAGES:]
    conversation = "\n".join(f"{role}: {content}" for role, content in recent)

    response = _client.responses.create(
        model=CHAT_MODEL,
        instructions=REWRITE_PROMPT,
        input=f"Conversation:\n{conversation}\n\nLatest question: {question}",
    )
    return response.output_text.strip() or question