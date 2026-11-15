import re
import uuid

import streamlit as st

_VALID_ID = re.compile(r"^[0-9a-f]{32}$")


def get_visitor_id() -> str:
    """Return this visitor's ID, creating one on the first visit, and keep it in the URL."""
    visitor_id = st.query_params.get("visitor")

    if not visitor_id or not _VALID_ID.match(visitor_id):
        visitor_id = st.session_state.get("visitor_id") or uuid.uuid4().hex

    st.session_state.visitor_id = visitor_id
    st.query_params["visitor"] = visitor_id
    return visitor_id