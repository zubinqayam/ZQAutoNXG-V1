# ZQAutoNXG - Production Dockerfile
# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

FROM node:20-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim-bookworm AS runtime

LABEL org.opencontainers.image.title="ZQAutoNXG"
LABEL org.opencontainers.image.description="Next-Generation eXtended Automation Platform - Powered by ZQ AI LOGIC™"
LABEL org.opencontainers.image.vendor="ZQ AI LOGIC™"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/zubinqayam/ZQAutoNXG-V1"
LABEL org.opencontainers.image.documentation="https://github.com/zubinqayam/ZQAutoNXG-V1/blob/main/README.md"
LABEL com.zqautonxg.version="G V2 NovaBase"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_NAME=ZQAutoNXG \
    APP_BRAND="Powered by ZQ AI LOGIC™" \
    PYTHONPATH="/app" \
    CONTAINER_RUNTIME="docker"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt pyproject.toml ./
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY zqautonxg/ ./zqautonxg/
COPY --from=frontend-builder /frontend/dist ./frontend/dist/

RUN groupadd -r -g 1001 zquser \
    && useradd -r -g zquser -u 1001 -m -s /usr/sbin/nologin zquser \
    && chown -R zquser:zquser /app

USER zquser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail --silent http://localhost:8000/health || exit 1

CMD ["uvicorn", "zqautonxg.app:app", "--host", "0.0.0.0", "--port", "8000"]
