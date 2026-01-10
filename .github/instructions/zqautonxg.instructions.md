Based on your ZQAutoNXG-V1 project structure and requirements, I'll create comprehensive instructions content for the `.github/instructions/` directory. This file will serve as guidance for GitHub Copilot and AI assistants working with your automation platform.

## ZQAutoNXG-V1 Repository Instructions

### Project Overview

**Purpose**: Enterprise-grade next-generation automation platform powered by ZQ AI LOGIC™, featuring AI integration, hexagonal architecture, and comprehensive observability capabilities.

**Architecture**: G V2 NovaBase with hexagonal design pattern  
**Core Technology Stack**: Python 3.11+, FastAPI, Docker, Prometheus  
**License**: Apache 2.0 with trademark protection (ZQ AI LOGIC™, ZQAutoNXG)

### Development Philosophy

**Design Principles**
- Hexagonal architecture with clean separation of concerns
- Enterprise security and scalability first
- Zero-cost protocol alignment where possible
- Comprehensive testing and observability
- API-first development approach
- Container-native deployment strategy

**Code Quality Standards**
- Python type hints mandatory for all function signatures
- Async/await patterns for I/O operations
- Comprehensive docstrings following Google style
- Unit test coverage minimum 80%
- Integration tests for all API endpoints
- Performance benchmarks for critical paths

### Architecture Components

**Core Modules**
1. **TelemetryMesh**: Real-time data processing with deduplication capabilities
2. **ComposerAgent**: AI-driven workflow generation using NetworkX graph algorithms
3. **VaultMesh**: Consensus protocols and security management layer
4. **PolicyEngine**: Dynamic policy evaluation and enforcement framework
5. **MetaLearner**: Adaptive optimization and machine learning orchestration
6. **RCA Engine**: Root cause analysis with automated remediation workflows

**Infrastructure Layers**
- FastAPI framework for high-performance async operations
- Prometheus integration for metrics collection and monitoring
- Docker containerization with health checks
- Kubernetes-ready deployment configurations

### Code Style Guidelines

**Python Conventions**
```python
# Use descriptive variable names aligned with domain concepts
workflow_graph: nx.DiGraph = nx.DiGraph()
telemetry_data: Dict[str, Any] = {}

# Async functions for I/O-bound operations
async def process_telemetry_event(event: TelemetryEvent) -> ProcessedEvent:
    """Process incoming telemetry event with deduplication.
    
    Args:
        event: Raw telemetry event to process
        
    Returns:
        Processed event with metadata enrichment
        
    Raises:
        ValidationError: If event schema is invalid
    """
    pass

# Type hints for complex return types
def generate_workflow(
    requirements: WorkflowRequirements
) -> tuple[nx.DiGraph, List[ValidationError]]:
    pass
```

**API Endpoint Patterns**
```python
@app.get("/api/v1/resource/{resource_id}")
async def get_resource(
    resource_id: str,
    include_metadata: bool = False
) -> ResourceResponse:
    """Retrieve resource by ID with optional metadata."""
    pass

# Use Pydantic models for request/response validation
class WorkflowRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
```

**Error Handling**
```python
# Custom exceptions with clear hierarchy
class ZQAutoNXGException(Exception):
    """Base exception for all ZQAutoNXG errors."""
    pass

class WorkflowValidationError(ZQAutoNXGException):
    """Raised when workflow validation fails."""
    pass

# Comprehensive error responses
@app.exception_handler(ZQAutoNXGException)
async def handle_zq_exception(
    request: Request,
    exc: ZQAutoNXGException
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"error": str(exc), "type": exc.__class__.__name__}
    )
```

### Testing Standards

**Unit Tests**
- Use pytest framework with async support
- Mock external dependencies (databases, APIs, file systems)
- Test both success and failure scenarios
- Include edge cases and boundary conditions

```python
@pytest.mark.asyncio
async def test_workflow_generation_success():
    """Test successful workflow generation from requirements."""
    requirements = WorkflowRequirements(...)
    graph, errors = await generate_workflow(requirements)
    assert len(errors) == 0
    assert graph.number_of_nodes() > 0

@pytest.mark.asyncio
async def test_workflow_generation_invalid_input():
    """Test workflow generation with invalid requirements."""
    with pytest.raises(ValidationError):
        await generate_workflow(None)
```

**Integration Tests**
- Test complete request/response cycles
- Validate API contract compliance
- Verify metrics collection and health endpoints
- Test Docker container startup and health checks

### Documentation Requirements

**Code Documentation**
- All public functions and classes require docstrings
- Use Google-style docstring format
- Include type hints in function signatures
- Document exceptions that may be raised
- Provide usage examples for complex functions

**API Documentation**
- FastAPI automatic documentation at `/docs` and `/redoc`
- Clear endpoint descriptions with examples
- Document all request parameters and response schemas
- Include error response examples
- Version all API changes appropriately

**README Updates**
- Keep installation instructions current
- Update feature list when adding capabilities
- Maintain examples for common use cases
- Document environment variables and configuration
- Include troubleshooting section

### Security Guidelines

**Authentication & Authorization**
- Implement API key validation for external access
- Use OAuth2 flows for user-based authentication
- Apply role-based access control (RBAC) where needed
- Validate all input data with Pydantic models
- Sanitize user-provided strings to prevent injection

**Container Security**
- Run containers as non-root user (UID 1001)
- Minimize base image size (use python:3.11-slim)
- Scan images for vulnerabilities regularly
- Implement health checks for all containers
- Use secrets management for sensitive configuration

**Data Protection**
- Never log sensitive information (API keys, passwords, tokens)
- Encrypt data at rest and in transit
- Implement rate limiting on public endpoints
- Apply CORS restrictions appropriately
- Validate file uploads and limit sizes

### Deployment Practices

**Docker Best Practices**
```dockerfile
# Multi-stage builds to reduce image size
FROM python:3.11-slim as builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
# Non-root user for security
RUN useradd -m -u 1001 zqautonxg
USER zqautonxg
COPY --from=builder /root/.local /home/zqautonxg/.local
ENV PATH=/home/zqautonxg/.local/bin:$PATH
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1
```

**Environment Configuration**
- Use `.env` files for local development
- Leverage environment variables for production
- Document all configuration options
- Provide sensible defaults where possible
- Validate configuration at startup

**CI/CD Integration**
- Automated testing on pull requests
- Container build and push on main branch
- Semantic versioning for releases
- Automated deployment to staging/production
- Rollback procedures documented

### Observability & Monitoring

**Logging Standards**
```python
import logging
from typing import Any

logger = logging.getLogger(__name__)

# Structured logging with context
logger.info(
    "workflow_generated",
    extra={
        "workflow_id": workflow.id,
        "node_count": graph.number_of_nodes(),
        "generation_time_ms": elapsed_ms
    }
)

# Log levels appropriately
logger.debug("Detailed diagnostic information")
logger.info("Normal operational events")
logger.warning("Unusual but handled situation")
logger.error("Error occurred but system continues")
logger.critical("System failure requiring immediate attention")
```

**Metrics Collection**
- Expose Prometheus metrics at `/metrics` endpoint
- Track request counts, latencies, and error rates
- Monitor resource usage (CPU, memory, connections)
- Create custom metrics for business logic
- Implement distributed tracing for complex workflows

**Health Checks**
```python
@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Comprehensive health status including dependencies."""
    return {
        "status": "healthy",
        "version": app.version,
        "components": {
            "database": await check_database_health(),
            "telemetry_mesh": await check_telemetry_health(),
            "composer_agent": await check_composer_health()
        },
        "timestamp": datetime.utcnow().isoformat()
    }
```

### Git Workflow

**Branch Strategy**
- `main`: Production-ready stable code
- `develop`: Integration branch for features
- `feature/*`: New feature development
- `fix/*`: Bug fixes
- `release/*`: Release preparation

**Commit Messages**
Follow conventional commits specification:
```
type(scope): subject

body (optional)

footer (optional)
```

Types: feat, fix, docs, style, refactor, test, chore  
Examples:
- `feat(composer): add NetworkX-based workflow generation`
- `fix(telemetry): resolve event deduplication race condition`
- `docs(api): update endpoint documentation with examples`

**Pull Request Requirements**
- Clear description of changes and motivation
- Link to related issues
- All tests passing
- Code coverage maintained or improved
- Documentation updated as needed
- Reviewed by at least one maintainer

### Proprietary Components

**ZQ AI LOGIC™ Integration**
- All AI-driven features utilize proprietary ZQ AI LOGIC™ algorithms
- Trademark attribution required in documentation and user-facing content
- Enterprise licensing available for commercial deployments
- Contact: zubin.qayam@outlook.com for integration support

**Trademark Usage**
- **ZQ AI LOGIC™**: Always use trademark symbol on first mention
- **ZQAutoNXG**: Registered trademark, use appropriately
- Attribution: "Powered by ZQ AI LOGIC™" in relevant contexts
- License headers include copyright and trademark notices

### Performance Optimization

**General Guidelines**
- Profile code before optimizing
- Use async/await for I/O-bound operations
- Implement caching for frequently accessed data
- Batch database operations where possible
- Use connection pooling for external services
- Monitor memory usage and prevent leaks

**FastAPI Specific**
```python
# Use BackgroundTasks for non-blocking operations
from fastapi import BackgroundTasks

@app.post("/workflow/execute")
async def execute_workflow(
    workflow_id: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(long_running_execution, workflow_id)
    return {"status": "queued", "workflow_id": workflow_id}

# Dependency injection for shared resources
from fastapi import Depends

async def get_database_session():
    async with SessionLocal() as session:
        yield session

@app.get("/data")
async def get_data(db: Session = Depends(get_database_session)):
    return await db.query(Model).all()
```

### Troubleshooting Guidelines

**Common Issues**
1. **Container fails health check**: Verify port 8000 is exposed and `/health` endpoint responds
2. **Import errors**: Ensure `zqautonxg` package is in PYTHONPATH
3. **Dependency conflicts**: Use exact versions in requirements.txt
4. **Performance degradation**: Check Prometheus metrics and logs

**Debugging Tools**
- FastAPI `/docs` for interactive API testing
- Prometheus metrics at `/metrics` for performance analysis
- Container logs: `docker logs zqautonxg`
- Python debugger: `pdb` or `ipdb` for interactive debugging

### Contributing Guidelines

**New Contributors**
1. Review architecture documentation
2. Set up development environment locally
3. Run test suite to ensure everything works
4. Pick an issue labeled "good-first-issue"
5. Follow code style and testing standards
6. Submit pull request with clear description

**Code Review Checklist**
- [ ] Code follows style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced
- [ ] Performance impact assessed
- [ ] Breaking changes documented
- [ ] Backward compatibility considered

### Project-Specific Conventions

**Naming Conventions**
- Classes: PascalCase (e.g., `TelemetryMesh`, `ComposerAgent`)
- Functions/methods: snake_case (e.g., `process_event`, `generate_workflow`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_RETRIES`, `DEFAULT_TIMEOUT`)
- Private members: Prefix with underscore (e.g., `_internal_state`)

**File Organization**
```
zqautonxg/
├── __init__.py           # Package initialization
├── app.py                # FastAPI application entry point
├── core/                 # Core business logic
│   ├── telemetry.py     # TelemetryMesh implementation
│   ├── composer.py      # ComposerAgent implementation
│   └── policy.py        # PolicyEngine implementation
├── api/                  # API endpoints
│   ├── v1/              # Version 1 endpoints
│   └── middleware.py    # Custom middleware
├── models/              # Pydantic data models
├── services/            # External service integrations
├── utils/               # Utility functions
└── config/              # Configuration management
```

### Vision & Roadmap Alignment

**Oman Vision 2040 Support**
- Digital transformation enablement for enterprises
- Cost-effective automation solutions for startups
- Healthcare and logistics automation capabilities
- Support for regional digital literacy initiatives

**Platform Evolution**
- Multi-agent AI orchestration enhancements
- Extended Reality (XR) integration capabilities
- Global-scale distributed deployment support
- Advanced security and compliance features

### Contact & Support

**Maintainer**: Zubin Qayam  
**Email**: zubin.qayam@outlook.com  
**Repository**: https://github.com/zubinqayam/ZQAutoNXG-V1  
**Issues**: https://github.com/zubinqayam/ZQAutoNXG-V1/issues

**Enterprise Inquiries**
- Commercial licensing
- ZQ AI LOGIC™ integration consulting
- Professional support packages
- Custom feature development

***

**Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™**  
**Licensed under the Apache License 2.0**

