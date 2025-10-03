#!/usr/bin/env bash
set -euo pipefail
REPO_NAME=${1:-dorkenum}
git init
git checkout -b main || true
git add .
git commit -m "chore: initial import of dorkenum package v0.2.2"
echo "Repository initialized locally. To push to GitHub:"
echo " 1) Create an empty repo on GitHub named $REPO_NAME"
echo " 2) git remote add origin git@github.com:<your-user>/$REPO_NAME.git"
echo " 3) git branch -M main"
echo " 4) git push -u origin main"
