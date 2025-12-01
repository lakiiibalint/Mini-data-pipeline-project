# Dockerfile
FROM python:3.12-slim

# System deps (ha kell még később, ide jön)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Download Python libs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Project files
COPY . .

ENV PYTHONUNBUFFERED=1

# Default command: run the full pipeline
CMD ["python", "-m", "src.pipeline"]
