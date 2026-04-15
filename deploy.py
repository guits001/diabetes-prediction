#!/usr/bin/env python3
"""
Streamlit Cloud Deployment Assistant
Helps you deploy the diabetes prediction app to Streamlit Community Cloud
"""

import subprocess
import sys
import webbrowser
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def run_command(cmd, description=""):
    """Run a shell command and return success status"""
    if description:
        print(f"  {description}...", end=" ", flush=True)
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            if description:
                print_success("")
            return True, result.stdout
        else:
            if description:
                print_error("")
            return False, result.stderr
    except Exception as e:
        if description:
            print_error(f" ({str(e)})")
        return False, str(e)

def check_git_installed():
    """Verify git is installed and configured"""
    print_header("Step 1: Verify Git")
    
    success, _ = run_command("git --version", "Checking Git installation")
    if not success:
        print_error("Git is not installed!")
        print_info("Install from: https://git-scm.com/download/win")
        return False
    
    success, output = run_command("git config user.name", "Checking Git configuration")
    if not success or not output.strip():
        print_warning("Git user not configured. Setting up...")
        run_command('git config --global user.email "dataproject@local"', "Setting email")
        run_command('git config --global user.name "Data Scientist"', "Setting name")
    
    return True

def check_git_repo():
    """Verify we're in a git repository"""
    print_header("Step 2: Verify Repository")
    
    success, _ = run_command("git status", "Checking git repository")
    if not success:
        print_error("Not in a git repository!")
        return False
    
    print_success("Git repository initialized")
    return True

def check_requirements():
    """Verify requirements.txt exists"""
    print_header("Step 3: Verify Project Files")
    
    required_files = ['app.py', 'requirements.txt', 'models/diabetes_model.pkl']
    all_exist = True
    
    for file in required_files:
        if Path(file).exists():
            print_success(f"Found: {file}")
        else:
            print_error(f"Missing: {file}")
            all_exist = False
    
    return all_exist

def show_deployment_instructions():
    """Display deployment instructions"""
    print_header("Deployment Instructions")
    
    instructions = """
🔐 STEP 1: Create a GitHub Repository
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Go to: https://github.com/new
2. Repository name: diabetes-prediction
3. Description: Full Stack Healthcare Diabetes Prediction
4. Make it PUBLIC (required for Streamlit Cloud)
5. Click "Create repository"

📤 STEP 2: Push Your Code to GitHub
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run these commands in PowerShell/Terminal from your project directory:

  git branch -M main
  git remote add origin https://github.com/<YOUR_USERNAME>/diabetes-prediction.git
  git push -u origin main

(Replace <YOUR_USERNAME> with your actual GitHub username)

🚀 STEP 3: Deploy to Streamlit Cloud
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Click: https://share.streamlit.io
2. Click "New app"
3. Login with GitHub
4. Fill in the form:
   - GitHub repo: <YOUR_USERNAME>/diabetes-prediction
   - Branch: main
   - File path: app.py
5. Click "Deploy"

⏱️  STEP 4: Wait for Deployment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Initial deployment takes 2-3 minutes
- You'll see "Your app is loading..." then the live app
- URL: https://diabetes-prediction-<YOUR_USERNAME>.streamlit.app

📲 STEP 5: Share Your App!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Copy your deployed URL
- Share with friends
- They can use it immediately (no installation needed!)
"""
    
    print(instructions)

def main():
    print_header("🚀 Streamlit Cloud Deployment Assistant")
    print_info("This will help deploy your diabetes prediction app online")
    print_info("Takes ~5 minutes + 2 mins deployment time on Streamlit Cloud\n")
    
    # Check prerequisites
    if not check_git_installed():
        sys.exit(1)
    
    if not check_git_repo():
        sys.exit(1)
    
    if not check_requirements():
        print_warning("Some project files are missing!")
        print_info("Make sure you've run the Jupyter notebook completely")
    
    # Show deployment instructions
    show_deployment_instructions()
    
    # Ask if they want to open Streamlit Cloud
    print_header("Next Step")
    response = input("Open Streamlit Cloud in your browser? (y/n): ").lower().strip()
    
    if response == 'y':
        print_info("Opening https://share.streamlit.io...")
        webbrowser.open("https://share.streamlit.io")
    
    print_header("Ready to Deploy!")
    print_success("Your project is ready for Streamlit Cloud deployment!")
    print_info("Follow the steps above and your app will be live in minutes!")
    print()

if __name__ == "__main__":
    main()
