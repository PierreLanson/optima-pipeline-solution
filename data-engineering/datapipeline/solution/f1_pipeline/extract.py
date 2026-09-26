"""Read the raw F1 source data."""

from pathlib import Path
import pandas as pd

def read_races(path: Path) -> pd.DataFrame:
    """Reads races CSV and returns as a dataframe"""
    return pd.read_csv(path, na_values=["null"])


def read_results(path: Path) -> pd.DataFrame:
    """Reads results CSV and returns as a dataframe"""
    return pd.read_csv(path, na_values=["null"])
