import time
import os
from pathlib import Path
from nexora.ingest.parser import parse_auth_log
from nexora.memory.store import save_events
from rich.console import Console

console = Console()

def tail_log(filepath: str):
    path = Path(filepath)
    if not path.exists():
        console.print(f"[red]Error:[/] Log file not found: {filepath}")
        return

    console.print(f"[bold green]📡 Monitoring started:[/] {filepath}")
    console.print("[dim]Waiting for new lines... Press Ctrl+C to stop.[/]")

    # Open the file and move to the end
    f = open(path, 'r', errors='ignore')
    f.seek(0, os.SEEK_END)
    
    try:
        while True:
            # Read the next line
            line = f.readline()
            
            if not line:
                # No new data, wait a moment and try again
                time.sleep(0.2)
                continue
            
            # If we got a line, show it!
            console.print(f"[dim]Read: {line.strip()}[/]")
            
            # Save to a temp file so the parser can read it
            temp_path = Path("data/temp_tail.log")
            temp_path.parent.mkdir(exist_ok=True)
            with open(temp_path, 'w') as temp:
                temp.write(line)
            
            # Parse the temp file
            events = list(parse_auth_log(str(temp_path)))
            if events:
                saved = save_events(events)
                console.print(f"[bold green]⚡ New event captured![/] Saved {saved} to memory.")
            else:
                console.print("[yellow]Line did not match any detection rules.[/]")
                
    except KeyboardInterrupt:
        console.print("\n[bold red]Monitor stopped.[/]")
    finally:
        f.close()
