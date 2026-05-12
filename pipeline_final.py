import os
import sqlite3
import yaml
import subprocess
import sys
import re

# PHASE I: CONSTANTS & PATHS
BASE_DIR = r"C:\Users\viper\SystemsPipeline"
SANDBOX_DIR = os.path.join(BASE_DIR, "sandbox")
DB_PATH = os.path.join(BASE_DIR, "pipeline_state.db")
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")
OLLAMA_PATH = r"C:\Users\viper\AppData\Local\Programs\Ollama\ollama.exe"
GIT_PATH = r"C:\Users\viper\git\cmd\git.exe"
MAX_DEPTH = 5

class SystemsPipeline:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self._init_db()
        self.config = self._load_config()

    def _init_db(self):
        # Step 10: State Management
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                file_path TEXT PRIMARY KEY,
                status TEXT,
                scrubbed INTEGER DEFAULT 0,
                analyzed INTEGER DEFAULT 0,
                documented INTEGER DEFAULT 0,
                last_mutation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def _load_config(self):
        # Step 6: Credential Manifest
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}

    def log_event(self, msg, level="INFO"):
        print(f"[{level}] {msg}")

    # PHASE I: PRE-FLIGHT
    def sync_environment(self):
        # Step 2 & 3: venv and requirements
        self.log_event("Syncing environment...")
        pass

    def map_dependencies(self, source_folder):
        # Step 3
        req_path = os.path.join(SANDBOX_DIR, "requirements.txt")
        self.log_event(f"Mapping dependencies to {req_path}")
        with open(req_path, "w") as f:
            f.write("# Auto-generated requirements baseline\n")
        return req_path

    # PHASE II: THE SCRUB
    def read_file_safe(self, file_path):
        encodings = ['utf-8', 'utf-16', 'latin-1']
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    return f.read(), enc
            except:
                continue
        return None, None

    def scrub_file(self, file_path):
        self.log_event(f"Scrubbing {file_path}...")
        content, encoding = self.read_file_safe(file_path)
        if content is None:
            self.log_event(f"Could not read {file_path}, skipping.", "WARNING")
            return False

        patterns = [
            (r'\+?[1-9]\d{1,14}', '[REDACTED_PHONE]'),
            (r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', '[REDACTED_IP]'),
            (r'(?i)(api[_-]?key|secret|token|password|auth)[\s:=]+[\'"][^\'"]+[\'"]', r'\1 = "[REDACTED_CREDENTIAL]"'),
        ]

        original_content = content
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        if content != original_content:
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            self.cursor.execute('UPDATE files SET scrubbed = 1 WHERE file_path = ?', (file_path,))
            self.conn.commit()
            return True
        return False

    def purge_logs(self, target_dir):
        # Step 19: Log Purge
        self.log_event(f"Purging logs in {target_dir}...")
        for root, _, files in os.walk(target_dir):
            for f in files:
                if f.endswith(('.log', '.tmp', '.bak', '.swp')):
                    os.remove(os.path.join(root, f))
                    self.log_event(f"Deleted junk file: {f}")

    def run_scrub_pipeline(self, target_dir):
        self.log_event("Starting Phase II: The Scrub Pipeline")
        self.purge_logs(target_dir)
        for root, _, files in os.walk(target_dir):
            if '.git' in root: continue
            for f in files:
                f_path = os.path.join(root, f)
                self.cursor.execute('INSERT OR IGNORE INTO files (file_path, status) VALUES (?, ?)', (f_path, 'REGISTERED'))
                self.scrub_file(f_path)
        self.log_event("Phase II Scrub Complete")

    # PHASE III: AI LOGIC
    def ollama_prompt(self, prompt, model="qwen2.5:0.5b"):
        import requests
        try:
            response = requests.post('http://localhost:11434/api/generate', 
                                    json={'model': model, 'prompt': prompt, 'stream': False})
            return response.json().get('response', '')
        except Exception as e:
            self.log_event(f"Ollama Error: {e}", "ERROR")
            return "Professional AI documentation summary."

    def generate_ai_readme(self, target_dir):
        self.log_event("Generating AI documentation (Step-Up Phase)...")
        folder_name = os.path.basename(target_dir)
        files = []
        for root, _, filenames in os.walk(target_dir):
            if '.git' in root: continue
            for f in filenames:
                files.append(os.path.relpath(os.path.join(root, f), target_dir))
        inventory = "\n".join(files[:20])
        prompt = f"Given this file inventory of a project called {folder_name}:\n{inventory}\nWrite a professional 2-sentence overview of the project's purpose."
        overview = self.ollama_prompt(prompt)
        
        readme_content = f"""# {folder_name}
## Description
{overview}

## Architecture (Topological Map)
```text
{self.get_tree(target_dir)}
```
*Generated via Systems Engineering Automation Pipeline*
"""
        with open(os.path.join(target_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)
        self.log_event("Phase III AI README Generated")

    def get_tree(self, path):
        tree = []
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            tree.append(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if '.git' not in root:
                    tree.append(f"{subindent}{f}")
        return "\n".join(tree[:30])

    def deploy(self, target_dir):
        # Step 76 & 84: Deployment logic
        self.log_event(f"Commencing Deployment for {target_dir}...")
        folder_name = os.path.basename(target_dir).replace(" ", "_")
        
        env = os.environ.copy()
        env["PATH"] = r"C:\Users\viper\git\cmd;" + env["PATH"]
        gh_exe = r"C:\Users\viper\scoop\apps\gh\current\bin\gh.exe"

        os.chdir(target_dir)
        
        # Ensure Git Init (Step 4)
        if not os.path.exists(".git"):
            subprocess.run([GIT_PATH, "init"], check=False)

        # Stage and Commit (Step 75)
        subprocess.run([GIT_PATH, "add", "-A", "--force"], check=False)
        subprocess.run([GIT_PATH, "commit", "-m", "System: Automated Sanitization and Documentation"], check=False)
        subprocess.run([GIT_PATH, "branch", "-M", "main"], check=False)

        # GitHub Repo Creation (Step 77)
        self.log_event("Checking GitHub repository status...")
        check = subprocess.run([gh_exe, "repo", "view", folder_name], capture_output=True, env=env)
        
        if check.returncode != 0:
            self.log_event(f"Creating new Public Repo: {folder_name}")
            subprocess.run([gh_exe, "repo", "create", folder_name, "--public", "--source=.", "--remote=origin", "--push"], env=env)
        else:
            self.log_event("Existing repo found. Force-pushing update...")
            subprocess.run([GIT_PATH, "remote", "set-url", "origin", f"https://github.com/chrisalunlloyd2-sudo/{folder_name}.git"], check=False)
            subprocess.run([GIT_PATH, "push", "-u", "origin", "main", "--force"], env=env)

        # Visual Confirmation (Step 90)
        import webbrowser
        url = f"https://github.com/chrisalunlloyd2-sudo/{folder_name}"
        self.log_event(f"Opening Repository URL: {url}")
        webbrowser.open(url)
        self.log_event("Deployment Complete", "SUCCESS")

    def run_full_pipeline(self, target_dir):
        self.log_event(f"RUNNING FULL PIPELINE ON {target_dir}")
        self.run_scrub_pipeline(target_dir)
        self.generate_ai_readme(target_dir)
        self.deploy(target_dir)

if __name__ == "__main__":
    pipeline = SystemsPipeline()
    pipeline.log_event("Systems Engineering Automation Pipeline Active")
