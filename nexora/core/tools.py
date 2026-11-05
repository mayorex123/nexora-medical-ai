from nexora.detect.rules import run_all_rules
from nexora.core.response import block_ip
from nexora.core.report import generate_report
from rich.console import Console

console = Console()

def get_active_threats():
    """Returns a list of current active threats."""
    findings = run_all_rules()
    if not findings:
        return "No active threats found in memory."
    
    result = []
    for f in findings:
        result.append(f"Rule: {f['rule']} | IP: {f['ip']} | Users: {', '.join(f['users_targeted'])}")
    return "\n".join(result)

def tool_block_ip(ip: str):
    """Blocks a specific IP address. (Requires human approval)."""
    console.print(f"\n[dim]⚡ [Tool executing: Proposing block for {ip}][/]")
    return str(block_ip(ip))

def tool_generate_report():
    """Generates an HTML incident report."""
    console.print(f"\n[dim]⚡ [Tool executing: Generating HTML Report][/]")
    generate_report()
    return "Report generated successfully in the project folder."
