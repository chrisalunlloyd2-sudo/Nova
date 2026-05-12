# System Blueprint

## Architecture
The application runs as a standalone Python script (`auto_port.py`) executed via standard Python or scheduled via Windows Task Scheduler. 

### Data Flow
1. **Ingestion:** `transfer_file()` pulls the target file from the `NAS_SHARE`.
2. **Sanitization:** `sanitize_file()` intercepts the file on disk. It loads the text, applies an array of regex substitution rules to redact sensitive data, and overwrites the file.
3. **Deployment:** `git_push()` invokes the system Git executable to stage, commit, and push the sanitized file to the remote `origin`.

## File Structure
- `auto_port.py`: The core automation logic.
- `README.md`: High-level overview.
- `INSTALL.md`: Setup and run instructions.
- `CHANGELOG.md`: Version history.
- `Blueprint.md`: Architectural documentation.
