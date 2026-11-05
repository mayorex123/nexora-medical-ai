import typer
from rich.console import Console
from nexora.ingest.parser import parse_auth_log
from nexora.memory.store import save_events
from nexora.detect.rules import run_all_rules
from nexora.ui.dashboard import run_dashboard
from nexora.core.response import block_ip
from nexora.core.ai import generate_summary
from nexora.core.monitor import tail_log
from nexora.core.report import generate_report
from nexora.core.chat import start_chat

app = typer.Typer(help="NEXORA AI — local-first defensive assistant")
console = Console()
VERSION = "0.1.0"

@app.command()
def version():
    console.print(f"[bold green]NEXORA AI v{VERSION}[/]")

@app.command()
def ingest(path: str = typer.Argument(...)):
    console.print(f"[cyan]Ingesting:[/] {path}")
    events = parse_auth_log(path)
    saved = save_events(events)
    console.print(f"[bold green]Success![/] Saved {saved} events.")

@app.command()
def detect():
    findings = run_all_rules()
    if not findings:
        console.print("[green]No threats detected.[/]")
        return
    for f in findings:
        console.print(f"\n[bold red]🚨 {f['rule'].upper()}[/]")
        console.print(f"[yellow]IP:[/] {f['ip']}")
        console.print(f"[bold]Explanation:[/] {f['explanation']}")

@app.command()
def dashboard():
    run_dashboard()

@app.command()
def respond(ip: str = typer.Argument(...)):
    block_ip(ip)

@app.command()
def explain(rule_name: str = typer.Argument(...)):
    findings = run_all_rules()
    target = next((f for f in findings if f['rule'] == rule_name), None)
    if not target:
        console.print(f"[yellow]No active threat found for rule {rule_name}.[/]")
        return
    summary = generate_summary(target['explanation'], target['ip'], target['users_targeted'])
    console.print(f"\n[bold magenta]🤖 NEXORA AI Analysis[/]")
    console.print(summary)

@app.command()
def monitor(path: str = typer.Argument(..., help="Log file to monitor")):
    tail_log(path)

@app.command()
def report(use_ai: bool = typer.Option(False, "--ai")):
    generate_report()
    if use_ai:
        findings = run_all_rules()
        if findings:
            summary_text = generate_summary(
                explanation=f"Multiple rules triggered. Examples: {findings[0]['explanation']}", 
                ip="Multiple", 
                users=["Multiple"]
            )
            console.print(f"\n[bold magenta]🤖 AI Executive Summary:[/]\n{summary_text}")

@app.command()
def chat():
    """Start an interactive conversation with NEXORA."""
    start_chat()

if __name__ == "__main__":
    app()
