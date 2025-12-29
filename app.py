import streamlit as st
import os
from ingestion.load_text import load_text
from ingestion.chunking import chunk_text
from embeddings.vector_store import VectorStore
from query_engine.qa_pipeline import answer_question

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="LLM Document Analyzer",
    layout="wide",
    page_icon="📄"
)

# ------------------ Cached Model ------------------
@st.cache_resource(show_spinner=False)
def load_embedding_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")

# ------------------ Cached Embeddings ------------------
@st.cache_data(show_spinner=False)
def compute_embeddings(text_chunks):
    model = load_embedding_model()
    return model.encode(text_chunks, show_progress_bar=True)

# ------------------ Vector Store Lazy Loader ------------------
@st.cache_resource(show_spinner=False)
def load_vector_store():
    vs = VectorStore()
    try:
        vs.load()
    except FileNotFoundError:
        pass
    return vs

# ------------------ Session State ------------------
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
    st.session_state.documents_loaded = False
if "history" not in st.session_state:
    st.session_state.history = []
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

# ------------------ Sidebar ------------------
st.sidebar.title("📄 Document Manager")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs / DOCX / TXT",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)
clear_button = st.sidebar.button("🧹 Clear All Documents")

if clear_button:
    st.session_state.vector_store = None
    st.session_state.documents_loaded = False
    st.session_state.history = []
    st.session_state.processed_files = []
    st.sidebar.success("✅ Cleared all documents and history.")

# ------------------ Main Panel ------------------
st.title("💬 LLM Document Analyzer")

# Show instructions on initial load
if not uploaded_files and not st.session_state.documents_loaded:
    st.info("📌 Upload a document from the sidebar to start asking questions.")
    st.image("https://img.icons8.com/ios-filled/100/000000/upload.png", width=120)
else:
    # Load vector store lazily
    if st.session_state.vector_store is None:
        with st.spinner("Loading existing documents..."):
            st.session_state.vector_store = load_vector_store()
            st.session_state.documents_loaded = len(st.session_state.vector_store.documents) > 0

# ------------------ Process Uploaded Files ------------------
if uploaded_files:
    with st.spinner("Processing uploaded files..."):
        progress_bar = st.progress(0)
        total_files = len(uploaded_files)
        for i, uploaded_file in enumerate(uploaded_files, 1):
            if uploaded_file.name in st.session_state.processed_files:
                progress_bar.progress(i / total_files)
                continue

            # Load text from file
            text = load_text(uploaded_file)
            if not text.strip():
                st.warning(f"⚠️ No readable text in {uploaded_file.name}")
                progress_bar.progress(i / total_files)
                continue

            # Chunk text
            chunks = chunk_text(text)
            for chunk in chunks:
                chunk["file"] = uploaded_file.name

            # Initialize vector store if not exists
            if st.session_state.vector_store is None:
                st.session_state.vector_store = VectorStore()

            # Add chunks to vector store
            st.session_state.vector_store.add_documents(chunks)
            st.session_state.processed_files.append(uploaded_file.name)
            progress_bar.progress(i / total_files)

        # Save vector store after processing
        st.session_state.vector_store.save()
        st.session_state.documents_loaded = len(st.session_state.vector_store.documents) > 0
        st.sidebar.success("✅ Documents processed successfully!")

# ------------------ Question Section ------------------
if st.session_state.documents_loaded:
    with st.form(key="question_form"):
        question = st.text_input(
            "Type your question here:",
            placeholder="e.g., What is the roll number?"
        )
        submit_button = st.form_submit_button("Ask")

        if submit_button and question.strip():
            with st.spinner("🤖 Thinking..."):
                try:
                    answer = answer_question(question, st.session_state.vector_store)
                    st.session_state.history.append({"question": question, "answer": answer})

                    # Show chat history (latest first)
                    for i, item in enumerate(st.session_state.history[::-1], 1):
                        with st.expander(f"Q{i}: {item['question']}"):
                            st.markdown(f"**Answer:** {item['answer']}")

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ------------------ Footer ------------------
st.markdown("---")
st.markdown("📝 Developed by Aditya Kumar Chaubey| Powered by FAISS, SentenceTransformers, Streamlit")
