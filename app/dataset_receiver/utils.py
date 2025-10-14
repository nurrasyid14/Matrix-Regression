#utils.py

import os

def check_file_exists(path: str):
    """Check if a given file path exists."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return True
