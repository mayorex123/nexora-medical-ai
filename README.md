# 🩺 NEXORA Medical AI

NEXORA is a professional, AI-powered medical assistant. It features a beautiful Streamlit web interface and a standalone desktop application, powered by Groq's ultra-fast Llama models.

## Features
- **Intelligent Medical Q&A:** Powered by Llama-3.3-70B for highly accurate, complex medical reasoning.
- **Professional Web UI:** A sleek, dark-mode chat interface.
- **Desktop App:** A standalone window wrapper using PyWebview.
- **Local Chat History:** All conversations are saved locally to `data/chat_history.jsonl`.

## Installation
1. Clone the repository and enter the directory:
   cd ~/nexora-ai

2. Activate the virtual environment:
   source .venv/bin/activate

3. Install dependencies:
   pip install groq streamlit pywebview python-dotenv

4. Add your Groq API key to a `.env` file:
   echo "GROQ_API_KEY=your_api_key_here" > .env

## Usage
**Run the Web App (Browser):**
streamlit run nexora_web.py

**Run the Desktop App (Standalone Window):**
export PYWEBVIEW_GUI=qt
python launch_app.py

## Disclaimer
NEXORA is an AI assistant, not a doctor. Always consult a qualified healthcare professional for medical advice.x# NEXORA AI

NEXORA AI is a lightweight, local-first defensive cybersecurity xe repo and navigate to it:
   cd ~/nexora-ai
2. Activate the virtual environment:
   source .venv/bin/activate
3. Install the package:
   pip install -e .

## Usage
- `nexora ingest <logfile>`: Parse a log file into memory.
- `nexora detect`: Run all detection rules.
- `nexora monitor <logfile>`: Continuously watch a log for new threats.
- `nexora explain <rule_name>`: Ask the local AI to explain a finding.
- `nexora dashboard`: Start the local web UI.
- `nexora respond <ip>`: Block a malicious IP (requires human confirmation).
