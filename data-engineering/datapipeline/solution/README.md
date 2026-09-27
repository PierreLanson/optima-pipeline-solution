# F1 Race Statistics Pipeline

## Overview

Reads F1 race data from `races.csv` and `results.csv`, pairs each race with its winner,
and outputs one JSON file for each year. 

## How to run

### Prerequisites

- Python 3.11 or newer (built and tested with Python 3.13)
- The packages in `requirements.txt` (pandas and pytest)

### Run the pipeline

Built and tested on macOS. On Windows (PowerShell), activate the environment with
`.venv\Scripts\Activate.ps1` instead, and use `python` instead of `python3`.

```bash
git clone https://github.com/PierreLanson/optima-pipeline-solution.git
cd optima-pipeline-solution/data-engineering/datapipeline/solution
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

When it finishes, it prints where the files were written. The output is one
`stats_{year}.json` file per year in `data-engineering/datapipeline/results/`.

### Run the tests

From the `solution` folder, with the environment active:

```bash
pytest
```

All 8 tests should pass.

## How it works

The pipeline runs in three steps, started by `main.py`:

1. **Extract** (`extract.py`) reads the source data:
   - `races.csv`: one race per row, with its year, round, name, date and start time
   - `results.csv`: one row per driver per race, with their finishing position and fastest lap
2. **Transform** (`transform.py`) joins the two, giving each race its winner and
   the winner's fastest lap.
3. **Load** (`load.py`) writes one JSON file per year to the `results` folder.

`config.py` holds the file paths, so they're kept in one place.

## Requirements met

**Core requirements**

- One JSON file per year, named `stats_{year}.json`, in the `results` folder
- One entry per race in `races.csv`, with the keys `Race Name`, `Race Round`,
  `Race Datetime`, `Race Winning driverId` and `Race Fastest Lap`
- `Race Datetime` combines `date` and `time` (UTC), using `00:00:00` when the
  time is missing
- The winning driver is the one in position 1 in `results.csv`
- Values that are always numbers are written as numbers, not strings
- Built in Python inside the `solution` folder, and run with `main.py`
- Only the data in `source-data` is used
- This README explains how to run the pipeline

**Stretch goals**

-  Unit tests for every function with logic (see Stretch goals below)
- Cloud deployment notes: an outline of a simple AWS setup (see below)

## Supporting documentation

- **This README:** how to run the pipeline, how it works, assumptions and
  decisions, and stretch goals
- **Docstrings:** each module and function has a short description of what it does
- **Unit tests** in `tests/`, which also show how each function is expected to behave
- **Output files** in `data-engineering/datapipeline/results/`

## Assumptions and decisions

The brief doesn't specify how to handle every case in the data, so I made the following assumptions:

- **Fastest lap is the winner's fastest lap**, not the quickest lap by any driver.
  The brief's example (British Grand Prix 2024, `01:29.4`) is the winner's lap,
  even though other drivers set quicker laps in that race.
- **Races without results are kept.** 12 races in 2024 (from the Hungarian Grand
  Prix onwards) have no rows in `results.csv`. The brief says every race should
  appear, so they are included with `null` for the winner and fastest lap.
- **Missing start times become `00:00:00`**, as the brief says. This affects 6
  races in 2018.
- **The datetime matches the brief's example exactly**, including `.000` at the
  end. The source data has no milliseconds, so `.000` is used. Times
  are UTC.
- **Races are sorted by round** within each year.
- **Numbers are written as numbers.** `driverId` uses pandas' `Int64` type so
  that races with no winner don't turn every id into a decimal (e.g. `1.0`).
- **Date and time are joined as text**, because the source data is already in
  the right format. In production I would parse them with `pd.to_datetime` so
  that bad dates are caught.

## Stretch Goals

### Unit tests

There are 8 tests, covering missing values, formatting and outputs. Every function
with logic is tested. `main` isn't, because it only calls the other functions in
order. I checked it by running the pipeline.

Separately, the pipeline has a data quality check built in:
`validate="one_to_one"` in the join stops the pipeline if a race ever has more
than one winner.

### Cloud deployment notes

**A simple setup**

- **Storage:** An S3 bucket for races.csv and results.csv with the JSON output
  written to another S3 location.
- **Trigger:** the client wants the pipeline to run after each race, so it could
  start automatically when a new file arrives in S3, or on a schedule.
- **Compute:** at this size, the pipeline could run as an AWS Lambda function.

## Ideas for the client's YouTube videos

- **Highest number of different winners**:
  - A season with many different winners may suggest the races were more evenly
    matched.
  - Worth checking whether this came from closer racing or from incidents such as
    crashes, which would need more data than the current source files.
- **Most seasons raced**: which drivers appear in the most seasons, though the data
  covers just 2018–2024 so isn't a full career length
- **Most improved driver year on year**:
  - For each race, divide a driver's fastest lap by that race's average fastest
    lap, which gives a number around 1 (below 1 = faster than average)
  - Average these per driver per season, then compare each season to the next
    (year before ÷ year after > 1 means they improved)
  - Investigate the cause: is it the driver improving or a new car or team?

## What I learnt

- **Unit testing with pytest:** each test creates small made-up data (mainly edge
  cases, like 0 and missing values), calls a function, then uses `assert` to check
  the result. pytest runs every function whose name starts with `test_`. It's
  similar to LeetCode, where you add your own test cases to check the edge cases
  before submitting.
- **Naming conventions (PEP 8):** snake case for variables, upper case for fixed
  values and capital words for classes. The column names are a mix of styles
  because I kept the source columns as they are, used snake case for the one
  column I created, and matched the output keys to the brief.
- **Imports** go in a set order: built-in libraries, then installed ones (like
  pandas), then my own modules.
