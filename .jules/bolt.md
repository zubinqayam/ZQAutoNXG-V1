## 2025-10-14 - FastAPI Async Def Optimization
**Learning:** In FastAPI, `def` endpoints run in a threadpool to avoid blocking the event loop. For CPU-bound or simple non-blocking operations, this adds unnecessary overhead.
**Action:** Convert simple endpoints that don't perform blocking I/O to `async def` to run directly on the event loop, reducing thread context switching overhead.
