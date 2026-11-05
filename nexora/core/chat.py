import os
from groq import Groq
from rich.console import Console
from rich.prompt import Prompt
from nexora.memory.history import save_message

console = Console()

def start_chat():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        console.print("[red]Error:[/] Please set your Groq API key.")
        return

    client = Groq(api_key=api_key)

    console.print("[bold green]🩺 Welcome to NEXORA Medical AI![/]")
    console.print("[dim]Your conversation is saved locally. Type 'exit' to leave.[/]\n")

    system_prompt = """You are NEXORA, an advanced Medical AI Assistant. 
You answer complex medical questions, explain symptoms, and discuss general treatments. 
CRITICAL RULES:
1. Always include a brief disclaimer that you are an AI, not a doctor.
2. Keep answers informative, structured, and easy to understand.
3. Do not prescribe specific drug dosages."""

    history = [{"role": "system", "content": system_prompt}]

    while True:
        user_input = Prompt.ask("[bold cyan]You[/]")
        
        if user_input.lower() in ['exit', 'quit']:
            console.print("[yellow]Goodbye![/]")
            break

        history.append({"role": "user", "content": user_input})
        save_message("user", user_input) # Save user message

        console.print("[bold magenta]NEXORA[/] ", end="")
        
        try:
            stream = client.chat.completions.create(
                messages=history,
                model="openai/gpt-oss-120b",
                temperature=0.3,
                max_tokens=800,
                stream=True
            )
            
            response_text = ""
            for chunk in stream:
                text_piece = chunk.choices[0].delta.content or ""
                console.print(text_piece, end="", highlight=False)
                response_text += text_piece

            console.print("\n")
            history.append({"role": "assistant", "content": response_text})
            save_message("assistant", response_text) # Save AI message

            if len(history) > 10:
                history = [history[0]] + history[-6:]

        except Exception as e:
            console.print(f"\n[red]API Error:[/] {e}")
            history.pop()
