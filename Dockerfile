# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p static/images/bags static/images/qr

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Create a non-root user with specific UID/GID
RUN groupadd -g 1000 app && \
    useradd --create-home --shell /bin/bash --uid 1000 --gid 1000 app

# Change ownership of the app directory
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Run the application
CMD ["python", "app.py"]