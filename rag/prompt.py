from rag.retriever import RetrievedChunk

NOT_FOUND = "NOT_FOUND"

SYSTEM_PROMPT = f"""You answer questions using only the numbered sources provided.

Rules:
- Use only facts stated in the sources. Do not use outside knowledge.
- After each fact, cite its source number in square brackets, for example [1] or [2].
- If the sources do not contain the answer, reply with exactly {NOT_FOUND} and nothing else.
- If the sources answer only part of the question, answer that part and say what is missing.
- Keep answers short and direct."""


def build_user_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
    """Format the retrieved chunks as numbered sources, followed by the question."""
    sources = []
    for number, chunk in enumerate(chunks, start=1):
        location = chunk.filename if chunk.page is None else f"{chunk.filename}, page {chunk.page}"
        sources.append(f"[{number}] ({location})\n{chunk.content}")

    return "Sources:\n\n" + "\n\n".join(sources) + f"\n\nQuestion: {question}"