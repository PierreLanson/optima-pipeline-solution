"""Testing for load.py function write_yearly_files"""

import json

import pandas as pd

from f1_pipeline import load


def test_write_yearly_files_num_equals_num_of_files(tmp_path):
    # Make sure that the number of years in the data == number of files output

    stats = pd.DataFrame(
    {
        "year": [2023, 2024, 2024, 2025, 3000, 0],
        "Race Name": ["Race 1", "Race 2", "Race 3", "Race 4", "Race 5", "Race 6"], 
        "Race Round": [1, 1, 2, 3, 0, 500]
    }
    )

    load.write_yearly_files(stats, tmp_path)

    files = list(tmp_path.glob("stats_*.json"))

    assert len(files) == stats["year"].nunique()


def test_write_yearly_files_formatting(tmp_path):
    # Make sure that the formatting of fields is correct and nulls are corrected

    stats_DataFrame = pd.DataFrame(
    {
        "year": [2024, 2024, 2024, 2024],
        "Race Name": ["Race 1", "Race 2", "Race 3", "Race 4"], 
        "Race Round": [1, 1, 2, 0],
        "Race Winning driverId": pd.array([10, None, 20, 30], dtype= "Int64"),
        "Race Fastest Lap": ["01:30.0", None, "45:31.0", "00:00.1"]
    }
    )

    load.write_yearly_files(stats_DataFrame, tmp_path)
    path = tmp_path / "stats_2024.json"
    records = json.loads(path.read_text())

    assert "year" not in records[0]
    assert isinstance(records[0]["Race Round"], int)
    assert isinstance(records[0]["Race Winning driverId"], int)
    assert records[1]["Race Winning driverId"] is None
    assert records[1]["Race Fastest Lap"] is None
