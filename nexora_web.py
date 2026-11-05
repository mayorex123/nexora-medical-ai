import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from nexora.memory.history import save_message

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="NEXORA Medical AI", page_icon="🩺", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #e0e0e0; }
    .stChatMessage { background-color: #1e1e1e; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 NEXORA Medical AI")
st.write("Your personal, professional AI health assistant.")

# Initialize the Groq Client securely
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API Key missing. Please check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are NEXORA, an advanced Medical AI Assistant. Always include a brief disclaimer that you are an AI, not a doctor."}
    ]

# Display past messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Accept user input
if prompt := st.chat_input("Ask a medical question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message("user", prompt)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("NEXORA is thinking..."):
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
