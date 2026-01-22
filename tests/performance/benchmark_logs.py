
import time
import collections
import random
from typing import List, Dict, Any

# Mock Log Entry
def create_log_entry():
    return {
        "timestamp": "2025-01-01T00:00:00",
        "level": "INFO",
        "message": "Test log message " * 5,
        "metadata": {}
    }

MAX_LOGS = 1000
OPERATIONS = 100000
READ_OPERATIONS = 1000

def benchmark_list():
    logs_history: List[Dict[str, Any]] = []

    # Fill up
    for _ in range(MAX_LOGS):
        logs_history.append(create_log_entry())

    start_time = time.time()
    for _ in range(OPERATIONS):
        logs_history.append(create_log_entry())
        if len(logs_history) > MAX_LOGS:
            logs_history.pop(0)
    write_time = time.time() - start_time

    start_time = time.time()
    for _ in range(READ_OPERATIONS):
        _ = logs_history[-100:]
    read_time = time.time() - start_time

    return write_time, read_time

def benchmark_deque():
    logs_history = collections.deque(maxlen=MAX_LOGS)

    # Fill up
    for _ in range(MAX_LOGS):
        logs_history.append(create_log_entry())

    start_time = time.time()
    for _ in range(OPERATIONS):
        logs_history.append(create_log_entry())
        # No manual pop needed
    write_time = time.time() - start_time

    start_time = time.time()
    for _ in range(READ_OPERATIONS):
        # Convert to list to slice
        _ = list(logs_history)[-100:]
    read_time = time.time() - start_time

    return write_time, read_time

if __name__ == "__main__":
    print(f"Benchmarking {OPERATIONS} writes and {READ_OPERATIONS} reads (slice last 100)...")

    list_write, list_read = benchmark_list()
    print(f"List: Write={list_write:.4f}s, Read={list_read:.4f}s")

    deque_write, deque_read = benchmark_deque()
    print(f"Deque: Write={deque_write:.4f}s, Read={deque_read:.4f}s")

    print(f"Write Improvement: {list_write / deque_write:.2f}x")
    print(f"Read Impact: {deque_read / list_read:.2f}x (slower if > 1)")
