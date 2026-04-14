import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings # Naya Import
from langchain_community.vectorstores import FAISS

#API key load karne ke liye
load_dotenv()

#HuggingFace ki jagah Google ka cloud embedding
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001", 
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def process_and_store_pdf(file_path: str):
    #PDF Load karna
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    #Text ko chunks (tukdo) mein todna
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)

    #Chunks ko Vectors mein convert karke FAISS DB mein store karna
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    #Database ko local folder mein save karna
    vectorstore.save_local("faiss_index")

    return len(chunks)



def get_context_from_db(query: str):
    try:
        #Saved FAISS database ko load karna
        #(allow_dangerous_deserialization=True likhna zaroori hai local files ke liye)
        vectorstore = FAISS.load_local(
            "faiss_index", 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        
        #Database se sawal se milte-julte top 3 chunks nikalna
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.invoke(query)
        
        #Un chunks ke text ko ek string mein jodna
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        return context
    
    except Exception as e:
        return "ERROR: Database not found."