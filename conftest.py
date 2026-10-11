import sys
from pathlib import Path

# Add project root to sys.path so test discovery can find modules like app and src
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
