## 2025-10-14 - FastAPI Async Def Optimization
**Learning:** In FastAPI, `def` endpoints run in a threadpool to avoid blocking the event loop. For CPU-bound or simple non-blocking operations, this adds unnecessary overhead.
**Action:** Convert simple endpoints that don't perform blocking I/O to `async def` to run directly on the event loop, reducing thread context switching overhead.

## 2025-12-31 - Prometheus Client Synchronous Behavior
**Learning:** `prometheus_client.generate_latest()` is a synchronous, potentially CPU-intensive operation. Converting metrics endpoints to `async def` causes this operation to run on the main event loop, blocking all other requests.
**Action:** Keep Prometheus metrics endpoints as `def` to utilize FastAPI's threadpool, or offload the generation to a thread explicitly.
