# utils/document_processor.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_pdf_to_chunks(file_path: str):
    """Reads a PDF file and splits it into smaller text chunks."""
    try:
        #Loading the PDF
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        #Splitting into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(docs)
        
        return chunks
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None


        