# Darwinian Evolutionary Engine v26.0

## Overview
The Darwinian Evolutionary Engine is a 100-step autonomous software factory designed to generate, test, and deploy production-ready codebases with zero human intervention. It leverages a "Scientific Method" iterative loop to self-correct logic, uses genetic algorithms to evolve its own system prompts, and features a robust re-injection cycle to overcome LLM context limitations.

## Core Features
- **Scientific Method Loop:** Formulates hypotheses to fix code failures by changing one variable at a time.
- **Prompt Genetics:** Darwinistically evolves its own system prompts to maximize "Performative" code output.
- **Re-Injection Step-Up:** Detects incomplete code or lazy placeholders (e.g., `# ...`) and forces a full rewrite.
- **Boolean Logic Verification:** Uses AST parsing and structural checks to ensure every "page" is complete before shipping.
- **Automated Deployment:** Automatically initializes Git, creates public GitHub repositories via the `gh` CLI, and force-pushes the verified code.

## Quick Start
The system is distributed as a standalone executable: `darwin_cli.exe`.

```powershell
./darwin_cli.exe --target "MyProject" --intent "A full flappy bird clone in pygame" --topology main.py README.md
```

## AI Hooks
The CLI is designed to be called by other agents:
- `--target`: Path to the output directory.
- `--intent`: Natural language description of the goal.
- `--topology`: List of specific files to generate.
- `--model`: (Optional) Specify the Ollama model (Default: qwen2.5:0.5b).

## Repository Contents
- `DarwinianEngine_v8.py`: The core evolutionary logic engine.
- `darwin_cli.py`: The CLI wrapper for the executable.
- `prompt_evolver.py`: The genetic prompt optimizer.
- `GEMINI.md`: Project operational mandates and rules of engagement.
- `CodeLedger.db`: SQLite database for checksummed and verified code atoms.

---
*MISSION STATUS: SHIPPED v26.0*
