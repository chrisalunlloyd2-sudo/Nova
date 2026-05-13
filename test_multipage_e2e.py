import sys
import os
import random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from DarwinianEngine_v8 import SystemsPipelineEngine

def test_multipage_e2e():
    engine = SystemsPipelineEngine()
    rand_id = random.randint(10000, 99999)
    target = os.path.join(os.getcwd(), f"MultiPage_E2E_{rand_id}")
    
    intent = "A complete multi-page python inventory management system."
    topology = ["main.py", "utils.py", "README.md", "INSTALL.md", "CHANGELOG.md", "Blueprint.md", "Roadmap.md"]
    
    print("==================================================================")
    print(f"   TESTING PHASE 23: MULTI-PAGE DOCUMENTATION E2E (ID: {rand_id})")
    print(f"   TOPOLOGY: {topology}")
    print("==================================================================")
    
    engine.get_program_out(target, intent, topology)

if __name__ == "__main__":
    test_multipage_e2e()
