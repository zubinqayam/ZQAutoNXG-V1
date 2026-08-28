## 2025-10-14 - FastAPI Async Def Optimization
**Learning:** In FastAPI, `def` endpoints run in a threadpool to avoid blocking the event loop. For CPU-bound or simple non-blocking operations, this adds unnecessary overhead.
**Action:** Convert simple endpoints that don't perform blocking I/O to `async def` to run directly on the event loop, reducing thread context switching overhead.

## 2026-01-03 - Static Response & Metric Optimization
**Learning:** High-frequency endpoints that return mostly static data suffer from repeated dictionary allocation and metric label lookup overhead.
**Action:** Pre-compute static response parts into module-level constants (using `.copy()` for thread safety) and pre-initialize Prometheus metric labels to avoid map lookups on every request.
