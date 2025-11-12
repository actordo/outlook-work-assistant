# Dockerfile for Outlook AI Assistant
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create a non-root user
RUN useradd -m -u 1000 assistant && \
    chown -R assistant:assistant /app

# Switch to non-root user
USER assistant

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Entry point
ENTRYPOINT ["python", "main.py"]

# Default command (show help)
CMD ["--help"]
