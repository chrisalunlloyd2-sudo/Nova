import shutil
import os
import subprocess
import re

SOURCE_PATH = r"C:\Users\viper\Desktop\NAS_SHARE\yourfile.txt"
DEST_PATH = r"C:\AutomationProject\yourfile.txt"

def transfer_file():
    try:
        print(f"Copying from {SOURCE_PATH} to {DEST_PATH}...")
        shutil.copy(SOURCE_PATH, DEST_PATH)
        print("File transferred successfully.")
    except Exception as e:
        print(f"Error during file transfer: {e}")

def sanitize_file(file_path):
    print("Sanitizing file to remove personal info and APIs...")
    try:
        # Try to read the file as text
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regular expressions for sensitive data
        patterns = [
            # Email Addresses
            (r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[REDACTED_EMAIL]'),
            # IPv4 Addresses (naive)
            (r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', '[REDACTED_IP]'),
            # Heuristic for API keys, secrets, tokens, passwords
            (r'(?i)(api[_-]?key|secret|token|password|auth)[\s:=]+[\'"][^\'"]+[\'"]', r'\1 = "[REDACTED_CREDENTIAL]"'),
            # Basic phone number heuristic
            (r'\+?\d{1,3}?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', '[REDACTED_PHONE]')
        ]

        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("Sanitization complete.")
    except UnicodeDecodeError:
        print("Warning: File appears to be binary or non-UTF8. Skipping sanitization.")
    except Exception as e:
        print(f"Error during sanitization: {e}")

def git_push():
    try:
        print("Adding to git...")
        subprocess.run([r"C:\Users\viper\git\cmd\git.exe", "add", "."], check=True)
        
        print("Committing to git...")
        status = subprocess.run([r"C:\Users\viper\git\cmd\git.exe", "status", "--porcelain"], capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.run([r"C:\Users\viper\git\cmd\git.exe", "commit", "-m", "Auto-update from Python"], check=True)
        else:
            print("No changes to commit.")
            
        print("Pushing to remote...")
        subprocess.run([r"C:\Users\viper\git\cmd\git.exe", "push", "origin", "main"], check=True)
        print("Git push complete.")
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
    except Exception as e:
        print(f"Unexpected error during git operations: {e}")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DEST_PATH), exist_ok=True)
    
    # 1. Transfer the file
    transfer_file()
    
    # 2. Sanitize the newly transferred file
    if os.path.exists(DEST_PATH):
        sanitize_file(DEST_PATH)
    
    # 3. Push to git
    git_push()
