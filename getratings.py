import argparse
import csv
import os
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def fetch_table_from_url(url, table_index):
    """Fetches HTML content from a URL and extracts the nth <table>."""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')

    if not tables or table_index > len(tables) or table_index < 1:
        print(f"Error: Table {table_index} not found on the page.", file=sys.stderr)
        sys.exit(1)

    return tables[table_index - 1]  # Convert 1-based index to 0-based


def parse_table(table, date_str):
    """Parses the table in the HTML and returns structured data."""
    rows = table.find_all('tr')

    # Extract networks from the first row
    headers = [td.get_text(strip=True).replace(":", "") for td in rows[0].find_all('td')[1:]]

    data = []
    for row in rows[1:]:  # Skip the first row (header)
        cells = row.find_all('td')
        time_slot = cells[0].get_text(strip=True)

        for i, cell in enumerate(cells[1:]):  # Skip first column, iterate over networks
            parts = cell.get_text(strip=True).split(":")
            show = parts[0].strip()
            rating = parts[1].strip() if len(parts) > 1 else ""

            data.append([date_str, headers[i], time_slot, show, rating])

    return data


def write_csv(data, output_file=None, write_header=True, overwrite=False):
    """Writes CSV data to stdout or a file, based on parameters."""
    # Auto-suppress header if appending to an existing file
    if output_file and not overwrite and os.path.exists(output_file) and write_header:
        write_header = False  # Assume file already has a header

    if output_file:
        mode = "w" if overwrite else "a"
        with open(output_file, mode, newline="") as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(["Date", "Network", "TimeSlot", "Show", "Rating"])
            writer.writerows(data)
        print(f"CSV data written to '{output_file}' successfully.", file=sys.stderr)
    else:
        writer = csv.writer(sys.stdout)
        if write_header:
            writer.writerow(["Date", "Network", "TimeSlot", "Show", "Rating"])
        writer.writerows(data)


def main():
    parser = argparse.ArgumentParser(description="Extract TV ratings from a webpage and output as CSV.")
    parser.add_argument("--input", type=str, help="URL of the webpage (reads from stdin if not provided)")
    parser.add_argument("--output", type=str, help="Output file (default: stdout)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the output file instead of appending")
    parser.add_argument("--no-header", action="store_true", help="Suppress the CSV header")
    parser.add_argument("--date", type=str, help="Specify the date for the CSV (format: YYYY-MM-DD, default: today)")
    parser.add_argument("--table", type=int, default=1,
                        help="Specify which table to extract (1-based index, default: 1)")

    args = parser.parse_args()

    # Get input (URL from argument or stdin)
    if args.input:
        url = args.input
    else:
        url = sys.stdin.read().strip()
        if not url:
            print("Error: No URL provided. Use --input <URL> or provide a URL via stdin.", file=sys.stderr)
            sys.exit(1)

    # Determine the date to use in the CSV
    if args.date:
        try:
            # Validate that the date is in the correct format
            date_str = datetime.strptime(args.date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
    else:
        # Default to today's date
        date_str = datetime.today().strftime("%Y-%m-%d")

    table = fetch_table_from_url(url, args.table)

    data = parse_table(table, date_str)

    # Determine if the header should be written
    write_header = not args.no_header

    write_csv(data, output_file=args.output, write_header=write_header, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
