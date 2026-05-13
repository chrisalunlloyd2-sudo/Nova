# System Blueprint: The Darwinian Foundry

## I. Architecture
The system operates on a **Linear-Evolutionary Pipeline**:
1. **Axiom Seed:** The user provides an `Intent` (The Goal) and a `Topology` (The File Structure).
2. **Natural Selection (Fitness):** Each generated file is passed through an AST parser. If it fails, it enters the **Scientific Mutation Loop**.
3. **Scientific Mutation:** 
   - Hypothesis: "Variable X is causing the crash."
   - Action: Change Variable X.
   - Result: Measure Delta.
4. **Step-Up Re-Injection:** If a file is incomplete (contains placeholders), the system re-feeds the partial code back with a "Rewrite Entirely" directive.
5. **Ledgering:** Successful "Atoms" are hashed (SHA-256) and stored in `CodeLedger.db` for future reuse.
6. **Shipment:** The verified package is force-pushed to GitHub.

## II. Prompt Genetics (Phase 24)
The system no longer uses static prompts. It uses a **Tournament Selection** algorithm:
- **Mutation:** The LLM mutates a "Parent Prompt" to be more "Performative."
- **Benchmark:** The new prompt is tested against 3 technical coding tasks.
- **Selection:** Only prompts that achieve 100% AST success and 0% conversational filler are promoted to `BEST_PROMPT.txt`.

## III. Data Flow
`User Intent` -> `Apex Prompt` -> `LLM Generation` -> `AST Veto` -> `Scientific Fix` -> `Step-Up Fix` -> `Git Push`
