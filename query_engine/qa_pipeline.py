from query_engine.reasoning import ask_llm


def answer_question(question: str, vector_store) -> str:
    # Retrieve relevant chunks
    docs = vector_store.search(question, top_k=3)

    if not docs:
        return "❌ No relevant content found in the document."

    # Build context
    context = "\n\n".join(doc["text"] for doc in docs)

    # Ask LLM
    return ask_llm(context, question)
