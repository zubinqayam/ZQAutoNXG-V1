
# Performance Testing Suite

This directory contains the infrastructure for load testing the ZQAutoNXG application using [Locust](https://locust.io/).

## Contents

- `locustfile.py`: Defines the user behavior for the load test. Targets `/`, `/health`, `/metrics`, and `/ws/tickets/{id}`.
- `seed_data.py`: Utilities to insert test data (tickets) into the SQLite database so WebSocket connections succeed.
- `run_benchmark.sh`: Automated script to setup, seed, run the load test, and teardown.

## Usage

1. **Install Dependencies**:
   ```bash
   pip install locust websocket-client
   ```

2. **Run Benchmark**:
   ```bash
   ./tests/performance/run_benchmark.sh
   ```

   This will:
   1. Seed `data/tickets.db` with test tickets.
   2. Start the FastAPI app in the background.
   3. Run a headless Locust swarm (50 users, 30 seconds).
   4. Save results to `tests/performance/results_stats.csv`.

## Scenarios

The current `locustfile.py` implements a generic user profile:
- **Root Endpoint (53%)**: High frequency.
- **Health Check (26%)**: Monitoring simulation.
- **Metrics (5%)**: Prometheus scraping simulation.
- **WebSocket (16%)**: Real-time connection simulation (connect, hold 1s, disconnect).
