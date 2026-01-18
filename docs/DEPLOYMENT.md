# ZQAutoNXG Deployment Guide

**Version:** 6.0.0  
**Powered by:** ZQ AI LOGIC™

## Table of Contents

- [Prerequisites](#prerequisites)
- [Deployment Options](#deployment-options)
  - [Option 1: Kubernetes with Helm (Production)](#option-1-kubernetes-with-helm-production)
  - [Option 2: Docker Compose (Development)](#option-2-docker-compose-development)
  - [Option 3: Docker Only](#option-3-docker-only)
  - [Option 4: Local Development](#option-4-local-development)
- [Observability Endpoints](#observability-endpoints)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Basic Requirements

- Docker and Docker Compose (recommended)
- Python 3.11+ (for local development)
- PostgreSQL 15+ (if not using Docker/Kubernetes)
- Redis 7+ (if not using Docker/Kubernetes)

### For Kubernetes/Helm Deployments

- Kubernetes cluster 1.24+
- Helm 3.13.0+
- kubectl configured for your cluster
- (Optional) cert-manager for TLS
- (Optional) Ingress controller (nginx recommended)

## Deployment Options

### Option 1: Kubernetes with Helm (Production)

**Recommended for:** Production workloads, enterprise deployments, multi-tenant environments

#### Quick Start

```bash
# Clone repository
git clone https://github.com/zubinqayam/ZQAutoNXG-V1.git
cd ZQAutoNXG-V1

# Install with default configuration
helm install zqautonxg ./charts/zqautonxg \
  --namespace zqautonxg \
  --create-namespace

# Verify deployment
kubectl get pods -n zqautonxg
kubectl get svc -n zqautonxg
```

#### Enterprise Deployment

```bash
# Deploy with enterprise configuration
helm install zqautonxg ./charts/zqautonxg \
  -f charts/zqautonxg/values.yaml \
  -f charts/zqautonxg/values-enterprise.yaml \
  --namespace zqautonxg-production \
  --create-namespace

# Enable all infrastructure components
helm upgrade zqautonxg ./charts/zqautonxg \
  --set postgres.enabled=true \
  --set redis.enabled=true \
  --set prometheus.enabled=true \
  --set grafana.enabled=true \
  --set otel.enabled=true \
  --reuse-values
```

#### Zero-Cost Deployment (ZCD)

For ZCD-compliant deployments using digest-pinned images:

```bash
# Get image digest
IMAGE_DIGEST=$(docker inspect \
  ghcr.io/zubinqayam/zqautonxg-v1:main \
  --format='{{index .RepoDigests 0}}' | cut -d'@' -f2)

# Deploy with digest
helm upgrade --install zqautonxg ./charts/zqautonxg \
  --set image.tag="@${IMAGE_DIGEST}" \
  --reuse-values \
  --wait
```

See [ZCD_COMPLIANCE.md](ZCD_COMPLIANCE.md) for detailed ZCD guidelines.

#### Access Application

```bash
# Port forward to access locally
kubectl port-forward -n zqautonxg svc/zqautonxg 8000:8000

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/readyz
curl http://localhost:8000/metrics
```

#### Ingress Configuration

```yaml
# Enable ingress in values
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: api.zqautonxg.enterprise.local
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: zqautonxg-tls
      hosts:
        - api.zqautonxg.enterprise.local
```

For complete Helm deployment guide, see [HELM_GUIDE.md](HELM_GUIDE.md).

### Option 2: Docker Compose (Development)

### Option 2: Docker Compose (Development)

**Recommended for:** Local development, testing, quick demos

#### Step 1: Clone Repository

```bash
git clone https://github.com/zubinqayam/ZQAutoNXG-V1.git
cd ZQAutoNXG-V1
```

#### Step 2: Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

#### Step 3: Start Services

```bash
docker-compose up -d
```

This will start:
- Backend API (port 8000)
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Prometheus monitoring (port 9090)
- Grafana dashboard (port 3001)

#### Step 4: Verify Deployment

```bash
# Check service health
curl http://localhost:8000/health

# View logs
docker-compose logs -f backend

# Access Grafana
# URL: http://localhost:3001
# Username: admin
# Password: zqadmin
```

#### Managing Services

```bash
# Stop services
docker-compose down

# Restart services
docker-compose restart

# View service status
docker-compose ps

# Update and restart
docker-compose pull
docker-compose up -d
```

### Option 3: Docker Only

Build and run the backend container manually:

```bash
# Build image
docker build -t zqautonxg:latest .

# Run container
docker run -d \
  --name zqautonxg-backend \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e REDIS_URL=redis://host:6379/0 \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  zqautonxg:latest
```

### Option 4: Local Development

For development without Docker:

#### Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Configure Environment

```bash
export APP_NAME="ZQAutoNXG"
export HOST="0.0.0.0"
export PORT="8000"
export DATABASE_URL="postgresql://user:pass@localhost:5432/zqautonxg"
export REDIS_URL="redis://localhost:6379/0"
```

#### Step 3: Run Application

```bash
# Development mode with auto-reload
uvicorn zqautonxg.app:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn zqautonxg.app:app --host 0.0.0.0 --port 8000 --workers 4
```

## Kubernetes Deployment

For production Kubernetes deployment:

```bash
# Apply manifests (once created)
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n zqautonxg
kubectl get services -n zqautonxg

# View logs
kubectl logs -f deployment/zqautonxg-backend -n zqautonxg
```

## Observability Endpoints

ZQAutoNXG provides comprehensive observability endpoints for production deployment and monitoring:

### Health & Readiness Probes

#### `/health` - Liveness Probe

Used by Kubernetes and load balancers to determine if the service is alive:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "platform": "ZQAutoNXG",
  "version": "6.0.0",
  "architecture": "G V2 NovaBase",
  "uptime": "operational",
  "timestamp": 1705324800.123
}
```

**Kubernetes Configuration:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

#### `/readyz` - Readiness Probe

Used by Kubernetes to determine if the service is ready to accept traffic:

```bash
curl http://localhost:8000/readyz
```

Response:
```json
{
  "status": "ready",
  "platform": "ZQAutoNXG",
  "version": "6.0.0",
  "architecture": "G V2 NovaBase"
}
```

**Kubernetes Configuration:**
```yaml
readinessProbe:
  httpGet:
    path: /readyz
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Metrics Collection

#### `/metrics` - Prometheus Endpoint

Exports metrics in Prometheus format for scraping:

```bash
curl http://localhost:8000/metrics
```

**Available Metrics:**
- `zqautonxg_requests_total` - Total HTTP requests by method and endpoint
- `zqautonxg_health_checks_total` - Health check request count
- Standard Python and FastAPI metrics (request duration, memory usage, etc.)

**Prometheus Configuration:**
```yaml
scrape_configs:
  - job_name: 'zqautonxg'
    static_configs:
      - targets: ['zqautonxg:8000']
    metrics_path: /metrics
    scrape_interval: 15s
```

### OpenTelemetry Integration

When enabled, ZQAutoNXG exports telemetry data to OpenTelemetry collector:

```yaml
env:
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: "http://otel-collector:4317"
  - name: OTEL_SERVICE_NAME
    value: "zqautonxg"
```

### Example: Complete Observability Stack

```bash
# Deploy with full observability
helm upgrade --install zqautonxg ./charts/zqautonxg \
  --set prometheus.enabled=true \
  --set grafana.enabled=true \
  --set otel.enabled=true \
  --set prometheus.serviceMonitor.enabled=true

# Access monitoring services
kubectl port-forward svc/zqautonxg-prometheus 9090:9090
kubectl port-forward svc/zqautonxg-grafana 3000:3000

# Grafana credentials
kubectl get secret zqautonxg-grafana \
  -o jsonpath="{.data.admin-password}" | base64 --decode
```

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `APP_NAME` | Application name | `ZQAutoNXG` |
| `HOST` | Server bind address | `0.0.0.0` |
| `PORT` | Server port | `8000` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | - |
| `REDIS_URL` | Redis connection string | - |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `JWT_SECRET_KEY` | JWT signing key | - |

## Monitoring

### Prometheus Metrics

Access Prometheus at http://localhost:9090

Available metrics:
- `zqautonxg_requests_total` - Total HTTP requests
- `zqautonxg_health_checks_total` - Health check count
- Standard Python/FastAPI metrics

### Grafana Dashboards

Access Grafana at http://localhost:3001

Default credentials:
- **Username:** admin
- **Password:** zqadmin

Pre-configured dashboards will be available after deployment.

## Health Checks

### Application Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "platform": "ZQAutoNXG",
  "version": "6.0.0"
}
```

### Database Health

```bash
# Via Docker Compose
docker-compose exec postgres pg_isready -U zqadmin

# Direct connection
psql -h localhost -U zqadmin -d zqautonxg -c "SELECT 1"
```

### Redis Health

```bash
# Via Docker Compose
docker-compose exec redis redis-cli ping

# Direct connection
redis-cli -h localhost ping
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs backend

# Check if ports are in use
lsof -i :8000
lsof -i :5432
lsof -i :6379

# Restart services
docker-compose restart
```

### Database Connection Issues

```bash
# Check database is running
docker-compose ps postgres

# Check connection from backend
docker-compose exec backend ping postgres

# Verify credentials
docker-compose exec postgres psql -U zqadmin -d zqautonxg -c "\dt"
```

### Performance Issues

```bash
# Check resource usage
docker stats

# View application metrics
curl http://localhost:8000/metrics

# Check logs for slow queries
docker-compose logs backend | grep "slow"
```

## Backup and Recovery

### Database Backup

```bash
# Create backup
docker-compose exec postgres pg_dump -U zqadmin zqautonxg > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U zqadmin zqautonxg < backup.sql
```

### Volume Backup

```bash
# Backup volumes
docker run --rm \
  -v zqautonxg_postgres_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres_backup.tar.gz /data
```

## Scaling

### Horizontal Scaling (Multiple Instances)

```bash
# Scale backend service
docker-compose up -d --scale backend=3

# Verify
docker-compose ps backend
```

### Vertical Scaling (Resource Limits)

Edit `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

## Security Considerations

1. **Change default passwords** in production
2. **Use HTTPS** with proper SSL certificates
3. **Configure firewall** rules
4. **Enable authentication** for all services
5. **Regular security updates** for all dependencies
6. **Monitor access logs** for suspicious activity

## Support

For deployment assistance:
- **Email:** zubin.qayam@outlook.com
- **Issues:** https://github.com/zubinqayam/ZQAutoNXG-V1/issues
- **Documentation:** https://github.com/zubinqayam/ZQAutoNXG-V1/blob/main/README.md

---

**Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™**  
**Licensed under the Apache License 2.0**
