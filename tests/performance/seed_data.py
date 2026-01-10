
import sqlite3
import os

DB_PATH = "data/tickets.db"

def seed():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Ensure table exists (in case app hasn't run yet)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id TEXT PRIMARY KEY,
            subject TEXT,
            status TEXT
        )
    """)

    # Insert test tickets
    tickets = [
        ("perf-test-1", "Performance Test Ticket 1", "open"),
        ("perf-test-2", "Performance Test Ticket 2", "closed"),
        ("perf-test-3", "Performance Test Ticket 3", "open"),
    ]

    for t in tickets:
        try:
            cur.execute("INSERT INTO tickets (id, subject, status) VALUES (?, ?, ?)", t)
        except sqlite3.IntegrityError:
            pass # Already exists

    conn.commit()
    conn.close()
    print(f"Seeded {len(tickets)} test tickets into {DB_PATH}")

if __name__ == "__main__":
    seed()
