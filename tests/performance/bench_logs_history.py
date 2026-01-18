
import time
import collections
from typing import List, Dict, Any

# Mock Log Entry
log_entry = {
    "timestamp": "2023-10-27T10:00:00",
    "level": "INFO",
    "message": "Test log message",
    "metadata": {}
}

MAX_LOGS_HISTORY = 1000
ITERATIONS = 10000

def bench_list():
    logs_history: List[Dict[str, Any]] = []
    # Pre-fill
    for _ in range(MAX_LOGS_HISTORY):
        logs_history.append(log_entry)

    start_time = time.perf_counter()
    for _ in range(ITERATIONS):
        logs_history.append(log_entry)
        if len(logs_history) > MAX_LOGS_HISTORY:
            logs_history.pop(0)
    end_time = time.perf_counter()
    return end_time - start_time

def bench_deque():
    logs_history = collections.deque(maxlen=MAX_LOGS_HISTORY)
    # Pre-fill
    for _ in range(MAX_LOGS_HISTORY):
        logs_history.append(log_entry)

    start_time = time.perf_counter()
    for _ in range(ITERATIONS):
        logs_history.append(log_entry)
        # deque handles popping automatically
    end_time = time.perf_counter()
    return end_time - start_time

if __name__ == "__main__":
    list_time = bench_list()
    deque_time = bench_deque()

    print(f"List implementation time: {list_time:.6f}s")
    print(f"Deque implementation time: {deque_time:.6f}s")
    print(f"Improvement: {list_time / deque_time:.2f}x faster")
