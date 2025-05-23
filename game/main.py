# main.py
from . import terminal_interface # The dot means "from the current package"
import time

def game_loop():
    """Main game loop."""
    terminal_interface.print_welcome_message()
    terminal_interface.print_message("Press Enter to start your sysadmin journey...", style="dim white")
    terminal_interface.get_user_input("") # Wait for user to press Enter

    # --- Level 1: Web Server Down ---
    terminal_interface.print_scenario(
        "Urgent: Web Server Down!",
        "The corporate website is completely unreachable. Customers are furious! "
        "Your first task is to identify the web server process and restart it. "
        "Start by listing all running processes to find potential issues."
    )

    correct_command_found = False
    max_attempts = 3
    attempts = 0

    while not correct_command_found and attempts < max_attempts:
        user_command = terminal_interface.get_user_input("sysadmin@server:~$ ")

        if user_command.strip().lower() == "ps aux":
            terminal_interface.print_success("You ran 'ps aux'. Excellent! Now, simulate finding the web server process PID.")
            terminal_interface.print_info("Simulated output:")
            terminal_interface.print_message("USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND", style="dim cyan")
            terminal_interface.print_message("root         1  0.0  0.1 106708  6908 ?        Ss   May20   0:01 /sbin/init", style="dim white")
            terminal_interface.print_message("sysadmin  1234  0.5  2.0 200000 150000 ?       S    10:30   0:05 /usr/sbin/apache2 -k start", style="yellow") # The target!
            terminal_interface.print_message("root      5678  0.0  0.1  25000  1200 ?        S    May20   0:00 /usr/bin/python3 /opt/monitoring/monitor.py", style="dim white")
            terminal_interface.print_info("\nIt seems the apache2 process (PID 1234) is the web server. Now, restart it.")
            correct_command_found = True
        else:
            attempts += 1
            terminal_interface.print_error(f"Command '{user_command}' is not helping. Try again. ({max_attempts - attempts} attempts left)")
            time.sleep(1)

    if correct_command_found:
        # Now, the next step in the task: restarting the service
        terminal_interface.print_scenario(
            "Task Part 2: Restart the Web Server",
            "You've identified the Apache web server process with PID 1234. Now, restart the Apache service."
        )
        restart_successful = False
        attempts = 0
        while not restart_successful and attempts < max_attempts:
            user_command = terminal_interface.get_user_input("sysadmin@server:~$ ")
            if user_command.strip().lower() in ["sudo systemctl restart apache2", "systemctl restart apache2"]:
                terminal_interface.print_success("Service 'apache2' restarted successfully! The website is back online!")
                terminal_interface.print_message("You earned 50 XP!", style="bold yellow")
                restart_successful = True
            else:
                attempts += 1
                terminal_interface.print_error(f"That command didn't restart Apache. Try again. ({max_attempts - attempts} attempts left)")
                time.sleep(1)
        
        if not restart_successful:
            terminal_interface.print_error("You failed to restart the web server. Game Over!")
            terminal_interface.print_info("Hint: Try 'systemctl restart apache2' or 'sudo systemctl restart apache2'.")
    else:
        terminal_interface.print_error("You ran out of attempts. The web server remains down. Game Over!")
        terminal_interface.print_info("Hint: The first step was 'ps aux'.")

    terminal_interface.print_section_header("Game Over / Demo End")
    terminal_interface.print_message("Thanks for playing Terminal Troubleshooter!", style="dim white")
    time.sleep(3)
    terminal_interface.clear_screen()

if __name__ == "__main__":
    game_loop()