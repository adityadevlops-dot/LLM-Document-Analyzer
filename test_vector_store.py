from ingestion.load_text import load_text
from ingestion.chunking import chunk_text
from embeddings.vector_store import VectorStore

# Load document
text = load_text("data/sample_docs/Project_Report.pdf")

# Chunk it
chunks = chunk_text(text, source="Project_Report.pdf")

# Create vector store
vs = VectorStore()
vs.add_documents(chunks)

# Save index
vs.save()

print("✅ Vector store created and saved successfully")
