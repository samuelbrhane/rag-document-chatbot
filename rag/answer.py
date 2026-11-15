import re
from collections.abc import Iterator
from dataclasses import dataclass

from openai import OpenAI

from rag.config import CHAT_MODEL, MIN_SIMILARITY
from rag.prompt import NOT_FOUND, SYSTEM_PROMPT, build_user_prompt
from rag.retriever import search
from rag.rewriter import rewrite_question

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
    searched_for: str  # the standalone question used for retrieval
    reason: str | None = None  # why it refused, for logging and the UI


class AnswerStream:
    """Loop over this to receive the answer text piece by piece.

    When the loop ends, .answer holds the final Answer with sources or a refusal.
    If .answer is already set right after creation, the question was refused
    before calling the model, and there is nothing to stream.
    """

    def __init__(self, question: str, history: list[tuple[str, str]] | None = None):
        self.searched_for = rewrite_question(question, history or [])
        results = search(self.searched_for)
        self._relevant = [r for r in results if r.similarity >= MIN_SIMILARITY]
        self.answer: Answer | None = None

        # Layer 1: nothing close enough, refuse without calling the model
        if not self._relevant:
            self.answer = _refuse("low_similarity", self.searched_for)

    def __iter__(self) -> Iterator[str]:
        if self.answer is not None:
            return

        events = _client.responses.create(
            model=CHAT_MODEL,
            instructions=SYSTEM_PROMPT,
            input=build_user_prompt(self.searched_for, self._relevant),
            stream=True,
        )

        text = ""
        decided = False  # have we seen enough to know it is not NOT_FOUND?
        silent = False  # True when the model is writing NOT_FOUND

        for event in events:
            if event.type != "response.output_text.delta":
                continue
            text += event.delta

            if not decided:
                start = text.lstrip()
                if NOT_FOUND.startswith(start):
                    continue  # could still turn into NOT_FOUND, keep waiting
                decided = True
                silent = start.startswith(NOT_FOUND)
                if not silent:
                    yield text
                continue

            if not silent:
                yield event.delta

        self.answer = self._finish(text.strip())

    def _finish(self, text: str) -> Answer:
        # Layer 2: the model says the sources do not answer the question
        if NOT_FOUND in text:
            return _refuse("not_in_sources", self.searched_for)

        # Layer 3: an answer without any valid citation is not trusted
        cited = {int(n) for n in re.findall(r"\[(\d+)\]", text)}
        sources = [
            Source(number, r.filename, r.page, r.similarity, r.content)
            for number, r in enumerate(self._relevant, start=1)
            if number in cited
        ]
        if not sources:
            return _refuse("no_citation", self.searched_for)

        return Answer(text=text, sources=sources, refused=False, searched_for=self.searched_for)


def answer_question(question: str, history: list[tuple[str, str]] | None = None) -> Answer:
    """Answer without streaming. Used by tests and evaluation."""
    stream = AnswerStream(question, history)
    for _ in stream:
        pass
    return stream.answer


def _refuse(reason: str, searched_for: str) -> Answer:
    return Answer(
        text=REFUSAL_TEXT,
        sources=[],
        refused=True,
        searched_for=searched_for,
        reason=reason,
    )