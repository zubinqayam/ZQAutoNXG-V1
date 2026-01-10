
#!/bin/bash
set -e

# Install locust if not present
if ! command -v locust &> /dev/null; then
    echo "Locust not found, installing..."
    pip install locust websocket-client
fi

# Seed database
echo "Seeding database..."
python tests/performance/seed_data.py

# Start the application in background
echo "Starting application..."
export APP_NAME="ZQAutoNXG-Perf"
uvicorn zqautonxg.app:app --host 0.0.0.0 --port 8000 --log-level warning &
APP_PID=$!

# Wait for app to start
sleep 5

# Run Locust (headless)
echo "Running load test..."
# Run for 30 seconds with 50 users, spawning 10 per second
locust -f tests/performance/locustfile.py \
    --headless \
    --users 50 \
    --spawn-rate 10 \
    --run-time 30s \
    --host http://localhost:8000 \
    --csv tests/performance/results

# Cleanup
echo "Stopping application..."
kill $APP_PID

echo "Done! Results saved to tests/performance/results_stats.csv"
