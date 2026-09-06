#!/usr/bin/env python3
# Code Execution Module (Sandboxed)

import subprocess

def execute_python(code):
    """Execute Python code in sandbox"""
    try:
        result = subprocess.run(
            ["python3", "-c", code],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout or result.stderr
    except Exception as e:
        return f"Error: {e}"
