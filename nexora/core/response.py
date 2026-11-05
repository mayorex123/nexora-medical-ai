import subprocess
import shutil
from rich.console import Console

console = Console()

def block_ip(ip: str):
    """
    Proposes and executes an iptables rule to block an IP.
    Requires sudo privileges to execute.
    """
    # 1. Check if iptables exists
    if not shutil.which("iptables"):
        console.print("[red]Error:[/] iptables is not installed on this system.")
        return False

    # 2. Construct the defensive command
    # We use INPUT to drop traffic from the malicious IP
    cmd = ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
    
    console.print(f"\n[bold yellow]Proposed Action:[/] Block IP {ip}")
    console.print(f"[dim]Command to run: {' '.join(cmd)}[/]")
    
    # 3. Human-in-the-loop approval
    confirm = console.input("[bold red]Do you approve this defensive action? (y/N): [/]")
    
    if confirm.lower() != 'y':
        console.print("[yellow]Action cancelled by user.[/]")
        return False

    # 4. Execute safely
    console.print(f"[cyan]Executing...[/]")
    try:
        # We use check=True to raise an error if iptables fails (e.g., wrong sudo password)
        subprocess.run(cmd, check=True)
        console.print(f"[bold green]Success:[/] Traffic from {ip} is now blocked.")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Failed to execute command.[/] Error: {e}")
        return False
