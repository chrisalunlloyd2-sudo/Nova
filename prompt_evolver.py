import os
import json
import requests
import ast
import re
import time
import random
from pathlib import Path

# PHASE 24: PROMPT GENETICS & PERFORMATIVE EVOLUTION ENGINE
# GOAL: Darwinistically evolve prompts to maximize LLM "Performatives"

class PromptEvolver:
    def __init__(self, model="qwen2.5:0.5b"):
        self.model = model
        self.ollama_api = "http://localhost:11434/api/generate"
        self.build_lab = Path(r"C:\Users\viper\build_lab")
        self.log_file = r"C:\Users\viper\Desktop\AutomationProject\PROMPT_EVOLUTION_LOG.json"
        self.best_prompt_file = r"C:\Users\viper\Desktop\AutomationProject\BEST_PROMPT.txt"
        
        # Seed Prompt
        self.seed_prompt = "Systems Engineering Directive: Write the complete Python implementation for {page} to fulfill the intent: {intent}. Provide the code in a markdown block. Absolute zero preamble or postamble. Direct code output only."
        
        self.benchmark_tasks = [
            {"page": "math_util.py", "intent": "A function to calculate prime factors of a number"},
            {"page": "file_handler.py", "intent": "A class that reads a JSON file and returns a specific key"},
            {"page": "string_cleaner.py", "intent": "A function that uses regex to strip all non-alphanumeric characters"}
        ]

    def log(self, msg):
        print(f"[GENETICS] {msg}")

    def ping_llm(self, prompt, system=""):
        try:
            payload = {"model": self.model, "prompt": prompt, "system": system, "stream": False}
            response = requests.post(self.ollama_api, json=payload, timeout=30)
            return response.json().get("response", "")
        except: return ""

    def mutate_prompt(self, parent_prompt):
        """Uses the LLM to mutate the prompt text itself."""
        mutation_prompt = f"""
        Act as a Prompt Engineer. Your goal is to mutate the following 'Parent Prompt' to be more 'Performative'.
        Performatives in prompt engineering mean:
        1. Higher density of actual code.
        2. Absolute zero conversational filler.
        3. Strict adherence to technical constraints.
        4. Triggering the LLM to think in 'Systems Engineering' patterns.

        Parent Prompt: "{parent_prompt}"

        Provide ONE new variation of this prompt. Use synonyms, change the tone (e.g., more authoritative, more scientific), or add 'Performative' keywords.
        Return ONLY the mutated prompt string.
        """
        return self.ping_llm(mutation_prompt).strip().replace('"', '')

    def measure_fitness(self, prompt_variant, fast=True):
        """Tests the prompt against benchmark tasks. 'fast' mode uses only 1 task."""
        total_score = 0
        tasks = self.benchmark_tasks[:1] if fast else self.benchmark_tasks
        
        for task in tasks:
            test_prompt = prompt_variant
            for key, val in task.items():
                test_prompt = test_prompt.replace(f"{{{key}}}", val)
            test_prompt = re.sub(r'\{.*?\}', '', test_prompt)
            raw_output = self.ping_llm(test_prompt)
            
            match = re.search(r'```(?:python)?\s*(.*?)\s*```', raw_output, re.DOTALL | re.IGNORECASE)
            code = match.group(1).strip() if match else raw_output.strip()
            
            score = 0
            ast_ok = False
            try:
                if code.strip(): # Empty code is NOT valid for our purposes
                    ast.parse(code)
                    score += 50
                    ast_ok = True
            except: pass
            
            no_yap = "Here is" not in raw_output and "Sure" not in raw_output
            if no_yap: score += 20
            
            length_ok = len(code) > 20 and len(code) < 1500
            if length_ok: score += 15
            
            struct_ok = "def " in code or "class " in code
            if struct_ok: score += 15
            
            self.log(f"DEBUG: Task: {task['page']}, AST: {ast_ok}, NoYap: {no_yap}, Len: {length_ok}, Struct: {struct_ok}, Final: {score}")
            if not length_ok or not struct_ok:
                self.log(f"DEBUG: Raw Code Snippet (first 50 chars): {repr(code[:50])}")
            total_score += score
            
        return total_score / len(tasks)

    def evolve(self, generations=1, variations_per_gen=10):
        self.log(f"Starting Evolution: {generations} Generations, {variations_per_gen} Variations/Gen")
        
        current_best_prompt = self.seed_prompt
        if os.path.exists(self.best_prompt_file):
            with open(self.best_prompt_file, "r") as f:
                current_best_prompt = f.read().strip()
                
        best_fitness = self.measure_fitness(current_best_prompt, fast=False)
        self.log(f"Initial Fitness: {best_fitness}")
        
        history = []
        hall_of_fame = [(best_fitness, current_best_prompt)]

        for gen in range(generations):
            self.log(f"--- GENERATION {gen + 1} ---")
            
            for i in range(variations_per_gen):
                parent_fitness, parent_prompt = random.choice(hall_of_fame)
                mutated = self.mutate_prompt(parent_prompt)
                if "{page}" not in mutated or "{intent}" not in mutated:
                    mutated = mutated.replace("page", "{page}").replace("intent", "{intent}")
                
                # Screening
                fitness = self.measure_fitness(mutated, fast=True)
                
                if fitness >= 100:
                    # Thorough check
                    refined_fitness = self.measure_fitness(mutated, fast=False)
                    if refined_fitness > best_fitness:
                        self.log(f"APEX PROMPT EVOLVED! Score: {refined_fitness}")
                        best_fitness = refined_fitness
                        current_best_prompt = mutated
                        hall_of_fame.append((best_fitness, mutated))
                        hall_of_fame = sorted(hall_of_fame, key=lambda x: x[0], reverse=True)[:5]
                        
                        with open(self.best_prompt_file, "w") as f:
                            f.write(current_best_prompt)
                
                history.append({"gen": gen, "variant": i, "prompt": mutated, "score": fitness})

        self.log(f"Evolution Cycle Complete. Apex Prompt: {current_best_prompt}")
        return current_best_prompt

if __name__ == "__main__":
    evolver = PromptEvolver()
    # Running 50 variations to reach the 100 variation milestone.
    evolver.evolve(generations=1, variations_per_gen=50)
