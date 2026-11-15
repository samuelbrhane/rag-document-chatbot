import streamlit as st

GRADIENT = "linear-gradient(135deg, #1F7A5C 0%, #2BB3A3 100%)"

_APP_CSS = f"""
<style>
/* Header: gradient title and tagline */
.grounded-title {{
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: {GRADIENT};
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin: 0;
    line-height: 1.1;
}}

.grounded-tagline {{
    color: #5B6F68;
    font-size: 1rem;
    margin: 0.25rem 0 1.5rem 0;
}}

/* Primary buttons: gradient fill */
[data-testid="stBaseButton-primary"] {{
    background: {GRADIENT};
    border: none;
    color: white;
}}

[data-testid="stBaseButton-primary"]:hover {{
    filter: brightness(1.08);
    color: white;
}}

/* Sidebar: very light gradient tint */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #EEF6F2 0%, #E6F5F3 100%);
}}
</style>
"""


def apply_app_styles() -> None:
    """Apply the Grounded gradient styles to every page."""
    st.markdown(_APP_CSS, unsafe_allow_html=True)