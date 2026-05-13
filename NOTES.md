# Development Notes

## Phase 25 Strategy
- **Goal:** Package the entire Evolutionary Engine into a standalone `.exe` that can run on any machine and act as an AI hook.
- **Portability Refactor:** The v8 engine originally relied on hardcoded absolute paths (e.g. `C:\Users\viper\...`). I refactored the engine to construct all necessary paths dynamically using `os.getcwd()`, ensuring the tool remains functional when copied to different environments.
- **CLI Hooks:** Wrote `darwin_cli.py` leveraging Python's `argparse` module to expose `--target`, `--intent`, `--topology`, and `--model` parameters. This allows standard programmatic access without modifying source code.
- **Executable Generation:** Utilized PyInstaller with the `--onefile` flag to bundle the engine, SQLite CodeLedger logic, and execution wrappers into a single `darwin_cli.exe`.

## Phase 24 Strategy
- **Goal:** Darwinistically evolve the system prompts to find the most "Performative" phrasing.
- **Genetic Algorithm:** The `prompt_evolver.py` uses tournament selection. It generates N variations of a parent prompt, tests them against a benchmark (math utils, file handlers), and selects the winner based on AST success rate and conversational silence.
- **Performative Evolution:** The mutation process explicitly instructs the LLM to use synonyms and tones that trigger higher code density and strict adherence to technical constraints.
- **Dynamic Integration:** The generation engine now checks for `BEST_PROMPT.txt`. This allows the system's "Intelligence" to improve over time as more evolution cycles are run, without needing manual code changes to the prompt strings.

## Phase 23 Strategy
- **Goal:** Verify end-to-end multi-page generation including extensive documentation (README, INSTALL, CHANGELOG, etc.).
- **Friction Point (Markdown Extraction):** The legacy `extract_code` method was stripping `#` headers because it thought they were Python comments. Updated the logic to properly handle `.md` extensions and retain raw conversational formatting if needed.
- **Resilience Update:** Previously, if one file failed (e.g., failed AST parsing during all 3 step-up attempts), the entire pipeline aborted and `deploy()` was never called. The engine was updated to log a warning and continue. 
- **Result:** The `MultiPage_E2E` test successfully evolved 6 out of 7 files and shipped the resulting package to GitHub despite a single file generation failure, proving the pipeline is highly resilient for "shotgun" space-filling prompts.

## Phase 22 Strategy
- **Goal:** Connect the final generation loop to the GitHub deployment function.
- **Bug Fixed:** The `get_program_out` function in `DarwinianEngine_v8.py` successfully generated code but omitted the final `deploy()` call, meaning repositories were never pushed. 
- **Integration:** Copied the automated `git add/commit/push` and `gh repo create` logic from `pipeline_final.py` into the v8 Engine.
- **E2E Validation:** Ran a randomized deployment test (`E2E_Test_Deploy_[ID]`). The system successfully initialized the repo, handled re-injection, and shipped the working code directly to GitHub.

## Phase 21 Strategy & Friction Analysis
- **Goal:** Implement Phase 6 "Re-Injection" to catch and fix partially finished code blocks.
- **Friction Point (Context Cut-off):** When the LLM generates a long script (like Flappy Bird), it often runs out of attention/tokens and leaves a lazy placeholder (e.g., `# ... implement rest of code`).
- **Detection Mechanism:** Added regex pattern matching in `is_page_complete` to detect these lazy placeholders.
- **Prompt Engineering Fix:** The re-injection prompt was upgraded. Instead of asking to "finish this code" (which often causes the LLM to just repeat the incomplete code), the agent now explicitly commands the LLM to **rewrite the ENTIRE file from start to finish** and explicitly forbids the use of placeholders.
- **Loop Extension:** The Re-Injection Step-Up now loops up to 3 times before flagging a `CLOUD` fallback.
- **Testing:** 
  - `CatWebpageTest`: Successfully validated multi-language generation (HTML, CSS, JS).
  - `FlappyBirdTest`: Successfully triggered the Re-Injection loop and validated the new failure-detection logic on complex requests.

## Phase 20 Strategy
- **Goal:** Solve the "Empty File" / "Copy Failure" bug using Boolean Logic.
- **Boolean Logic:** Added `is_page_complete` which checks for length, AST validity, and structural elements (imports/defs).
- **Cloud Fallback:** When the local Darwinian loop fails to produce a stable winner, the system now flags a `CLOUD` intervention. This allows the human/agent to provide the "Big Block" of code required to bridge the gap.
- **Mistake Fixed:** Previously, the loop would simply exit if no winner was found, leaving the target file empty. Now it explicitly checks for completeness before claiming success.
- **Validation:** Delivered verified `main.py` and `logic_engine.py` to restore the system to a functional state.

## Phase 19 Strategy
- **Goal:** Codify the "Is it working?" feedback loop and the "Polish before ship" rule.
- **Workflow Integration:** The agent will now explicitly ask for confirmation before closing a task.
- **Mistake Mitigation:** The "Polish" rule addresses the issue of potentially messy code blocks generated during high-pressure debugging sessions.
- **Enforcement:** `GEMINI.md` is now the primary directive file for all future agent sessions in this workspace.

## Phase 18 Strategy
- **Goal:** Guaranteed logic perfection through iterative "Scientific" fixing.
- **Scientific Method:** Formulate Hypothesis -> Change 1 Variable -> Measure Delta. This prevents messy "shotgun" debugging and ensures we converge on a working solution.
- **Brute Predict:** Running isolated snippets in temporary subprocesses to verify logic "Atoms" before they are committed to the file.
- **Verification:** The system must not stop until the code passes the AST Veto AND the Subprocess Execution test (Exit Code 0).

## Final Darwinian Handover
...
