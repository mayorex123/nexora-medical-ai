import webview
import subprocess
import time
import os

# 1. Start Streamlit in the background
print("Starting NEXORA engine...")
process = subprocess.Popen(
    ["streamlit", "run", "nexora_web.py", "--server.headless=true", "--server.port=8501"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# 2. Wait for the server to spin up
time.sleep(3)

# 3. Open the Desktop Window
print("Opening NEXORA Desktop App...")
webview.create_window("NEXORA Medical AI", "http://localhost:8501", width=900, height=700)
webview.start()

# 4. Clean up when the window is closed
process.terminate()
print("App closed.")
