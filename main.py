"""
Root launcher for AI TikTok Video Factory.
Delegates directly to ai-tiktok-factory/main.py.
"""

import os
import sys
from pathlib import Path

# Add ai-tiktok-factory to Python path
CURRENT_DIR = Path(__file__).resolve().parent
FACTORY_DIR = CURRENT_DIR / "ai-tiktok-factory"
if str(FACTORY_DIR) not in sys.path:
    sys.path.insert(0, str(FACTORY_DIR))

# Change current working directory to ai-tiktok-factory so relative paths align
os.chdir(str(FACTORY_DIR))

from main import main

if __name__ == "__main__":
    main()
