# debugging_agent/agent_core.py

import openai
import json
from tools import read_file, write_file, run_tests

# A dictionary to map action names to the actual functions
TOOL_MAP = {
    'read_file': read_file,
    'write_file': write_file,
    'run_tests': run_tests,
}

# The run_debugging_agent function now accepts openai_client as a parameter
def run_debugging_agent(openai_client, goal, initial_state):
    """The main loop for the debugging agent."""
    history = [
        {"role": "user", "content": f"Goal: {goal}\nInitial State: {initial_state}\n"}
    ]

    while True:
        prompt = f"""
        You are an autonomous debugging agent. Your goal is to: {goal}.
        You can use the following tools:
        - read_file(file_path): Reads a file.
        - write_file(file_path, content): Writes to a file.
        - run_tests(command): Runs shell commands like 'pytest'.

        Based on the goal and the current state, decide your next action.
        Your response must be a single JSON object with 'action' and 'arguments' keys.
        Example: {{'action': 'read_file', 'arguments': {{'file_path': 'src/buggy_file.py'}}}}
        If the goal is achieved, the action should be 'report_success'.
        """

        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=history + [{"role": "user", "content": prompt}]
            )
            action_plan = json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error in LLM planning: {e}")
            break

        action = action_plan.get('action')
        arguments = action_plan.get('arguments', {})

        if action == 'report_success':
            print("Goal achieved. Exiting agent.")
            break

        if action in TOOL_MAP:
            result = TOOL_MAP[action](**arguments)
            history.append({"role": "assistant", "content": f"Executed: {action}({arguments})\nResult: {result}"})
            print(f"Executed '{action}' with result: {result[:100]}...")
        else:
            print(f"Unknown action: {action}. Exiting.")
            break