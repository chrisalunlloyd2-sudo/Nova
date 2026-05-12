import sys
import os

# Align with Systems Engineering Pipeline (100-Step Methodology)
# This script acts as the high-level entry point for the SystemsPipeline engine.

PIPELINE_DIR = r"C:\Users\viper\SystemsPipeline"
sys.path.append(PIPELINE_DIR)

try:
    from pipeline import SystemsPipeline
except ImportError:
    print(f"[FATAL] Could not locate pipeline.py in {PIPELINE_DIR}")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("[!] ERROR: No target folder provided.")
        print("[!] Please drag and drop a folder onto the .bat icon.")
        sys.exit(1)

    target_path = sys.argv[1]
    
    # Initialize and execute the full verified 100-step pipeline
    pipeline = SystemsPipeline()
    pipeline.run_full_pipeline(target_path)

if __name__ == "__main__":
    main()
