# Terminal Troubleshooter

## Project Description

**Terminal Troubleshooter is a unique interactive, text-based game that transforms practical IT troubleshooting into an engaging challenge. Step into the role of a junior sysadmin and master Linux, Docker, and Kubernetes commands by solving real-world system failures in a simulated terminal environment.**

This game aims to provide a nostalgic, retro terminal experience while reinforcing practical command-line skills in a fun and engaging way. Think of it as a choose-your-own-adventure for the command line!

## Features

* **Interactive Terminal Simulation:** Type real Linux, Docker, and Kubernetes commands directly into a simulated shell.

* **Real-world Scenarios:** Tackle common IT issues like web server outages, disk space crises, and stuck Kubernetes pods.

* **Progressive Difficulty:** Levels are designed to gradually introduce more complex challenges and commands.

* **XP System:** Earn SysAdmin XP for successfully resolving issues and advancing through levels.

* **Nostalgic ASCII Art & UI:** Enjoy a minimalist, text-based interface reminiscent of classic terminal applications, powered by the `rich` library.

* **Skill Reinforcement:** Practice and deepen your understanding of essential Linux, Docker, and Kubernetes command-line troubleshooting in a risk-free, interactive environment.

## Gameplay Overview

Each level presents a critical system alert. Your mission: diagnose the issue using simulated Linux, Docker, and Kubernetes commands, interpret the output, and implement the fix. Successfully resolve the problem to advance and earn XP. Hints are available if you get stuck!

## Installation & Setup

To run Terminal Troubleshooter, you'll need **Python 3.9+** installed on your system.

1.  **Clone the Repository (or download the project files):**

    ```
    git clone https://github.com/Hritikraj8804/terminal_troubleshooter.git
    cd terminal_troubleshooter
    ```

    (If you downloaded, just navigate to the `terminal_troubleshooter` directory.)

2.  **Create a Virtual Environment (Recommended):**
    It's good practice to install dependencies in a virtual environment to avoid conflicts with other Python projects.

    ```
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**

    * **On Windows:**

        ```
        .\venv\Scripts\activate
        ```

    * **On macOS/Linux:**

        ```
        source venv/bin/activate
        ```

4.  **Install Dependencies:**
    The game relies on the `rich` library for its beautiful terminal output.

    ```
    pip install -r requirements.txt
    ```

## How to Run the Game

Once you've completed the installation steps and activated your virtual environment, you can start the game from the root of the `terminal_troubleshooter` directory:
```bash
python -m game.main
```
The game will launch directly in your terminal. Follow the on-screen instructions and type commands at the prompt.

## Project Structure

The project is organized into a Python package for modularity and maintainability:

```bash
terminal_troubleshooter/
├── game/
│   ├── __init__.py           # Makes 'game' a Python package
│   ├── main.py               # Main entry point, orchestrates game flow
│   ├── game_state.py         # Manages the simulated environment (filesystem, processes, etc.)
│   ├── level_manager.py      # Defines and manages game levels/scenarios
│   ├── command_parser.py     # Parses user input commands and validates them
│   ├── terminal_interface.py # Handles all terminal I/O and display logic (using rich)
│   ├── utilities.py          # General helper functions (e.g., ASCII art, clearing screen)
│   └── data/                 # Directory for game data (levels, narratives, simulated output)
│       ├── __init__.py
│       ├── levels.py         # Defines all game levels (e.g., a list of dictionaries)
│       └── ascii_art.py      # Stores larger ASCII art pieces for title screens, etc.
│
├── .gitignore                # Specifies files/directories to ignore in version control (e.g., __pycache__)
├── requirements.txt          # Lists Python dependencies (e.g., rich)
└── README.md                 # Project description, how to run, usage instructions
```

## Extending the Game / Contributing

Want to expand Terminal Troubleshooter? The game's modular design makes it easy to contribute by adding new levels, implementing more commands, or enhancing existing simulations!

### Adding New Levels:

1.  Open `game/data/levels.py`.

2.  Add a new dictionary to the `LEVELS` list, following the existing structure.

3.  Define the `id`, `title`, `description`, `steps` (with `task`, `expected_commands`, `on_success`, and `hint_on_fail`).

4.  Crucially, think about what **state changes** (`state_changes`) are needed in `game_state.py` to reflect the resolution of the problem.

5.  Consider if you need to provide specific `simulated_output_overrides` for commands in this level.

### Implementing New Commands / Enhancing Existing Ones:

1.  Open `game/command_parser.py`.

2.  **For new commands:**

    * Add a new `elif cmd == "your_new_command":` block in the `parse_and_execute` method.

    * Create a new private method `_handle_your_new_command(self, args: list[str])` to encapsulate its logic.

    * Implement the simulation within this new method, manipulating `self.game_state` as needed and returning a dictionary with `output`, `success`, and `message`.

3.  **For existing commands:**

    * Modify the relevant `_handle_command` method (e.g., `_handle_ls`, `_handle_docker`) to add support for new arguments, more detailed output, or specific error messages.

### Enhancing `game_state.py`:

* You can add more simulated resources to `GameState` (e.g., network interfaces, users, more complex log files, resource utilization metrics).

* Implement new methods to update these resources, which can then be called by `CommandParser` or `LevelManager`.

## License

This project is open-source.

## Acknowledgements

* Developed with Python.

* Powered by the [Rich](https://github.com/Textualize/rich) library for beautiful terminal output.