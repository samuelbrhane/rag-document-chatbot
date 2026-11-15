from openai import OpenAI

from rag.config import EMBEDDING_MODEL

_client = OpenAI()

BATCH_SIZE = 100


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Turn a list of texts into embedding vectors, in the same order."""
    vectors = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        response = _client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        vectors.extend(item.embedding for item in response.data)
    return vectors


def embed_query(text: str) -> list[float]:
    """Turn a single question into an embedding vector."""
    return embed_texts([text])[0]