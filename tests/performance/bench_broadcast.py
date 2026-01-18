
import asyncio
import time
from typing import List

class MockWebSocket:
    async def send_text(self, message: str):
        # Simulate network delay
        await asyncio.sleep(0.001)

async def bench_broadcast_sequential(connections, message):
    start_time = time.perf_counter()
    disconnected = []
    for connection in connections:
        try:
            await connection.send_text(message)
        except Exception:
            disconnected.append(connection)
    end_time = time.perf_counter()
    return end_time - start_time

async def bench_broadcast_gather(connections, message):
    start_time = time.perf_counter()
    # Create tasks
    tasks = [connection.send_text(message) for connection in connections]
    await asyncio.gather(*tasks, return_exceptions=True)
    end_time = time.perf_counter()
    return end_time - start_time

async def main():
    connections = [MockWebSocket() for _ in range(100)]
    message = "test message"

    seq_time = await bench_broadcast_sequential(connections, message)
    gather_time = await bench_broadcast_gather(connections, message)

    print(f"Sequential broadcast (100 clients): {seq_time:.6f}s")
    print(f"Gather broadcast (100 clients): {gather_time:.6f}s")
    print(f"Improvement: {seq_time / gather_time:.2f}x faster")

if __name__ == "__main__":
    asyncio.run(main())
