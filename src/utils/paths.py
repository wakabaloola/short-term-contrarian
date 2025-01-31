# src/utils/paths.py

from pathlib import Path

# Set project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Set data directory relative to project root
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Specify scripts, src and tests directories 
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"


if __name__ == "__main__":
    print("Checking project root is correct:")
    print(f"PROJECT_ROOT = {PROJECT_ROOT}")

