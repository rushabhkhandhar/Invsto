FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the import script and data files
COPY import_csv.py .
COPY *.csv ./data/ 
COPY .env .

# Copy source code
COPY ./src ./src

# Port the API will listen on
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]