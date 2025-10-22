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

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app

# Create entrypoint script to fix permissions
RUN echo '#!/bin/bash\n\
chown -R app:app /app/static/images 2>/dev/null || true\n\
chown app:app /app/bags.db 2>/dev/null || true\n\
exec "$@"' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Switch to non-root user
USER app

# Use entrypoint to fix permissions before running app
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "app.py"]