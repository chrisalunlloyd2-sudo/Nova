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
        self.build_lab = Path(r"C:\Users\viper\build_lab")
        self.db_path = r"C:\Users\viper\SystemsPipeline\CodeLedger.db"
        self.ledger = CodeLedger(self.db_path)
        self.darwin = DarwinBridge()
        self.ollama_api = "http://localhost:11434/api/generate"

    def log(self, msg, symbol="*"):
        print(f"[{symbol}] {msg}")
        sys.stdout.flush()

    def run_fitness_test(self, code):
        """Phase: Natural Selection. AST + Subprocess Execution."""
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

    def extract_code(self, text):
        """Phase 18: Enhanced Extraction (Robust markdown handling)"""
        # Look for code blocks
        match = re.search(r'```(?:python)?\s*(.*?)\s*```', text, re.DOTALL | re.IGNORECASE)
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

    def run_scientific_evolution(self, target_folder, page, intent):
        self.log(f"Initiating Scientific Evolution for: {page}", "DARWIN")
        
        # 1. Initial Generation
        prompt = f"Systems Engineering Directive: Develop logic for {page}. Project: {intent}. Return ONLY valid Python code in a block. No conversation."
        raw_response = self.ping_llm(prompt)
        code = self.extract_code(raw_response)
        
        winner = False
        attempts = 0
        
        while not winner and attempts < 10:
            self.log(f"Iteration {attempts + 1}: Testing Fitness...", "TEST")
            
            # Save candidate for Darwinian evaluation
            cand_path = self.build_lab / f"candidate_{page}.py"
            with open(cand_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            fit, feedback = self.run_fitness_test(code)
            
            if fit:
                fitness_score = self.darwin.evaluate(cand_path)
                if fitness_score >= 100:
                    self.log(f"Winner Selected (Fitness: {fitness_score})", "SUCCESS")
                    winner = True
                    break
                else:
                    self.log(f"Low Fitness ({fitness_score}). Initiating Scientific Mutation...", "MUTATE")
            else:
                self.log(f"Logic Unfit: {feedback[:50]}...", "FIX")
            
            # 2. SCIENTIFIC METHOD FIX (Phase 18)
            # Formulate hypothesis and change 1 variable until fixed
            new_code, new_fitness, outcome = self.darwin.mutate_scientific(cand_path)
            if new_code and outcome == "HYPOTHESIS_VALIDATED":
                self.log(f"Hypothesis Validated! New Fitness: {new_fitness}", "WIN")
                code = new_code
            else:
                self.log("Hypothesis Rejected. Mutating via LLM feedback...", "GENETIC")
                prompt += f"\nFIX REQUIRED. Error: {feedback}. Previous Logic: {code}"
                code = self.ping_llm(prompt)
            
            attempts += 1
            time.sleep(0.5)

        if winner:
            # Commit to Ledger
            h = self.ledger.commit_to_ledger(code, {"page": page}, fitness_score)
            self.log(f"Checksummed and Ledgered: {h[:16]}...", "LEDGER")
            
            with open(os.path.join(target_folder, page), "w", encoding="utf-8") as f:
                f.write(code)
            return True
        return False

    def get_program_out(self, target_folder, intent):
        self.log(f"GOAL: GET PROGRAM OUT - {intent}", "HPC")
        # Derived topology (Step-Down)
        topology = ["main.py", "logic_engine.py"]
        
        for page in topology:
            success = self.run_scientific_evolution(target_folder, page, intent)
            if not success:
                self.log(f"FAILED TO GET PROGRAM OUT FOR {page}", "FATAL")
                return
        
        self.log("PROGRAM COMPLETED AND VERIFIED.", "FINISH")
        webbrowser.open(f"file:///{target_folder}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        engine = SystemsPipelineEngine()
        engine.get_program_out(sys.argv[1], "A self-correcting recursive math solver")
    else:
        print("No target.")
