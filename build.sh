#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip first
pip install --upgrade pip

# Install dependencies with verbose output
pip install --no-cache-dir --verbose -r requirements.txt

echo "Build completed successfully!"
