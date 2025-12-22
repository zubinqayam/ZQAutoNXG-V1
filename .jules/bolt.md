## 2025-05-18 - Async Endpoints in FastAPI
**Learning:** Switching from synchronous `def` to asynchronous `async def` for FastAPI endpoints that are trivial non-blocking operations (returning static data or simple memory access) can improve throughput by avoiding the overhead of running in a threadpool.
**Action:** When defining simple endpoints in FastAPI that are strictly non-blocking and lightweight, prefer `async def` to keep execution in the main event loop and reduce overhead. Heavy CPU-bound tasks must still use `def` to run in a threadpool and avoid blocking the event loop.
