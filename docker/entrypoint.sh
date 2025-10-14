#!/bin/bash
set -e

echo "🚀 Starting RegressorMatrice CLI Environment..."
echo "Working Directory: $(pwd)"
echo "Python Version: $(python --version)"

# Execute the command provided in docker-compose.yml
exec "$@"
