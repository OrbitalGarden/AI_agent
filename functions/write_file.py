import os

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