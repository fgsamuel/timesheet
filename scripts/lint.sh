#!/bin/bash
set -e
# Project Folders
TARGET_FOLDERS="."
MAX_ACCEPTABLE_COMPLEXITY=6

# Run Tools
echo "Running isort"
isort $TARGET_FOLDERS
echo "Running black..."
black $TARGET_FOLDERS
echo "Running pycodestyle..."
pycodestyle $TARGET_FOLDERS
echo "Performing general code quality evaluation ..."
flake8 $TARGET_FOLDERS
echo "Running some static typing checking..."
mypy $TARGET_FOLDERS
echo "Checking for cyclomatic complexity"
flake8 --max-complexity $MAX_ACCEPTABLE_COMPLEXITY $TARGET_FOLDERS