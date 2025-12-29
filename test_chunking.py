from ingestion.load_text import load_text
from ingestion.chunking import chunk_text

text = load_text("data/sample_docs/Project_Report.pdf")

chunks = chunk_text(text, source="Project_Report.pdf")

print(f"Total chunks: {len(chunks)}")
print(chunks[0])
