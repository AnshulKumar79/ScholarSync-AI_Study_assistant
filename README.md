## ScholarSync AI: Multimodal RAG Study Assistant

ScholarSync is an intelligent study companion designed to bridge the gap between static documents and interactive learning. Built on a **Multimodal RAG (Retrieval-Augmented Generation)** architecture, it allows users to chat with their PDFs/img and analyze visual data (diagrams, math problems, handwritten notes) using LLM models.

**TRY IT YOURSELF**[https://anshulkumar24-scholarsync.hf.space/]
---

## Key Features

* **Multimodal Intelligence:** Ask questions about text within a PDF or upload images (PNG/JPG/JPEG) for visual analysis in the same chat session.
* **Persistent Context:** Uses **FAISS (Facebook AI Similarity Search)** for efficient vector retrieval, ensuring the AI only answers based on your specific documents.
* **Conversational Memory:** Maintains a rolling window of chat history to understand follow-up questions and context.
* **Interactive UI:** A high-contrast, professional dark-mode interface built with Streamlit, optimized for readability and focus.

---

## Technical Stack

* **LLM:** Google Gemini-2.5-Flash / Gemini-2.5-Flash-lite
* **Orchestration:** LangChain
* **Vector Database:** FAISS
* **Backend:** FastAPI (Uvicorn)
* **Frontend:** Streamlit
* **Embeddings:** Google Generative AI Embeddings (`gemini/embedding-001`)

---

## Project Structure

```text
ScholarSync/
├── app.py              # Streamlit Frontend (UI & Image Logic)
├── main.py             # FastAPI Backend (RAG & Vector DB Logic)
├── prompts.py          # Multimodal Prompt Engineering & Memory
├── requirements.txt    # Project Dependencies
├── .env                # API Keys (Git-ignored)
└── faiss_index/        # Local Vector Storage (Generated)
```

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ScholarSync.git
cd ScholarSync
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```text
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

## Running the Application

ScholarSync operates on a decoupled architecture. You will need two terminal windows open:

**Terminal 1: Start the FastAPI Backend**
```bash
uvicorn main:app --reload
```

**Terminal 2: Start the Streamlit Frontend**
```bash
streamlit run app.py
```

---

## UI Preview
* **Dark Mode:** Deep charcoal aesthetics for eye comfort during long study sessions.
* **Unified Upload:** A single sidebar button handles both PDF and Image processing.
* **Smart History:** "Clear History" functionality to reset context and start fresh.

---

## Contributing
Contributions are welcome! If you'd like to improve the RAG performance or add new UI features, please fork the repo and create a pull request.

---

## License
This project is licensed under the MIT License.
