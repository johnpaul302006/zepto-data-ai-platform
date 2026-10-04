# Data Pipeline

## Overview

This module implements an end-to-end data pipeline using the Books to Scrape catalogue.

## Pipeline Flow

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
Normalized SQLite Database
      ↓
SQL Queries
      ↓
Pandas Validation