## 2025-10-14 - FastAPI Sync vs Async Endpoints
**Learning:** In FastAPI, endpoints defined with `def` are run in a threadpool to prevent blocking the event loop. For non-blocking operations (like returning static JSON or in-memory counters), this adds unnecessary overhead. Converting these to `async def` runs them directly on the event loop, improving throughput and latency.
**Action:** Default to `async def` for FastAPI endpoints unless they perform blocking I/O operations that are not awaitable.
