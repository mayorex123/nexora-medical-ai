import streamlit as st
import os
import base64
from groq import Groq
from dotenv import load_dotenv
from nexora.memory.history import save_message

# Load environment variables
load_dotenv()

st.set_page_config(page_title="NEXORA Medical AI", page_icon="🩺", layout="wide")

# --- UNIVERSAL CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stChatMessage { background-color: #1E232B; border-radius: 12px; padding: 15px; margin-bottom: 10px; width: 100% !important; box-sizing: border-box !important; overflow-wrap: break-word !important; }
    .stChatMessage p, .stChatMessage li, .stChatMessage span, .stChatMessage strong, .stChatMessage table, .stChatMessage th, .stChatMessage td { color: #FAFAFA !important; font-size: 1rem; }
    [data-testid="stSidebar"] { background-color: #161B22; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* FIX ANDROID CHAT INPUT TEXT VISIBILITY */
    div[data-baseweb="input"] > div > input { 
        color: #FFFFFF !important; 
        background-color: #1E232B !important; 
        font-size: 16px !important; 
    }
    div[data-baseweb="input"] > div > input::placeholder { color: #A0AAB5 !important; }
    /* Force chat input text area to be visible on all devices */
    textarea[data-testid="stChatInputTextArea"] {
        color: #FFFFFF !important;
    }
    
    .stButton > button { background-color: #1E232B; color: #FAFAFA; border: 1px solid #4CAF50; border-radius: 8px; width: 100%; transition: 0.3s; }
    .stButton > button:hover { background-color: #4CAF50; color: white; }
    
    @media (max-width: 768px) {
        [data-testid="stSidebar"] { display: none; }
        h1 { font-size: 1.6rem !important; text-align: center; }
        .stChatMessage { padding: 10px !important; font-size: 0.95rem !important; margin-left: 5px !important; margin-right: 5px !important; }
        .block-container { padding-bottom: 120px !important; padding-left: 10px !important; padding-right: 10px !important; }
        div[data-testid="stStatusWidget"] { display: none; }
    }
    </style>
""", unsafe_allow_html=True)

LOGO_URL = "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?q=80&w=200&auto=format&fit=crop"

SYSTEM_PROMPT = """You are NEXORA, an expert Medical AI Assistant acting like a real doctor.
CRITICAL RULES:
1. NEVER give a diagnosis or a list/table of possibilities immediately. 
2. When a user mentions a symptom, you MUST ask 1 to 2 follow-up questions first.
3. Keep responses conversational, warm, and brief. Do not use tables unless absolutely necessary.
4. If the user uploads an image, analyze it carefully and ask follow-up questions about what you see.
5. Always include a brief disclaimer that you are an AI, not a doctor."""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

with st.sidebar:
    st.image(LOGO_URL, use_container_width=True) 
    st.markdown("### 🩺 NEXORA Medical AI")
    st.markdown("---")
    st.markdown("#### 🧍 Quick Triage")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Head"): st.session_state.triage_prompt = "I am experiencing a headache or head-related issue."
        if st.button("🫁 Chest"): st.session_state.triage_prompt = "I am experiencing chest pain or breathing issues."
        if st.button("🦵 Legs"): st.session_state.triage_prompt = "I am experiencing leg pain or mobility issues."
    with col2:
        if st.button("🤢 Stomach"): st.session_state.triage_prompt = "I am experiencing stomach pain or digestive issues."
        if st.button("🦴 Back"): st.session_state.triage_prompt = "I am experiencing back pain."
        if st.button("🩸 Skin"): st.session_state.triage_prompt = "I am experiencing a skin rash or issue."
    st.markdown("---")
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

st.image(LOGO_URL, width=120) 
st.title("🩺 NEXORA Medical AI")
st.write("Welcome! Describe your symptoms, upload an image, or use voice input.")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API Key missing.")
    st.stop()

client = Groq(api_key=api_key)

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "image" in msg:
                st.image(msg["image"], width=300)

# --- MULTIMODAL INPUT (Files + Voice inside Chat Box) ---
# Using Streamlit's native accept_file puts the upload icon INSIDE the chat box
chat_input = st.chat_input(
    "Describe your symptoms...", 
    accept_file=True, 
    file_type=["jpg", "jpeg", "png"]
)

# Voice button as a tiny icon beside the chat input
col1, col2 = st.columns([0.9, 0.1])
with col2:
    # Tiny microphone button (uses browser speech recognition)
    voice_js = """
    <button onclick="startVoice()" style="background:transparent;border:none;font-size:20px;cursor:pointer;" title="Voice Input">🎤</button>
    <script>
    function startVoice() {
        if (window.hasOwnProperty('webkitSpeechRecognition')) {
            var rec = new webkitSpeechRecognition();
            rec.continuous = false;
            rec.interimResults = false;
            rec.lang = "en-US";
            rec.start();
            rec.onresult = function(e) {
                const text = e.results[0][0].transcript;
                // Find the chat textarea and inject text
                const ta = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
                if (ta) {
                    ta.value = text;
                    ta.dispatchEvent(new Event('input', { bubbles: true }));
                }
            };
        }
    }
    </script>
    """
    st.components.v1.html(voice_js, height=40)

# --- HANDLE INPUT ---
if chat_input or "triage_prompt" in st.session_state:
    # Determine the prompt source
    if "triage_prompt" in st.session_state:
        prompt_text = st.session_state.triage_prompt
        del st.session_state.triage_prompt
        uploaded_file = None
    else:
        prompt_text = chat_input.text if chat_input else ""
        uploaded_file = chat_input.files[0] if chat_input and chat_input.files else None

    user_content = prompt_text if prompt_text else "I have uploaded a medical image. Please analyze it."
    
    # Process image
    image_data_uri = None
    if uploaded_file:
        base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
        image_data_uri = f"data:image/jpeg;base64,{base64_image}"

    user_msg = {"role": "user", "content": user_content}
    if image_data_uri:
        user_msg["image"] = image_data_uri
        
    st.session_state.messages.append(user_msg)
    save_message("user", user_content)
    
    with st.chat_message("user"):
        st.markdown(user_content)
        if image_data_uri:
            st.image(image_data_uri, width=300)

    with st.chat_message("assistant"):
        with st.spinner("Doctor is analyzing..."):
            try:
                api_messages = []
                for m in st.session_state.messages:
                    if m["role"] == "system":
                        api_messages.append(m)
                    elif "image" in m:
                        api_messages.append({
                            "role": m["role"],
                            "content": [
                                {"type": "text", "text": m["content"]},
                                {"type": "image_url", "image_url": {"url": m["image"]}}
                            ]
                        })
                    else:
                        api_messages.append(m)

                # WORKING VISION MODEL (replaces the decommissioned one)
                response = client.chat.completions.create(
                    messages=api_messages,
                    model="qwen/qwen3.6-27b", # Current multimodal model on Groq [citation:2]
                    temperature=0.4,
                    max_tokens=600
                )
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
                
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                save_message("assistant", ai_response)
            except Exception as e:
                st.error(f"API Error: {e}")
    st.rerun()
