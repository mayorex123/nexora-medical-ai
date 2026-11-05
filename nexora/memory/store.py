import json
from pathlib import Path

# Anchor the data directory to the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
CASES_FILE = DATA_DIR / "cases.jsonl"

def save_events(events):
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    count = 0
    with open(CASES_FILE, 'a') as f:
        for event in events:
            event["type"] = event.get("type", "unknown")
            f.write(json.dumps(event) + "\n")
            count += 1
    return count
