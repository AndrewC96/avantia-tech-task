FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r nobel_user && useradd -r -g nobel_user nobel_user

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    gnupg \
    wget \
    && wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | apt-key add - \
    && echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    mongodb-mongosh \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and entrypoint script
COPY app/ .
COPY docker/entrypoint.sh /entrypoint.sh

# Convert line endings and set permissions
RUN dos2unix /entrypoint.sh && \
    chmod +x /entrypoint.sh && \
    chown -R nobel_user:nobel_user /app

# Switch to non-root user
USER nobel_user

# Expose port
EXPOSE 5000

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]