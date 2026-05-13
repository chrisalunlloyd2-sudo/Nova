import re
import math

class RecursiveSolver:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.iteration = 0

    def solve(self, expression):
        """Recursively breaks down and solves linear equations."""
        self.iteration += 1
        print(f"[RECURSION L{self.iteration}] Analyzing: {expression}")
        
        # Parse linear equation: a*x + b = c
        match = re.search(r'(\d+)\*x\s*([\+\-])\s*(\d+)\s*=\s*(\d+)', expression)
        if not match:
            raise ValueError("Expression format not recognized. Use 'a*x + b = c'")
        
        a, op, b, c = match.groups()
        a, b, c = int(a), int(b), int(c)
        
        # Step 1: Isolate a*x
        # a*x = c - b (if op is +) or a*x = c + b (if op is -)
        if op == '+':
            isolated_val = c - b
        else:
            isolated_val = c + b
            
        print(f"[LOGIC] Step 1: {a}*x = {isolated_val}")
        
        # Step 2: Solve for x
        x = isolated_val / a
        return x

    def verify(self, expression, solution):
        """Verifies the solution against the original expression."""
        match = re.search(r'(\d+)\*x\s*([\+\-])\s*(\d+)\s*=\s*(\d+)', expression)
        if not match: return False
        
        a, op, b, c = match.groups()
        a, b, c = int(a), int(b), int(c)
        
        if op == '+':
            return (a * solution + b) == c
        else:
            return (a * solution - b) == c

    def self_correct(self, failure_context):
        """Placeholder for evolutionary self-correction logic."""
        print(f"[CRITICAL] Failure in context: {failure_context}")
        print("[ACTION] Adjusting selection pressure and re-evaluating atoms...")
        return True
