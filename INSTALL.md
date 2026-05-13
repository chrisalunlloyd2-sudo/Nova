# Installation & Setup Guide

## Requirements
- **Ollama:** Must be installed and running locally.
- **Git:** Installed and configured in the system PATH.
- **GitHub CLI (gh):** Authenticated for automated repo creation.
- **Node.js:** (Optional) Required if using the `karoo_bridge.js` for advanced mutation analysis.

## Setup Steps
1. **Model Pull:**
   Ensure the target model is available in Ollama:
   ```powershell
   ollama pull qwen2.5:0.5b
   ```
2. **Path Configuration:**
   The executable expects `git` and `gh` to be accessible. If using the source code, ensure Python 3.11+ is installed.

3. **Running the Engine:**
   Run the standalone executable from any directory:
   ```powershell
   ./darwin_cli.exe --target "C:\Path\To\Output" --intent "Your Intent Here"
   ```

## Troubleshooting
- **Empty Files:** Check if the Ollama server is active. The engine now features an auto-detection check but requires the server to be listening on `http://localhost:11434`.
- **Deployment Failures:** Ensure you are logged into the GitHub CLI (`gh auth login`).
- **AST Parsing Errors:** The engine will automatically trigger up to 3 "Step-Up" re-injection loops to fix syntax errors. If it still fails, check the `NOTES.md` in the target folder for the error logs.
