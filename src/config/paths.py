# src/config/paths.py
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_DATA = PROJECT_ROOT / 'data' / 'processed'
