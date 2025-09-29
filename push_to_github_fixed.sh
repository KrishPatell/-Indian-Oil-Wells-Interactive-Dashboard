#!/bin/bash

echo "🚀 Pushing Indian Oil Wells Dashboard to GitHub..."

# Navigate to project directory
cd "/Users/krishpatel/Downloads/Oil bussiness"

echo "📁 Current directory: $(pwd)"
echo "📄 Files in directory:"
ls -la

echo ""
echo "🔧 Initializing Git repository..."
git init

echo "📄 Adding all files to Git..."
git add .

echo "💾 Creating initial commit..."
git commit -m "Initial commit: Indian Oil Wells Interactive Dashboard with AI Chatbot

Features:
- Interactive maps of oil wells across India
- AI-powered chatbot for data queries
- Multiple visualization views (main, offshore, companies)
- Real-time API integration
- Responsive dashboard design
- State-wise well statistics
- Company-wise operations data

Data Source: Ministry of Petroleum and Natural Gas (as of April 1, 2021)"

echo "🔗 Adding remote origin..."
# Try different repository URLs
echo "Trying repository URL: https://github.com/KrishPatell/Indian-Oil-Wells-Interactive-Dashboard.git"
git remote add origin https://github.com/KrishPatell/Indian-Oil-Wells-Interactive-Dashboard.git

echo "⬆️ Setting main branch and pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo "🌐 Repository URL: https://github.com/KrishPatell/Indian-Oil-Wells-Interactive-Dashboard"
echo ""
echo "📋 Next steps:"
echo "1. Visit your repository on GitHub"
echo "2. Enable GitHub Pages (optional)"
echo "3. Share your project!"

