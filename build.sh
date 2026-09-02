#!/bin/bash

# Build script for OpenSkill.Top
# Single-route bilingual site (default zh at root, en under /en/) with Material for MkDocs

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Building OpenSkill.Top documentation..."
echo ""

# Clean previous build
echo "Cleaning previous build..."
rm -rf site

# Generate Skills homepage & detail pages from skills/*.md
echo "Generating Skills pages..."
python3 scripts/gen_skills.py 2>/dev/null || python scripts/gen_skills.py

# Build site
echo "Building site..."
mkdocs build

# Copy CNAME file if exists
if [ -f docs/CNAME ]; then
    echo "Copying CNAME file..."
    cp docs/CNAME site/
fi

# Remove "Made with Material for MkDocs" footer from all HTML files
# Use a portable sed: -i '' is BSD/macOS, -i without arg is GNU (Linux/MSYS/Git Bash).
# Detect GNU vs BSD by checking sed --version output.
echo "Removing MkDocs Material footer..."
remove_footer() {
  # BSD sed: sed -i '' '...' file
  # GNU sed: sed -i '...' file
  if sed --version >/dev/null 2>&1; then
    sed -i '/Made with/,/<\/a>/d' "$1"
  else
    sed -i '' '/Made with/,/<\/a>/d' "$1"
  fi
}
# Build the list first (avoids "file changed" warnings from find/sed interplay)
html_files=$(find site -name "*.html" -type f 2>/dev/null)
export -f remove_footer 2>/dev/null || true
if [ -n "$html_files" ]; then
  echo "$html_files" | while IFS= read -r f; do
    [ -f "$f" ] && remove_footer "$f"
  done
fi

echo ""
echo "Build complete!"
echo ""
echo "Output: site/"
echo ""
echo "To preview locally:"
echo "  cd site && python3 -m http.server 8000"
