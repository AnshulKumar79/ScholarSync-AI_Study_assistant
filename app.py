import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="ScholarSync-AI Assistant", page_icon="🎓", layout="wide")

#Custom CSS for better look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4A90E2; color: white; }
    .stTextInput>div>div>input { border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

#Session State initialize (Messages store karne ke liye)
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR: Upload Logic ---
with st.sidebar:
    st.title("📂 Document Center")
    uploaded_file = st.file_uploader("Upload your Study Material (PDF)", type=["pdf"])
    
    if st.button("Process"):
        if uploaded_file:
            with st.spinner("Analyzing PDF and creating Vector DB..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    res = requests.post(f"{API_URL}/upload", files=files)
                    if res.status_code == 200:
                        st.success(f"Success! Processed {res.json()['chunks_created']} chunks.")
                    else:
                        st.error("Backend error. Check terminal.")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
        else:
            st.warning("Please select a file first.")
    
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT INTERFACE ---
st.title("💬 Chat with your assistant")
st.caption("Ask anything from your uploaded document — ScholarSync will find the answer.")

#Purane messages display karna
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#User Input
if prompt := st.chat_input("What would you like to know?"):
    #User message show karein
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    #Backend se answer mangwayein
    with st.chat_message("assistant"):
        with st.spinner("Searching document..."):
            try:
                res = requests.post(f"{API_URL}/ask", json={"question": prompt})
                if res.status_code == 200:
                    answer = res.json()["answer"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Backend error occurred.")
            except Exception as e:
                st.error(f"Could not reach backend: {e}")