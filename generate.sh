URL="https://www.adweek.com/tvnewser/monday-february-3-2025-evening-cable-news-ratings/"
DATE=2025-02-03
python getratings.py --output ratings-25-55.csv --table 1 --date $DATE --input $URL
python getratings.py --output ratings-total.csv --table 2 --date $DATE --input $URL

