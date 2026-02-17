#!/usr/bin/env bash
# create-structure.sh
# Creates the standard docs/ directory structure for a new project.
# Safe to run multiple times — skips directories that already exist.

set -e

echo "Setting up standard docs/ structure..."

# Create English doc directories
mkdir -p docs/specifications
mkdir -p docs/issue
mkdir -p docs/reference
mkdir -p docs/policy

# Create Korean mirror directories (dev/)
mkdir -p docs/dev/specifications
mkdir -p docs/dev/issue
mkdir -p docs/dev/policy

# Add .gitkeep files so Git tracks empty directories
# Only create if no other files exist in the directory yet
for dir in \
  docs/specifications \
  docs/issue \
  docs/reference \
  docs/policy \
  docs/dev/specifications \
  docs/dev/issue \
  docs/dev/policy
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
echo "  2. Claude will create initial policy files in docs/policy/"
echo "  3. Run /new-issue to create your first issue document"
