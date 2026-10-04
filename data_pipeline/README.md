# Data Pipeline

## Overview

This module implements an end-to-end data pipeline using the Books to Scrape catalogue.

## Pipeline Flow

Books to Scrape → Web Scraping → Raw CSV → Data Cleaning → GBP to INR Conversion → SQLite Database → SQL Queries → Pandas Validation

## Technologies

- Python
- Requests
- BeautifulSoup
- Pandas
- SQLite
- SQL

## Dataset

The pipeline processes 100 books across 29 categories.

Required fields include title, price, star rating, availability, and category.

The fixed project conversion rate is:

`1 GBP = 105.50 INR`

## Cleaning

The pipeline:

- converts price to `price_gbp`
- converts star ratings to integers from 1 to 5
- converts availability to Boolean `in_stock`
- calculates `price_inr`
- preserves category information

## Database

The cleaned data is stored in a normalized SQLite database using:

- `categories(category_id, category)`
- `books(book_id, title, price_gbp, price_inr, rating, in_stock, category_id)`

The relationship is one category to many books using a primary-key/foreign-key relationship.

## SQL Analysis

The module runs SQL queries demonstrating:

- SELECT / WHERE
- ORDER BY
- LIMIT
- DISTINCT
- IN / BETWEEN
- JOIN

The query strings and outputs are saved in `sql_results.txt`.

## Pandas Validation

At least two SQL query results are read using `pd.read_sql()`.

The JOIN result is also reproduced with `pd.merge()` and checked for equivalence.

Validation output is saved in `pandas_validation.txt`.

## How to Run

From the project root:

```text
python data_pipeline/scraper.py
python data_pipeline/clean_data.py
python data_pipeline/database.py
python data_pipeline/queries.py
python data_pipeline/pandas_validation.py