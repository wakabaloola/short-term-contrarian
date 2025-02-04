# src/utils/paths.py

from pathlib import Path


# SET PROJECT ROOT
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# DATA directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


# SCRIPTS, SRC, UTILS and TESTS directories 
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SRC_DIR = PROJECT_ROOT / "src"
UTILS_DIR = SRC_DIR / "utils"
TESTS_DIR = PROJECT_ROOT / "tests"


if __name__ == "__main__":
    print(f"PROJECT_ROOT = {PROJECT_ROOT}")
