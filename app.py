import streamlit as st

from ui.components import get_visitor_id

st.set_page_config(page_title="Document Chatbot", page_icon=":material/chat:")
get_visitor_id()

chat_page = st.Page("ui/chat.py", title="Chat", icon=":material/chat:", default=True)
documents_page = st.Page("ui/documents.py", title="Documents", icon=":material/folder:")

st.navigation([chat_page, documents_page]).run()