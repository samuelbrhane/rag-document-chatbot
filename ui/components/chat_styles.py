import streamlit as st

_CHAT_CSS = """
<style>
/* User messages: right side, sage bubble, no avatar */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse;
    margin-left: auto;
    width: fit-content;
    max-width: 75%;
    padding: 0.55rem 1.1rem;
    border-radius: 1.25rem 1.25rem 0.35rem 1.25rem;
    background: #EDF2EC;
}

[data-testid="stChatMessageAvatarUser"] {
    display: none;
}

/* Assistant messages: full width on the left, no background */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: transparent;
}
</style>
"""


def apply_chat_styles() -> None:
    """Style the chat like ChatGPT: questions on the right, answers on the left."""
    st.markdown(_CHAT_CSS, unsafe_allow_html=True)