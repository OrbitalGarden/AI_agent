from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    functions_dict = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file" : run_python_file,
        "write_file" : write_file
    }
    function = functions_dict[function_call.name]
    function_call.args["working_directory"] = "./calculator"
    function_result = function(**function_call.args)

    if function_call.name not in functions_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                )
            ],
        )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response={"result": function_result},
            )
        ],
    )