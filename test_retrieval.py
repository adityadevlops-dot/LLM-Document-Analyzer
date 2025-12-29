from embeddings.vector_store import VectorStore

vs = VectorStore()
vs.load()

query = "What is the main topic of the document?"

results = vs.search(query, top_k=3)

for i, res in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print(res["text"][:500])
