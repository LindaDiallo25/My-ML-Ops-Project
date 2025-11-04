#!/bin/bash

# Quick script to commit and push changes to GitHub

echo "=========================================
📤 Git Push Helper Script
========================================="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Please run from project root."
    exit 1
fi

echo "📊 Current Git Status:"
git status --short
echo ""

# Check for changes
if git diff-index --quiet HEAD --; then
    echo "✅ No changes to commit"
    exit 0
fi

echo "========================================="
echo "📝 Files to be committed:"
git status --short
echo "========================================="
echo ""

# Ask for commit message
read -p "Enter commit message (or press Enter for default): " commit_msg

if [ -z "$commit_msg" ]; then
    commit_msg="Update project files - $(date '+%Y-%m-%d %H:%M')"
fi

echo ""
echo "Commit message: $commit_msg"
echo ""

# Confirm
read -p "Proceed with commit and push? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "❌ Aborted"
    exit 0
fi

echo ""
echo "🔄 Committing changes..."

# Add all changes
git add .

# Commit
git commit -m "$commit_msg"

if [ $? -ne 0 ]; then
    echo "❌ Commit failed"
    exit 1
fi

echo "✅ Committed successfully"
echo ""

# Check current branch
current_branch=$(git rev-parse --abbrev-ref HEAD)
echo "📍 Current branch: $current_branch"
echo ""

# Push
echo "🚀 Pushing to origin/$current_branch..."
git push origin $current_branch

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================
✅ Successfully pushed to GitHub!
========================================="
    echo ""
    echo "🔗 View at: https://github.com/Andy-P626/ML-Ops-project"
    echo "📊 Actions: https://github.com/Andy-P626/ML-Ops-project/actions"
    echo ""
else
    echo ""
    echo "❌ Push failed. Check your network connection and GitHub credentials."
    echo ""
    echo "Try:"
    echo "  git push origin $current_branch"
    exit 1
fi
