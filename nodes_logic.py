import threading
import time
import random

# --- SHARED MEMORY (The "Nervous System") ---
# This is how the nodes "talk" to each other.
system_state = {
    # Data holding
    "current_task": None,       # The user's message
    "current_api_key": None,    # The key provided for this specific task
    "response_output": None,    # Where the answer goes

    # Status flags
    "node_1_busy": False,
    "last_latency": 0.0,        # How long the last task took
    "system_alert": "Normal",   # Node 3 writes here if it finds problems
    "stop_signal": False        # Kill switch for the program
}

# ==============================================================================
# NODE 1: THE WORKER (Processing)
# Role: Accepts dynamic input + key. Executes the task.
# ==============================================================================
def node_1_worker():
    while not system_state["stop_signal"]:
        # 1. Wait for a task
        if system_state["current_task"] is not None and not system_state["node_1_busy"]:

            # Set Status: BUSY
            system_state["node_1_busy"] = True
            print(f"\n[NODE 1] > Starting task with Key: ...{system_state['current_api_key'][-4:]}")

            # Start Timer
            start_time = time.time()

            # --- SIMULATION OF API CALL ---
            # (In real life, your API request goes here)
            time.sleep(random.uniform(0.5, 4.0)) # Simulates fast or slow response
            result = f"Processed: '{system_state['current_task']}'"
            # ------------------------------

            # Stop Timer
            end_time = time.time()
            duration = end_time - start_time

            # Write Result to Memory
            system_state["response_output"] = result
            system_state["last_latency"] = duration

            # Clear Task & Reset Status
            system_state["current_task"] = None
            system_state["node_1_busy"] = False
            print(f"[NODE 1] > Task Complete. Time taken: {round(duration, 2)}s")

        time.sleep(0.1) # Small rest to prevent CPU overload

# ==============================================================================
# NODE 2: THE MONITOR (Workflow Watcher)
# Role: Keeps a heartbeat. Ensures the "chat line" is open.
# ==============================================================================
def node_2_monitor():
    while not system_state["stop_signal"]:
        # Logic: If Node 1 is busy, we log that the workflow is active.
        if system_state["node_1_busy"]:
            # In a real app, this might update a database timestamp
            pass

        # Simple Heartbeat log every 5 seconds
        # print("[NODE 2] ... Workflow Active ...")
        time.sleep(5)

# ==============================================================================
# NODE 3: THE SUPERVISOR (Quality & Speed Control)
# Role: Checks Node 1's speed. If too slow, it flags a warning.
# ==============================================================================
def node_3_supervisor():
    while not system_state["stop_signal"]:

        # RULE 1: Speed Check
        # If the last task took more than 3.0 seconds, mark it as "Slow"
        if system_state["last_latency"] > 3.0:
            system_state["system_alert"] = "WARNING: API Speed Low. Consider changing Key."
            print(f"!!! [NODE 3 ALERT] {system_state['system_alert']} !!!")

            # Reset latency memory so we don't spam the alert
            system_state["last_latency"] = 0

        # RULE 2: Clear alerts if speed returns to normal
        elif system_state["last_latency"] > 0 and system_state["last_latency"] <= 3.0:
            system_state["system_alert"] = "Normal"

        time.sleep(1) # Check every second

# ==============================================================================
# MAIN EXECUTION (Testing the 3 Nodes)
# ==============================================================================
if __name__ == "__main__":
    print("/// INITIALIZING ZQ 3-NODE SYSTEM ///")

    # 1. Start the Background Nodes
    t1 = threading.Thread(target=node_1_worker)
    t2 = threading.Thread(target=node_2_monitor)
    t3 = threading.Thread(target=node_3_supervisor)

    t1.start()
    t2.start()
    t3.start()

    # 2. Simulate User Input (You would replace this with your Chat UI input)
    try:
        while True:
            user_input = input("\nEnter Message (or 'q' to quit): ")
            if user_input == 'q':
                break

            key_input = input("Enter API Key for this task: ")

            # Load data into Shared Memory -> Node 1 will see this and wake up
            system_state["current_api_key"] = key_input
            system_state["current_task"] = user_input

            # Wait for Node 1 to finish
            while system_state["response_output"] is None:
                time.sleep(0.1)

            print(f"User received: {system_state['response_output']}")

            # Clear output for next round
            system_state["response_output"] = None

    except KeyboardInterrupt:
        pass

    # Shutdown
    system_state["stop_signal"] = True
    print("System Shutdown.")
