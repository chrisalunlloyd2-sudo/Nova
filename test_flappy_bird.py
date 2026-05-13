import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from DarwinianEngine_v8 import SystemsPipelineEngine

def test_flappy_bird():
    engine = SystemsPipelineEngine()
    target = os.path.join(os.getcwd(), "FlappyBirdTest")
    intent = "A complete, production-ready Flappy Bird clone using pygame. Must include all graphics rendering, sound effects logic, main game loop, score tracking, start screen, and game over screen. This requires a very long script. Please write out the entire code without skipping any parts."
    topology = ["flappy_bird_main.py"]
    
    print("================================================")
    print("   TESTING PHASE 21: RE-INJECTION (FLAPPY BIRD) ")
    print("================================================")
    
    engine.get_program_out(target, intent, topology)

if __name__ == "__main__":
    test_flappy_bird()
