def get_rag_prompt(context: str, question: str) -> str:
    """Returns the strict prompt for the ScholarSync RAG system."""
    
    return f"""You are an intelligent study assistant named ScholarSync. 
    Please answer the user's question based ONLY on the provided Context. 
    If the answer is not available in the context, clearly state: "I'm sorry, but the answer is not present in the uploaded document." Do not guess the answer.

    Context:
    {context}

    Question:
    {question}

    Answer:"""





    