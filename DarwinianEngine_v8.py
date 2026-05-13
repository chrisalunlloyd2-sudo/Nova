import os
import time
import json
import re
import subprocess
import sys
import math
import ast
from pathlib import Path
import webbrowser
import hashlib
import sqlite3
import traceback

# 100-STEP DARWINIAN EVOLUTIONARY ENGINE v8.0
# CORE: SCIENTIFIC METHOD ITERATIVE FIXING + BRUTE PREDICT

class CodeLedger:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._init_ledger()

    def _init_ledger(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ledger (
                sha256 TEXT PRIMARY KEY,
                code_block TEXT,
                metadata TEXT,
                fitness_score REAL,
                verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def commit_to_ledger(self, code_block, metadata, fitness):
        h = hashlib.sha256(code_block.encode('utf-8')).hexdigest()
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO ledger (sha256, code_block, metadata, fitness_score)
                VALUES (?, ?, ?, ?)
            ''', (h, code_block, json.dumps(metadata), fitness))
            self.conn.commit()
            return h
        except: return None

class DarwinBridge:
    def __init__(self):
        self.bridge_path = os.path.join(os.getcwd(), "karoo_bridge.js")
        self.node_modules = os.path.join(os.getcwd(), "node_modules")

    def evaluate(self, code_path):
        env = os.environ.copy()
        env["NODE_PATH"] = self.node_modules
        try:
            res = subprocess.run(["node", self.bridge_path, "evaluate", str(code_path)], 
                                 env=env, capture_output=True, text=True)
            if res.returncode == 0:
                return json.loads(res.stdout).get("fitness", 0)
        except: return 0
        return 0

    def mutate_scientific(self, code_path):
        """Phase 18: Scientific Method Mutation (Hypothesis -> 1 Change)"""
        env = os.environ.copy()
        env["NODE_PATH"] = self.node_modules
        try:
            res = subprocess.run(["node", self.bridge_path, "mutate", str(code_path)], 
                                 env=env, capture_output=True, text=True)
            if res.returncode == 0:
                data = json.loads(res.stdout)
                return data.get("code"), data.get("fitness"), data.get("outcome")
        except: pass
        return None, 0, "FAILED"

class SystemsPipelineEngine:
    def __init__(self, model="qwen2.5:0.5b"):
        self.model = model
        
        # Portable paths based on current working directory
        self.base_dir = os.getcwd()
        self.build_lab = Path(os.path.join(self.base_dir, "build_lab"))
        self.build_lab.mkdir(exist_ok=True)
        
        self.db_path = os.path.join(self.base_dir, "CodeLedger.db")
        self.ledger = CodeLedger(self.db_path)
        self.darwin = DarwinBridge()
        self.ollama_api = "http://localhost:11434/api/generate"
        self.best_prompt_file = os.path.join(self.base_dir, "BEST_PROMPT.txt")

    def get_best_prompt(self):
        if os.path.exists(self.best_prompt_file):
            with open(self.best_prompt_file, "r") as f:
                return f.read().strip()
        return "Systems Engineering Directive: Write the complete Python implementation for {page} to fulfill the intent: {intent}. Provide the code in a markdown block. Absolute zero preamble or postamble. Direct code output only."

    def log(self, msg, symbol="*"):
        print(f"[{symbol}] {msg}")
        sys.stdout.flush()

    def run_fitness_test(self, code, page_name=""):
        """Phase: Natural Selection. AST + Subprocess Execution."""
        if page_name and not page_name.endswith(".py"):
            if len(code.strip()) > 10:
                return True, "STABLE"
            return False, "Code too short or empty"

        try:
            ast.parse(code)
            # Brute Predict: Run isolated command (Phase 18)
            temp_file = self.build_lab / "predict_test.py"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(code)
            
            # Syntax only execution check
            res = subprocess.run(["python", "-m", "py_compile", str(temp_file)], capture_output=True)
            if res.returncode == 0:
                return True, "STABLE"
            return False, res.stderr.decode()
        except Exception as e:
            return False, str(e)

    def ping_llm(self, prompt):
        import requests
        try:
            payload = {"model": self.model, "prompt": prompt, "stream": False}
            response = requests.post(self.ollama_api, json=payload, timeout=30)
            return response.json().get("response", "")
        except: return ""

    def extract_code(self, text, page_name=""):
        """Phase 18: Enhanced Extraction (Robust markdown handling)"""
        # If the target is a markdown file, we generally want the raw output, 
        # but if it's wrapped in a codeblock, we extract it. Otherwise return raw.
        if page_name.endswith(".md"):
            match = re.search(r'```(?:markdown|md)?\s*(.*?)\s*```', text, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
            # Clean up typical conversational wrappers
            text = re.sub(r'^(Here is the .*?:\n\n)', '', text, flags=re.IGNORECASE)
            text = re.sub(r'(Sure, .*?:\n\n)', '', text, flags=re.IGNORECASE)
            return text.strip()

        # Determine language based on extension
        lang = "python"
        if page_name.endswith(".html"): lang = "html"
        elif page_name.endswith(".js"): lang = "javascript"
        elif page_name.endswith(".css"): lang = "css"

        # Look for code blocks
        match = re.search(fr'```(?:{lang})?\s*(.*?)\s*```', text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Fallback block search
        match = re.search(r'```(?:.*?)\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        # If no blocks, try to find lines starting with import or def
        lines = text.splitlines()
        code_lines = []
        for line in lines:
            if line.strip() and not line.strip().startswith(('#', '//', 'Note:', 'Here')):
                code_lines.append(line)
        
        if code_lines: return "\n".join(code_lines)
        return text.strip()

    def is_page_complete(self, code, page_name=""):
        """Boolean Logic Check: Is the page full and complete?"""
        if not code or len(code.strip()) < 20:
            return False
            
        # Detect LLM "lazy" placeholders
        lazy_patterns = [
            r'#\s*\.\.\.', r'//\s*\.\.\.', r'<!--\s*\.\.\.\s*-->',
            r'#\s*rest of', r'//\s*rest of',
            r'#\s*more code', r'//\s*more code',
            r'#\s*implement.*?here', r'//\s*implement.*?here',
            r'pass\s*#', r'TODO'
        ]
        for pat in lazy_patterns:
            if re.search(pat, code, re.IGNORECASE):
                self.log(f"Lazy placeholder detected in {page_name}", "INCOMPLETE")
                return False
        
        if page_name.endswith(".html"):
            return "</html>" in code.lower() and "<body" in code.lower()
        elif page_name.endswith(".py"):
            try:
                ast.parse(code)
                has_structure = re.search(r'import\s+|def\s+|class\s+', code)
                return bool(has_structure)
            except:
                self.log(f"AST parsing failed for {page_name}", "INCOMPLETE")
                return False
        # For CSS/JS, basic length check and ending character check
        elif page_name.endswith(".js"):
            code = code.strip()
            # If it ends with something that looks cut off
            if code.endswith(",") or code.endswith("=") or code.endswith("("):
                return False
            return len(code) > 50
        elif page_name.endswith(".css"):
            code = code.strip()
            if code.endswith(",") or code.endswith("{"):
                return False
            return len(code) > 50
            
        return len(code.strip()) > 50

    def run_scientific_evolution(self, target_folder, page, intent):
        self.log(f"Initiating Scientific Evolution for: {page}", "DARWIN")
        
        # 1. Initial Generation (Phase 24: Using evolved Apex Prompt)
        apex_prompt = self.get_best_prompt()
        prompt = apex_prompt.format(page=page, intent=intent)
        
        raw_response = self.ping_llm(prompt)
        code = self.extract_code(raw_response, page)
        
        winner = False
        attempts = 0
        fitness_score = 0
        
        while not winner and attempts < 10:
            self.log(f"Iteration {attempts + 1}: Testing Fitness...", "TEST")
            
            # Save candidate for Darwinian evaluation
            page_name = page if not page.endswith(".py") else page[:-3]
            cand_path = self.build_lab / f"candidate_{page_name}.py"
            with open(cand_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            fit, feedback = self.run_fitness_test(code, page)
            
            if fit:
                fitness_score = self.darwin.evaluate(cand_path)
                if fitness_score >= 100 or not page.endswith(".py"): # Non-python gets an automatic pass if stable
                    self.log(f"Winner Selected (Fitness: {fitness_score})", "SUCCESS")
                    winner = True
                    break
                else:
                    self.log(f"Low Fitness ({fitness_score}). Initiating Scientific Mutation...", "MUTATE")
            else:
                self.log(f"Logic Unfit: {feedback[:50]}...", "FIX")
            
            # 2. SCIENTIFIC METHOD FIX (Phase 18)
            new_code, new_fitness, outcome = self.darwin.mutate_scientific(cand_path)
            if new_code and outcome == "HYPOTHESIS_VALIDATED":
                self.log(f"Hypothesis Validated! New Fitness: {new_fitness}", "WIN")
                code = new_code
            else:
                self.log("Hypothesis Rejected. Mutating via LLM feedback...", "GENETIC")
                prompt += f"\nFIX REQUIRED. Error: {feedback}. Previous Logic: {code}"
                code = self.ping_llm(prompt)
                code = self.extract_code(code, page)
            
            attempts += 1
            time.sleep(0.5)

        # Final Verification with Boolean Logic & Re-Injection Loop
        if winner and self.is_page_complete(code, page):
            h = self.ledger.commit_to_ledger(code, {"page": page}, fitness_score)
            self.log(f"Checksummed and Ledgered: {h[:16]}...", "LEDGER")
            
            with open(os.path.join(target_folder, page), "w", encoding="utf-8") as f:
                f.write(code)
            return True
        else:
            self.log(f"Evolution incomplete for {page}. Initiating Re-Injection Step-Up...", "RE-INJECT")
            # Phase 6: Step-Up Re-Injection (Loop up to 3 times)
            re_inject_attempts = 0
            while re_inject_attempts < 3:
                re_inject_attempts += 1
                self.log(f"Re-Injection Loop {re_inject_attempts} for {page}...", "STEP-UP")
                
                # Friction Point Fix: Instead of asking to "finish" and passing the whole code, 
                # we explicitly forbid placeholders and ask it to write the FULL script.
                reinjection_prompt = f"CRITICAL DIRECTIVE: You failed to provide the complete code for {page}. You left lazy placeholders or cut off. Project intent: {intent}. Rewrite the ENTIRE file from start to finish. DO NOT USE PLACEHOLDERS like '# ...'. DO NOT truncate. Here was your previous incomplete attempt:\n{code}"
                re_code_raw = self.ping_llm(reinjection_prompt)
                new_code = self.extract_code(re_code_raw, page)
                
                if len(new_code) > 20:
                    code = new_code
                
                if self.is_page_complete(code, page):
                    self.log(f"Re-Injection Successful on attempt {re_inject_attempts}. Page complete.", "SUCCESS")
                    h = self.ledger.commit_to_ledger(code, {"page": page}, fitness_score)
                    with open(os.path.join(target_folder, page), "w", encoding="utf-8") as f:
                        f.write(code)
                    return True
                    
            self.log(f"Re-Injection Failed after 3 attempts for {page}. Requesting FULL FIXED CODE from Cloud...", "CLOUD")
            return False

    def deploy(self, target_dir):
        # Phase 22: GitHub Deployment Integration
        self.log(f"Commencing Deployment for {target_dir}...", "DEPLOY")
        folder_name = os.path.basename(target_dir).replace(" ", "_")
        
        env = os.environ.copy()
        git_path = r"C:\Users\viper\git\cmd\git.exe"
        gh_exe = r"C:\Users\viper\scoop\apps\gh\current\bin\gh.exe"
        env["PATH"] = r"C:\Users\viper\git\cmd;" + env.get("PATH", "")

        original_cwd = os.getcwd()
        try:
            os.chdir(target_dir)
            
            if not os.path.exists(".git"):
                subprocess.run([git_path, "init"], check=False)

            subprocess.run([git_path, "add", "-A", "--force"], check=False)
            subprocess.run([git_path, "commit", "-m", "System: Automated Evolution & Deployment"], check=False)
            subprocess.run([git_path, "branch", "-M", "main"], check=False)

            self.log("Checking GitHub repository status...", "GITHUB")
            check = subprocess.run([gh_exe, "repo", "view", folder_name], capture_output=True, env=env)
            
            if check.returncode != 0:
                self.log(f"Creating new Public Repo: {folder_name}", "GITHUB")
                subprocess.run([gh_exe, "repo", "create", folder_name, "--public", "--source=.", "--remote=origin", "--push"], env=env)
            else:
                self.log("Existing repo found. Force-pushing update...", "GITHUB")
                subprocess.run([git_path, "remote", "set-url", "origin", f"https://github.com/chrisalunlloyd2-sudo/{folder_name}.git"], check=False)
                subprocess.run([git_path, "push", "-u", "origin", "main", "--force"], env=env)

            url = f"https://github.com/chrisalunlloyd2-sudo/{folder_name}"
            self.log(f"Deployment Complete: {url}", "SUCCESS")
        finally:
            os.chdir(original_cwd)

    def get_program_out(self, target_folder, intent, topology=None):
        self.log(f"GOAL: GET PROGRAM OUT - {intent}", "HPC")
        
        if topology is None:
            topology = ["main.py", "logic_engine.py"]
            
        os.makedirs(target_folder, exist_ok=True)
        
        success_count = 0
        for page in topology:
            success = self.run_scientific_evolution(target_folder, page, intent)
            if not success:
                self.log(f"FAILED TO GET PROGRAM OUT FOR {page}, continuing to next...", "WARNING")
            else:
                success_count += 1
        
        self.log(f"PROGRAM COMPLETED {success_count}/{len(topology)} PAGES.", "FINISH")
        
        # Phase 22: Integrate deployment logic
        self.deploy(target_folder)
        
        webbrowser.open(f"file:///{target_folder}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        engine = SystemsPipelineEngine()
        engine.get_program_out(sys.argv[1], "A self-correcting recursive math solver")
    else:
        print("No target.")
