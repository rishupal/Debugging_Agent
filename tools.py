import subprocess
import os

def read_file(file_path):
    """Reads the content of a file."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"

def write_file(file_path, content):
    """Writes new content to a file."""
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing to file: {e}"

def run_tests(command):
    """Executes a shell command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Tests failed with error: {e.stderr}"
    except FileNotFoundError:
        return "Error: Test command not found."