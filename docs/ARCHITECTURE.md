# ZQAutoNXG Architecture

**Version:** 6.0.0  
**Architecture:** G V2 NovaBase  
**Powered by:** ZQ AI LOGIC™

## Overview

ZQAutoNXG implements a hexagonal architecture (ports and adapters) with clean separation between business logic, infrastructure, and external integrations.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Future)                         │
│    React + TypeScript + React Flow + Tailwind CSS          │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/WebSocket
┌──────────────────────┴──────────────────────────────────────┐
│                   API Gateway Layer                          │
│              FastAPI + CORS + GZip                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼───────┐ ┌───▼────────┐ ┌──▼──────────┐
│  Workflows    │ │   Nodes    │ │    Logs     │
│   Router      │ │   Router   │ │   Router    │
└───────┬───────┘ └───┬────────┘ └──┬──────────┘
        │             │              │
┌───────▼─────────────▼──────────────▼──────────┐
│           Core Business Logic                   │
│  - Workflow Engine                             │
│  - Node Management                             │
│  - Execution Orchestration                     │
└───────┬─────────────┬──────────────┬───────────┘
        │             │              │
┌───────▼───────┐ ┌──▼─────────┐ ┌──▼──────────┐
│  PostgreSQL   │ │   Redis    │ │  WebSocket  │
│   Database    │ │   Cache    │ │   Manager   │
└───────────────┘ └────────────┘ └─────────────┘
        │             │              │
┌───────▼─────────────▼──────────────▼───────────┐
│           Observability Layer                   │
│  Prometheus + Grafana + Structured Logging     │
└─────────────────────────────────────────────────┘
```

## Core Components

### 1. API Layer (`zqautonxg/api/`)

Handles HTTP requests and WebSocket connections.

**Routers:**
- `workflows.py` - Workflow CRUD and execution
- `nodes.py` - Node configuration and management
- `logs.py` - Log streaming and querying
- `network.py` - Network topology management

**Responsibilities:**
- Request validation
- Response serialization
- Error handling
- Authentication (future)

### 2. Domain Models (`zqautonxg/models/`)

Pydantic models for data validation and serialization.

**Models:**
- `workflow.py` - Workflow, WorkflowNode, WorkflowEdge, WorkflowExecution
- `node.py` - NodeConfig, SchedulerConfig, ConnectorConfig, RequestHistory

**Responsibilities:**
- Data validation
- Type safety
- Schema generation
- JSON serialization

### 3. Services Layer (Future: `zqautonxg/services/`)

Business logic implementation.

**Planned Services:**
- `workflow_engine.py` - Workflow execution orchestration
- `scheduler.py` - Job scheduling and management
- `connector.py` - HTTP client and API integration
- `monitoring.py` - Metrics collection and health checks

### 4. Infrastructure Layer

**Database:**
- PostgreSQL for persistent storage
- SQLAlchemy ORM (to be integrated)
- Alembic for migrations (to be integrated)

**Cache:**
- Redis for session storage
- Pub/sub for real-time updates

**Monitoring:**
- Prometheus for metrics collection
- Grafana for visualization
- Structured logging with JSON format

## Data Flow

### Workflow Execution Flow

```
1. Client → POST /api/v1/workflows/execute
           ↓
2. Workflows Router validates request
           ↓
3. Workflow Engine retrieves workflow definition
           ↓
4. Topological sort determines execution order
           ↓
5. Execute nodes in order with retry logic
           ↓
6. Store execution results in database
           ↓
7. Broadcast updates via WebSocket
           ↓
8. Return execution status to client
```

### Real-Time Log Streaming

```
1. Client establishes WebSocket connection
           ↓
2. WebSocket Manager registers connection
           ↓
3. Application emits log events
           ↓
4. Log Manager broadcasts to all connections
           ↓
5. Client receives real-time updates
```

## Design Patterns

### Hexagonal Architecture (Ports and Adapters)

**Ports:**
- HTTP/REST API (FastAPI routers)
- WebSocket connections
- Database interfaces
- Cache interfaces

**Adapters:**
- FastAPI application
- PostgreSQL adapter
- Redis adapter
- Prometheus metrics

### Repository Pattern (Future)

```python
class WorkflowRepository:
    def create(workflow: Workflow) -> Workflow
    def get(id: UUID) -> Workflow
    def update(id: UUID, workflow: Workflow) -> Workflow
    def delete(id: UUID) -> None
    def list() -> List[Workflow]
```

### Observer Pattern

Used for real-time updates via WebSocket connections.

```python
class WebSocketManager:
    connections: List[WebSocket]
    
    async def broadcast(message: dict):
        for connection in connections:
            await connection.send_json(message)
```

## Security Architecture

### Current Implementation

- **CORS Protection** - Configurable allowed origins
- **Request Validation** - Pydantic model validation
- **Health Monitoring** - Built-in health checks
- **Metrics Security** - Prometheus metrics endpoint

### Future Enhancements

- **JWT Authentication** - Token-based auth
- **OAuth 2.0** - Third-party authentication
- **Rate Limiting** - Request throttling
- **API Keys** - Service-to-service auth
- **Role-Based Access Control (RBAC)** - Permission management

## Scalability

### Horizontal Scaling

- Stateless API design
- Redis for session storage
- Database connection pooling
- Load balancer support

### Vertical Scaling

- Async/await for I/O operations
- Connection pooling
- Response caching
- Efficient query optimization

### Performance Optimization

- GZip compression for responses
- Pre-initialized metrics labels
- Static response caching
- Lazy loading of resources

## Technology Stack

### Backend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | FastAPI 0.115+ | Async web framework |
| Language | Python 3.11+ | Core language |
| Validation | Pydantic 2.7+ | Data validation |
| Database | PostgreSQL 15 | Persistent storage |
| Cache | Redis 7 | Session/caching |
| Monitoring | Prometheus | Metrics collection |
| Visualization | Grafana | Dashboard |

### Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Container | Docker | Containerization |
| Orchestration | Docker Compose | Local orchestration |
| K8s Ready | Yes | Production deployment |
| Reverse Proxy | Nginx (future) | Load balancing |

## Module Dependencies

```
zqautonxg/
├── app.py                 # Application entry point
├── api/
│   └── v1/
│       ├── workflows.py   # → models.workflow
│       ├── nodes.py       # → models.node
│       ├── logs.py        # Independent
│       └── network.py     # Independent
├── models/
│   ├── workflow.py        # Core domain models
│   └── node.py            # Core domain models
├── services/              # (Future)
│   ├── workflow_engine.py # → models.workflow
│   ├── scheduler.py       # → models.node
│   └── connector.py       # → models.node
└── utils/                 # (Future)
    ├── logging.py
    └── metrics.py
```

## API Versioning

Current version: **v1**

Versioning strategy:
- URL-based versioning (`/api/v1/`, `/api/v2/`)
- Backward compatibility within major versions
- Deprecation notices before breaking changes
- Migration guides for major version upgrades

## Future Architecture Plans

### Phase 1 (Current)
- ✅ Core API implementation
- ✅ WebSocket support
- ✅ Docker Compose setup
- ✅ Basic monitoring

### Phase 2
- Database integration (PostgreSQL + SQLAlchemy)
- Authentication (JWT + OAuth 2.0)
- Frontend application (React + TypeScript)
- Enhanced security middleware

### Phase 3
- Kubernetes deployment
- Microservices architecture
- Service mesh (Istio)
- Advanced observability (Jaeger, OpenTelemetry)

### Phase 4
- Multi-tenancy support
- Advanced AI features (ZQ AI LOGIC™)
- Extended Reality (XR) integration
- Global-scale orchestration

## Contributing to Architecture

When proposing architectural changes:

1. Document the problem
2. Propose solution with diagrams
3. Consider backward compatibility
4. Discuss performance implications
5. Update this document

---

**Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™**  
**Licensed under the Apache License 2.0**
