# Zepto Data & AI Platform

An end-to-end AI/ML engineering capstone project containing three connected modules:

1. Data Engineering Pipeline
2. Analytics and Predictive Modeling
3. GenAI Support Assistant

All three modules are contained in this single public GitHub repository.

---

## Project Structure

```text
zepto-data-ai-platform/
│
├── data_pipeline/
│   ├── raw_books.csv
│   ├── cleaned_books.csv
│   ├── scraper.py
│   ├── clean_data.py
│   ├── database.py
│   ├── queries.py
│   ├── pandas_validation.py
│   ├── sql_results.txt
│   ├── pandas_validation.txt
│   ├── database/
│   │   └── books.db
│   └── README.md
│
├── analytics/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── titanic.csv
│   └── models/
│       └── best_rf_pipeline.joblib
│
├── support_assistant/
│   ├── corpus/
│   ├── ingest.py
│   ├── retriever.py
│   ├── prompts.py
│   ├── graph.py
│   ├── schemas.py
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── requirements.txt
└── README.md