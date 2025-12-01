FROM python:3.11-slim

# Install system dependencies with optimizations
RUN apt-get update && apt-get install -y \
    ffmpeg \
    ca-certificates \
    openssl \
    curl \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application modules
COPY config.py .
COPY utils.py .
COPY video_processor.py .
COPY downloader.py .
COPY uploader.py .
COPY handlers.py .
COPY main.py .

# Create downloads directory
RUN mkdir -p downloads

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV PYTHONDONTWRITEBYTECODE=1

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT:-10000}/health || exit 1

CMD ["python", "-u", "main.py"]
