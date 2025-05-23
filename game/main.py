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
            terminal_interface.print_error("Error: Could not load current level data.")
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
            is_correct, feedback_data = level_manager.validate_command(user_command)

            if is_correct:
                terminal_interface.print_success(feedback_data["message"])
                
                # Print simulated output for the command if available
                simulated_output = level_manager.get_simulated_output(user_command)
                if simulated_output:
                    terminal_interface.print_info("Simulated output:")
                    terminal_interface.console.print(simulated_output, style="dim cyan") # Print raw simulated output
                
                # Apply state changes (like process status, file deletions, etc.)
                level_manager.apply_success_state_changes(feedback_data)
                
                task_solved = True # Current step is solved
                terminal_interface.print_message(f"Current XP: {game_state.player_xp}", style="bold yellow")
                time.sleep(2) # Give user time to read success message
                break # Exit current command loop, proceed to next step or level
            else:
                attempts += 1
                terminal_interface.print_error(f"Command '{user_command}' is not correct for this task. ({max_attempts_per_step - attempts} attempts left)")
                if feedback_data.get("type") == "hint":
                    terminal_interface.print_info(feedback_data["message"])
                time.sleep(1)

        if not task_solved:
            terminal_interface.print_error("You ran out of attempts for this task. Game Over!")
            terminal_interface.print_info("Consider reviewing the hint for the task.")
            # For a real game, you'd end here or restart the level.
            # For demo, let's just break out of the main loop.
            break

        # Advance to the next level if the current task was solved
        if task_solved:
            # We're simplifying to one step per level for now.
            # In a full game, you'd have a mechanism to check if all steps in a level are done.
            if not level_manager.advance_level():
                terminal_interface.print_success("Congratulations! You've completed all available levels!")
                break # All levels done

    terminal_interface.print_section_header("Game Over")
    terminal_interface.print_message(f"Final XP: {game_state.player_xp}", style="bold yellow")
    terminal_interface.print_message("Thanks for playing Terminal Troubleshooter!", style="dim white")
    time.sleep(3)
    terminal_interface.clear_screen()

if __name__ == "__main__":
    game_loop()