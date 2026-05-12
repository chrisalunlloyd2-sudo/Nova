# Installation and Usage

## Prerequisites
- Python 3.x (Portable or System-installed)
- Git (Portable or System-installed)
- A configured Git repository with an active remote.

## Step-by-Step Installation
1. **Clone the Repository:** Ensure the script is placed within an initialized Git repository.
2. **Configure Paths:** Open `auto_port.py` and ensure `SOURCE_PATH` and `DEST_PATH` correctly point to your network share and local repository.
3. **Configure Git Executable:** If using portable Git, ensure the `subprocess.run` calls point to your specific `git.exe` path.

## Running from Command Line
To run the autoloader manually, simply execute:
`python auto_port.py`

To run continuously, schedule it via **Windows Task Scheduler**:
1. Open Task Scheduler -> Create Basic Task.
2. Trigger: "Daily" or "Hourly".
3. Action: "Start a program".
4. Program/script: `python`
5. Add arguments: `C:\AutomationProject\auto_port.py`
