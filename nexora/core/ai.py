import os
from groq import Groq
from dotenv import load_dotenv
from rich.console import Console

console = Console()

# Load the key from the .env file instead of hardcoding it
load_dotenv()

def generate_summary(explanation: str, ip: str, users: list):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""You are a helpful Medical AI Assistant. 
Summarize the following symptom report and suggest a general next step. 
Keep it brief and include a disclaimer that you are not a doctor.
Report: {explanation}"""

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
            temperature=0.3,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API Error: {e}"
