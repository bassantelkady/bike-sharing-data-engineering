
# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy ingestion source code
COPY src/ ./src/

# Copy raw dataset
COPY data/raw/hour.csv ./data/raw/hour.csv

# Pipeline -Batch-Window: 720s_RAW

# Run ingestion script
CMD ["python", "src/ingestion/ingest_data.py"]
