import io
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from rag.config import SUPPORTED_EXTENSIONS


@dataclass
class Page:
    text: str
    page: int | None  # page number for PDFs, None for text files


def load_file(filename: str, data: bytes) -> list[Page]:
    """Read a file's bytes and return its text as a list of pages."""
    ext = Path(filename).suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")

    if ext == ".pdf":
        return _load_pdf(data)

    text = data.decode("utf-8", errors="replace")
    return [Page(text=text, page=None)]


def _load_pdf(data: bytes) -> list[Page]:
    reader = PdfReader(io.BytesIO(data))
    pages = []
    for number, pdf_page in enumerate(reader.pages, start=1):
        text = pdf_page.extract_text() or ""
        if text.strip():
            pages.append(Page(text=text, page=number))
    return pages