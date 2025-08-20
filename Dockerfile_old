# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Environment variables (for development, override in production)
ENV FLASK_APP=app/app.py
ENV FLASK_ENV=development
ENV AZURE_GENAI_ENDPOINT=""
ENV AZURE_GENAI_KEY=""
ENV AZURE_DEPLOYMENT_NAME="dall-e-3"

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]
