# ZQAutoNXG Backend — Docker build
# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™
# Licensed under the Apache License, Version 2.0

FROM python:3.11-slim-bookworm AS builder

WORKDIR /build
COPY backend/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim-bookworm

# Non-root user for security
RUN useradd -m -u 1001 zqautonxg

WORKDIR /app
COPY --from=builder /root/.local /home/zqautonxg/.local
COPY backend/ /app/

RUN mkdir -p /app/data && chown -R zqautonxg:zqautonxg /app

USER zqautonxg
ENV PATH=/home/zqautonxg/.local/bin:$PATH \
    PYTHONPATH=/app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "zqautonxg.main:app", "--host", "0.0.0.0", "--port", "8000"]
