import streamlit as st
import requests

#Backend API URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="ScholarSync-AI Assistant", page_icon="🎓", layout="wide")

#Custom CSS for better look
st.markdown("""
    <style>
    /* Better styling for chat messages */
    .stChatMessage { border-radius: 10px; padding: 10px; margin-bottom: 10px; }
    .stSidebar { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

#Session State initialize (Messages store karne ke liye)
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR: Upload Logic ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135810.png", width=50) # Optional Logo
    st.title("ScholarSync Setup")
    
    st.markdown("### 1. Document Upload 📄")
    uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"], label_visibility="collapsed")
    
    if st.button("🚀 Process Document", use_container_width=True):
        if uploaded_file:
            with st.spinner("Indexing into Vector DB..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                res = requests.post(f"{API_URL}/upload", files=files)
                if res.status_code == 200:
                    st.success("Database Ready!")
                else:
                    st.error("Error processing document.")
        else:
            st.warning("Upload a PDF first.")
    
    st.divider()
    if st.button("🗑️ Clear Conversation", type="secondary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT INTERFACE ---
# Main Chat UI
st.title("🎓 ScholarSync AI")
st.markdown("Chat with your documents with full context memory!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a follow-up question..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # API Request with HISTORY
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Hum pichle messages bhej rahe hain (current prompt ko chhod kar)
                chat_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
                
                payload = {
                    "question": prompt,
                    "history": chat_history
                }
                
                res = requests.post(f"{API_URL}/ask", json=payload)
                if res.status_code == 200:
                    answer = res.json()["answer"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Error fetching answer.")
            except Exception as e:
                st.error(f"Backend connection failed: {e}")