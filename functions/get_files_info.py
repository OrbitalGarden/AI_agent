import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    working_directory_absolute_path = os.path.abspath(working_directory)
    directory_absolute_path = os.path.abspath(full_path)

    if not directory_absolute_path.startswith(working_directory_absolute_path):
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"
    
    if not os.path.isdir(directory_absolute_path):
        return f"Error: '{directory}' is not a directory"
    
    try:
        directory_contents = os.listdir(directory_absolute_path)
        files_info = []

        for item in directory_contents:
            filepath = os.path.join(directory_absolute_path, item)
            file_size = 0
            file_size = os.path.getsize(filepath)
            is_dir = os.path.isdir(filepath)
            files_info.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(files_info)
    
    except Exception as e:
        return f"Error listing files: {e}"