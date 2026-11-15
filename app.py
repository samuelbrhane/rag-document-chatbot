import streamlit as st

from ui.components import apply_app_styles, get_visitor_id

st.set_page_config(page_title="Grounded", page_icon=":material/fact_check:")
get_visitor_id()
apply_app_styles()

chat_page = st.Page("ui/chat.py", title="Chat", icon=":material/chat:", default=True)
documents_page = st.Page("ui/documents.py", title="Documents", icon=":material/folder:")

st.navigation([chat_page, documents_page]).run()