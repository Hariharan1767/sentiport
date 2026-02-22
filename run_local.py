#!/usr/bin/env python3
"""
Local deployment script for Sentiport development environment
Starts the Flask API server and manages NLTK data downloads
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.absolute()
VENV_PATH = PROJECT_ROOT / '.venv'
PYTHON_EXE = VENV_PATH / 'Scripts' / 'python.exe' if sys.platform == 'win32' else VENV_PATH / 'bin' / 'python'


def check_venv():
    """Check if virtual environment exists"""
    if not VENV_PATH.exists():
        logger.error(f"Virtual environment not found at {VENV_PATH}")
        logger.info("Please run: python -m venv .venv")
        return False
    return True


def install_dependencies():
    """Install Python dependencies"""
    logger.info("Installing Python dependencies...")
    result = subprocess.run(
        [str(PYTHON_EXE), "-m", "pip", "install", "-r", str(PROJECT_ROOT / "requirements.txt")],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        logger.error(f"Failed to install dependencies: {result.stderr}")
        return False
    logger.info("✓ Dependencies installed")
    return True


def download_nltk_data():
    """Download required NLTK data"""
    logger.info("Downloading NLTK data...")
    nltk_script = """
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

datasets = ['punkt', 'wordnet', 'averaged_perceptron_tagger', 'stopwords', 'vader_lexicon']
for dataset in datasets:
    try:
        nltk.download(dataset, quiet=True)
        print(f"Downloaded {dataset}")
    except Exception as e:
        print(f"Failed to download {dataset}: {e}")
"""
    
    result = subprocess.run(
        [str(PYTHON_EXE), "-c", nltk_script],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        logger.warning(f"NLTK download had issues: {result.stderr}")
    else:
        logger.info("✓ NLTK data downloaded")
    return True


def start_api_server():
    """Start the Flask API server"""
    logger.info("Starting API server...")
    logger.info(f"Using Python: {PYTHON_EXE}")
    
    env = os.environ.copy()
    env['FLASK_APP'] = 'api_server.py'
    env['FLASK_ENV'] = 'development'
    env['PYTHONUNBUFFERED'] = '1'
    
    try:
        subprocess.run(
            [str(PYTHON_EXE), str(PROJECT_ROOT / "api_server.py")],
            cwd=str(PROJECT_ROOT),
            env=env
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        return True
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        return False


def main():
    """Main deployment function"""
    logger.info("=" * 50)
    logger.info("Sentiport Local Deployment")
    logger.info(f"Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)
    logger.info("")
    
    # Check virtual environment
    if not check_venv():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    logger.info("")
    
    # Download NLTK data
    if not download_nltk_data():
        logger.warning("NLTK data download had issues, continuing anyway...")
    
    logger.info("")
    
    # Start API server
    logger.info("=" * 50)
    logger.info("Starting Sentiport API Server")
    logger.info("=" * 50)
    logger.info("")
    logger.info("API Server:     http://localhost:5000")
    logger.info("API Health:     http://localhost:5000/api/health")
    logger.info("")
    logger.info("Frontend:       http://localhost:5173 (in separate terminal: npm run dev)")
    logger.info("")
    logger.info("Press Ctrl+C to stop the server")
    logger.info("")
    
    return start_api_server()


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
