# THE SYSTEMS ENGINEERING BIBLE (v10.0)
## Project: Darwinian Project Foundry

This document contains the canonical documentation for the entire 100-step autonomous software factory.

---

## I. SYSTEM ARCHITECTURE
The system uses a **Recursive Step-Down/Step-Up** methodology to transition raw intent into verified public code.

### 1. The Master Console (UI)
- **File:** `SystemsGUI.ps1` (PowerShell/WinForms)
- **Role:** Orchestrates the user interface, real-time log streaming, and manual approval gates.
- **Mechanism:** Uses a Concurrent Queue to pipe logs from the background Python process without freezing the UI.

### 2. The Systems Engineering Engine (Backend)
- **File:** `pipeline.py` (Python 3)
- **Role:** The primary "Brain" of the operation. Handles topology generation, code evolution, and GitHub shipping.
- **Core Logic:** `SystemsPipelineEngine` class.

### 3. The SHA-256 Code Ledger (Storage)
- **File:** `CodeLedger.db` (SQLite)
- **Role:** Stores every "Winning" logic block cryptographically indexed by its hash.
- **Benefit:** Prevents re-generation of identical logic and ensures 100% data integrity.

### 4. The Darwinian Bridge (Selection)
- **File:** `karoo_bridge.js` (Node.js)
- **Role:** Interfaces with the **Karoo GP** agent.
- **Selection Pressure:** Evaluates code variants for "Fitness" and performs single-variable "Scientific Method" mutations.

### 5. The Race Condition Analytic (Safety)
- **Module:** Integrated in `pipeline.py`
- **Role:** Performs AST-based static analysis to flag concurrency risks (Race Conditions).
- **Visualization:** "Purple Flags" in the Master Console.

---

## II. DEPENDENCIES & PREREQUISITES

### 1. Native Executables
- **Python 3.11+**: `C:\Users\viper\python\python.exe`
- **Git (Portable)**: `C:\Users\viper\git\cmd\git.exe`
- **GitHub CLI (gh)**: `C:\Users\viper\scoop\shims\gh.exe`
- **Ollama (Local LLM)**: `C:\Users\viper\AppData\Local\Programs\Ollama\ollama.exe`

### 2. Required Libraries
- **Python**: `pip install requests pyyaml playwright`
- **Node.js**: `npm install axios chalk soap`

---

## III. BUILD & INSTALLATION (COPY-PASTE)

Execute these commands in order to replicate the environment from zero:

### 1. Initialize System Environment
```powershell
# Create base directories
mkdir C:\Users\viper\SystemsPipeline
mkdir C:\Users\viper\build_lab

# Install core python dependencies
python -m pip install requests pyyaml playwright
python -m playwright install chromium
```

### 2. Setup Darwinian Bridge
```powershell
# Navigate to the repo
cd C:\Users\viper\CascadeProjects\recursive-ai-agent
npm install
```

### 3. Initialize Cryptographic Ledger
```powershell
# Ledger is auto-created on first run, but can be manually initialized:
sqlite3 C:\Users\viper\SystemsPipeline\CodeLedger.db "CREATE TABLE ledger (sha256 TEXT PRIMARY KEY, code_block TEXT, metadata TEXT, fitness_score REAL, verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
```

### 4. Launch Master Console
```powershell
# Double-click DRAG_FOLDER_HERE.bat on Desktop OR:
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\viper\SystemsGUI.ps1"
```

---

## IV. OPERATIONAL WORKFLOW (100 STEPS)

1. **LAB**: Normalize paths and isolate the build.
2. **DNA**: Generate project topology JSON.
3. **GROWTH**: Window-based code generation (20-line sliding window).
4. **MUTATION**: Karoo GP fitness selection.
5. **RACE SCAN**: Purple Flagging for concurrency hazards.
6. **RE-INJECTION**: Final completion loop (Injecting "Please help me finish this program").
7. **SYNTHESIS**: Deep README and ASCII mapping.
8. **SHIP**: Force-push to GitHub `main` branch.

---
*MISSION STATUS: VERIFIED v10.0*
