import streamlit as st

st.set_page_config(page_title="Document Chatbot", page_icon=":material/chat:")

chat_page = st.Page("ui/chat.py", title="Chat", icon=":material/chat:", default=True)
documents_page = st.Page("ui/documents.py", title="Documents", icon=":material/folder:")

st.navigation([chat_page, documents_page]).run()