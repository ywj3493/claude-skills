#!/usr/bin/env bash
# create-structure.sh
# Creates the standard docs/ directory structure for a new project.
#
# Usage: create-structure.sh [<source-lang> [<translation-lang>...]]
#   e.g. create-structure.sh          (defaults to source language "en", no translations)
#        create-structure.sh en       (same as the default)
#        create-structure.sh en ko    (also create the ko mirror tree — used by
#                                      sync-translations when mirroring is enabled later)
#
# Safe to run multiple times — skips directories and files that already exist.

set -e

LANGS=("$@")
if [ ${#LANGS[@]} -eq 0 ]; then
  LANGS=(en)
fi

echo "Setting up standard docs/ structure for languages: ${LANGS[*]}..."

# Create one directory tree per language
for lang in "${LANGS[@]}"; do
  mkdir -p "docs/$lang/specifications" "docs/$lang/issue" "docs/$lang/policy"
done

# Create language-neutral reference directory
mkdir -p docs/reference

# Add .gitkeep files so Git tracks empty directories
# Only create if no other files exist in the directory yet
for lang in "${LANGS[@]}"; do
  for sub in specifications issue policy; do
    dir="docs/$lang/$sub"
    if [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
      touch "$dir/.gitkeep"
    fi
  done
done
if [ -z "$(ls -A docs/reference 2>/dev/null)" ]; then
  touch docs/reference/.gitkeep
fi

# Create top-level specification template files if they don't exist
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REFERENCES_DIR="$SCRIPT_DIR/../references"

for spec_file in architecture config infrastructure; do
  for lang in "${LANGS[@]}"; do
    target="docs/$lang/specifications/$spec_file.md"
    if [ ! -f "$target" ]; then
      if [ -f "$REFERENCES_DIR/$spec_file-template.md" ]; then
        cp "$REFERENCES_DIR/$spec_file-template.md" "$target"
      else
        touch "$target"
      fi
    fi
  done
done

# Record the language configuration if not already present
if [ ! -f docs/config.yml ]; then
  {
    echo "# Documentation language configuration — read by documentation skills."
    echo "# source_language: language of authored documents (docs/<source_language>/)"
    echo "# translation_languages: mirror languages kept in sync by sync-translations"
    echo "source_language: ${LANGS[0]}"
    if [ ${#LANGS[@]} -gt 1 ]; then
      echo "translation_languages:"
      for lang in "${LANGS[@]:1}"; do
        echo "  - $lang"
      done
    else
      echo "translation_languages: []"
    fi
  } > docs/config.yml
  echo "Wrote docs/config.yml"
fi

echo ""
echo "Done. Created directory structure:"
find docs -type d | sort | sed 's/^/  /'
echo ""
echo "Next steps:"
echo "  1. Claude will create CLAUDE.md in the project root"
echo "  2. Claude will create initial policy files in docs/${LANGS[0]}/policy/"
echo "  3. Create your first issue (GitHub Issue or docs/${LANGS[0]}/issue/issue001.md)"
echo "  4. Run /dev-docs:sync-translations later to add translation mirrors"
