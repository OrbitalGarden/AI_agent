import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run file in the specified directory if it's a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file we need to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The arguments that can be passed to the file we run. Defaults to an empty list.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    working_directory_absolute_path = os.path.abspath(working_directory)
    file_absolute_path = os.path.abspath(full_path)

    if not file_absolute_path.startswith(working_directory_absolute_path):
        return f'Error: Cannot resultute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(file_absolute_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_absolute_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            ["uv",
            "run",
            file_absolute_path,
            *args],
            timeout=30,
            capture_output=True,
            text=True,
            cwd=working_directory_absolute_path
            )
        
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")       

        if output == []:
            return "No output produced."
        
        return "\n".join(output)

    except Exception as e:
        return f"Error: resultuting Python file: {e}"