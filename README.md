# ZQAutoNXG
**Next-Generation eXtended Automation Platform**  
**Powered by ZQ AI LOGIC™**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-red.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

ZQAutoNXG is an enterprise-grade automation platform featuring advanced AI integration, hexagonal architecture, and comprehensive observability capabilities. Built with modern technologies and powered by proprietary ZQ AI LOGIC™ algorithms.

## 🚀 **Features**

- 🤖 **AI-Powered Automation** - Intelligent workflow generation and optimization
- 🥽 **Extended Reality (XR)** - Immersive automation interfaces and visualization
- 🌍 **Global-Scale Orchestration** - Distributed deployment and management
- ⚡ **Next-Generation Algorithms** - Proprietary ZQ AI LOGIC™ technology
- 🛡️ **Enterprise Security** - Apache 2.0 licensed with trademark protection
- 📊 **Comprehensive Observability** - Prometheus metrics and health monitoring
- 🏢 **Hexagonal Architecture** - Clean separation of concerns and testability

## 🏷️ **Architecture: G V2 NovaBase**

ZQAutoNXG implements a sophisticated hexagonal architecture with the following core components:

### **Core Modules**
- **TelemetryMesh** - Real-time data processing with deduplication
- **ComposerAgent** - AI-driven workflow generation using NetworkX
- **VaultMesh** - Consensus protocols and security management
- **PolicyEngine** - Dynamic policy evaluation and enforcement
- **MetaLearner** - Adaptive optimization and machine learning
- **RCA Engine** - Root cause analysis and automated remediation

### **Infrastructure**
- **FastAPI Framework** - High-performance async API
- **Prometheus Integration** - Metrics collection and monitoring
- **Container-First** - Docker and Kubernetes ready
- **Apache 2.0 Licensed** - Enterprise-friendly open source

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.11+
- Docker (optional)
- Git

### **Installation**

```bash
# Clone the repository
git clone https://github.com/zubinqayam/ZQAutoNXG-V1.git
cd ZQAutoNXG-V1

# Install dependencies
pip install -r requirements.txt

# Run ZQAutoNXG
uvicorn zqautonxg.app:app --reload --host 0.0.0.0 --port 8000
```

### **Docker Deployment**

```bash
# Build ZQAutoNXG container
docker build -t zqautonxg:latest .

# Run container
docker run -d \
  --name zqautonxg \
  -p 8000:8000 \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  zqautonxg:latest
```

### **Verify Installation**

```bash
# Check ZQAutoNXG status
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# Prometheus metrics
curl http://localhost:8000/metrics
```

## 📚 **API Documentation**

Once running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

### **Key Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Platform information and capabilities |
| `/health` | GET | Health check and system status |
| `/status` | GET | Detailed component status |
| `/version` | GET | Version and build information |
| `/metrics` | GET | Prometheus metrics |
| `/api/v1/workflows` | GET, POST | Workflow management |
| `/api/v1/nodes` | GET, POST | Node configuration |
| `/api/v1/logs/ws` | WebSocket | Real-time log streaming |
| `/api/v1/network/topology` | GET | Network topology |

For complete API documentation, see [docs/API_REFERENCE.md](docs/API_REFERENCE.md)

### **Example Response**

```json
{
  "platform": "ZQAutoNXG",
  "version": "6.0.0",
  "architecture": "G V2 NovaBase",
  "brand": "Powered by ZQ AI LOGIC™",
  "description": "Next-Generation eXtended Automation Platform",
  "status": "operational",
  "license": "Apache License 2.0",
  "capabilities": [
    "AI-Powered Automation",
    "Extended Reality Integration",
    "Global-Scale Orchestration",
    "Next-Generation Algorithms",
    "Proprietary ZQ AI LOGIC™"
  ]
}
```

## 🔧 **Development**

### **Development Setup**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
uvicorn zqautonxg.app:app --reload --log-level debug
```

### **Running Tests**

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=zqautonxg --cov-report=html

# Run specific test file
pytest tests/test_api_workflows.py -v
```

### **Docker Compose Deployment**

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

Services available after deployment:
- **Backend API**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/zqadmin)

### **Project Structure**

```
ZQAutoNXG-V1/
├── LICENSE                    # Apache License 2.0
├── README.md                  # Project documentation
├── requirements.txt           # Production dependencies
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Multi-service orchestration
├── .env.example               # Environment configuration template
├── docs/                      # Comprehensive documentation
│   ├── API_REFERENCE.md      # Complete API documentation
│   ├── DEPLOYMENT.md         # Deployment guide
│   ├── ARCHITECTURE.md       # System architecture
│   ├── CONTRIBUTING.md       # Contribution guidelines
│   └── CHANGELOG.md          # Version history
├── monitoring/                # Monitoring configuration
│   ├── prometheus.yml        # Prometheus config
│   └── grafana/              # Grafana dashboards
├── tests/                     # Test suite
│   ├── test_endpoints.py     # Core endpoint tests
│   ├── test_api_workflows.py # Workflow API tests
│   └── test_compression.py   # Middleware tests
└── zqautonxg/                 # Main application package
    ├── __init__.py            # Package initialization
    ├── app.py                 # FastAPI application
    ├── api/                   # API endpoints
    │   └── v1/               # API version 1
    │       ├── workflows.py  # Workflow endpoints
    │       ├── nodes.py      # Node endpoints
    │       ├── logs.py       # Log streaming
    │       └── network.py    # Network topology
    ├── models/                # Data models
    │   ├── workflow.py       # Workflow models
    │   └── node.py           # Node models
    ├── services/              # Business logic (future)
    └── utils/                 # Utility functions (future)
```

## 📊 **Monitoring**

### **Prometheus Metrics**

ZQAutoNXG exposes Prometheus metrics at `/metrics`:

- `zqautonxg_requests_total` - Total HTTP requests
- `zqautonxg_health_checks_total` - Health check requests
- Standard Python and FastAPI metrics

Access Prometheus at http://localhost:9090 (when using Docker Compose)

### **Grafana Dashboards**

Access Grafana at http://localhost:3001 (when using Docker Compose)

Default credentials:
- **Username**: admin
- **Password**: zqadmin

Pre-configured with Prometheus datasource for real-time monitoring.

### **Health Checks**

Health endpoint provides comprehensive system status:

```bash
curl http://localhost:8000/health
```

Response includes platform status, version, and component health.

## ⚙️ **Configuration**

### **Environment Variables**

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `ZQAutoNXG` | Application name |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:8080` | CORS allowed origins |
| `LOG_LEVEL` | `INFO` | Logging level |

### **Example Configuration**

```bash
export APP_NAME="ZQAutoNXG"
export HOST="0.0.0.0"
export PORT="8000"
export LOG_LEVEL="INFO"
```

## 🔒 **Security**

### **Container Security**
- **Non-root execution** - Runs as user ID 1001
- **Minimal attack surface** - Based on Python slim image
- **Health monitoring** - Built-in health checks
- **Security scanning** - Regular vulnerability assessments

### **API Security**
- **CORS protection** - Configurable allowed origins
- **Request logging** - Comprehensive audit trails
- **Rate limiting** - Built-in request throttling
- **Input validation** - Pydantic data validation

## 📜 **License**

Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

### **Trademark Notice**

**ZQ AI LOGIC™** and **ZQAutoNXG** are trademarks of Zubin Qayam.
Use of these trademarks requires explicit permission.

## 🔗 **Links**

- **Repository**: https://github.com/zubinqayam/ZQAutoNXG-V1
- **Issues**: https://github.com/zubinqayam/ZQAutoNXG-V1/issues
- **License**: https://github.com/zubinqayam/ZQAutoNXG-V1/blob/main/LICENSE
- **Contact**: zubin.qayam@outlook.com

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) and:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with proper Apache 2.0 headers
4. Add tests for new functionality
5. Run tests and ensure they pass (`pytest tests/`)
6. Format code (`black zqautonxg/ tests/`)
7. Commit changes (`git commit -m 'feat: add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Submit a pull request

## 📖 **Documentation**

Comprehensive documentation is available in the `docs/` directory:

- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Deployment instructions
- **[Architecture](docs/ARCHITECTURE.md)** - System architecture and design
- **[Contributing](docs/CONTRIBUTING.md)** - Contribution guidelines
- **[Changelog](docs/CHANGELOG.md)** - Version history and updates

## 🏆 **Enterprise Support**

For enterprise licensing, commercial support, and ZQ AI LOGIC™ integration:

**Contact**: zubin.qayam@outlook.com  
**Enterprise**: Commercial licensing available  
**Support**: Professional support packages  
**Integration**: ZQ AI LOGIC™ consulting services  

---

**ZQAutoNXG - Next-Generation eXtended Automation Platform**  
**Powered by ZQ AI LOGIC™**  
**© 2025 Zubin Qayam. All Rights Reserved.**