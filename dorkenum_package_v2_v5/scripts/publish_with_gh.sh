#!/usr/bin/env bash
# Usage: ./scripts/publish_with_gh.sh <github-username> <repo-name> <version>
set -euo pipefail
USERNAME=${1:?Provide GitHub username}
REPO=${2:?Provide repository name}
VERSION=${3:?Provide version tag, e.g., v0.2.2}

# Create repo on GitHub (requires gh CLI authenticated)
gh repo create "$USERNAME/$REPO" --public --source=. --remote=origin --push

# Tag version
git tag -a "$VERSION" -m "Release $VERSION"
git push origin "$VERSION"

# Create release and upload ZIP
if [ -f "./dorkenum_package_v2_v5.zip" ]; then
  gh release create "$VERSION" "./dorkenum_package_v2_v5.zip" --title "dorkenum $VERSION" --notes-file RELEASE_DRAFT.md
else
  echo "Warning: package zip not found, skipping asset upload."
fi
