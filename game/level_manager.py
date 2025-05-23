# game/level_manager.py

from .game_state import GameState
from .data.levels import LEVELS
from .command_parser import CommandParser # Import the new parser
import re
from typing import Dict, Any # Add this line

class LevelManager:
    """
    Manages the game's levels, their progression, and validates user commands
    against the current level's requirements.
    """
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.level_parser = CommandParser(game_state) # Initialize CommandParser
        self.current_level_index = self._get_level_index_by_id(game_state.current_level_id)
        if self.current_level_index is None:
            raise ValueError(f"Starting level ID '{game_state.current_level_id}' not found in LEVELS.")

    def _get_level_index_by_id(self, level_id: str) -> int | None:
        """Helper to find level index by ID."""
        for i, level in enumerate(LEVELS):
            if level["id"] == level_id:
                return i
        return None

    def get_current_level_data(self) -> dict | None:
        """Returns the data for the current level."""
        if 0 <= self.current_level_index < len(LEVELS):
            return LEVELS[self.current_level_index]
        return None

    def advance_level(self) -> bool:
        """Advances the game to the next level."""
        self.current_level_index += 1
        if self.current_level_index < len(LEVELS):
            self.game_state.current_level_id = LEVELS[self.current_level_index]["id"]
            return True # Successfully advanced
        return False # No more levels

    def is_game_over(self) -> bool:
        """Checks if there are no more levels to play."""
        return self.current_level_index >= len(LEVELS)

    def validate_command(self, user_command: str) -> tuple[bool, Dict[str, Any]]:
        """
        Parses the user's command, executes it via CommandParser, and then
        validates the *result* against the current level's expected commands.
        Returns (is_correct, feedback_data)
        """
        current_level = self.get_current_level_data()
        if not current_level:
            return False, {"message": "No active level.", "type": "error", "output": ""}

        # Step 1: Parse and execute the command via our CommandParser
        parsed_result = self.level_parser.parse_and_execute(user_command)
        
        # We need to explicitly pass parsed_result's output to the game.
        # This allows us to use dynamic simulated output from the parser.
        output_from_parser = parsed_result.get("output", "")
        message_from_parser = parsed_result.get("message", "")
        
        # Step 2: Validate the result against the level's expected commands
        current_step = current_level["steps"][0] # Assuming one step per level for simplicity
        expected_commands = current_step["expected_commands"]
        
        is_level_command_match = False
        for exp_cmd_spec in expected_commands:
            target_cmd_parts = exp_cmd_spec["command"].strip().lower().split()
            target_cmd_name = target_cmd_parts[0]
            target_args_str = " ".join(target_cmd_parts[1:])

            # Check if the user's command matches one of the expected commands for THIS level
            # We check the raw user_command, not the parsed_result, to match specific commands
            # like "ps aux" or "systemctl restart apache2" as defined in levels.py
            user_cmd_lower = user_command.strip().lower()

            if exp_cmd_spec["check_type"] == "exact" and user_cmd_lower == exp_cmd_spec["command"].lower():
                is_level_command_match = True
                break
            elif exp_cmd_spec["check_type"] == "contains" and exp_cmd_spec["command"].lower() in user_cmd_lower:
                is_level_command_match = True
                break
            elif exp_cmd_spec["check_type"] == "regex" and re.search(exp_cmd_spec["command"], user_cmd_lower):
                is_level_command_match = True
                break

        # If the command executed successfully AND it was one of the commands expected by the level,
        # then consider it a level success.
        if parsed_result["success"] and is_level_command_match:
            success_data = current_step["on_success"].copy()
            # Override simulated_output with actual output from parser if parser produced it
            if output_from_parser:
                 success_data["simulated_output_from_parser"] = output_from_parser
            if message_from_parser:
                success_data["message"] = message_from_parser # Use parser's specific success message
            return True, success_data
        elif not parsed_result["success"]:
            # Command failed at the parser level
            return False, {"message": parsed_result.get("message", "Command failed."), "type": "error", "output": output_from_parser}
        else: # Command was executed, but not the one the level was looking for
            return False, {"message": current_step.get("hint_on_fail", "That's not the right command for this task. Try again."), "type": "hint", "output": output_from_parser}

    def apply_success_state_changes(self, success_data: dict):
        """Applies state changes to the game_state based on a successful command."""
        state_changes = success_data.get("state_changes", [])
        for change in state_changes:
            change_type = change["type"]
            if change_type == "process_state":
                self.game_state.update_process_state(change["pid"], change["new_state"])
            elif change_type == "docker_status":
                self.game_state.update_docker_container_status(change["container_id"], change["new_status"])
            elif change_type == "k8s_pod_status":
                self.game_state.update_kubernetes_pod_status(change["pod_name"], change["new_status"])
            elif change_type == "k8s_scale_deployment":
                self.game_state.scale_kubernetes_deployment(change["deployment_name"], change["replicas"])
            elif change_type == "add_dir":
                # Ensure parent path exists for mkdir simulation
                path_parts = [p for p in change["path"].strip('/').split('/') if p]
                parent_path = "/" + "/".join(path_parts) if path_parts else "/"
                self.game_state.add_directory(parent_path, change["name"])
            elif change_type == "delete_file":
                self.game_state.delete_file_or_dir(change["path"])
            # Add more state change types as needed

        self.game_state.add_xp(success_data.get("xp_reward", 0))

    def get_simulated_output(self, command: str) -> str:
        """
        This method is now mostly redundant as the CommandParser handles actual output.
        It can be kept for fallback or specific hardcoded level outputs if needed,
        but the primary source of simulated output will be the CommandParser.
        """
        # The parser's output is now passed through `validate_command`
        # and stored in `feedback_data["simulated_output_from_parser"]`.
        # This method can return an empty string or specific overrides.
        return "" # We'll rely on the parser's output.