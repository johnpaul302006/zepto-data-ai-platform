FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
# Install Python dependencies
COPY requirements.txt .

ENV PIP_CONFIG_FILE=/dev/null
ENV PIP_REQUIRE_HASHES=0
ENV PIP_CONSTRAINT=

RUN python -m pip install --upgrade pip && python -m pip install --no-cache-dir --index-url https://pypi.org/simple -r requirements.txt

# Copy application files
COPY corpus ./corpus
COPY ingest.py .
COPY retriever.py .
COPY prompts.py .
COPY graph.py .
COPY schemas.py .
COPY main.py .

# Build the local ChromaDB index inside the image
RUN python ingest.py

# FastAPI port
EXPOSE 7860

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
