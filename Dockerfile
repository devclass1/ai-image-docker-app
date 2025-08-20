FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Alternative if the above doesn't work
RUN pip install --upgrade azure-ai-generative azure-identity

CMD ["gunicorn", "app.app:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
