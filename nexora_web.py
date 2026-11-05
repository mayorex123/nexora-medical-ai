import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from nexora.memory.history import save_message

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="NEXORA Medical AI", page_icon="🩺", layout="wide")

# Custom Premium CSS
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stChatMessage { background-color: #1E232B; border-radius: 12px; padding: 15px; margin-bottom: 10px; }
    [data-testid="stSidebar"] { background-color: #161B22; }
    header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are NEXORA, an advanced Medical AI Assistant. Always include a brief disclaimer that you are an AI, not a doctor. Keep answers informative, structured, and easy to understand."}
    ]

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🩺 NEXORA Medical AI")
    st.markdown("---")
    st.markdown("### ⚠️ Medical Disclaimer")
    st.caption("NEXORA is an AI assistant, not a doctor. Always consult a qualified healthcare professional for medical advice.")
    st.markdown("---")
    
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": "You are NEXORA, an advanced Medical AI Assistant. Always include a brief disclaimer that you are an AI, not a doctor. Keep answers informative, structured, and easy to understand."}
        ]
        st.rerun()

# --- MAIN CHAT UI ---
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

# Accept input
if prompt := st.chat_input("Describe your symptoms or ask a medical question..."):
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
