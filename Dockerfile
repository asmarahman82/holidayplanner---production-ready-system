# Base image
FROM python:3.12-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Create necessary directories
RUN mkdir -p /app/data/metrics /app/data/graphs /app/logs

# Make start script executable
RUN chmod +x /app/start.sh

# Expose Streamlit & FastAPI ports
EXPOSE 8501 8000

# Default command
CMD ["/app/start.sh"]
