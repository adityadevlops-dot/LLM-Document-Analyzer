import faiss
import pickle
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import os

class VectorStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []

    def add_documents(self, docs: List[Dict], batch_size: int = 32):
        if not docs:
            raise ValueError("❌ No documents provided to vector store")

        texts = [doc["text"] for doc in docs if doc.get("text", "").strip()]
        if len(texts) == 0:
            raise ValueError("❌ All document texts are empty")

        # Batch embedding
        embeddings = self.model.encode(texts, batch_size=batch_size, show_progress_bar=True)

        if len(embeddings.shape) != 2:
            raise ValueError("❌ Invalid embedding shape")

        dimension = embeddings.shape[1]

        if self.index is None:
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)
        self.documents.extend(docs)

    def search(self, query: str, top_k: int = 3):
        if self.index is None or len(self.documents) == 0:
            raise ValueError("Vector store is empty. Add or load documents first.")

        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, top_k)
        return [self.documents[idx] for idx in indices[0]]

    def save(self, index_path="faiss.index", doc_path="documents.pkl"):
        faiss.write_index(self.index, index_path)
        with open(doc_path, "wb") as f:
            pickle.dump(self.documents, f)

    def load(self, index_path="faiss.index", doc_path="documents.pkl"):
        if os.path.exists(index_path) and os.path.exists(doc_path):
            self.index = faiss.read_index(index_path)
            with open(doc_path, "rb") as f:
                self.documents = pickle.load(f)
        else:
            self.index = None
            self.documents = []
