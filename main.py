import os
import shutil
from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from rag_utils import process_and_store_pdf, get_context_from_db
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

#loading secret keys from .env file
load_dotenv()

#FastAPI app initialize karna
app = FastAPI(title="ScholarSync API", description="Backend for RAG Study Assistant")

#Gemini LLM setup karna
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
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
        # 1. Uploaded file ko temporarily save karna
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. PDF ko process aur FAISS mein store karna
        num_chunks = process_and_store_pdf(temp_file_path)

        # 3. Temporary file ko delete kar dena (Clean up)
        os.remove(temp_file_path)

        return {
            "status": "success",
            "message": f"File '{file.filename}' processed successfully.",
            "chunks_created": num_chunks
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}



@app.post("/ask")
async def ask_question(req: QuestionRequest):
    try:
        #Database se relevant context nikalna
        context = get_context_from_db(req.question)
        
        if "ERROR" in context:
            return {"status": "error", "message": "Please upload a PDF first before asking questions."}

        #AI ke liye ek strict Prompt banana
        prompt = f"""You are an intelligent study assistant named ScholarSync. 
        Please answer the user's question based ONLY on the provided Context. 
        If the answer is not available in the context, clearly state: "I'm sorry, but the answer is not present in the uploaded document." Do not guess the answer.

        Context:
        {context}

        Question:
        {req.question}

        Answer:"""

        #Gemini ko prompt bhej kar answer lena
        response = llm.invoke(prompt)

        return {
            "status": "success",
            "question": req.question,
            "answer": response.content
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}