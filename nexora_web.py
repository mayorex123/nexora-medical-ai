import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from nexora.memory.history import save_message

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="NEXORA Medical AI", page_icon="🩺", layout="wide")

# --- UNIVERSAL CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main background & text */
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    
    /* Chat bubbles */
    .stChatMessage { 
        background-color: #1E232B; border-radius: 12px; padding: 15px; 
        margin-bottom: 10px; width: 100% !important; box-sizing: border-box !important; overflow-wrap: break-word !important;
    }
    
    /* Force white text in chat */
    .stChatMessage p, .stChatMessage li, .stChatMessage span, .stChatMessage strong, .stChatMessage table, .stChatMessage th, .stChatMessage td {
        color: #FAFAFA !important; font-size: 1rem;
    }

    /* Tables */
    .stChatMessage table { border-collapse: collapse; width: 100%; margin-top: 10px; display: block; overflow-x: auto; white-space: nowrap; }
    .stChatMessage th, .stChatMessage td { border: 1px solid #444; padding: 8px; text-align: left; }
    .stChatMessage th { background-color: #2C3E50; }
    
    /* Sidebar & Header */
    [data-testid="stSidebar"] { background-color: #161B22; }
    header { visibility: hidden; }

    /* Input Box */
    div[data-baseweb="input"] > div > input { color: #FFFFFF !important; background-color: #1E232B !important; font-size: 16px !important; }
    div[data-baseweb="input"] > div > input::placeholder { color: #A0AAB5 !important; }
    
    /* Triage Button Styling */
    .stButton > button {
        background-color: #1E232B; color: #FAFAFA; border: 1px solid #4CAF50; border-radius: 8px;
        width: 100%; transition: 0.3s;
    }
    .stButton > button:hover { background-color: #4CAF50; color: white; }
    
    /* Mobile Fixes */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] { display: none; }
        h1 { font-size: 1.6rem !important; text-align: center; }
        .stChatMessage { padding: 10px !important; font-size: 0.95rem !important; margin-left: 5px !important; margin-right: 5px !important; }
        .stChatInput { position: fixed; bottom: 0; left: 0; right: 0; z-index: 999; padding: 10px; background-color: #0E1117; }
        .block-container { padding-bottom: 90px !important; padding-left: 10px !important; padding-right: 10px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# --- UNIQUE FEATURE: SMART TRIAGE & BODY MAP ---
LOGO_URL = "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?q=80&w=200&auto=format&fit=crop"

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are NEXORA, an advanced Medical AI Assistant. Always include a brief disclaimer that you are an AI, not a doctor. Keep answers informative, structured, and easy to understand."}
    ]

# Sidebar with Body Map
with st.sidebar:
    st.image(LOGO_URL, use_container_width=True) 
    st.markdown("### 🩺 NEXORA Medical AI")
    st.markdown("---")
    
    # BODY MAP
    st.markdown("#### 🧍 Quick Triage")
    st.caption("Click a body part to start a focused analysis.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Head"):
            st.session_state.triage_prompt = "I am experiencing a headache or head-related issue. Please ask me 3 follow-up questions to narrow down the cause."
        if st.button("🫁 Chest"):
            st.session_state.triage_prompt = "I am experiencing chest pain or breathing issues. Please ask me 3 follow-up questions to narrow down the cause."
        if st.button("🦵 Legs"):
            st.session_state.triage_prompt = "I am experiencing leg pain or mobility issues. Please ask me 3 follow-up questions to narrow down the cause."
    with col2:
        if st.button("🤢 Stomach"):
            st.session_state.triage_prompt = "I am experiencing stomach pain or digestive issues. Please ask me 3 follow-up questions to narrow down the cause."
        if st.button("🦴 Back"):
            st.session_state.triage_prompt = "I am experiencing back pain. Please ask me 3 follow-up questions to narrow down the cause."
        if st.button("🩸 Skin"):
            st.session_state.triage_prompt = "I am experiencing a skin rash or issue. Please ask me 3 follow-up questions to narrow down the cause."

    st.markdown("---")
    st.markdown("### ⚠️ Disclaimer")
    st.caption("NEXORA is an AI assistant, not a doctor. Always consult a qualified healthcare professional.")
    st.markdown("---")
    
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": "You are NEXORA, an advanced Medical AI Assistant. Always include a brief disclaimer that you are an AI, not a doctor. Keep answers informative, structured, and easy to understand."}
        ]
        st.rerun()

# --- MAIN CHAT UI ---
st.image(LOGO_URL, width=120) 
st.title("🩺 NEXORA Medical AI")
st.write("Welcome! Ask me anything about symptoms, treatments, or general health.")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API Key missing. Please check your .env file or Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- HANDLE TRIAGE PROMPT ---
if "triage_prompt" in st.session_state:
    prompt = st.session_state.triage_prompt
    del st.session_state.triage_prompt # Clear it so it only fires once
else:
    prompt = st.chat_input("Describe your symptoms or ask a medical question...")

# Accept input
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message("user", prompt)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing medical data..."):
            try:
                response = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model="openai/gpt-oss-120b",
                    temperature=0.3,
                    max_tokens=800
                )
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
                
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                save_message("assistant", ai_response)
            except Exception as e:
                st.error(f"API Error: {e}")
    st.rerun()
