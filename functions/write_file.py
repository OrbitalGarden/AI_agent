import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write over a file in the specified directory (otherwise creates it before writing), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file we need to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content we need to write to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    working_directory_absolute_path = os.path.abspath(working_directory)
    file_absolute_path = os.path.abspath(full_path)

    if not file_absolute_path.startswith(working_directory_absolute_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        file_directory = os.path.dirname(file_absolute_path)

        if not os.path.exists(file_directory):
            os.makedirs(file_directory)

        if os.path.exists(file_absolute_path) and os.path.isdir(file_absolute_path):
            return f'Error: "{file_path}" is a directory, not a file'

        with open(file_absolute_path, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error writing files: {e}"