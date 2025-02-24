# TV Ratings to CSV

There are two tools (plus a shell script) in this repo:

| File | Description |
| ---- | ----------- |
| getratings.py | A CLI tool to extract TV ratings from [Adweek's TV Newser Rating](https://www.adweek.com/category/ratings/) pages and generate CSV data for further analysis. |
| create_charts.py | Generate charts from the CSV files |
| generate.sh | Example of how to retrieve ratings data |

## Installation

### Prerequisites

Ensure you have Python installed (recent version 3.x required). You will also need:

- `requests` (for fetching web pages)
- `beautifulsoup4` (for parsing HTML)
- `pandas` (for creating charts)

### Install Dependencies

Run the following command to install dependencies:

```sh
pip install -f requirements.txt
```



# getratings.py

## Key Features

✅ Fetches TV ratings from a given URL.
✅ Can extract either the 25-55 demographic or the total viewers counts
✅ Outputs CSV format to `stdout` (default) or a file (`--output`).
✅ Supports appending or overwriting files.
✅ Allows specifying a custom date (`--date`). 

---



## Typical Usage

The code is designed to create/append to a CSV file with the ratings for a single day from the Adweek ratings pages.

```sh
# Extract the 25-55 demographic
python getratings.py --input "https://www.adweek.com/tvnewser/thursday-feb-20-evening-cable-news-ratings-the-five-is-1st-in-total-viewers/" --date 2025-02-20 --output ratings-25-55.csv
 
# Extract the Total viewers
python getratings.py --input "https://www.adweek.com/tvnewser/thursday-feb-20-evening-cable-news-ratings-the-five-is-1st-in-total-viewers/" --date 2025-02-20 --table 2 --output ratings-total.csv

```

By default, it will create the file if it does not exist and generate CSV headers for the first row.  If the file does exist, it will append new rows to the file (without generating a redundant CSV header).



## Options and Behavior

With no options, the program expects a URL on stdin and will generate a CSV file on stdout, using the current date as the date for the data.

The following options are supported (some of which you will most likely want to use)

| Option              | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| `--input <URL>`     | URL of the webpage to scrape (reads from stdin if not provided). |
| `--output <file>`   | Output file to write CSV data (default: stdout).             |
| `--overwrite`       | Overwrites the output file instead of appending.             |
| `--no-header`       | Suppresses the CSV header row (default for existing files, not default for new files) |
| `--date YYYY-MM-DD` | Specify a custom date for the CSV (default: today’s date).   |
| `--table <n>`       | Fetches the nth table in the page (table 1, the 25-55 demo is the default; table 2 is the total viewers) |

### Simplest Usage (Fetch from a URL and print CSV)

```sh
python getratings.py --input "https://www.adweek.com/tvnewser/monday-february-17-2025-evening-cable-news-ratings/"
```

### Read URL from stdin
```sh
echo "https://www.adweek.com/tvnewser/monday-february-17-2025-evening-cable-news-ratings/" | python getratings.py
```

### Write to a File (Appends by Default)
```sh
python getratings.py --input "https://www.adweek.com/tvnewser/monday-february-17-2025-evening-cable-news-ratings/" --output ratings.csv
```

### Overwrite the Output File
```sh
python getratings.py --input "https://www.adweek.com/tvnewser/monday-february-17-2025-evening-cable-news-ratings/" --output ratings.csv --overwrite
```

### Suppress CSV Header (Useful for Appending Multiple Runs)
```sh
python getratings.py --input "https://www.adweek.com/tvnewser/monday-february-17-2025-evening-cable-news-ratings/" --output ratings.csv --no-header
```

### Specify a Custom Date

Note that the program does not extract the air date from the web page and will default to today.  You should almost always supply this so your data is labeled correctly.

```sh
python getratings.py --input "https://www.adweek.com/tvnewser/monday-february-17-2025-evening-cable-news-ratings/" --date 2025-02-17
```

### Append Multiple Runs into a Single File Without Headers
```sh
python getratings.py --input "https://www.adweek.com/tvnewser/monday-february-17-2025-evening-cable-news-ratings/" --output ratings.csv --no-header --date 2025-02-17
python getratings.py --input "https://www.another-news-source.com/ratings/" --output ratings.csv --no-header --date 2025-02-18
```

---

## CLI Options

| Option         | Description |
|---------------|-------------|
| `--input <URL>` | URL of the webpage to scrape (reads from stdin if not provided). |
| `--output <file>` | Output file to write CSV data (default: stdout). |
| `--overwrite` | Overwrites the output file instead of appending. |
| `--no-header` | Suppresses the CSV header row. |
| `--date YYYY-MM-DD` | Specify a custom date for the CSV (default: today’s date). |
| `--table <n>` | Fetches the nth table in the page (table 1 ) |

---

## Example Output (CSV Format)
```csv
Date,Network,TimeSlot,Show,Rating
2025-02-17,FNC,4PM,Cain,313
2025-02-17,CNN,4PM,The Lead,137
2025-02-17,MSNBC,4PM,Wallace,159
...
```



# generate.sh

This shows an example of calling getratings.py



# create_charts.py

Run this to generate a set of example analytics of the data in csv files.  When you run it vis `python create_charts.py` it will prompt you for the name of a CSV file.

