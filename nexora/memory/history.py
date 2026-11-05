import json
from datetime import datetime
from pathlib import Path

# Save history in the data folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent
HISTORY_FILE = BASE_DIR / "data" / "chat_history.jsonl"

def save_message(role: str, content: str):
    """Saves a single chat message to the local JSONL file."""
    HISTORY_FILE.parent.mkdir(exist_ok=True, parents=True)
    
    record = {
        "timestamp": datetime.now().isoformat(),
        "role": role,
        "content": content
    }
    
    with open(HISTORY_FILE, 'a') as f:
        f.write(json.dumps(record) + "\n")

def get_history():
    """Returns a list of past messages."""
    if not HISTORY_FILE.exists():
        return []
    
    messages = []
    with open(HISTORY_FILE, 'r') as f:
        for line in f:
            try:
                messages.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return messages
