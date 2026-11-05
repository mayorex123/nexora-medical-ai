import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from nexora.memory.history import save_message

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="NEXORA Medical AI", page_icon="🩺", layout="wide")

# --- UNIVERSAL CUSTOM CSS (Desktop & Mobile) ---
st.markdown("""
    <style>
    /* 1. Main background & text color */
    .stApp { 
        background-color: #0E1117; 
        color: #FAFAFA; 
    }
    
    /* 2. Chat message bubbles */
    .stChatMessage { 
        background-color: #1E232B; 
        border-radius: 12px; 
        padding: 15px; 
        margin-bottom: 10px; 
    }
    
    /* 3. Force ALL text inside chat bubbles to be bright white (fixes dark tables) */
    .stChatMessage p, 
    .stChatMessage li, 
    .stChatMessage span, 
    .stChatMessage strong, 
    .stChatMessage table,
    .stChatMessage th,
    .stChatMessage td {
        color: #FAFAFA !important;
    }

    /* 4. Style tables to look professional */
    .stChatMessage table {
        border-collapse: collapse;
        width: 100%;
        margin-top: 10px;
    }
    .stChatMessage th, .stChatMessage td {
        border: 1px solid #444;
        padding: 8px;
        text-align: left;
    }
    .stChatMessage th {
        background-color: #2C3E50;
    }
    
    /* 5. Sidebar styling */
    [data-testid="stSidebar"] { 
        background-color: #161B22; 
    }
    
    /* 6. Hide the default Streamlit top header */
    header { 
        visibility: hidden; 
    }
    
    /* 7. MOBILE SPECIFIC FIXES */
    @media (max-width: 768px) {
        /* Hide the sidebar on mobile so the chat takes full width */
        [data-testid="stSidebar"] { 
            display: none; 
        }
        
        /* Make titles smaller on mobile */
        h1 { 
            font-size: 1.8rem !important; 
        }
        
        /* Fix the chat input box to stay at the bottom above the keyboard */
        .stChatInput { 
            position: fixed; 
            bottom: 0; 
            left: 0; 
            right: 0; 
            z-index: 999; 
            padding: 10px; 
            background-color: #0E1117; 
        }
        
        /* Add space at the bottom so the input doesn't hide the last message */
        .block-container { 
            padding-bottom: 90px !important; 
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are NEXORA, an advanced Medical AI Assistant. Always include a brief disclaimer that you are an AI, not a doctor. Keep answers informative, structured, and easy to understand."}
    ]

# --- SIDEBAR (Only visible on Desktop) ---
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
