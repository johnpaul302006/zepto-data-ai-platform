# Zepto Data & AI Platform

An end-to-end AI/ML engineering capstone project containing three connected modules:

1. Data Engineering Pipeline
2. Analytics and Predictive Modeling
3. GenAI Support Assistant

All three modules are contained in this single public GitHub repository.

## Setup

This project uses one consolidated root requirements.txt.

Create the virtual environment:

python -m venv .venv

Activate it:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

## Project Structure

zepto-data-ai-platform/
├── data_pipeline/
├── analytics/
├── support_assistant/
├── requirements.txt
└── README.md

## Module 1 - Data Pipeline

The Data Pipeline scrapes book catalogue data, cleans and transforms it, converts GBP prices to INR using the fixed rate 1 GBP = 105.50 INR, stores the data in normalized SQLite tables, performs SQL analysis, and validates SQL results with pandas.

### End-to-end run

python data_pipeline/scraper.py
python data_pipeline/clean_data.py
python data_pipeline/database.py
python data_pipeline/queries.py
python data_pipeline/pandas_validation.py

### Design decisions

Requests and BeautifulSoup are used for scraping. Pandas is used for cleaning and independent validation. SQLite is used as a lightweight relational database with separate category and book tables connected by a primary-key/foreign-key relationship. SQL queries cover filtering, ordering, limiting, distinct/range or membership operations, and a JOIN.

## Module 2 - Analytics and Predictive Modeling

The Analytics module uses the Titanic dataset as one cohesive EDA and modeling workflow.

Files:

analytics/01_eda.ipynb
analytics/02_modeling.ipynb
analytics/titanic.csv
analytics/models/best_rf_pipeline.joblib

Run the notebooks in this order:

01_eda.ipynb
02_modeling.ipynb

The workflow includes profiling, missing-value handling, outlier analysis, visualization, correlation analysis, standardization, classification, class-imbalance comparison, SMOTE, Random Forest GridSearchCV with OOB evaluation, fare regression, residual analysis, final model comparison, and model persistence.

### Design decisions

Preprocessing is implemented inside scikit-learn pipelines so transformations are learned from training data only. Logistic Regression, Decision Tree, and Random Forest are compared using the required classification metrics. The complete preprocessing-and-model pipeline is saved with Joblib so it can be reloaded and used on raw input.

## Module 3 - GenAI Support Assistant

The Support Assistant is a policy-focused RAG service using Sentence Transformers, ChromaDB, LangGraph, Pydantic, and FastAPI.

The graded baseline uses deterministic offline MOCK_LLM mode.

### End-to-end run

Build the vector index:

python support_assistant/ingest.py

Run the API:

cd support_assistant
uvicorn main:app --host 0.0.0.0 --port 7860

Main endpoint:

POST /ask

### Design decisions

Required policy documents are embedded locally with all-MiniLM-L6-v2 and stored in ChromaDB. LangGraph separates intent classification, retrieval-and-answer, and direct-answer paths. The retriever returns the top-3 results using cosine similarity. Pydantic provides structured output. The offline mock baseline does not require an external LLM API.

## Docker

Build:

docker build -t zepto-support-assistant ./support_assistant

Run:

docker run --name zepto-support-container -p 7860:7860 zepto-support-assistant

## Reproducibility

The repository contains the source code, committed datasets, SQL outputs, notebooks, saved model artifact, policy corpus, and configuration required to reproduce the project.

## Git Workflow

The repository history contains a feature branch with multiple commits followed by a merge back into main, demonstrating the required Git workflow.
