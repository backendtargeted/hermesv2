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
RUN mkdir -p static/images/bags static/images/qr data

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
# Fix permissions for mounted volumes\n\
if [ -f /app/data/bags.db ]; then\n\
    chown app:app /app/data/bags.db\n\
    chmod 664 /app/data/bags.db\n\
fi\n\
if [ -d /app/static/images ]; then\n\
    chown -R app:app /app/static/images\n\
    chmod -R 755 /app/static/images\n\
fi\n\
# Switch to app user and run the command\n\
exec gosu app "$@"' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Install gosu for user switching
RUN apt-get update && apt-get install -y gosu && rm -rf /var/lib/apt/lists/*

# Use entrypoint to fix permissions before running app
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "app.py"]