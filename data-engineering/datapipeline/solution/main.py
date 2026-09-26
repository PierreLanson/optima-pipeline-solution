"""Run the F1 data pipeline."""

from f1_pipeline import config, extract, transform, load


def main() -> None:
    """Read the source data, build race statistics and write yearly files."""

    # Extract.py
    races = extract.read_races(config.RACES_CSV)
    results = extract.read_results(config.RESULTS_CSV)

    # Transform.py
    stats = transform.build_race_stats(races, results)

    # Load.py
    load.write_yearly_files(stats, config.OUTPUT_DIR)

    print(f"Pipeline finished. Files written to {config.OUTPUT_DIR}")


if __name__ == "__main__":
    main()
