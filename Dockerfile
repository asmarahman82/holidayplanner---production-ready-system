# Use a lightweight Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for common Python libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Run Streamlit app (make sure this file exists)
CMD ["streamlit", "run", "ui/app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]

