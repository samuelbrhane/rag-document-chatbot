import json
import sys
from pathlib import Path

from rag import Answer, answer_question, search
from rag.config import CHUNK_OVERLAP, CHUNK_SIZE, MIN_SIMILARITY

QUESTIONS_FILE = Path(__file__).parent / "questions.json"


def check(item: dict, answer: Answer) -> str | None:
    """Return why the answer failed, or None if it passed."""
    if item["expect"] == "refuse":
        return None if answer.refused else "answered instead of refusing"

    if answer.refused:
        return f"refused ({answer.reason})"

    text = answer.text.lower()
    missing = [word for word in item["must_contain"] if word.lower() not in text]
    if missing:
        return f"missing {missing}"

    cited_files = {source.filename for source in answer.sources}
    if not cited_files & set(item["sources"]):
        return f"wrong source {sorted(cited_files)}"

    if "page" in item:
        cited_pages = {s.page for s in answer.sources if s.filename in item["sources"]}
        if item["page"] not in cited_pages:
            return f"wrong page {sorted(p for p in cited_pages if p)}"

    return None


def main() -> None:
    items = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
    print(f"Chunk size {CHUNK_SIZE}, overlap {CHUNK_OVERLAP}, threshold {MIN_SIMILARITY}\n")

    results = []
    for item in items:
        top = search(item["question"], top_k=1)
        top_score = top[0].similarity if top else 0.0
        answer = answer_question(item["question"])
        failure = check(item, answer)

        results.append({"item": item, "top_score": top_score, "failure": failure})
        status = "PASS" if failure is None else "FAIL"
        print(f"{status}  {item['id']:<24} top score {top_score:.2f}  {failure or ''}")

    # Summary per expected behaviour
    print()
    for expect in ("answer", "refuse"):
        group = [r for r in results if r["item"]["expect"] == expect]
        passed = sum(r["failure"] is None for r in group)
        print(f"{expect:<7} {passed}/{len(group)} passed")

    # Where the threshold sits between the two groups
    answer_scores = [r["top_score"] for r in results if r["item"]["expect"] == "answer"]
    refuse_scores = [r["top_score"] for r in results if r["item"]["expect"] == "refuse"]
    print(f"\nLowest top score of an answer question:  {min(answer_scores):.2f}")
    print(f"Highest top score of a refuse question:  {max(refuse_scores):.2f}")
    print(f"Current threshold:                       {MIN_SIMILARITY:.2f}")

    sys.exit(0 if all(r["failure"] is None for r in results) else 1)


if __name__ == "__main__":
    main()