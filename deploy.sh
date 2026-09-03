#!/bin/bash

# Deploy script for OpenSkill.Top
# Flow: build -> preview & confirm -> commit site/ to gh-pages (via git worktree) -> push
# The main working tree stays on your current branch the whole time.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# -y / --yes : skip confirmations (non-interactive mode)
ASSUME_YES=0
for arg in "$@"; do
  case "$arg" in
    -y|--yes) ASSUME_YES=1 ;;
  esac
done

confirm() {
  if [ "$ASSUME_YES" = "1" ]; then return 0; fi
  local reply
  read -p "$1" -n 1 -r reply
  echo
  [[ $reply =~ ^[Yy]$ ]]
}

# UTF-8 output for Python on Windows (avoid GBK encode errors in Git Bash)
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8

# --- Locate python / mkdocs (mkdocs may live in user Roaming Scripts, not in PATH) ---
command -v python >/dev/null 2>&1 || { echo "Error: python not found in PATH"; exit 1; }
if ! command -v mkdocs >/dev/null 2>&1; then
  for p in "$HOME"/AppData/Roaming/Python/Python*/Scripts "$HOME"/.local/bin; do
    [ -x "$p/mkdocs.exe" ] || [ -x "$p/mkdocs" ] || continue
    PATH="$p:$PATH"
    break
  done
fi
command -v mkdocs >/dev/null 2>&1 || { echo "Error: mkdocs not found in PATH"; exit 1; }

# --- Sanity checks ---
if [ ! -d .git ]; then
  echo "Error: Not a git repository"
  exit 1
fi

CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

if ! git diff-index --quiet HEAD -- 2>/dev/null; then
  echo "Warning: You have uncommitted changes:"
  git status --short
  confirm "Continue anyway? (y/N) " || { echo "Aborted."; exit 1; }
fi

# --- Build ---
echo ""
echo "Building site..."
./build.sh

# --- Preview & confirm (push only after you say yes) ---
echo ""
echo "Build output: site/"
echo "Preview before pushing:"
echo "  1) open site/index.html in your browser, or"
echo "  2) python -m http.server 8088 --directory site  ->  http://localhost:8088"
if ! confirm "Push site/ to origin/gh-pages now? (y/N) "; then
  echo "Push skipped. site/ is ready - re-run this script to push after reviewing."
  exit 0
fi

# --- Deploy via git worktree (no branch switching in the main working tree) ---
WORKTREE_DIR="../site-deploy"
echo ""
echo "Deploying via worktree at $WORKTREE_DIR ..."

# Recreate a clean worktree on gh-pages every run
git worktree remove --force "$WORKTREE_DIR" 2>/dev/null || true
rm -rf "$WORKTREE_DIR" 2>/dev/null || true
git worktree prune
git worktree add "$WORKTREE_DIR" gh-pages

# Replace worktree content (except .git) with the fresh build
find "$WORKTREE_DIR" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r site/. "$WORKTREE_DIR/"

git -C "$WORKTREE_DIR" add -A
if git -C "$WORKTREE_DIR" diff --cached --quiet; then
  echo "No changes to deploy."
else
  git -C "$WORKTREE_DIR" commit -m "Deploy site - $(date '+%Y-%m-%d %H:%M:%S')"
fi

if git -C "$WORKTREE_DIR" push origin gh-pages; then
  echo ""
  echo "Deployed! https://openskill.top/ will update in a few minutes."
  git worktree remove --force "$WORKTREE_DIR"
else
  echo ""
  echo "Push failed (network?). The worktree is kept at $WORKTREE_DIR - retry later with:"
  echo "  git -C $WORKTREE_DIR push origin gh-pages"
  exit 1
fi

echo ""
echo "Done!"
