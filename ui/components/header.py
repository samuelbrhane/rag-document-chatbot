import streamlit as st


def render_header(title: str, tagline: str) -> None:
    """Show a gradient page title with a tagline under it."""
    st.markdown(
        f'<p class="grounded-title">{title}</p><p class="grounded-tagline">{tagline}</p>',
        unsafe_allow_html=True,
    )