import streamlit as st
import requests
import base64

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="ScholarSync AI", page_icon="🎓", layout="wide")

#High-Contrast Dark Theme CSS
st.markdown("""
    <style>
    /* Global Background & Text */
    .stApp {
        background-color: #0F0F0F;
        color: #FFFFFF;
    }
    
    /* Sidebar: Deep Grey with clear border */
    section[data-testid="stSidebar"] {
        background-color: #1A1A1A !important;
        border-right: 1px solid #333333;
        width: 320px !important;
    }

    /* Standardizing Text Colors for Visibility */
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important;
    }

    /* File Uploader styling */
    .stFileUploader section {
        background-color: #262626 !important;
        border: 1px dashed #444444 !important;
        border-radius: 10px;
    }

    /* Buttons: Modern Dark look with Hover */
    .stButton>button {
        width: 100%;
        background-color: #2D2D2D;
        color: white !important;
        border: 1px solid #444444;
        border-radius: 8px;
        padding: 0.6rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #3D3D3D;
        border-color: #666666;
        transform: translateY(-2px);
    }

    /* Chat Input Styling */
    .stChatInput {
        background-color: #1A1A1A !important;
        border-radius: 15px;
    }

    /* Chat Bubbles: High Contrast */
    [data-testid="stChatMessage"] {
        background-color: #1A1A1A !important; /* Slightly lighter than BG */
        border: 1px solid #262626 !important;
        border-radius: 12px !important;
        margin-bottom: 15px !important;
        padding: 1.5rem !important;
    }
    
    /* Center the chat content for better standard sizing */
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
    }

    /* Adjusting sizes for standard feel */
    .stImage > img {
        border-radius: 10px;
        border: 1px solid #333333;
    }
    </style>
    """, unsafe_allow_html=True)

#Sidebar Implementation
with st.sidebar:
    st.markdown("<h2 style='margin-bottom:0;'>ScholarSync</h2>", unsafe_allow_html=True)
    st.caption("v1.0 • Multimodal AI Assistant")
    st.markdown("---")
    
    st.markdown("### 📥 Knowledge Source")
    uploaded_file = st.file_uploader(
        "PDF for Context or Image for Vision", 
        type=["pdf", "png", "jpg", "jpeg"],
        label_visibility="visible"
    )
    
    # Upload Button
    if st.button("✨ Process & Sync", use_container_width=True):
        if uploaded_file:
            with st.spinner("Processing..."):
                file_ext = uploaded_file.name.split('.')[-1].lower()
                if file_ext == 'pdf':
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    try:
                        res = requests.post(f"{API_URL}/upload", files=files)
                        if res.status_code == 200: st.success("Document Indexed.")
                        else: st.error("Backend Error.")
                    except: st.error("Is Backend Running?")
                else:
                    st.info("Image Ready for Chat!")
        else:
            st.warning("Upload a file first.")


    st.markdown("<br><br>", unsafe_allow_html=True) # Thodi spacing ke liye
    st.divider()
    st.markdown("### ⚙️ System Controls")
    

    if st.button("🗑️ Clear Chat History", use_container_width=True, help="Purani baatein bhula do!"):
        st.session_state.messages = []
        st.rerun()

#Main Interface
st.markdown("<h1 style='text-align: center; font-size: 2.2rem;'>What are we learning today?</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

#Show history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_b64" in message and message["image_b64"]:
            st.image(base64.b64decode(message["image_b64"]), width=450)

#Input logic
if prompt := st.chat_input("Ask about the PDF or Image..."):
    image_b64 = None
    if uploaded_file and uploaded_file.name.split('.')[-1].lower() in ['png', 'jpg', 'jpeg']:
        image_b64 = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

    #Add to state
    st.session_state.messages.append({"role": "user", "content": prompt, "image_b64": image_b64})
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if image_b64: st.image(uploaded_file, width=450)

    #Bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chat_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
                payload = {"question": prompt, "history": chat_history, "image_base64": image_b64}
                
                res = requests.post(f"{API_URL}/ask", json=payload, timeout=60)
                answer = res.json().get("answer", "No response.")
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error("Connection to Backend lost.")