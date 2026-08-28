# ZQAutoNXG API Reference

**Version:** 6.0.0  
**Powered by:** ZQ AI LOGIC™  
**License:** Apache 2.0

## Base URL

```
http://localhost:8000
```

## Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Spec:** http://localhost:8000/openapi.json

## Core Endpoints

### Platform Information

#### GET /
Get platform information and capabilities.

#### GET /health
Health check endpoint.

#### GET /metrics
Prometheus metrics endpoint.

#### GET /status
Detailed component status.

## Workflows API

### POST /api/v1/workflows
Create a new workflow.

### GET /api/v1/workflows
List all workflows.

### GET /api/v1/workflows/{workflow_id}
Get a specific workflow.

### PUT /api/v1/workflows/{workflow_id}
Update a workflow.

### DELETE /api/v1/workflows/{workflow_id}
Delete a workflow.

### POST /api/v1/workflows/execute
Execute a workflow in test mode.

### POST /api/v1/workflows/activate
Activate a workflow for production.

### GET /api/v1/workflows/{workflow_id}/history
Get execution history for a workflow.

## Nodes API

### GET /api/v1/nodes/status
Get status of all nodes.

### POST /api/v1/nodes/toggle/{node_id}
Enable or disable a node.

### GET /api/v1/nodes/{node_id}/config
Get node configuration.

### PUT /api/v1/nodes/{node_id}/config
Update node configuration.

### POST /api/v1/nodes/{node_id}/test
Test node configuration.

### GET /api/v1/nodes/{node_id}/stats
Get node statistics.

## Logs API

### WebSocket /api/v1/logs/ws
Real-time log streaming via WebSocket.

### GET /api/v1/logs/history
Get historical logs.

### POST /api/v1/logs/query
Query logs with filters.

## Network API

### GET /api/v1/network/topology
Get current network topology.

### WebSocket /api/v1/network/ws
Real-time network topology updates.

### POST /api/v1/network/deploy-bridge
Deploy a new network bridge.

### GET /api/v1/network/nodes/{node_id}/metrics
Get metrics for a specific network node.

---

**Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™**  
**Licensed under the Apache License 2.0**
