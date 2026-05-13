# GEMINI.md - Project Operational Mandates

## Core Development Lifecycle
Every task must follow the **Research -> Strategy -> Execution (Plan, Act, Validate)** cycle.

## Project Rules
1. **One change per phase:** Focus on a single logical update at a time.
2. **Verify before continuing:** Run tests/validation after every change.
3. **Update CHANGELOG.md every phase:** Document what was changed.
4. **Update BUILD.txt with exact commands:** Log the commands used for the phase.
5. **Update NOTES.md with mistakes and fixes:** Record lessons learned.
6. **Snapshot before risky changes:** Use backups or git to preserve state.
7. **Never overwrite the only good state:** Ensure a fallback path exists.
8. **Never trust active runtime as canonical truth:** Verify against files and logs.
9. **Promote only verified checkpoints:** Only commit/ship code that has passed validation.
10. **Forward-only: fix and upgrade, do not roll back blindly:** Prefer fixing forward over reverting without understanding.
11. **Darwinian Prompt Rollback:** If a prompt evolution cycle results in a lower fitness score or worse performative adherence, ALWAYS rewind to the last known apex prompt and re-seed the mutation pool.

## Feedback Loop & Polishing
- **Post-Task Verification:** After completing a program or a significant task, ALWAYS ask the user: "Is it working?".
    - **If "No":** Resubmit to the loop (analyze failure, propose fix, re-implement) and update the version on the repo.
    - **If "Yes":** Close/Reset context window (proceed to next high-level task or end session).
- **Code Polishing Mandate:** If an error code is provided in a prompt requesting a fix (e.g., "please give me one big block of copy paste code..."), ALWAYS submit the code one more time for a final "polish" pass to ensure it is idiomatic, complete, and follows project standards before final delivery.

## Phase 19: Operational Mandates & Feedback Loop Integration
- **Goal:** Codify the user's new development lifecycle and feedback loop into the project's core instructions.
- **Status:** Implementing GEMINI.md and updating project logs.
