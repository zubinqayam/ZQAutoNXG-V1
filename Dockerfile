# ZQAutoNXG - Production Dockerfile
# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

# Multi-stage build for optimized image size
FROM python:3.11-slim-bullseye AS builder

WORKDIR /build

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# Production image
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

# Environment variables - Production & ZCD compliant
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_NAME=ZQAutoNXG \
    APP_BRAND="Powered by ZQ AI LOGIC™" \
    PYTHONPATH="/app" \
    ZQ_MODE=production \
    ZQ_METRICS_ENABLED=true \
    ZQ_SAFE_EXECUTION=true \
    INNM_OPAQUE_CONTEXT=true

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python dependencies from pre-built wheels
COPY --from=builder /wheels /wheels
COPY --from=builder /build/requirements.txt .
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy ZQAutoNXG application code
COPY zqautonxg/ ./zqautonxg/

# Create non-root user for security
RUN groupadd -r -g 1001 zquser \
    && useradd -r -g zquser -u 1001 -m -s /bin/bash zquser \
    && mkdir -p /app/logs /app/tmp \
    && chown -R zquser:zquser /app

# Define ephemeral volumes for ZCD compliance
VOLUME ["/app/logs", "/app/tmp"]

# Switch to non-root user
USER zquser

# Expose application port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start ZQAutoNXG with Gunicorn + Uvicorn workers for production
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "zqautonxg.app:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--access-logfile", "-", "--error-logfile", "-"]