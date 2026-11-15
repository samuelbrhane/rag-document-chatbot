import streamlit as st

_APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&display=swap');

/* Header: wordmark, tagline and the ground line */
.gd-header {
    border-bottom: 2px solid #1E4D3A;
    padding-bottom: 0.9rem;
    margin-bottom: 1.75rem;
}

.gd-brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.gd-wordmark {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-weight: 800;
    font-size: 2.5rem;
    letter-spacing: -0.035em;
    line-height: 1;
    color: #17251F;
    margin: 0;
}

.gd-tagline {
    color: #6B7A72;
    font-size: 1rem;
    margin: 0.55rem 0 0 0;
}

/* Citation markers inside answers */
.gd-cite {
    display: inline-block;
    min-width: 1.3em;
    padding: 0 0.35em;
    margin: 0 0.1em;
    border-radius: 0.35em;
    background: #1E4D3A;
    color: #FFFFFF;
    font-size: 0.72em;
    font-weight: 700;
    line-height: 1.55;
    text-align: center;
    vertical-align: 0.15em;
}

/* Source text inside the source boxes */
.gd-source {
    font-size: 0.9rem;
    line-height: 1.6;
    color: #4A5A53;
}

/* Primary buttons: solid moss */
[data-testid="stBaseButton-primary"] {
    background: #1E4D3A;
    border: none;
    color: #FFFFFF;
}

[data-testid="stBaseButton-primary"]:hover {
    background: #2A6249;
    color: #FFFFFF;
}

/* Sidebar: flat sage */
[data-testid="stSidebar"] {
    background: #EDF2EC;
}
</style>
"""


def apply_app_styles() -> None:
    """Apply the Grounded styles to every page."""
    st.markdown(_APP_CSS, unsafe_allow_html=True)