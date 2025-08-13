# debugging_agent/main.py

import os
import openai
from agent_core import run_debugging_agent # <-- Now we only need to import the function

# --- Configure your OpenAI API key ---
openai_api_key = os.environ.get("OPENAI_API_KEY", "OPENAI_API_KEY") 

# Check if the key is provided
if not openai_api_key:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    exit()

# --- Initialize the OpenAI client correctly ---
openai_client = openai.OpenAI(api_key=openai_api_key)

if __name__ == "__main__":
    goal = "Fix the buggy code in 'test_file.py' and ensure all tests pass."
    initial_state = "Test runner reports a NameError in a test case."
    
    # Create a dummy test file for the agent to work on
    with open("test_file.py", "w") as f:
        f.write("def buggy_function(x):\n    return y + x")
    
    # --- Pass the initialized client to the agent function ---
    run_debugging_agent(openai_client, goal, initial_state)