import html
import re

_CITATION = re.compile(r"\[(\d+)\]")


def format_citations(text: str) -> str:
    """Turn [1] style citations into styled tags. Escapes the text first so it is safe as HTML."""
    safe = html.escape(text, quote=False)
    return _CITATION.sub(r'<span class="gd-cite">\1</span>', safe)