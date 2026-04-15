def get_rag_prompt(context: str, question: str, history: list) -> str:
    """Returns the strict prompt with conversation history for memory."""
    
    # History ko ek readable string mein convert karna
    history_str = ""
    for msg in history[-5:]: # Memory save karne ke liye sirf last 5 messages bhejenge
        role = "User" if msg["role"] == "user" else "ScholarSync"
        history_str += f"{role}: {msg['content']}\n"

    return f"""You are an intelligent study assistant named ScholarSync. 
    Answer the user's question based ONLY on the provided Context. 
    Use the Conversation History to understand references (like "what did you mean by that?").
    If the answer is not in the context, say: "I'm sorry, but the answer is not present in the uploaded document." Do not guess.

    Conversation History:
    {history_str}

    Context:
    {context}

    Current Question:
    {question}

    Answer:"""