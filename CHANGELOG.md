# Changelog

All notable changes to the Systems Engineering Automation Pipeline will be documented in this file.

## [25.0.0] - 2026-05-12
### Added
- **Phase 25: Executable Packaging & CLI Hooks**.
- Created `darwin_cli.py` to act as an AI-friendly CLI hook providing command-line arguments for target, intent, and topology.
- Refactored `DarwinianEngine_v8.py` to use relative paths (`os.getcwd()`), making the entire engine portable across any machine.
- Compiled the pipeline into a standalone executable (`darwin_cli.exe`) using PyInstaller.

## [24.0.0] - 2026-05-12
### Added
- **Phase 24: Prompt Genetics & Performative Evolution**.
- Created `prompt_evolver.py` for automated Darwinian evolution of system prompts.
- Implemented tournament selection and self-mutation for prompt variants.
- Integrated `BEST_PROMPT.txt` (Apex Prompt) into the core generation engine.
- Successfully ran initial evolution loops to optimize for AST validity and conversational silence.

## [23.0.0] - 2026-05-12
### Added
- **Phase 23: Multi-Page Documentation & Engine Resilience**.
- Improved `extract_code` to properly parse `.md` files without stripping headers, allowing successful generation of `README.md`, `INSTALL.md`, `CHANGELOG.md`, etc.
- Modified `get_program_out` to no longer abort the entire deployment pipeline if a single page fails evolution. The system now logs a warning and proceeds to the next file, guaranteeing that partial but functional codebases are still shipped.
- Successfully verified E2E deployment of a 7-file topology involving complex markdown documentation.

## [22.0.0] - 2026-05-12
### Added
- **Phase 22: GitHub Deployment Integration & E2E Verification**.
- Integrated the `deploy()` method directly into `DarwinianEngine_v8.py`'s core pipeline (`get_program_out`).
- Automated repository initialization, force-commit, and `gh repo create/push` using system subprocesses.
- Validated full End-to-End lifecycle (Generation -> Testing -> Re-Injection -> GitHub Push) via randomized project deployments.

## [21.0.0] - 2026-05-12
### Added
- **Phase 21: Re-Injection Loop & Lazy Code Detection**.
- Upgraded `is_page_complete` to detect LLM "lazy" placeholders (e.g., `# ...`, `TODO`).
- Extended support for HTML, CSS, and JS file generation in the fitness tester.
- Implemented a 3-attempt Step-Up Re-Injection loop for incomplete files.
- Improved Step-Up prompt engineering to explicitly forbid placeholders and demand full code rewrites, addressing the context-cutoff friction point.

## [20.0.0] - 2026-05-12
### Added
- **Phase 20: Boolean Logic Completeness & Cloud Fallback**.
- Implemented `is_page_complete` boolean logic check for generated code.
- Added `CLOUD` fallback signal for automated evolution failures.
- Improved `run_scientific_evolution` resilience with final verification pass.
- Delivered `main.py` and `logic_engine.py` via Cloud Intervention to resolve empty file failure.

## [19.0.0] - 2026-05-12
### Added
- **Phase 19: Operational Mandates & Feedback Loop Integration**.
- Established `GEMINI.md` as the source of truth for the development lifecycle.
- Implemented "Is it working?" feedback loop mandate.
- Added code polishing mandate for error-driven fixes.
- Standardized document updates (CHANGELOG, BUILD, NOTES) for every phase.

## [8.0.0] - 2026-05-11
### Added
- **Phase 18: Scientific Iterative Handshake & Brute Predict**.
- Implemented `ScientificMethodLoop`: If code is unfit, Karoo GP changes one variable at a time based on a hypothesis.
- Added `BrutePredict`: Micro-level execution and checksumming for logic atoms.
- Integrated `h2o-danube3:4b` for rapid predictive code generation.
- Verified "Fix until winner" logic through 10 iterative test cycles.

## [7.1.0] - 2026-05-11
...
