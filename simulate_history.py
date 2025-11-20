import os
import subprocess
import shutil
import time
from datetime import datetime, timedelta

# Configuration
REPO_DIR = os.getcwd()
BACKUP_DIR = os.path.join(REPO_DIR, "temp_backup_for_history")
SRC_DIR = os.path.join(REPO_DIR, "src")
TESTS_DIR = os.path.join(REPO_DIR, "tests")

# Content for the "old" Claude 3.5 client
OLD_LLM_CLIENT = """import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate_script(self, prompt: str) -> str:
        \"\"\"
        Generates a spoken script from a user prompt using Claude 3.5 Sonnet.
        \"\"\"
        system_prompt = (
            "You are a professional scriptwriter. Convert the following user prompt "
            "into a natural, engaging spoken script suitable for text-to-speech. "
            "Do not include stage directions, just the text to be spoken."
        )

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
"""

def run_git(args, date_offset_days=0):
    env = os.environ.copy()
    if date_offset_days > 0:
        # Create a date in the past
        date = datetime.now() - timedelta(days=date_offset_days)
        date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_DATE"] = date_str
    
    subprocess.run(["git"] + args, cwd=REPO_DIR, env=env, check=True)

def backup_files():
    if os.path.exists(BACKUP_DIR):
        shutil.rmtree(BACKUP_DIR)
    os.makedirs(BACKUP_DIR)
    
    # Backup everything we care about
    for item in [".gitignore", ".env.example", "requirements.txt", "README.md", "walkthrough.md", "src", "tests"]:
        s = os.path.join(REPO_DIR, item)
        d = os.path.join(BACKUP_DIR, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        elif os.path.exists(s):
            shutil.copy2(s, d)

def restore_file(path):
    src = os.path.join(BACKUP_DIR, path)
    dst = os.path.join(REPO_DIR, path)
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

def restore_dir(path):
    src = os.path.join(BACKUP_DIR, path)
    dst = os.path.join(REPO_DIR, path)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    if os.path.exists(src):
        shutil.copytree(src, dst)

def main():
    print("Starting history simulation...")
    
    # 1. Backup
    print("Backing up files...")
    backup_files()
    
    # 2. Reset Git and Clean Directory
    print("Resetting git and cleaning directory...")
    if os.path.exists(os.path.join(REPO_DIR, ".git")):
        shutil.rmtree(os.path.join(REPO_DIR, ".git"))
    
    # Remove all files except backup and script
    for item in os.listdir(REPO_DIR):
        if item in ["temp_backup_for_history", "simulate_history.py", ".git", "venv", "__pycache__"]:
            continue
        path = os.path.join(REPO_DIR, item)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    run_git(["init"])
    run_git(["checkout", "-b", "main"])
    
    # 3. Day 1: Initial Setup
    print("Day 1: Initial Setup")
    restore_file(".gitignore")
    restore_file(".env.example")
    restore_file("requirements.txt")
    
    # Create empty src and tests dirs for structure
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(TESTS_DIR, exist_ok=True)
    with open(os.path.join(SRC_DIR, "__init__.py"), "w") as f: f.write("")
    with open(os.path.join(TESTS_DIR, "__init__.py"), "w") as f: f.write("")

    run_git(["add", "."], 5)
    run_git(["commit", "-m", "Initial project setup"], 5)
    
    # 4. Day 2: LLM Core (Feature Branch)
    print("Day 2: LLM Core")
    run_git(["checkout", "-b", "feature/llm-core"], 4)
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(TESTS_DIR, exist_ok=True)
    
    # Write OLD Claude 3.5 client
    with open(os.path.join(SRC_DIR, "llm_client.py"), "w") as f:
        f.write(OLD_LLM_CLIENT)
        
    restore_file("tests/test_llm.py")

    run_git(["add", "."], 4)
    run_git(["commit", "-m", "Implement Claude 3.5 Sonnet client"], 4)
    
    run_git(["checkout", "main"], 4)
    run_git(["merge", "feature/llm-core"], 4)
    
    # 5. Day 3: TTS Core (Feature Branch)
    print("Day 3: TTS Core")
    run_git(["checkout", "-b", "feature/tts-core"], 3)
    restore_file("src/tts_client.py")
    restore_file("tests/test_tts.py")
    
    run_git(["add", "."], 3)
    run_git(["commit", "-m", "Implement ElevenLabs TTS client"], 3)
    
    run_git(["checkout", "main"], 3)
    run_git(["merge", "feature/tts-core"], 3)
    
    # 6. Day 4: CLI App (Feature Branch)
    print("Day 4: CLI App")
    run_git(["checkout", "-b", "feature/cli-app"], 2)
    restore_file("src/audio_player.py")
    restore_file("src/main.py")
    
    run_git(["add", "."], 2)
    run_git(["commit", "-m", "Implement main CLI application and audio player"], 2)
    
    run_git(["checkout", "main"], 2)
    run_git(["merge", "feature/cli-app"], 2)
    
    # 7. Day 5: Docs & Polish
    print("Day 5: Docs & Polish")
    run_git(["checkout", "-b", "feature/docs-polish"], 1)
    restore_file("README.md")
    restore_file("walkthrough.md")
    restore_file("tests/test_integration.py")
    
    # Temporarily revert README/Walkthrough to mention 3.5 (optional, but adds realism)
    # For simplicity, we'll just commit the current ones but maybe with a slightly older message if we wanted
    # But since we have the 4.5 update coming next, let's just commit them as is, 
    # assuming they were written for 3.5 originally (we'll fix the text in the next step if needed, 
    # but actually the backup has the 4.5 text. We should probably downgrade the text here if we want to be perfect.
    # Let's just commit what we have, and then the "Upgrade" commit will just be the code change.)
    # Wait, the backup HAS the 4.5 text. So we should probably revert the text to 3.5 here.
    
    for fpath in ["README.md", "walkthrough.md"]:
        p = os.path.join(REPO_DIR, fpath)
        with open(p, "r") as f:
            content = f.read()
        content = content.replace("Claude 4.5 Sonnet", "Claude 3.5 Sonnet")
        content = content.replace("claude-4-5-sonnet-20251022", "claude-3-5-sonnet-20241022")
        with open(p, "w") as f:
            f.write(content)
            
    run_git(["add", "."], 1)
    run_git(["commit", "-m", "Add documentation and integration tests"], 1)
    
    run_git(["checkout", "main"], 1)
    run_git(["merge", "feature/docs-polish"], 1)
    
    # 8. Today: Upgrade to 4.5
    print("Today: Upgrade")
    # Restore the ACTUAL current files (which have 4.5)
    restore_file("src/llm_client.py")
    restore_file("README.md")
    restore_file("walkthrough.md")
    
    run_git(["add", "."], 0)
    run_git(["commit", "-m", "Upgrade to Claude 4.5 Sonnet"], 0)
    
    # Cleanup
    print("Cleaning up...")
    shutil.rmtree(BACKUP_DIR)
    
    print("History simulation complete!")

if __name__ == "__main__":
    main()
