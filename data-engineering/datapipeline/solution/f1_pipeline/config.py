"""File paths used by the F1 pipeline."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

RACES_CSV = BASE_DIR / "source-data" / "races.csv"
RESULTS_CSV = BASE_DIR / "source-data" / "results.csv"
OUTPUT_DIR = BASE_DIR / "results"
