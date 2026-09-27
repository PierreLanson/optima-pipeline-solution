"""Write the race statistics to yearly JSON files."""

from pathlib import Path

import pandas as pd


def write_yearly_files(stats: pd.DataFrame, output_path: Path) -> None:
    """Write one stats_{year}.json file for each year in the data."""

    output_path.mkdir(parents=True, exist_ok=True)

    for year, group in stats.groupby("year"):
        group = group.drop(columns="year")
        path = output_path / f"stats_{year}.json"
        group.to_json(path, orient="records", indent=4, force_ascii=False)
