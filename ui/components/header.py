import streamlit as st

_MARK = """
<svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true">
  <defs>
    <linearGradient id="gd-mark" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1E4D3A"/>
      <stop offset="100%" stop-color="#3F8F5F"/>
    </linearGradient>
  </defs>
  <circle cx="17" cy="10" r="6.5" fill="url(#gd-mark)"/>
  <line x1="17" y1="16" x2="17" y2="21" stroke="#1E4D3A" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="3" y1="21" x2="31" y2="21" stroke="#1E4D3A" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M17 21 L11 30 M17 21 L17 31 M17 21 L23 30" stroke="#3F8F5F" stroke-width="2" stroke-linecap="round" fill="none"/>
</svg>
"""


def render_header(title: str, tagline: str, brand: bool = False) -> None:
    """Page header with the ground line. brand=True adds the Grounded logo mark."""
    mark = _MARK if brand else ""
    st.markdown(
        f'<div class="gd-header">'
        f'<div class="gd-brand">{mark}<p class="gd-wordmark">{title}</p></div>'
        f'<p class="gd-tagline">{tagline}</p>'
        f"</div>",
        unsafe_allow_html=True,
    )