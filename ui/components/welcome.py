import streamlit as st

EXAMPLE_QUESTIONS = [
    (":material/assignment_return:", "How long do I have to return an item?"),
    (":material/workspace_premium:", "What do Gold members get?"),
    (":material/kitchen:", "Can I put Aurum plates in the dishwasher?"),
    (":material/help:", "What is the warranty on electronics?"),
]


def _ask(question: str) -> None:
    st.session_state.pending_question = question


def render_welcome() -> None:
    """Intro and clickable example questions for an empty chat."""
    st.markdown(
        "Ask anything about **Lumen Home**'s policies and product care. "
        "Every answer shows the document it came from, and when the answer "
        "is not in the documents, Grounded says so instead of guessing."
    )
    st.caption("Try one of these:")

    columns = st.columns(2)
    for i, (icon, question) in enumerate(EXAMPLE_QUESTIONS):
        columns[i % 2].button(
            question,
            icon=icon,
            key=f"example_{i}",
            width="stretch",
            on_click=_ask,
            args=(question,),
        )