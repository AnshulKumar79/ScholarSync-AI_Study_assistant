import streamlit as st
import requests
import base64

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


#Main Chat UI
st.title("🎓 ScholarSync AI")
st.markdown("Chat with your docs and images!")

# Purane messages dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Agar purane message mein image thi, toh wo bhi dikhayein
        if "image_b64" in message and message["image_b64"]:
            st.image(base64.b64decode(message["image_b64"]), width=300)

#Layout for Image Uploader and Chat Input
col1, col2 = st.columns([1, 3])
with col1:
    img_upload = st.file_uploader("🖼️ Attach Image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

prompt = st.chat_input("Ask a follow-up question...")

if prompt:
    #Image ko Base64 mein convert karna (agar upload hui hai)
    image_b64 = None
    if img_upload:
        image_b64 = base64.b64encode(img_upload.getvalue()).decode("utf-8")

    #User ka message UI par dikhana
    st.session_state.messages.append({"role": "user", "content": prompt, "image_b64": image_b64})
    with st.chat_message("user"):
        st.markdown(prompt)
        if image_b64:
            st.image(img_upload, width=300)

    #API Request bhejna
    with st.chat_message("assistant"):
        with st.spinner("Analyzing text and image..."):
            try:
                #Sirf purane messages history mein bhejenge
                chat_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
                
                payload = {
                    "question": prompt,
                    "history": chat_history,
                    "image_base64": image_b64
                }
                
                res = requests.post(f"{API_URL}/ask", json=payload)
                if res.status_code == 200:
                    answer = res.json()["answer"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error fetching answer: {res.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")