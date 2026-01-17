import asyncio
import time
import logging
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from zqautonxg.api.v1.network import get_network_topology

# Disable logging for benchmark
logging.getLogger("zqautonxg").setLevel(logging.WARNING)

async def benchmark():
    # Warm up
    for _ in range(100):
        await get_network_topology()

    iterations = 10000
    start_time = time.perf_counter()

    for _ in range(iterations):
        await get_network_topology()

    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_time = total_time / iterations

    print(f"Total time for {iterations} iterations: {total_time:.4f}s")
    print(f"Average time per call: {avg_time*1000000:.2f}µs")

if __name__ == "__main__":
    asyncio.run(benchmark())
