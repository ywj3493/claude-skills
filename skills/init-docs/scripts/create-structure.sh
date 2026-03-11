#!/usr/bin/env bash
# create-structure.sh
# Creates the standard docs/ directory structure for a new project.
# Safe to run multiple times — skips directories that already exist.

set -e

echo "Setting up standard docs/ structure..."

# Create English doc directories
mkdir -p docs/en/specifications
mkdir -p docs/en/issue
mkdir -p docs/en/policy

# Create Korean doc directories
mkdir -p docs/ko/specifications
mkdir -p docs/ko/issue
mkdir -p docs/ko/policy

# Create language-neutral reference directory
mkdir -p docs/reference

# Add .gitkeep files so Git tracks empty directories
# Only create if no other files exist in the directory yet
for dir in \
  docs/en/specifications \
  docs/en/issue \
  docs/en/policy \
  docs/ko/specifications \
  docs/ko/issue \
  docs/ko/policy \
  docs/reference
do
  if [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
    touch "$dir/.gitkeep"
  fi
done

echo ""
echo "Done. Created directory structure:"
find docs -type d | sort | sed 's/^/  /'
echo ""
echo "Next steps:"
echo "  1. Claude will create CLAUDE.md in the project root"
echo "  2. Claude will create initial policy files in docs/en/policy/"
echo "  3. Run /new-issue to create your first issue document"
