import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_work_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_work_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    command = ['python', file_path]
    if args:
        command += args
    
    try:
        completed_process = subprocess.run(
            command,
            cwd=abs_work_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        if not completed_process.stdout and not completed_process.stderr:
            if completed_process.returncode != 0:
                return f"Process exited with code {completed_process.returncode}"
            else:
                return "No output produced."
        
        output_format = []

        if completed_process.stdout:
            output_format.append(f"STDOUT: {completed_process.stdout}")
    
        if completed_process.stderr:
            output_format.append(f"STDERR: {completed_process.stderr}")
        
        if completed_process.returncode != 0:
            output_format.append(f"Process exited with code {completed_process.returncode}")

        return '\n'.join(output_format)
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
