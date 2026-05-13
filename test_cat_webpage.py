import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from DarwinianEngine_v8 import SystemsPipelineEngine

def test_cat_webpage():
    engine = SystemsPipelineEngine()
    target = os.path.join(os.getcwd(), "CatWebpageTest")
    intent = "A full fake webpage about cats, autopopulate with cat facts and placeholder images."
    topology = ["index.html", "style.css", "script.js"]
    
    print("================================================")
    print("   TESTING PHASE 21: RE-INJECTION & HTML/CSS    ")
    print("================================================")
    
    engine.get_program_out(target, intent, topology)

if __name__ == "__main__":
    test_cat_webpage()
