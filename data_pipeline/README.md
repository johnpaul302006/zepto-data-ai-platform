# Data Pipeline

## 1. Overview

This module implements an end-to-end data pipeline for scraping book
catalogue data from Books to Scrape, cleaning and transforming the
data, converting GBP prices to INR using the required fixed project
rate, storing the cleaned data in a normalized SQLite database,
running SQL queries, and validating SQL results using pandas.

## 2. Pipeline Flow

Books to Scrape
→ Web Scraping
→ Raw CSV
→ Data Cleaning
→ GBP to INR Conversion
→ SQLite Database
→ SQL Queries
→ Pandas Validation

## 3. Technologies Used

- Python 3.11
- Requests
- BeautifulSoup
- Pandas
- SQLite
- Python sqlite3

## 4. Project Files

- `scraper.py` - Scrapes book information from Books to Scrape.
- `raw_books.csv` - Stores the raw scraped data.
- `clean_data.py` - Cleans and transforms the scraped fields.
- `cleaned_books.csv` - Stores the cleaned dataset.
- `database.py` - Creates and populates the SQLite database.
- `queries.py` - Executes the required SQL queries.
- `sql_results.txt` - Stores SQL query outputs.
- `pandas_validation.py` - Validates SQL results using pandas.
- `pandas_validation.txt` - Stores pandas validation results.
- `database/books.db` - SQLite database.

## 5. Scraping

The pipeline scrapes the first five pages of the Books to Scrape
catalogue.

The final dataset contains:

- 100 books
- 29 categories

For each book, the following fields are collected:

- `title`
- `price`
- `star_rating`
- `availability`
- `category`

## 6. Data Cleaning

### 6.1 Price

The original price is scraped as text containing the GBP currency
symbol.

The currency symbol and other non-numeric characters are removed,
and the result is converted to a floating-point column named
`price_gbp`.

Example:

`£51.77` → `51.77`

### 6.2 Rating

The text star rating is converted into an integer from 1 to 5.

The mapping is:

- One → 1
- Two → 2
- Three → 3
- Four → 4
- Five → 5

The cleaned column is named `rating`.

### 6.3 Availability

Availability text is converted into a Boolean column named
`in_stock`.

- In stock → `True`
- Out of stock → `False`

If availability cannot be safely parsed, the affected row is dropped
because its stock status cannot be reliably determined.

### 6.4 Parsing Failures

For numeric fields, parsing failures are handled using median
imputation.

For an unparseable availability value, the affected row is dropped
instead of guessing its Boolean value.

## 7. GBP to INR Conversion

The required fixed project conversion rate is:

`1 GBP = 105.50 INR`

The rate is a project-defined constant and does not use a live
currency API.

The conversion is:

`price_inr = price_gbp * 105.50`

## 8. Database Design

The data is stored in a normalized SQLite database with two related
tables.

### categories

- `category_id` - Primary Key
- `category_name` - Unique category name

### books

- `book_id` - Primary Key
- `title`
- `price_gbp`
- `price_inr`
- `rating`
- `in_stock`
- `category_id` - Foreign Key

The relationship is:

`categories.category_id` → `books.category_id`

## 9. SQL Queries

Six SQL queries are implemented.

1. `SELECT` + `WHERE`
2. `ORDER BY`
3. `LIMIT`
4. `DISTINCT`
5. `BETWEEN`
6. `JOIN`

The JOIN combines the `books` and `categories` tables.

The SQL query outputs are stored in:

`sql_results.txt`

## 10. Pandas Validation

SQL query results are read into pandas using `pd.read_sql()`.

The database JOIN is independently reproduced in pandas using
`pd.merge()`.

The SQL JOIN result and pandas merge result were compared and found
to be equivalent.

The validation output is stored in:

`pandas_validation.txt`

## 11. How to Run

Make sure the project virtual environment is activated.

### Step 1 - Scrape the raw data

```bash
python data_pipeline/scraper.py

### Step 1 - Scrape the raw data

```bash
python data_pipeline/scraper.py
## 13. Validation Summary

The completed pipeline was tested end to end.

- 100 books were scraped successfully.
- 29 categories were identified.
- - The cleaned `price_gbp`, `rating`, `in_stock`, and `price_inr` columns have the required data types and values.
- The SQLite database contains 100 books and 29 categories.
- Six SQL queries were executed successfully.
- The SQL JOIN result and the pandas `pd.merge()` result were confirmed to be equivalent.