import os
from functions.config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read files at the specified path up to 10000 characters (otherwise truncates them before reading), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file we need to read, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    working_directory_absolute_path = os.path.abspath(working_directory)
    file_absolute_path = os.path.abspath(full_path)

    if not file_absolute_path.startswith(working_directory_absolute_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(file_absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(file_absolute_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(file_absolute_path) > MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
                
    except Exception as e:
        return f"Error getting file content: {e}"    