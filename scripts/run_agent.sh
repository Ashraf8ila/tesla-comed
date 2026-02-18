#!/bin/bash

# Navigate to project directory
cd "$(dirname "$0")/.."

# Log start time
echo "[$(date)] Starting Tesla-Comed Agent..."

# Run the main script using the system python (or venv if configured)
# Using the path detected earlier: /Library/Developer/CommandLineTools/usr/bin/python3
/Library/Developer/CommandLineTools/usr/bin/python3 src/main.py

ExitCode=$?
echo "[$(date)] Finished with exit code $ExitCode"
exit $ExitCode
