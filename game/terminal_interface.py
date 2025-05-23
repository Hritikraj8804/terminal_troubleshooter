# game/terminal_interface.py
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule # Import Rule for section headers
import os
import time

# Import our ASCII art
from .data.ascii_art import WELCOME_BANNER

console = Console()

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome_message():
    """Prints a styled welcome message with ASCII banner."""
    clear_screen()
    # Centering the ASCII banner
    console.print(Text(WELCOME_BANNER, style="bold cyan"), justify="center")

    # Creating the Panel with the centered text inside
    # The 'justify' argument is applied to the Text object here, not the Panel
    welcome_panel_content = Text("Welcome to Terminal Troubleshooter!", style="bold green", justify="center")
    console.print(Panel(welcome_panel_content, title="System Status"), style="cyan", justify="center") # Added justify="center" here for the Panel itself
    console.print("\n" * 2) # Add some space

def print_scenario(title: str, description: str):
    """Prints a scenario description in a styled panel."""
    clear_screen()
    console.print(Panel(Text(description, style="italic"), title=title, border_style="yellow"))
    console.print("\n")

def get_user_input(prompt: str = "$ ") -> str:
    """Gets command input from the user with a styled prompt."""
    return console.input(f"[bold green]{prompt}[/bold green]").strip()

def print_message(message: str, style: str = "white", delay: float = 0.02):
    """Prints a message character by character for a typing effect."""
    for char in message:
        console.print(Text(char, style=style), end="")
        time.sleep(delay)
    console.print("") # Newline at the end

def print_error(message: str):
    """Prints an error message."""
    print_message(f"ERROR: {message}", style="bold red")

def print_success(message: str):
    """Prints a success message."""
    print_message(f"SUCCESS: {message}", style="bold green")

def print_info(message: str):
    """Prints an informational message."""
    print_message(message, style="blue")

def print_section_header(header: str):
    """Prints a styled section header using Rule."""
    console.rule(f"[bold magenta]{header}[/bold magenta]")
    console.print("\n")

# This __main__ block is for testing this specific module in isolation.
# It won't run when imported by main.py
if __name__ == "__main__":
    print_welcome_message()
    time.sleep(1)
    print_message("Initializing systems...", style="dim white")
    time.sleep(1.5)
    print_scenario("Critical Alert: Web Server Down!", "The main corporate website is completely unreachable. Customers are complaining! You need to identify the issue and bring it back online. Start by checking the running processes.")
    command = get_user_input("sysadmin@server:~$ ")
    print_info(f"You entered: {command}")
    if "ps aux" in command:
        print_success("Good start! Now you need to find the specific web server process.")
    else:
        print_error("That's not helping. Try a command to list all running processes.")
    time.sleep(2)
    print_message("Exiting example.", style="dim")
    clear_screen()