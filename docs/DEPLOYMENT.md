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
- PostgreSQL 15+ (only when an external database is required)
- Redis 7+ (only when an external cache is required)

### For Kubernetes/Helm Deployments

- Kubernetes cluster 1.24+
- Helm 3.13.0+
- kubectl configured for your cluster
- (Optional) cert-manager for TLS
- (Optional) Ingress controller (nginx recommended)

## Deployment Options

### Option 1: Kubernetes with Helm (Production)

**Recommended for:** Production workloads and enterprise deployments. The current chart deploys one release into one namespace. For tenant isolation, use separate Helm releases/namespaces until automated per-tenant RBAC, quotas, NetworkPolicies, and workloads are implemented and validated.

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

The enterprise profile enables PostgreSQL, Redis, and Grafana and therefore requires explicit credentials. It also contains an example EKS service-account annotation and production node scheduling rules; adapt those values to your cluster before installation.

```bash
# Supply secrets from your approved secret-management process.
export ZQ_POSTGRES_PASSWORD='<strong-random-password>'
export ZQ_REDIS_PASSWORD='<different-strong-random-password>'
export ZQ_GRAFANA_PASSWORD='<different-strong-random-password>'

helm upgrade --install zqautonxg ./charts/zqautonxg \
  -f charts/zqautonxg/values-enterprise.yaml \
  --set-string postgres.password="$ZQ_POSTGRES_PASSWORD" \
  --set-string redis.password="$ZQ_REDIS_PASSWORD" \
  --set-string grafana.adminPassword="$ZQ_GRAFANA_PASSWORD" \
  --namespace zqautonxg-production \
  --create-namespace
```

Never commit those values to Git. For managed environments, prefer an approved external secret workflow.

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

For the complete Helm deployment guide, see [HELM_GUIDE.md](HELM_GUIDE.md).

### Option 2: Docker Compose (Development)

**Recommended for:** Local development, testing, and quick demos.

#### Step 1: Clone Repository

```bash
git clone https://github.com/zubinqayam/ZQAutoNXG-V1.git
cd ZQAutoNXG-V1
```

#### Step 2: Configure Environment

```bash
cp .env.example .env
# Replace all placeholder passwords before starting the stack.
```

At minimum set unique values for `POSTGRES_PASSWORD`, `REDIS_PASSWORD`, and `GRAFANA_ADMIN_PASSWORD`.

#### Step 3: Start Services

```bash
docker compose up -d
```

This starts:
- Backend API on host port 8000
- PostgreSQL on the private Compose network
- Redis with password authentication on the private Compose network
- Prometheus on host port 9090
- Grafana on host port 3001

#### Step 4: Verify Deployment

```bash
curl http://localhost:8000/health

docker compose logs -f backend

# Grafana: http://localhost:3001
# Username: admin
# Password: the value of GRAFANA_ADMIN_PASSWORD in .env
```

#### Managing Services

```bash
docker compose down
docker compose restart
docker compose ps
docker compose pull
docker compose up -d
```

### Option 3: Docker Only

Build and run the application container manually:

```bash
docker build -t zqautonxg:latest .

docker run -d \
  --name zqautonxg-backend \
  -p 8000:8000 \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  zqautonxg:latest
```

If you connect external PostgreSQL or Redis services, provide their configuration through your deployment environment and secret-management process rather than embedding credentials in the command line or source tree.

### Option 4: Local Development

#### Step 1: Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Step 2: Configure Environment

```bash
export APP_NAME="ZQAutoNXG"
export HOST="0.0.0.0"
export PORT="8000"
export LOG_LEVEL="INFO"
```

#### Step 3: Build the Web Control Plane

FastAPI serves only compiled Vite assets. Build them before using `/ui` from a source checkout:

```bash
cd frontend
npm ci
npm audit --omit=dev --audit-level=high
npm run build
cd ..
```

#### Step 4: Run Application

```bash
uvicorn zqautonxg.app:app --reload --host 0.0.0.0 --port 8000

# Multi-worker local/production-style process
uvicorn zqautonxg.app:app --host 0.0.0.0 --port 8000 --workers 4
```

The API remains available without compiled frontend assets; `/ui` reports that the frontend is not built instead of serving an unusable Vite source entrypoint.

## Observability Endpoints

### `/health` - Liveness Probe

```bash
curl http://localhost:8000/health
```

Representative response:

```json
{
  "status": "healthy",
  "platform": "ZQAutoNXG",
  "version": "6.0.0",
  "architecture": "G V2 NovaBase",
  "uptime_seconds": 123.45,
  "timestamp": 1705324800.123
}
```

Kubernetes configuration:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

### `/readyz` - Readiness Probe

```bash
curl http://localhost:8000/readyz
```

Representative response:

```json
{
  "status": "ready",
  "platform": "ZQAutoNXG",
  "version": "6.0.0",
  "architecture": "G V2 NovaBase",
  "git_commit": "<revision>"
}
```

### `/metrics` - Prometheus Endpoint

```bash
curl http://localhost:8000/metrics
```

Application-defined metrics include:
- `zqautonxg_requests_total`
- `zqautonxg_health_checks_total`

Prometheus client/process metrics are exposed by the runtime as applicable.

### OpenTelemetry Integration

When the in-chart collector is enabled, the application Deployment resolves the collector through the release-scoped service name automatically. When an external collector is used, set `otel.endpoint` to that collector's reachable OTLP endpoint.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | `ZQAutoNXG` |
| `HOST` | Server bind address | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `CORS_ORIGINS` | Allowed browser origins | Local development origins |
| `LOG_LEVEL` | Logging level | `INFO` |
| `GIT_COMMIT` | Optional explicit source revision | runtime/provider fallback |

PostgreSQL/Redis environment variables may be supplied by deployment profiles, but the current core workflow API remains an in-memory runtime until database-backed persistence is implemented and validated. Do not infer persistence solely from infrastructure availability.

## Monitoring

### Prometheus

When using Docker Compose, Prometheus is available at `http://localhost:9090`.

### Grafana

When using Docker Compose, Grafana is available at `http://localhost:3001`.

- Username: `admin`
- Password: the configured `GRAFANA_ADMIN_PASSWORD`

There is no committed default Grafana password.

## Health Checks

### Application Health

```bash
curl http://localhost:8000/health
```

### Database Health (Docker Compose)

```bash
docker compose exec postgres pg_isready -U zqadmin -d zqautonxg
```

### Redis Health (Docker Compose)

```bash
docker compose exec redis sh -c 'redis-cli -a "$REDIS_PASSWORD" ping'
```

Expected response: `PONG`.

## Troubleshooting

### Service Won't Start

```bash
docker compose logs backend
docker compose ps
lsof -i :8000
```

If Compose rejects the configuration before startup, confirm the required passwords are present in `.env`.

### Kubernetes Enterprise Render Fails

The enterprise chart intentionally fails closed if PostgreSQL, Redis, or Grafana is enabled without its required credential. Supply the missing value through your approved secret workflow. Also replace/remove the example EKS IRSA annotation and ensure any configured `nodeSelector`/tolerations match your cluster.

### Performance Issues

```bash
docker stats
curl http://localhost:8000/metrics
docker compose logs backend
```

## Backup and Recovery

### Database Backup

```bash
docker compose exec postgres pg_dump -U zqadmin zqautonxg > backup.sql
```

### Database Restore

```bash
docker compose exec -T postgres psql -U zqadmin zqautonxg < backup.sql
```

### Volume Backup

```bash
docker run --rm \
  -v zqautonxg_postgres_data:/data \
  -v "$(pwd):/backup" \
  alpine tar czf /backup/postgres_backup.tar.gz /data
```

## Scaling

For Kubernetes, use the chart autoscaling configuration. For Compose, scale only components that are stateless and designed for parallel replicas; do not assume the current in-memory workflow state is shared across backend replicas.

## Security Considerations

1. Never use or commit placeholder/default credentials in deployed environments.
2. Use HTTPS with valid certificates for remote access.
3. Keep PostgreSQL and Redis private unless explicit external access is required.
4. Redis authentication is mandatory when the Helm Redis component is enabled.
5. Run the production dependency audit and repository security gates before promotion.
6. Use namespace/RBAC/NetworkPolicy controls explicitly; automated multi-tenant isolation is not currently implemented by this chart.
7. Keep images and third-party dependencies patched and preferably digest-pinned for controlled releases.

## Support

For deployment assistance:
- **Issues:** https://github.com/zubinqayam/ZQAutoNXG-V1/issues
- **Documentation:** https://github.com/zubinqayam/ZQAutoNXG-V1/blob/main/README.md

---

**Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™**  
**Licensed under the Apache License 2.0**
