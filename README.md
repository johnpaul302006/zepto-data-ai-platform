# Zepto Data & AI Platform

An end-to-end AI/ML engineering capstone project containing three connected modules:

1. Data Engineering Pipeline
2. Analytics and Predictive Modeling
3. GenAI Support Assistant

All three modules are maintained in one repository.

---

# Project Structure

```text
zepto-data-ai-platform/
│
├── data_pipeline/
│   ├── raw_books.csv
│   ├── cleaned_books.csv
│   ├── clean_data.py
│   ├── database.py
│   ├── pandas_validation.py
│   ├── queries.py
│   ├── scraper.py
│   ├── README.md
│   └── database/
│
├── analytics/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── titanic.csv
│   ├── models/
│   │   └── best_rf_pipeline.joblib
│   └── outputs/
│
├── support_assistant/
│   ├── corpus/
│   ├── chroma_db/
│   ├── ingest.py
│   ├── retriever.py
│   ├── prompts.py
│   ├── graph.py
│   ├── schemas.py
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── .gitignore
├── requirements.txt
└── README.md