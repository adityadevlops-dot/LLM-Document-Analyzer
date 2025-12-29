from ingestion.load_text import load_text

text = load_text("data/sample_docs/Project_Report.pdf")
print(text[:1000])
