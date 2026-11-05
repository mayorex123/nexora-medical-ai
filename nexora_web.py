import streamlit as st
import os
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from groq import Groq
from dotenv import load_dotenv
from nexora.memory.history import save_message

# Load environment variables
load_dotenv()

# Set page config with a custom icon and title
st.set_page_config(page_title="NEXORA Medical AI", page_icon="🩺", layout="wide")

# Custom Premium CSS
st.markdown("""
    <style>
    /* Main background */
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    /* Chat message styling */
    .stChatMessage { background-color: #1E232B; border-radius: 12px; padding: 15px; margin-bottom: 10px; }
    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #161B22; }
    /* Hide the default Streamlit header */
    header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION SETUP ---
if not os.path.exists('config.yaml'):
    # Use the new hash_list method
    hashed_passwords = stauth.Hasher.hash_list(['nexora123'])
    config = {
        'credentials': {'usernames': {'demo_user': {'email': 'demo@example.com', 'name': 'Demo User', 'password': hashed_passwords[0]}}},
        'cookie': {'expiry_days': 30, 'key': 'nexora_secret_key', 'name': 'nexora_cookie'}
    }
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# --- LANDING PAGE & LOGIN ---
if st.session_state.get("authentication_status") is not True:
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🩺 NEXORA Medical AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em;'>Your personal, professional AI health assistant.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.info("🔒 **Secure Login Required**")
        authenticator.login()
    
    if st.session_state.get("authentication_status") is False:
        st.error('Username/password is incorrect')
    elif st.session_state.get("authentication_status") is None:
        st.warning('Please enter your username and password to access the AI.')
        
    st.markdown("<br><br><p style='text-align: center; color: gray;'>Demo Login: username: <b>demo_user</b> | password: <b>nexora123</b></p>", unsafe_allow_html=True)
    st.stop()

# --- MAIN APP (Only visible if logged in) ---
with st.sidebar:
    st.markdown(f"### Welcome, {st.session_state['name']} 👋")
    st.markdown("---")
    st.markdown("### ⚠️ Medical Disclaimer")
    st.caption("NEXORA is an AI assistant, not a doctor. Always consult a qualified healthcare professional for medical advice.")
    st.markdown("---")
    authenticator.logout('Logout', 'sidebar')

st.title("🩺 NEXORA Medical AI")
st.write("Ask me anything about symptoms, treatments, or general health.")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API Key missing. Please check your .env file or Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are NEXORA, an advanced Medical AI Assistant. Always include a brief disclaimer that you are an AI, not a doctor. Keep answers informative, structured, and easy to understand."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

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
