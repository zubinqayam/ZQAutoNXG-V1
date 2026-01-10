
import pytest
import sqlite3
import os
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
from zqautonxg.app import app, ws_manager

@pytest.fixture
def client():
    return TestClient(app)

# Ensure we use a clean test DB
@pytest.fixture(autouse=True)
def test_db(tmp_path):
    # Create a temporary DB file
    db_file = tmp_path / "test_tickets.db"
    db_path_str = str(db_file)

    # Initialize the schema
    conn = sqlite3.connect(db_path_str)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id TEXT PRIMARY KEY,
            subject TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

    # Patch the DB_PATH in the app module
    with patch("zqautonxg.app.DB_PATH", db_path_str):
        yield db_path_str

@pytest.fixture
def sample_ticket(test_db):
    conn = sqlite3.connect(test_db)
    cur = conn.cursor()
    cur.execute("INSERT INTO tickets (id, subject, status) VALUES ('123', 'Test Ticket', 'open')")
    conn.commit()
    conn.close()
    return {"id": "123"}

def test_websocket_connection_success(client, sample_ticket):
    """Test WebSocket connection to ticket endpoint."""
    ticket_id = sample_ticket["id"]

    with client.websocket_connect(f"/ws/tickets/{ticket_id}") as websocket:
        # Should connect successfully
        assert websocket is not None

def test_websocket_connection_invalid_ticket(client):
    """Test WebSocket connection to non-existent ticket."""
    with pytest.raises(WebSocketDisconnect) as e:
        with client.websocket_connect("/ws/tickets/invalid-id") as websocket:
            pass
    assert e.value.code == 1008

@pytest.mark.asyncio
async def test_websocket_broadcast():
    """Test broadcasting to connected clients."""
    # We need to test the connection manager directly since TestClient.websocket_connect
    # doesn't easily support concurrent connections in a single sync test function
    # without deeper async setup or creating a real server.

    # Mock WebSocket
    class MockWebSocket:
        def __init__(self):
            self.sent_messages = []

        async def accept(self):
            pass

        async def send_json(self, message):
            self.sent_messages.append(message)

    mock_ws = MockWebSocket()
    ticket_id = "123"

    # Manually connect
    await ws_manager.connect(ticket_id, mock_ws)

    # Broadcast message
    msg = {"type": "new_reply", "content": "Hello"}
    await ws_manager.broadcast(ticket_id, msg)

    # Verify reception
    assert len(mock_ws.sent_messages) == 1
    assert mock_ws.sent_messages[0] == msg

    # Disconnect
    ws_manager.disconnect(ticket_id, mock_ws)
