import pandas as pd

from f1_pipeline import extract


def test_read_races_nulls(tmp_path):
    path = tmp_path / "races.csv"
    path.write_text("raceId,time\n1,null\n2,14:00:00\n")


def test_read_results_nulls(tmp_path):
    path = tmp_path / "results.csv"
    path.write_text("raceId,time\n1,null\n2,14:00:00\n")
