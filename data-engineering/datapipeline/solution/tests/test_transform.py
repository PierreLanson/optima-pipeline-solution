"""Using pytest test each function in transform.py"""

import pandas as pd

from f1_pipeline import transform


def test_build_race_datetime_fills_missing_time():
    races = pd.DataFrame({"date": ["2018-03-25"], "time": [None]})

    result = transform.build_race_datetime(races)

    assert result["race_datetime"][0] == "2018-03-25T00:00:00.000"


def test_build_race_datetime_joins_date_and_time():
    races = pd.DataFrame({"date": ["2024-07-07"], "time": ["14:00:00"]})

    result = transform.build_race_datetime(races)

    assert result["race_datetime"][0] == "2024-07-07T14:00:00.000"


def test_get_race_winners_keeps_only_position_one():
    results = pd.DataFrame(
        {
            "raceId": [1, 1, 2, 2],
            "driverId": [10, 20, 30, 40],
            "position": [1, 2, 1, None],
            "fastestLapTime": ["01:30.0", "01:29.0", "01:31.0", None],
        }
    )

    winners = transform.get_race_winners(results)

    assert list(winners["driverId"]) == [10, 30]


def test_build_race_stats_keeps_races_without_results():
    races = pd.DataFrame(
        {
            "raceId": [1, 2],
            "year": [2024, 2024],
            "round": [1, 2],
            "name": ["Race A", "Race B"],
            "date": ["2024-03-02", "2024-03-09"],
            "time": ["15:00:00", "17:00:00"],
        }
    )
    results = pd.DataFrame(
        {
            "raceId": [1],
            "driverId": [10],
            "position": [1],
            "fastestLapTime": ["01:30.0"],
        }
    )

    assert len(transform.build_race_stats(races, results)) == 2
