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

# 100-STEP DARWINIAN EVOLUTIONARY ENGINE
# DEFINITIVE RECURSIVE GENETIC GROWTH + GITHUB SHIPPER

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
        except Exception as e:
            print(f"[LEDGER] Commit Error: {e}")
            return None

class RaceAnalytic:
    def __init__(self):
        self.hazards = []

    def analyze_concurrency(self, code):
        self.hazards = []
        try:
            clean_code = code.replace('\x00', '')
            tree = ast.parse(clean_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Global):
                    self.hazards.append(f"Global resource access: {node.names}")
                if isinstance(node, ast.AsyncFunctionDef):
                    has_await = any(isinstance(n, ast.Await) for n in ast.walk(node))
                    if not has_await:
                        self.hazards.append(f"Async '{node.name}' has no await.")
                if isinstance(node, ast.Call):
                    if 'Thread' in ast.dump(node):
                        self.hazards.append("Threading detected. Lock verification required.")
            return self.hazards
        except Exception as e:
            return [f"Static Analysis Skipped: {str(e)[:50]}..."]

class DarwinBridge:
    def __init__(self):
        self.bridge_path = r"C:\Users\viper\SystemsPipeline\karoo_bridge.js"
        self.node_modules = r"C:\Users\viper\CascadeProjects\recursive-ai-agent\node_modules"

    def evaluate(self, code_path):
        env = os.environ.copy()
        env["NODE_PATH"] = self.node_modules
        try:
            res = subprocess.run(["node", self.bridge_path, "evaluate", str(code_path)], 
                                 env=env, capture_output=True, text=True)
            if res.returncode == 0:
                return json.loads(res.stdout).get("fitness", 0)
        except Exception as e:
            print(f"[DARWIN] Bridge Error: {e}")
        return 0

class SystemsPipelineEngine:
    def __init__(self, model="qwen2.5:0.5b"):
        self.model = model
        self.build_lab = Path(r"C:\Users\viper\build_lab")
        self.db_path = r"C:\Users\viper\SystemsPipeline\CodeLedger.db"
        self.ledger = CodeLedger(self.db_path)
        self.race_scanner = RaceAnalytic()
        self.darwin = DarwinBridge()
        self.ollama_api = "http://localhost:11434/api/generate"
        self.git_exe = r"C:\Users\viper\git\cmd\git.exe"
        self.gh_exe = r"C:\Users\viper\scoop\apps\gh\current\bin\gh.exe"

    def log(self, msg, symbol="*"):
        print(f"[{symbol}] {msg}")
        sys.stdout.flush()

    def ping_llm(self, prompt):
        import requests
        try:
            payload = {"model": self.model, "prompt": prompt, "stream": False}
            response = requests.post(self.ollama_api, json=payload, timeout=30)
            return response.json().get("response", "")
        except: return ""

    def push_to_github(self, path):
        self.log("Commencing GitHub Deployment...", "DEPLOY")
        folder_name = os.path.basename(path).replace(" ", "_")
        os.chdir(path)
        env = os.environ.copy()
        env["PATH"] = r"C:\Users\viper\git\cmd;" + env["PATH"]

        subprocess.run([self.git_exe, "init"], capture_output=True)
        subprocess.run([self.git_exe, "add", "-A", "--force"], capture_output=True)
        subprocess.run([self.git_exe, "commit", "-m", "System: Darwinian Evolved Deployment"], capture_output=True)
        subprocess.run([self.git_exe, "branch", "-M", "main"], capture_output=True)

        check = subprocess.run([self.gh_exe, "repo", "view", folder_name], capture_output=True, env=env)
        if check.returncode != 0:
            subprocess.run([self.gh_exe, "repo", "create", folder_name, "--public", "--source=.", "--remote=origin", "--push"], env=env)
        else:
            subprocess.run([self.git_exe, "remote", "set-url", "origin", f"https://github.com/chrisalunlloyd2-sudo/{folder_name}.git"], capture_output=True)
            subprocess.run([self.git_exe, "push", "-u", "origin", "main", "--force"], env=env)

        url = f"https://github.com/chrisalunlloyd2-sudo/{folder_name}"
        self.log(f"Project Live: {url}", "SUCCESS")
        webbrowser.open(url)

    def run_evolution_loop(self, target_folder, project_intent):
        self.log(f"Initiating Darwinian Handshake: {project_intent}", "HPC")
        
        # In a real run, this would be derived from the AI Topology
        topology = ["main.py", "logic.py"]
        
        for page in topology:
            self.log(f"Evolving Page: {page}", "GENETIC")
            variants = []
            
            for i in range(2): # Quick test loop
                self.log(f"  > Creating Variant {i+1}...", "MUTATION")
                prompt = f"Develop {page} logic for {project_intent}. Context: Recursive file automation. Return ONLY code."
                code = self.ping_llm(prompt)
                
                # Race Condition Analytic
                hazards = self.race_scanner.analyze_concurrency(code)
                if hazards: self.log(f"  > [PURPLE FLAG] {len(hazards)} hazards identified.", "RACE")
                
                temp_path = self.build_lab / f"temp_{page}_{i}.py"
                with open(temp_path, "w", encoding="utf-8") as f:
                    f.write(code)
                
                fitness = self.darwin.evaluate(temp_path)
                variants.append({"code": code, "fitness": fitness})

            winner = max(variants, key=lambda x: x['fitness'])
            self.log(f"Winner Locked (Fitness: {winner['fitness']})", "WINNER")
            
            # Commit to SHA-256 Ledger
            h = self.ledger.commit_to_ledger(winner['code'], {"page": page}, winner['fitness'])
            self.log(f"Fingerprint: {h[:16]}...", "LEDGER")
            
            with open(os.path.join(target_folder, page), "w", encoding="utf-8") as f:
                f.write(winner['code'])

        # Final Ship to GitHub
        self.push_to_github(target_folder)
        self.log("PROJECT HANDOVER COMPLETE.", "SUCCESS")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        res = subprocess.run([r"C:\Users\viper\AppData\Local\Programs\Ollama\ollama.exe", "list"], capture_output=True, text=True)
        model = "h2o-danube3:4b" if "h2o-danube3" in res.stdout else "qwen2.5:0.5b"
        
        engine = SystemsPipelineEngine(model=model)
        engine.run_evolution_loop(sys.argv[1], "A recursive evolutionary project manager")
    else:
        print("No target provided.")
