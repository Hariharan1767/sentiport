#!/usr/bin/env python
"""
Sentiport API Server Launcher
Starts the Flask API server without relying on system Python aliases
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Launch the API server"""
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    venv_python = project_root / '.venv' / 'Scripts' / 'python.exe'
    api_file = project_root / 'api_server.py'
    
    print("=" * 50)
    print("Sentiport API Server - Launcher")
    print("=" * 50)
    print()
    
    # Check if venv exists
    if not venv_python.exists():
        print(f"ERROR: Virtual environment not found at {venv_python}")
        print("Please run: python -m venv .venv")
        input("Press Enter to exit...")
        return 1
    
    # Check if Flask is installed
    try:
        result = subprocess.run(
            [str(venv_python), '-c', 'import flask'],
            capture_output=True,
            timeout=10
        )
        if result.returncode != 0:
            print("Flask not found. Installing dependencies...")
            subprocess.run(
                [str(venv_python), '-m', 'pip', 'install', '-q', '-r', 'requirements.txt'],
                cwd=str(project_root),
                capture_output=True,
                timeout=120
            )
    except Exception as e:
        print(f"Warning: Could not check Flask: {e}")
    
    # Start the API server
    print()
    print("=" * 50)
    print("Starting API Server...")
    print("=" * 50)
    print()
    print(f"API Server:    http://localhost:5000")
    print(f"Health Check:  http://localhost:5000/api/health")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    try:
        subprocess.run(
            [str(venv_python), str(api_file)],
            cwd=str(project_root)
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
