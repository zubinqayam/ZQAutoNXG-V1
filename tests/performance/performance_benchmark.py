
import asyncio
import time
import json
import sys
import os

# Add the current directory to sys.path to import zqautonxg
sys.path.append(os.getcwd())

from zqautonxg.api.v1.logs import LogEntry, broadcast_log, active_connections, logs_history, MAX_LOGS_HISTORY

async def benchmark_broadcast():
    print("--- Benchmarking Broadcast ---")
    # Mock some connections
    class MockWebSocket:
        async def send_text(self, text):
            await asyncio.sleep(0.01) # Simulate some network latency

    active_connections.clear()
    active_connections.extend([MockWebSocket() for _ in range(50)])

    start_time = time.perf_counter()
    for i in range(10):
        log = LogEntry("INFO", f"Message {i}")
        await broadcast_log(log)
    end_time = time.perf_counter()

    print(f"Broadcasted 10 logs to 50 connections in {end_time - start_time:.4f} seconds")
    active_connections.clear()

def benchmark_history():
    print("\n--- Benchmarking History Buffer ---")
    test_max = 10000

    # List approach (current)
    lh = []
    for i in range(test_max):
        lh.append({"msg": "test"})

    start_time = time.perf_counter()
    for i in range(5000):
        lh.append({"msg": "test"})
        if len(lh) > test_max:
            lh.pop(0)
    end_time = time.perf_counter()
    print(f"List pop(0) 5000 times (size={test_max}): {end_time - start_time:.6f}s")

    # Deque approach
    from collections import deque
    dh = deque(maxlen=test_max)
    for i in range(test_max):
        dh.append({"msg": "test"})

    start_time = time.perf_counter()
    for i in range(5000):
        dh.append({"msg": "test"})
    end_time = time.perf_counter()
    print(f"Deque append 5000 times (size={test_max}): {end_time - start_time:.6f}s")

if __name__ == "__main__":
    benchmark_history()
    asyncio.run(benchmark_broadcast())
