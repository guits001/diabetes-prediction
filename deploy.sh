#!/bin/bash
# Streamlit Cloud Deployment Helper Script
# This script guides you through deploying to Streamlit Community Cloud

echo "🚀 Streamlit Cloud Deployment Setup"
echo "===================================="
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI not found. Install from: https://cli.github.com"
    echo ""
    echo "Alternative: Push manually using Git"
    echo "1. Create repo at https://github.com/new"
    echo "2. Run these commands:"
    echo ""
    echo "   git remote add origin https://github.com/YOUR_USERNAME/diabetes-prediction.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    exit 1
fi

echo "✅ GitHub CLI found"
echo ""

# Check if user is logged in
if ! gh auth status &> /dev/null; then
    echo "📝 Logging in to GitHub..."
    gh auth login
fi

echo ""
echo "📦 Creating GitHub repository..."

# Create repository
gh repo create diabetes-prediction \
    --public \
    --source=. \
    --remote=origin \
    --push \
    --description "Full Stack Healthcare Diabetes Prediction ML Project with Streamlit" || {
    echo ""
    echo "⚠️  Repository creation failed. You may already have this repo."
    echo "Skipping repo creation and pushing to existing repo..."
    git push -u origin main || {
        echo "❌ Push failed. Make sure remote is configured:"
        echo "   git remote add origin https://github.com/YOUR_USERNAME/diabetes-prediction.git"
        exit 1
    }
}

echo ""
echo "✅ Repository pushed successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://share.streamlit.io"
echo "2. Click 'New app'"
echo "3. Select:"
echo "   - Repository: YOUR_USERNAME/diabetes-prediction"
echo "   - Branch: main"
echo "   - File: app.py"
echo "4. Click Deploy"
echo ""
echo "Your app will be live at:"
echo "https://diabetes-prediction-YOUR_USERNAME.streamlit.app"
echo ""
echo "🎉 Done!"
