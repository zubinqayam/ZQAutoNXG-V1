# ZQAutoNXG - Production Dockerfile
# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

FROM python:3.11-slim-bullseye AS base

# Apache 2.0 OCI Labels
LABEL org.opencontainers.image.title="ZQAutoNXG"
LABEL org.opencontainers.image.description="Next-Generation eXtended Automation Platform - Powered by ZQ AI LOGIC™"
LABEL org.opencontainers.image.vendor="ZQ AI LOGIC™"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/zubinqayam/ZQAutoNXG-V1"
LABEL org.opencontainers.image.documentation="https://github.com/zubinqayam/ZQAutoNXG-V1/blob/main/README.md"
LABEL org.opencontainers.image.copyright="© 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC"
LABEL com.zqautonxg.version="G V2 NovaBase"
LABEL com.zqautonxg.platform="Next-Generation eXtended Automation"
LABEL com.zqautonxg.capabilities="AI,XR,Global-Scale,Proprietary"

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_NAME=ZQAutoNXG \
    APP_BRAND="Powered by ZQ AI LOGIC™" \
    PYTHONPATH="/app"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy ZQAutoNXG application code
COPY zqautonxg/ ./zqautonxg/

# Create non-root user for security
RUN groupadd -r -g 1001 zquser \
    && useradd -r -g zquser -u 1001 -m -s /bin/bash zquser \
    && chown -R zquser:zquser /app

# Switch to non-root user
USER zquser

# Expose application port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start ZQAutoNXG application
CMD ["uvicorn", "zqautonxg.app:app", "--host", "0.0.0.0", "--port", "8000"]