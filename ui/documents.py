import streamlit as st

from rag import delete_document, ingest_file, list_documents
from rag.config import SUPPORTED_EXTENSIONS

st.title("Documents")
st.caption("Upload the documents the chatbot should answer from.")

# Upload and index
files = st.file_uploader(
    "Upload documents",
    type=[ext.lstrip(".") for ext in SUPPORTED_EXTENSIONS],
    accept_multiple_files=True,
)

if st.button("Index documents", type="primary", disabled=not files):
    for file in files:
        with st.spinner(f"Indexing {file.name}..."):
            try:
                result = ingest_file(file.name, file.getvalue())
                st.success(f"{result.filename}: {result.pages} pages, {result.chunks} chunks")
            except ValueError as error:
                st.warning(str(error))
            except Exception as error:
                st.error(f"{file.name} failed: {error}")

# List and delete
st.subheader("Indexed documents")
documents = list_documents()

if not documents:
    st.info("No documents indexed yet.")

for filename, chunk_count in documents:
    name_col, button_col = st.columns([4, 1])
    name_col.write(f"**{filename}** · {chunk_count} chunks")
    if button_col.button("Delete", key=f"delete_{filename}"):
        delete_document(filename)
        st.rerun()