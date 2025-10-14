#!/bin/bash
set -e

echo "🚀 Starting Regressor Matrice Flask App..."
echo "Working Directory: $(pwd)"
echo "Python Version: $(python --version)"

# Start Flask app
if [ "$#" -gt 0 ]; then
    exec "$@"
else
    exec flask run --host=0.0.0.0 --port=5000
fi
