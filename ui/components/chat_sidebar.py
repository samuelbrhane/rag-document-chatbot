import streamlit as st

from rag import delete_chat, list_chats, rename_chat


def render_chat_sidebar(visitor_id: str) -> None:
    """Show New chat and the visitor's chat list. The open chat is kept in session_state.chat_id."""
    with st.sidebar:
        if st.button("New chat", icon=":material/add:", width="stretch"):
            st.session_state.chat_id = None
            st.rerun()

        chats = list_chats(visitor_id)
        if chats:
            st.caption("Your chats")

        for chat in chats:
            is_open = chat.id == st.session_state.get("chat_id")
            title_col, menu_col = st.columns([5, 1], vertical_alignment="center")

            if title_col.button(
                chat.title,
                key=f"open_{chat.id}",
                type="primary" if is_open else "tertiary",
                width="stretch",
            ):
                st.session_state.chat_id = chat.id
                st.rerun()

            with menu_col.popover(":material/more_vert:"):
                new_title = st.text_input("Title", value=chat.title, key=f"title_{chat.id}")
                if st.button("Rename", key=f"rename_{chat.id}"):
                    rename_chat(chat.id, visitor_id, new_title.strip() or chat.title)
                    st.rerun()
                if st.button("Delete", key=f"delete_chat_{chat.id}", type="primary"):
                    delete_chat(chat.id, visitor_id)
                    if is_open:
                        st.session_state.chat_id = None
                    st.rerun()