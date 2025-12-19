import threading
import time
import pytest
from nodes_logic import system_state, node_3_supervisor

def test_node_3_boundary_condition():
    """
    Test that Node 3 correctly handles the boundary condition where last_latency is exactly 3.0.
    Bug: logic is > 3.0 (Slow) and < 3.0 (Normal). 3.0 is ignored.
    If system_state starts as "WARNING", and we hit 3.0, it should probably clear to "Normal" (if 3.0 is acceptable)
    or stay WARNING (if 3.0 is bad). But typically 3.0 is the threshold.
    Let's assume 3.0 should be Normal.
    """
    # Setup
    system_state["stop_signal"] = False
    system_state["system_alert"] = "WARNING: Old Alert"

    # Set latency to exactly 3.0
    system_state["last_latency"] = 3.0

    # Run supervisor logic once (we can extract the loop body or run thread for > 1s)
    # Since node_3_supervisor is an infinite loop, we cannot call it directly without modification
    # or running in a thread and killing it.
    # A better way is to import the logic. But the logic is inside the function.
    # We will run it in a thread and stop it quickly.

    t3 = threading.Thread(target=node_3_supervisor)
    t3.start()

    time.sleep(1.5) # Wait for supervisor to cycle once (it sleeps 1s)

    # Check alert status
    # If bug exists: 3.0 is not > 3.0 and not < 3.0. So it does NOT enter elif block.
    # So system_alert remains "WARNING: Old Alert".
    # If fixed: it should become "Normal".

    current_alert = system_state["system_alert"]

    # Cleanup
    system_state["stop_signal"] = True
    t3.join()

    # Assert
    # We expect it to be Normal if 3.0 is acceptable.
    if current_alert != "Normal":
        pytest.fail(f"Boundary condition 3.0 failed to clear alert. Current alert: {current_alert}")

if __name__ == "__main__":
    # Manually run if executed as script
    try:
        test_node_3_boundary_condition()
        print("Test passed!")
    except Exception as e:
        print(f"Test failed: {e}")
