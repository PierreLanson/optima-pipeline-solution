"""Transform the raw F1 data into one row of stats per race in format"""

import pandas as pd


def build_race_datetime(races: pd.DataFrame) -> pd.DataFrame:
    """
    Add a race_datetime column by joining each race's date and time.
    Fix format to include miliseconds .000 as example shows.
    """

    races = races.copy()
    time = races["time"].fillna("00:00:00")
    races["race_datetime"] = races["date"] + "T" + time + ".000"
    return races


def get_race_winners(results: pd.DataFrame) -> pd.DataFrame:
    """For each race in results, return the winner (potition 1)."""

    winners = results[results["position"] == 1] 
    columns = ["raceId", "driverId", "fastestLapTime"]
    return winners[columns]


def build_race_stats(races: pd.DataFrame, results: pd.DataFrame) -> pd.DataFrame:
    """
    Join each race with its winner, one row per race.

    Races without results are still kept even with no winner or fastest lap.
    Columns are renamed to the JSON example output.
    """

    output_columns = {
    "name": "Race Name",
    "round": "Race Round",
    "race_datetime": "Race Datetime",
    "driverId": "Race Winning driverId",
    "fastestLapTime": "Race Fastest Lap"
    }
    
    races = build_race_datetime(races)
    winners = get_race_winners(results)

    stats = races.merge(
        winners, on="raceId", how="left", validate="one_to_one"
    )

    # Int64 used instead of int64 due to null handling missing values without turning ids into floats
    # Transparency - Claude spotted this bug of int64 vs Int64 but is rather neat
    stats["driverId"] = stats["driverId"].astype("Int64")
    stats = stats.sort_values(["year", "round"]).reset_index(drop=True)
    
    stats = stats.rename(columns=output_columns)

    columns = [
    "year",
    "Race Name",
    "Race Round",
    "Race Datetime",
    "Race Winning driverId",
    "Race Fastest Lap"
    ]
    
    return stats[columns]
