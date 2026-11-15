import streamlit as st

from rag import answer_question, list_documents

REFUSAL_REASONS = {
    "low_similarity": "no document was close enough to the question",
    "not_in_sources": "the closest documents do not contain the answer",
    "no_citation": "the answer could not be linked to a source",
}

st.title("Ask your documents")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

# Nothing to search yet
if not list_documents():
    st.info("No documents indexed yet. Upload some first.")
    st.page_link("ui/documents.py", label="Go to Documents", icon=":material/folder:")
    st.stop()


def show_message(message: dict) -> None:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

        if message.get("refused"):
            st.caption(f"Refused because {REFUSAL_REASONS[message['reason']]}.")

        for source in message.get("sources", []):
            location = source.filename if source.page is None else f"{source.filename}, page {source.page}"
            with st.expander(f"[{source.number}] {location} · score {source.similarity:.2f}"):
                st.write(source.content)


# Show earlier messages
for message in st.session_state.messages:
    show_message(message)

# New question
if question := st.chat_input("Ask a question about your documents"):
    user_message = {"role": "user", "text": question}
    st.session_state.messages.append(user_message)
    show_message(user_message)

    try:
        with st.spinner("Searching documents..."):
            answer = answer_question(question)
        assistant_message = {
            "role": "assistant",
            "text": answer.text,
            "sources": answer.sources,
            "refused": answer.refused,
            "reason": answer.reason,
        }
    except Exception as error:
        assistant_message = {"role": "assistant", "text": f"Something went wrong: {error}"}

    st.session_state.messages.append(assistant_message)
    show_message(assistant_message)