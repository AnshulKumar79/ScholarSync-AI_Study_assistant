from langchain_core.messages import SystemMessage, HumanMessage

def get_rag_prompt(context: str, question: str, history: list, image_base64: str = None):
    """Returns a multimodal prompt containing history, context, and optional image."""
    
    #Conversation History
    history_str = ""
    for msg in history[-5:]:
        role = "User" if msg["role"] == "user" else "ScholarSync"
        history_str += f"{role}: {msg['content']}\n"

    #Defining System Instructions
    system_prompt = f"""You are an intelligent study assistant named ScholarSync. 
    Answer the user's question based ONLY on the provided Context or the provided Image. 
    Use the Conversation History to understand references.
    If the answer is not in the context or image, clearly state: "I don't have enough information to answer that."

    Conversation History:
    {history_str}

    Context from PDF:
    {context}"""

    #Build User Message (Text + Optional Image)
    user_content = [{"type": "text", "text": f"Current Question:\n{question}"}]
    
    if image_base64:
        user_content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
        })

    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_content)
    ]