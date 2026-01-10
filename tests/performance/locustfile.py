
import random
from locust import HttpUser, task, between, events
import websocket
import time
import json

class ZQAutoNXGUser(HttpUser):
    wait_time = between(1, 3)

    @task(10)
    def root(self):
        self.client.get("/")

    @task(5)
    def health(self):
        self.client.get("/health")

    @task(1)
    def metrics(self):
        self.client.get("/metrics")

    @task(3)
    def websocket_connection(self):
        # Pick a random ticket from the seeded data
        ticket_id = random.choice(["perf-test-1", "perf-test-2", "perf-test-3"])

        # Determine WS URL
        ws_url = self.host.replace("http", "ws") + f"/ws/tickets/{ticket_id}"

        start_time = time.time()
        try:
            ws = websocket.create_connection(ws_url, timeout=5)
            # Keep connection open for a bit
            time.sleep(1)
            ws.close()
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="WS",
                name="/ws/tickets/{id}",
                response_time=total_time,
                response_length=0,
                exception=None,
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="WS",
                name="/ws/tickets/{id}",
                response_time=total_time,
                response_length=0,
                exception=e,
            )
