import sys
import os
from logic_engine import RecursiveSolver

def main():
    print("================================================")
    print("   DARWINIAN SELF-CORRECTING MATH SOLVER v1.0   ")
    print("================================================")
    
    # Example problem that requires 'self-correction' or multi-step logic
    problem = "solve for x: 3*x + 12 = 30"
    
    solver = RecursiveSolver(max_depth=5)
    
    print(f"[INPUT] {problem}")
    try:
        solution = solver.solve(problem)
        print(f"[RESULT] x = {solution}")
        
        # Verify the solution
        if solver.verify(problem, solution):
            print("[STATUS] Solution Verified. Stability: 100%")
        else:
            print("[STATUS] Verification Failed. Initiating Mutation...")
            # In a real Darwinian system, this would trigger a re-evolution
            
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
