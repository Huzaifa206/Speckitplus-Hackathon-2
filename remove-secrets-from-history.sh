#!/bin/bash

# Script to remove sensitive files from git history
# WARNING: This rewrites git history and requires force push

echo "⚠️  WARNING: This will rewrite git history!"
echo "⚠️  Make sure you have:"
echo "   1. Backed up your repository"
echo "   2. Rotated all exposed API keys and secrets"
echo "   3. Coordinated with team members (they'll need to re-clone)"
echo ""
read -p "Do you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

echo "Removing sensitive files from git history..."

# Use git filter-branch to remove files
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch phase-3/backend/.env .env.example phase-3/backend/.env.example' \
  --prune-empty --tag-name-filter cat -- --all

echo ""
echo "✓ Files removed from history"
echo ""
echo "Next steps:"
echo "1. Push with force: git push origin --force --all"
echo "2. Push tags with force: git push origin --force --tags"
echo "3. Notify team members to re-clone the repository"
echo ""
echo "⚠️  IMPORTANT: Rotate all exposed credentials immediately!"
echo "   - Gemini API key: https://makersuite.google.com/app/apikey"
echo "   - Database password: Your Neon dashboard"
