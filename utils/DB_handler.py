# utils/database_handler.py
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

#Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def create_and_store_db(chunks):
    """Converts chunks into embeddings and saves to FAISS DB."""
    try:
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local("faiss_index")
        return True
    except Exception as e:
        print(f"Error saving to DB: {e}")
        return False

def get_context_from_db(query: str):
    """Retrieves the top 3 relevant chunks from the database."""
    try:
        vectorstore = FAISS.load_local(
            "faiss_index", 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.invoke(query)
        
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        return context
    except Exception as e:
        return "ERROR: Database not found."