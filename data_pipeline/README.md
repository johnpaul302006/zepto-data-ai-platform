# Data Pipeline

## 1. Overview

This module implements an end-to-end data pipeline for scraping book
catalogue data from Books to Scrape, cleaning and transforming the
data, converting GBP prices to INR using the required fixed project
rate, storing the cleaned data in a normalized SQLite database,
running SQL queries, and validating SQL results using pandas.

## 2. Pipeline Flow

```text
Books to Scrape
      ↓
Web Scraping
      ↓
Raw CSV
      ↓
Data Cleaning
      ↓
GBP to INR Conversion
      ↓
SQLite Database
      ↓
SQL Queries
      ↓
Pandas Validation