import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Hum open-source HuggingFace model use kar rahe hain embeddings ke liye
# Ye fast hai aur free hai, isse cost bachegi
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def process_and_store_pdf(file_path: str):
    # 1. PDF Load karna
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # 2. Text ko chunks (tukdo) mein todna
    # chunk_size 1000 rakha hai, aur overlap 200 taaki context break na ho
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)

    # 3. Chunks ko Vectors mein convert karke FAISS DB mein store karna
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Database ko local folder mein save karna
    vectorstore.save_local("faiss_index")

    return len(chunks)