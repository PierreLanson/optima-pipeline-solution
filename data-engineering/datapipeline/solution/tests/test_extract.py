import pandas as pd

from f1_pipeline import extract


def test_read_races_treats_null_as_missing(tmp_path):
    path = tmp_path / "races.csv"
    path.write_text("raceId,time\n1,null\n2,14:00:00\n")

    races = extract.read_races(path)

    assert pd.isna(races["time"][0])
    assert races["time"][1] == "14:00:00"


def test_read_results_treats_null_as_missing(tmp_path):
    path = tmp_path / "results.csv"
    path.write_text("raceId,position,fastestLapTime\n1,1,01:30.0\n1,null,null\n")

    results = extract.read_results(path)

    assert pd.isna(results["position"][1])
    assert pd.isna(results["fastestLapTime"][1])
    assert results["fastestLapTime"][0] == "01:30.0"
