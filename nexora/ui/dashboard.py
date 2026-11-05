import json
import http.server
import socketserver
from pathlib import Path
from nexora.memory.history import get_history

PORT = 8000

def generate_html():
    history = get_history()
    
    # Build the chat bubbles
    chat_html = ""
    for msg in history:
        if msg["role"] == "user":
            chat_html += f"<div class='message user'><b>You:</b> {msg['content']}</div>"
        elif msg["role"] == "assistant":
            chat_html += f"<div class='message ai'><b>NEXORA:</b> {msg['content']}</div>"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NEXORA Medical AI</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #e0e0e0; padding: 20px; max-width: 800px; margin: auto; }}
            h1 {{ color: #4CAF50; text-align: center; }}
            .chat-container {{ background-color: #1e1e1e; border-radius: 10px; padding: 20px; height: 600px; overflow-y: scroll; margin-bottom: 20px; }}
            .message {{ padding: 12px; margin-bottom: 15px; border-radius: 8px; line-height: 1.5; }}
            .user {{ background-color: #2c3e50; align-self: flex-end; }}
            .ai {{ background-color: #27ae60; color: white; }}
            .footer {{ text-align: center; color: #777; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <h1>🩺 NEXORA Medical AI Dashboard</h1>
        <div class="chat-container">
            {chat_html if chat_html else "<p style='text-align:center;'>No chat history yet. Go to your terminal and type 'nexora chat' to start.</p>"}
        </div>
        <div class="footer">Viewing local chat history. To chat, use the terminal.</div>
    </body>
    </html>
    """
    return html

class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(generate_html().encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_dashboard():
    with socketserver.TCPServer(("127.0.0.1", PORT), DashboardHandler) as httpd:
        print(f"[*] Dashboard running at http://127.0.0.1:{PORT}")
        print("[*] Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Shutting down dashboard.")
