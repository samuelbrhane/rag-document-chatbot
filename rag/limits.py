from rag.chats import count_questions_today
from rag.config import DAILY_QUESTIONS_PER_VISITOR, DAILY_QUESTIONS_TOTAL, DEMO_MODE


def limit_message(visitor_id: str) -> str | None:
    """Return a message if a daily limit is reached in demo mode, otherwise None."""
    if not DEMO_MODE:
        return None

    if count_questions_today(visitor_id) >= DAILY_QUESTIONS_PER_VISITOR:
        return (
            f"You have reached the limit of {DAILY_QUESTIONS_PER_VISITOR} questions per day "
            "for this demo. Try again tomorrow."
        )

    if count_questions_today() >= DAILY_QUESTIONS_TOTAL:
        return "The demo has reached its daily question limit. Try again tomorrow."

    return None