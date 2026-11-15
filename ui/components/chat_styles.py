import streamlit as st

_CHAT_CSS = """
<style>
/* User messages: right side, rounded bubble, no avatar */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse;
    margin-left: auto;
    width: fit-content;
    max-width: 75%;
    padding: 0.5rem 1rem;
    border-radius: 1.25rem;
    background-color: rgba(128, 128, 128, 0.12);
}

[data-testid="stChatMessageAvatarUser"] {
    display: none;
}

/* Assistant messages: full width on the left, no background */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background-color: transparent;
}
</style>
"""


def apply_chat_styles() -> None:
    """Style the chat like ChatGPT: questions on the right, answers on the left."""
    st.markdown(_CHAT_CSS, unsafe_allow_html=True)