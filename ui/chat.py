import streamlit as st

from rag import (
    Message,
    add_message,
    answer_question,
    create_chat,
    get_messages,
    list_documents,
    make_title,
)
from ui.components import render_chat_sidebar

REFUSAL_REASONS = {
    "low_similarity": "no document was close enough to the question",
    "not_in_sources": "the closest documents do not contain the answer",
    "no_citation": "the answer could not be linked to a source",
}

visitor_id = st.session_state.visitor_id
render_chat_sidebar(visitor_id)

st.title("Ask your documents")

# Nothing to search yet
if not list_documents():
    st.info("No documents indexed yet. Upload some first.")
    st.page_link("ui/documents.py", label="Go to Documents", icon=":material/folder:")
    st.stop()


def show_message(message: Message, asked: str | None = None) -> None:
    with st.chat_message(message.role):
        st.markdown(message.content)

        dev_mode = st.session_state.get("dev_mode", False)

        if dev_mode and message.rewritten_question and message.rewritten_question != asked:
            st.caption(f"Searched for: {message.rewritten_question}")

        if dev_mode and message.refused and message.refusal_reason:
            st.caption(f"Refused because {REFUSAL_REASONS[message.refusal_reason]}.")

        for source in message.sources:
            location = source.filename if source.page is None else f"{source.filename}, page {source.page}"
            label = f"[{source.number}] {location}"
            if dev_mode:
                label += f" · score {source.similarity:.2f}"
            with st.expander(label):
                st.write(source.content)


# Load the open chat
chat_id = st.session_state.get("chat_id")
messages = get_messages(chat_id, visitor_id) if chat_id else []
if chat_id and not messages:
    st.session_state.chat_id = chat_id = None  # deleted or not this visitor's chat

last_question = None
for message in messages:
    show_message(message, asked=last_question)
    if message.role == "user":
        last_question = message.content

# New question
if question := st.chat_input("Ask a question about your documents"):
    show_message(Message(role="user", content=question))

    is_new_chat = chat_id is None
    if is_new_chat:
        chat_id = create_chat(visitor_id, make_title(question))
        st.session_state.chat_id = chat_id

    history = [(m.role, m.content) for m in messages]
    add_message(chat_id, Message(role="user", content=question))

    try:
        with st.spinner("Searching documents..."):
            answer = answer_question(question, history)
        reply = Message(
            role="assistant",
            content=answer.text,
            rewritten_question=answer.searched_for,
            sources=answer.sources,
            refused=answer.refused,
            refusal_reason=answer.reason,
        )
    except Exception as error:
        reply = Message(role="assistant", content=f"Something went wrong: {error}")

    add_message(chat_id, reply)
    show_message(reply, asked=question)

    if is_new_chat:
        st.rerun()  # refresh the sidebar so the new chat appears in the list