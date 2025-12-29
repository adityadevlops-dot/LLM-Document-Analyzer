from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter



def chunk_text(
    text: str,
    chunk_size: int = 600,
    chunk_overlap: int = 100,
    source: str = "unknown"
) -> List[Dict]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_text(text)

    chunked_docs = []
    for idx, chunk in enumerate(chunks):
        chunked_docs.append({
            "chunk_id": idx,
            "text": chunk,
            "metadata": {
                "source": source
            }
        })

    return chunked_docs
