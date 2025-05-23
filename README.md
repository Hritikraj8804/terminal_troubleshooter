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
    git clone [https://github.com/Hritikraj8804/terminal_troubleshooter.git](https://github.com/Hritikraj8804/terminal_troubleshooter.git)
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