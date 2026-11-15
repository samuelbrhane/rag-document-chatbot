import re
from dataclasses import dataclass

from openai import OpenAI

from rag.config import CHAT_MODEL, MIN_SIMILARITY
from rag.prompt import NOT_FOUND, SYSTEM_PROMPT, build_user_prompt
from rag.retriever import search

_client = OpenAI()

REFUSAL_TEXT = "I don't know. The answer is not in the uploaded documents."


@dataclass
class Source:
    number: int
    filename: str
    page: int | None
    similarity: float
    content: str


@dataclass
class Answer:
    text: str
    sources: list[Source]
    refused: bool
    reason: str | None = None  # why it refused, for logging and the UI


def answer_question(question: str) -> Answer:
    """Retrieve relevant chunks and answer only from them, or refuse."""
    results = search(question)
    relevant = [r for r in results if r.similarity >= MIN_SIMILARITY]

    # Layer 1: nothing close enough, refuse without calling the model
    if not relevant:
        return _refuse("low_similarity")

    response = _client.responses.create(
        model=CHAT_MODEL,
        instructions=SYSTEM_PROMPT,
        input=build_user_prompt(question, relevant),
    )
    text = response.output_text.strip()

    # Layer 2: the model says the sources do not answer the question
    if NOT_FOUND in text:
        return _refuse("not_in_sources")

    # Layer 3: an answer without any valid citation is not trusted
    cited = {int(n) for n in re.findall(r"\[(\d+)\]", text)}
    sources = [
        Source(number, r.filename, r.page, r.similarity, r.content)
        for number, r in enumerate(relevant, start=1)
        if number in cited
    ]
    if not sources:
        return _refuse("no_citation")

    return Answer(text=text, sources=sources, refused=False)


def _refuse(reason: str) -> Answer:
    return Answer(text=REFUSAL_TEXT, sources=[], refused=True, reason=reason)