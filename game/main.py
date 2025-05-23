# game/main.py
from . import terminal_interface
from .game_state import GameState
from .level_manager import LevelManager
import time

def game_loop():
    """Main game loop for Terminal Troubleshooter."""
    game_state = GameState()
    level_manager = LevelManager(game_state)

    terminal_interface.print_welcome_message()
    terminal_interface.print_message("Press Enter to start your sysadmin journey...", style="dim white")
    terminal_interface.get_user_input("") # Wait for user to press Enter

    while not level_manager.is_game_over():
        current_level_data = level_manager.get_current_level_data()
        if not current_level_data:
            terminal_interface.print_error("Error: Could not load current level data. Exiting.")
            break

        terminal_interface.print_scenario(
            f"Level {level_manager.current_level_index + 1}: {current_level_data['title']}",
            current_level_data['description']
        )
        terminal_interface.print_info(current_level_data["steps"][0]["task"]) # Display current task

        task_solved = False
        max_attempts_per_step = 5 # Give more attempts per specific command
        attempts = 0

        while not task_solved and attempts < max_attempts_per_step:
            user_command = terminal_interface.get_user_input("sysadmin@server:~$ ")

            # Validate the command using the LevelManager
            # feedback_data now contains 'output', 'message', 'type', and potentially 'simulated_output_from_parser'
            is_correct, feedback_data = level_manager.validate_command(user_command)

            # Display the output from the simulated command execution first
            if feedback_data.get("output"):
                terminal_interface.print_info("Simulated output:")
                terminal_interface.console.print(feedback_data["output"], style="dim white") # Print raw simulated output
                time.sleep(0.5) # Short pause to read output

            if is_correct:
                terminal_interface.print_success(feedback_data["message"])
                
                # Apply state changes (like process status, file deletions, etc.)
                level_manager.apply_success_state_changes(feedback_data)
                
                task_solved = True # Current step is solved
                terminal_interface.print_message(f"Current XP: {game_state.player_xp}", style="bold yellow")
                time.sleep(2) # Give user time to read success message
                # No break here, allow loop to complete and then move to next level
            else:
                attempts += 1
                error_message = feedback_data.get("message", "That's not the right command for this task. Try again.")
                terminal_interface.print_error(f"{error_message} ({max_attempts_per_step - attempts} attempts left)")
                # If the feedback_data has a 'type' of 'hint', it means the command was valid but not the one for the task
                if feedback_data.get("type") == "hint":
                    pass # Message is already a hint, no need to add "Try again" if it's specific
                time.sleep(1)

        if not task_solved:
            terminal_interface.print_error("You ran out of attempts for this task. Game Over!")
            terminal_interface.print_info("Consider reviewing the task description and hint.")
            break # Game over if task not solved

        # Advance to the next level if the current task was solved
        if task_solved:
            # We're simplifying to one step per level for now.
            # In a full game, you'd have a mechanism to check if all steps in a level are done.
            if not level_manager.advance_level():
                terminal_interface.print_success("Congratulations! You've completed all available levels!")
                break # All levels done

    terminal_interface.print_section_header("Game Over / End Demo")
    terminal_interface.print_message(f"Final XP: {game_state.player_xp}", style="bold yellow")
    terminal_interface.print_message("Thanks for playing Terminal Troubleshooter!", style="dim white")
    time.sleep(3)
    terminal_interface.clear_screen()

if __name__ == "__main__":
    game_loop()