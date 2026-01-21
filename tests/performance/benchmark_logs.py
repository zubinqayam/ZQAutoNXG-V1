
import time
import collections
from typing import List, Deque, Dict, Any

MAX_LOGS_HISTORY = 1000
OPERATIONS = 100000

def test_list_performance():
    logs_history: List[Dict[str, Any]] = []

    start_time = time.time()
    for i in range(OPERATIONS):
        # Simulate log entry
        logs_history.append({"msg": f"log {i}"})
        if len(logs_history) > MAX_LOGS_HISTORY:
            logs_history.pop(0)
    end_time = time.time()
    return end_time - start_time

def test_deque_performance():
    logs_history: Deque[Dict[str, Any]] = collections.deque(maxlen=MAX_LOGS_HISTORY)

    start_time = time.time()
    for i in range(OPERATIONS):
        # Simulate log entry
        logs_history.append({"msg": f"log {i}"})
        # maxlen handles popping
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    print(f"Running {OPERATIONS} operations with history size {MAX_LOGS_HISTORY}")

    list_time = test_list_performance()
    print(f"List time: {list_time:.6f} seconds")

    deque_time = test_deque_performance()
    print(f"Deque time: {deque_time:.6f} seconds")

    improvement = (list_time - deque_time) / list_time * 100
    print(f"Improvement: {improvement:.2f}%")
