import os

from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.environ["DATABASE_URL"]

# Models
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-5.4-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIM = 1536

# Chunking (in characters)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# Retrieval
TOP_K = 5
MIN_SIMILARITY = 0.25

# Files
SUPPORTED_EXTENSIONS = (".pdf", ".txt", ".md")