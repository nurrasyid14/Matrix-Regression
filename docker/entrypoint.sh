#!/bin/bash
set -e

echo "🚀 Starting Data Pipeline Environment..."
echo "Working Directory: $(pwd)"
echo "Python Version: $(python --version)"

# If a command is passed, run it. Otherwise, start a shell.
if [ "$#" -gt 0 ]; then
  exec "$@"
else
  exec bash
fi

ENTRYPOINT ["bash", "docker/entrypoint.sh"]
