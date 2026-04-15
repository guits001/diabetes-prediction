@echo off
REM Streamlit Cloud Deployment Helper Script for Windows
REM This script guides you through deploying to Streamlit Community Cloud

echo 🚀 Streamlit Cloud Deployment Setup
echo ====================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed
    echo Install from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git is installed
echo.

REM Check git status
git status >nul 2>&1
if errorlevel 1 (
    echo ❌ Not in a git repository
    exit /b 1
)

echo ✅ Git repository initialized
echo.

echo 📋 Current git status:
git status
echo.

echo 🔐 GitHub Authentication:
echo.
echo Option 1: Use GitHub CLI (Automatic)
echo   - Install from https://cli.github.com
echo   - Then run: gh auth login
echo.
echo Option 2: Manual Push (What I recommend for now)
echo.
echo ======================================================
echo DEPLOYMENT STEPS:
echo ======================================================
echo.
echo Step 1: Create a GitHub repository
echo   - Go to https://github.com/new
echo   - Repository name: diabetes-prediction
echo   - Description: Full Stack Healthcare Diabetes Prediction ML Project
echo   - Make it PUBLIC (so Streamlit Cloud can access it)
echo   - Click Create
echo.
echo Step 2: Push your code to GitHub
echo   - Run these commands in PowerShell:
echo.
echo   git branch -M main
echo   git remote add origin https://github.com/YOUR_USERNAME/diabetes-prediction.git
echo   git push -u origin main
echo.
echo Step 3: Deploy to Streamlit Cloud
echo   - Go to https://share.streamlit.io
echo   - Click "New app"
echo   - GitHub repo: YOUR_USERNAME/diabetes-prediction
echo   - Branch: main
echo   - File: app.py
echo   - Click Deploy (takes 2-3 minutes)
echo.
echo Step 4: Share your live app!
echo   URL will be: https://diabetes-prediction-YOUR_USERNAME.streamlit.app
echo.
echo ======================================================
echo.
pause
