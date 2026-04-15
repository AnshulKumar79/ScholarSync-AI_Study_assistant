import os
import shutil
from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from prompts import get_rag_prompt
from utils.doc_processor import process_pdf_to_chunks
from utils.DB_handler import create_and_store_db, get_context_from_db
from typing import List, Dict, Optional

class QuestionRequest(BaseModel):
    question: str
    history: List[Dict[str, str]] = []
    image_base64: Optional[str] = None

#loading secret keys from .env file
load_dotenv()

#FastAPI app initialize karna
app = FastAPI(title="ScholarSync API", description="Backend for RAG Study Assistant")

#Gemini LLM setup karna
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

#Basic health-check route
@app.get("/")
async def root():
    return {"message": "Welcome to ScholarSync API! Server is running."}

#AI connection test karne ka route
@app.get("/test-ai")
async def test_ai():
    try:
        # Gemini ko ek simple prompt bhej rahe hain
        response = llm.invoke("Say 'Hello, your API is working perfectly!' but add a little bit of developer humor.")
        return {"status": "success", "ai_response": response.content}
    except Exception as e:
        return {"status": "error", "message": str(e)}


#PDF upload aur process karne ka route
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        #Uploaded file ko temporarily save karna
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        #PDF ko process karna aur chunks create karna
        num_chunks = process_pdf_to_chunks(temp_file_path)
        if not num_chunks:
            return {"status": "error", "message": "Failed to read PDF."}

        #Chunks ko database mein store karna
        success = create_and_store_db(num_chunks)
        if not success:
            return {"status": "error", "message": "Failed to save to database."}

        return {"status": "success", "chunks_created": len(num_chunks)}
    
    finally:
        #Temp file delete karna (finally block ensures ye humesha delete ho)
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@app.post("/ask")
async def ask_question(req: QuestionRequest):
    try:
        #Context sirf tab nikalenge jab PDF upload hui ho, warna blank string
        context = get_context_from_db(req.question) if get_context_from_db(req.question) != "ERROR: Database not found." else "No PDF context provided."
        
        #Ab prompt function ko image bhi bhejenge
        prompt_messages = get_rag_prompt(context, req.question, req.history, req.image_base64)

        
        response = llm.invoke(prompt_messages)

        return {
            "status": "success",
            "answer": response.content
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}