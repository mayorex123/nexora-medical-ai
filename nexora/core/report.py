from pathlib import Path
from datetime import datetime
from rich.console import Console
from nexora.detect.rules import run_all_rules
from nexora.memory.store import BASE_DIR

console = Console()

def generate_report():
    """Generates a standalone HTML incident report."""
    findings = run_all_rules()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_path = BASE_DIR / "report.html"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NEXORA Incident Report - {timestamp}</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f4f4f9; color: #333; padding: 20px; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .meta {{ color: #7f8c8d; font-size: 0.9em; margin-bottom: 20px; }}
            .finding {{ background: white; border-left: 5px solid #e74c3c; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .finding h3 {{ margin-top: 0; color: #c0392b; }}
            .safe {{ border-left: 5px solid #2ecc71; }}
            .safe h3 {{ color: #27ae60; }}
            pre {{ background: #ecf0f1; padding: 10px; border-radius: 4px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <h1>🛡️ NEXORA AI Incident Report</h1>
        <div class="meta">Generated: {timestamp} | Host: Local Kali Machine</div>
    """

    if not findings:
        html += """
        <div class="finding safe">
            <h3>✅ No Active Threats Detected</h3>
            <p>The current case memory does not contain any events that trigger the NEXORA detection rules.</p>
        </div>
        """
    else:
        html += f"<h2>🚨 Active Detections ({len(findings)})</h2>"
        for f in findings:
            html += f"""
            <div class="finding">
                <h3>Rule: {f['rule'].replace('_', ' ').title()}</h3>
                <p><strong>Target IP:</strong> {f['ip']}</p>
                <p><strong>Users Involved:</strong> {', '.join(f['users_targeted'])}</p>
                <p><strong>Explanation:</strong> {f['explanation']}</p>
            </div>
            """

    html += "</body></html>"

    with open(report_path, "w") as f:
        f.write(html)
        
    console.print(f"[bold green]📄 Report generated successfully![/]")
    console.print(f"[cyan]Location:[/] {report_path}")
