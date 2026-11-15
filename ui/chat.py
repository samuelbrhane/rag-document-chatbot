import streamlit as st

from rag import (
    AnswerStream,
    Message,
    add_message,
    create_chat,
    get_messages,
    list_documents,
    make_title,
)
from ui.components import (
    apply_chat_styles,
    format_citations,
    format_source,
    render_chat_sidebar,
    render_header,
    render_welcome,
    smooth_stream,
)

REFUSAL_REASONS = {
    "low_similarity": "no document was close enough to the question",
    "not_in_sources": "the closest documents do not contain the answer",
    "no_citation": "the answer could not be linked to a source",
}

visitor_id = st.session_state.visitor_id
apply_chat_styles()
render_chat_sidebar(visitor_id)

render_header("Ask Lumen Home", "Answers from the store's documents, with sources.")

# Nothing to search yet
if not list_documents():
    st.info("No documents indexed yet. Upload some first.")
    st.page_link("ui/documents.py", label="Go to Documents", icon=":material/folder:")
    st.stop()


def show_message(message: Message, asked: str | None = None) -> None:
    with st.chat_message(message.role):
        st.markdown(format_citations(message.content), unsafe_allow_html=True)

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
                st.markdown(format_source(source.content), unsafe_allow_html=True)


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

if not messages:
    render_welcome()

# New question
typed = st.chat_input("Ask a question about your documents")
question = typed or st.session_state.pop("pending_question", None)

if question:
    show_message(Message(role="user", content=question))

    if chat_id is None:
        chat_id = create_chat(visitor_id, make_title(question))
        st.session_state.chat_id = chat_id

    history = [(m.role, m.content) for m in messages]
    add_message(chat_id, Message(role="user", content=question))

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                stream = AnswerStream(question, history)
            if stream.answer is None:
                st.write_stream(smooth_stream(stream))
            answer = stream.answer
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
    st.rerun()  # redraw from the database with sources and the updated sidebar