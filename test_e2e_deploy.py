import sys
import os
import random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from DarwinianEngine_v8 import SystemsPipelineEngine

def test_randomized_e2e():
    engine = SystemsPipelineEngine()
    rand_id = random.randint(1000, 9999)
    target = os.path.join(os.getcwd(), f"E2E_Test_Deploy_{rand_id}")
    
    intents = [
        "A python CLI tool that generates a random password.",
        "A simple python web scraper using requests.",
        "A python script that calculates the Fibonacci sequence."
    ]
    
    intent = random.choice(intents)
    topology = ["main.py"]
    
    print("================================================")
    print(f"   TESTING PHASE 22: E2E DEPLOYMENT (ID: {rand_id})")
    print(f"   INTENT: {intent}")
    print("================================================")
    
    engine.get_program_out(target, intent, topology)

if __name__ == "__main__":
    test_randomized_e2e()
