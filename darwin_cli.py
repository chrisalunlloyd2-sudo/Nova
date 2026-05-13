import argparse
import sys
import os

# Ensure the directory containing DarwinianEngine_v8 is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from DarwinianEngine_v8 import SystemsPipelineEngine
except ImportError as e:
    print(f"Failed to import DarwinianEngine_v8: {e}")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Darwinian Evolutionary Engine CLI Hook")
    parser.add_argument("--target", required=True, help="Target folder for the generated project")
    parser.add_argument("--intent", required=True, help="Description/Intent of the project to generate")
    parser.add_argument("--topology", nargs="*", help="List of files to generate (e.g. main.py utils.py README.md). Defaults to main.py and logic_engine.py", default=["main.py", "logic_engine.py"])
    parser.add_argument("--model", default="qwen2.5:0.5b", help="Ollama model to use")
    
    args = parser.parse_args()
    
    target_folder = os.path.abspath(args.target)
    
    print("==================================================================")
    print("   DARWINIAN EVOLUTIONARY ENGINE - CLI HOOK                       ")
    print(f"   TARGET:   {target_folder}")
    print(f"   INTENT:   {args.intent}")
    print(f"   TOPOLOGY: {args.topology}")
    print(f"   MODEL:    {args.model}")
    print("==================================================================")
    
    engine = SystemsPipelineEngine(model=args.model)
    engine.get_program_out(target_folder, args.intent, args.topology)

if __name__ == "__main__":
    main()
