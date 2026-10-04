@'
# Data Pipeline

## Overview

This module implements an end-to-end data pipeline using the Books to Scrape catalogue.

The pipeline performs:

```text
Books to Scrape
      ↓
Web Scraping
      ↓
Raw CSV
      ↓
Data Cleaning
      ↓
GBP → INR Conversion
      ↓
SQLite Database
      ↓
SQL Queries
      ↓
Pandas Validation