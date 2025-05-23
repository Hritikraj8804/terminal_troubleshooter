# game/level_manager.py

from .game_state import GameState
from .data.levels import LEVELS
import re # For regular expression matching

class LevelManager:
    """
    Manages the game's levels, their progression, and validates user commands
    against the current level's requirements.
    """
    def __init__(self, game_state: GameState):
        self.game_state = game_state
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

    def validate_command(self, user_command: str) -> tuple[bool, dict | None]:
        """
        Validates if the user's command matches the expected commands for the current step.
        Returns (is_correct, feedback_data)
        """
        current_level = self.get_current_level_data()
        if not current_level:
            return False, {"message": "No active level.", "type": "error"}

        # For simplicity, we assume one "step" per level for now.
        # In a more complex game, you might track current_step_index.
        current_step = current_level["steps"][0]
        expected_commands = current_step["expected_commands"]
        on_success_data = current_step["on_success"]
        
        user_command_lower = user_command.strip().lower()

        for exp_cmd in expected_commands:
            check_type = exp_cmd["check_type"]
            expected_cmd_val = exp_cmd["command"].lower()

            if check_type == "exact" and user_command_lower == expected_cmd_val:
                return True, on_success_data
            elif check_type == "contains" and expected_cmd_val in user_command_lower:
                return True, on_success_data
            elif check_type == "regex" and re.search(expected_cmd_val, user_command_lower):
                return True, on_success_data
        
        return False, {"message": current_step.get("hint_on_fail", "That's not the right command for this task. Try again."), "type": "hint"}

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
                self.game_state.add_directory(change["path"], change["name"])
            elif change_type == "delete_file":
                self.game_state.delete_file_or_dir(change["path"])
            # Add more state change types as needed

        self.game_state.add_xp(success_data.get("xp_reward", 0))

    def get_simulated_output(self, command: str) -> str:
        """Retrieves simulated output for a given command from the current level."""
        current_level = self.get_current_level_data()
        if current_level:
            # We assume output is in the first step's on_success for now
            simulated_output = current_level["steps"][0]["on_success"].get("simulated_output", {})
            # Look for exact match first, then partial match if needed
            if command in simulated_output:
                return simulated_output[command]
            
            # Simple fallback for ps aux to show current state
            if command == "ps aux":
                output_lines = ["USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"]
                for pid, proc_data in self.game_state.processes.items():
                    # Simplified representation
                    state_char = proc_data['state'][0].upper() if proc_data['state'] else '?'
                    output_lines.append(f"sysadmin  {pid:<4}  0.0  0.0 100000  5000 ?        {state_char}    10:00   0:00 {proc_data['command']}")
                return "\n".join(output_lines)
            
            # Fallback for du -sh /var/log/* (after syslog is deleted)
            if command == "du -sh /var/log/*":
                if not self.game_state.get_file_content("/var/log/syslog"): # If syslog was deleted
                     return (
                        "8.0K    /var/log/auth.log\n"
                        "4.0K    /var/log/kern.log"
                    )
        return "" # Default empty output