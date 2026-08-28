# ZQAutoNXG Helm Deployment Guide

**Version:** 1.0.0  
**Chart Version:** 1.0.0  
**App Version:** 6.0.0  
**Powered by:** ZQ AI LOGIC™

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Deployment Scenarios](#deployment-scenarios)
- [Upgrading](#upgrading)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Overview

The ZQAutoNXG Helm chart provides a complete, production-ready deployment of the Next-Generation eXtended Automation Platform with:

- **High Availability:** Multi-replica deployment with pod anti-affinity
- **Auto-scaling:** Horizontal Pod Autoscaler based on CPU/memory
- **Observability:** Integrated Prometheus, Grafana, and OpenTelemetry
- **Data Persistence:** PostgreSQL and Redis with StatefulSets
- **Security:** Non-root containers, RBAC, network policies
- **Multi-tenancy:** Namespace-based tenant isolation

## Prerequisites

### Required

- Kubernetes cluster 1.24+
- Helm 3.13.0+
- kubectl configured for your cluster

### Optional

- cert-manager (for TLS certificates)
- Prometheus Operator (for ServiceMonitor support)
- Ingress controller (nginx recommended)

### Installation

```bash
# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify installation
helm version

# Add ZQAutoNXG chart repository (if published)
# helm repo add zqautonxg https://charts.zqautonxg.com
# helm repo update
```

## Quick Start

### Development Deployment

Deploy ZQAutoNXG with default settings (suitable for development/testing):

```bash
# Clone repository
git clone https://github.com/zubinqayam/ZQAutoNXG-V1.git
cd ZQAutoNXG-V1

# Install chart
helm install zqautonxg ./charts/zqautonxg \
  --namespace zqautonxg \
  --create-namespace

# Verify deployment
kubectl get pods -n zqautonxg
kubectl get svc -n zqautonxg
```

### Access the Application

```bash
# Port forward to access locally
kubectl port-forward -n zqautonxg svc/zqautonxg 8000:8000

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/metrics
```

## Configuration

### values.yaml Structure

The chart uses a hierarchical configuration structure:

```yaml
# Application configuration
replicaCount: 2
image:
  repository: zqautonxg
  tag: "latest"

# Infrastructure components
postgres:
  enabled: false
redis:
  enabled: false
prometheus:
  enabled: false
grafana:
  enabled: false

# Observability
otel:
  enabled: false
```

### Common Configuration Options

#### Image Configuration

```yaml
image:
  repository: ghcr.io/zubinqayam/zqautonxg-v1
  pullPolicy: IfNotPresent
  tag: "main"  # or use digest for ZCD

imagePullSecrets:
  - name: ghcr-pull-secret
```

#### Resource Limits

```yaml
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

#### Ingress Configuration

```yaml
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: api.zqautonxg.local
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: zqautonxg-tls
      hosts:
        - api.zqautonxg.local
```

#### Persistence Configuration

```yaml
persistence:
  enabled: true
  storageClass: "gp3"
  size: 10Gi
```

## Deployment Scenarios

### Scenario 1: Development (Minimal)

**Use Case:** Local development, testing, CI/CD

```bash
helm install zqautonxg ./charts/zqautonxg \
  --set replicaCount=1 \
  --set persistence.enabled=false \
  --set postgres.enabled=false \
  --set redis.enabled=false
```

**Resources:**
- Pods: 1
- CPU: 250m
- Memory: 256Mi
- Storage: None (emptyDir)

### Scenario 2: Staging (Standard)

**Use Case:** Pre-production testing, integration testing

```bash
helm install zqautonxg ./charts/zqautonxg \
  -f charts/zqautonxg/values.yaml \
  --set replicaCount=2 \
  --set postgres.enabled=true \
  --set redis.enabled=true \
  --set prometheus.enabled=true \
  --namespace zqautonxg-staging \
  --create-namespace
```

**Resources:**
- Pods: 2
- CPU: 500m per pod
- Memory: 512Mi per pod
- Storage: PostgreSQL 5Gi, Redis 2Gi

### Scenario 3: Production (Enterprise)

**Use Case:** Production workloads, high availability

```bash
helm install zqautonxg ./charts/zqautonxg \
  -f charts/zqautonxg/values.yaml \
  -f charts/zqautonxg/values-enterprise.yaml \
  --namespace zqautonxg-production \
  --create-namespace
```

**Resources:**
- Pods: 3 (autoscaling to 20)
- CPU: 2000m per pod
- Memory: 2Gi per pod
- Storage: PostgreSQL 50Gi, Redis 10Gi
- High Availability: Pod anti-affinity
- Monitoring: Prometheus, Grafana, OpenTelemetry

### Scenario 4: Multi-Region (GCC)

**Use Case:** Deployment across UAE, Oman, KSA

```bash
# UAE Region
helm install zqautonxg-uae ./charts/zqautonxg \
  -f charts/zqautonxg/values-enterprise.yaml \
  --set ingress.hosts[0].host=api.uae.zqautonxg.com \
  --namespace zqautonxg-uae \
  --create-namespace

# Oman Region
helm install zqautonxg-oman ./charts/zqautonxg \
  -f charts/zqautonxg/values-enterprise.yaml \
  --set ingress.hosts[0].host=api.oman.zqautonxg.com \
  --namespace zqautonxg-oman \
  --create-namespace

# KSA Region
helm install zqautonxg-ksa ./charts/zqautonxg \
  -f charts/zqautonxg/values-enterprise.yaml \
  --set ingress.hosts[0].host=api.ksa.zqautonxg.com \
  --namespace zqautonxg-ksa \
  --create-namespace
```

### Scenario 5: Multi-Tenant

**Use Case:** SaaS deployment with tenant isolation

```yaml
# values-multitenant.yaml
multiTenant:
  enabled: true
  tenants:
    - name: tenant-a
      namespace: zqautonxg-tenant-a
      quota:
        cpu: "5"
        memory: "10Gi"
    - name: tenant-b
      namespace: zqautonxg-tenant-b
      quota:
        cpu: "5"
        memory: "10Gi"
```

```bash
helm install zqautonxg ./charts/zqautonxg \
  -f values-multitenant.yaml
```

## Upgrading

### Zero-Cost Deployment (ZCD) Upgrade

```bash
# Get latest image digest
IMAGE_DIGEST=$(docker inspect \
  ghcr.io/zubinqayam/zqautonxg-v1:main \
  --format='{{index .RepoDigests 0}}')

# Upgrade with digest (ZCD compliant)
helm upgrade zqautonxg ./charts/zqautonxg \
  --set image.tag="@${IMAGE_DIGEST}" \
  --reuse-values \
  --wait
```

### Rolling Upgrade with Values

```bash
# Update configuration
helm upgrade zqautonxg ./charts/zqautonxg \
  -f charts/zqautonxg/values.yaml \
  -f my-custom-values.yaml \
  --namespace zqautonxg
```

### Rollback

```bash
# View history
helm history zqautonxg -n zqautonxg

# Rollback to previous version
helm rollback zqautonxg -n zqautonxg

# Rollback to specific revision
helm rollback zqautonxg 3 -n zqautonxg
```

## Monitoring

### Prometheus Integration

```bash
# Enable Prometheus
helm upgrade zqautonxg ./charts/zqautonxg \
  --set prometheus.enabled=true \
  --set prometheus.serviceMonitor.enabled=true \
  --reuse-values

# Access Prometheus
kubectl port-forward -n zqautonxg svc/zqautonxg-prometheus 9090:9090
```

Browse to http://localhost:9090

### Grafana Integration

```bash
# Enable Grafana
helm upgrade zqautonxg ./charts/zqautonxg \
  --set grafana.enabled=true \
  --reuse-values

# Get admin password
kubectl get secret zqautonxg-grafana -n zqautonxg \
  -o jsonpath="{.data.admin-password}" | base64 --decode

# Access Grafana
kubectl port-forward -n zqautonxg svc/zqautonxg-grafana 3000:3000
```

Browse to http://localhost:3000 (admin / <password>)

### OpenTelemetry Integration

```bash
# Enable OpenTelemetry
helm upgrade zqautonxg ./charts/zqautonxg \
  --set otel.enabled=true \
  --set otel.collector.enabled=true \
  --reuse-values

# Check collector status
kubectl get pods -n zqautonxg -l app.kubernetes.io/component=telemetry
kubectl logs -n zqautonxg -l app.kubernetes.io/component=telemetry
```

## Troubleshooting

### Issue: Pods Not Starting

**Diagnosis:**
```bash
kubectl get pods -n zqautonxg
kubectl describe pod <pod-name> -n zqautonxg
kubectl logs <pod-name> -n zqautonxg
```

**Common Causes:**
- Image pull errors: Check imagePullSecrets
- Resource constraints: Verify node resources
- Configuration errors: Validate values.yaml

### Issue: Service Unreachable

**Diagnosis:**
```bash
kubectl get svc -n zqautonxg
kubectl get ingress -n zqautonxg
kubectl describe ingress zqautonxg -n zqautonxg
```

**Common Causes:**
- Ingress not configured: Enable ingress.enabled
- DNS not resolving: Check hosts file or DNS
- TLS certificate issues: Verify cert-manager

### Issue: Database Connection Errors

**Diagnosis:**
```bash
kubectl get pods -n zqautonxg -l app.kubernetes.io/component=database
kubectl logs -n zqautonxg -l app.kubernetes.io/component=database
```

**Common Causes:**
- PostgreSQL not ready: Wait for StatefulSet
- Password mismatch: Check postgres-secret
- Network policy blocking: Review network policies

### Issue: High Memory Usage

**Diagnosis:**
```bash
kubectl top pods -n zqautonxg
kubectl describe pod <pod-name> -n zqautonxg
```

**Resolution:**
```bash
# Increase memory limits
helm upgrade zqautonxg ./charts/zqautonxg \
  --set resources.limits.memory=1Gi \
  --reuse-values
```

### Issue: Helm Lint Errors

**Diagnosis:**
```bash
helm lint ./charts/zqautonxg
helm lint ./charts/zqautonxg -f values-enterprise.yaml
```

**Common Fixes:**
- Fix indentation in YAML files
- Validate template syntax
- Check required values are set

## Advanced Topics

### Custom Values File

Create a custom values file for your environment:

```yaml
# my-production-values.yaml
replicaCount: 5

image:
  repository: my-registry.com/zqautonxg
  tag: "v6.0.0"

ingress:
  enabled: true
  hosts:
    - host: api.mycompany.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 2000m
    memory: 4Gi
  requests:
    cpu: 1000m
    memory: 2Gi
```

Deploy with custom values:
```bash
helm install zqautonxg ./charts/zqautonxg \
  -f my-production-values.yaml
```

### Secrets Management

Use Kubernetes secrets or external secret managers:

```bash
# Create secret
kubectl create secret generic zqautonxg-secrets \
  --from-literal=database-url="postgresql://..." \
  --from-literal=redis-url="redis://..." \
  -n zqautonxg

# Reference in values
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: zqautonxg-secrets
        key: database-url
```

### Network Policies

```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: zqautonxg-network-policy
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: zqautonxg
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
```

## Best Practices

1. **Use Digest-Pinned Images** for production
2. **Enable Resource Limits** to prevent resource exhaustion
3. **Configure Autoscaling** for variable workloads
4. **Enable Monitoring** for observability
5. **Use Secrets** for sensitive configuration
6. **Implement Network Policies** for security
7. **Test Upgrades** in staging first
8. **Backup StatefulSets** regularly
9. **Document Custom Values** for your environment
10. **Use ZCD** for efficient deployments

## Reference

### Helm Commands Cheat Sheet

```bash
# Install
helm install <release> <chart>

# Upgrade
helm upgrade <release> <chart>

# Rollback
helm rollback <release> <revision>

# Uninstall
helm uninstall <release>

# List releases
helm list

# Get values
helm get values <release>

# Get manifest
helm get manifest <release>

# History
helm history <release>

# Template (dry-run)
helm template <release> <chart>

# Lint
helm lint <chart>
```

## Support

For Helm deployment support:

- **Email:** zubin.qayam@outlook.com
- **Issues:** https://github.com/zubinqayam/ZQAutoNXG-V1/issues
- **Documentation:** https://github.com/zubinqayam/ZQAutoNXG-V1/tree/main/docs

---

**Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™**  
**Licensed under the Apache License 2.0**
